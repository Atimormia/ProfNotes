# Garbage Collector Spikes

I've seen a bunch of tickets saying the game hitches, and every one of them was hard to reproduce. A 10-minute check shows nothing, so the ticket gets marked "Can't reproduce". Then the bug appears during a playtest, and only then does it become clear that it depends on session duration. Even with that clue, nobody can trigger it on demand, so it slides down the priority list. Then it shows up in production anyway.

A bug like this doesn't fail to reproduce because it isn't there. It fails because its signature is time, and a process that tests moments never sees it. When someone finally catches it, the profiler gives the same unhelpful answer every time: not a function, not a system, just a collector doing its job on a graph that quietly grew larger than anyone intended.

---

## The Blind Spot: Retained Too Long, Released Too Early

There are two easy answers to a GC hitch, and both are reasonable:

* **Tune the collector:** Change the interval, enable incremental mode, hide the pass behind a loading screen. These help, and I come back to them below. But they lower the price of walking the graph without asking why the graph is that size.
* **Ban allocation everywhere:** Enforce zero-allocation discipline in every loop. In genuinely hot code that is the right call. Applied everywhere, it targets allocation churn when many of these hitches are about retention, and it pays the cost of the discipline in code that never needed it.

Neither survives contact with a hitch that grows with session length. The mechanic sits underneath both: the collector's cost follows what is reachable, not what you just freed. The engine-level detail is folded below for anyone who wants it, and the argument reads the same without it.

<details>
<summary>Under the hood: how Unreal and Unity collect (optional reading)</summary>

Why does anyone pay for a collector at all? The C++ alternative is smart pointers, and reference counting charges at a different place: every copy of a `shared_ptr` is an atomic increment, every destruction a decrement, and a cycle never reaches zero, so two objects pointing at each other leak until someone turns one side into a `weak_ptr`. A game world is full of cycles: actors own components that point back at the actor, widgets point at what they display, delegates point both ways. Counting also frees in a cascade, so dropping one pointer can release a deep chain at a moment nobody chose. A tracing collector flips the trade: assigning a reference is free, cycles need no special handling, and the cost is batched into one pass over what is still reachable. In Unreal there is a second reason. Because the collector finds references through reflection, the engine can serialize them and null them when a target is destroyed, which is what lets Blueprint designers work without reasoning about ownership. The price is the pause, and the pause is the subject of this post.

### Unreal's Mark-And-Sweep Mechanism
Unreal's collector is mark-and-sweep over `UObject`s only. Every `UObject` is registered in a global object array, and reflection (the `UPROPERTY` macro and the code generated behind it) tells the collector where each object's references live, so it traverses them exactly instead of guessing. A pass flags objects as candidates for collection, runs reachability analysis from the roots to clear the flag on everything it reaches, then gathers and destroys whatever stayed flagged. Parts run in parallel, but the game thread waits unless incremental reachability is enabled, which is why it shows up as a hitch. Reachability analysis is the expensive stage and scales with the objects and references it traverses: in a test Epic's own engineer ran with around 600 thousand objects alive, it took close to 20 ms.

Clustering is Unreal's way of cutting that traversal. A cluster is a root object plus the subobjects it owns, treated by the collector as one unit: if the root is reachable, the whole group is marked reachable without walking every reference inside it, and the group lives and dies together. A class opts in by overriding `CanBeInCluster`, and the parent builds the cluster with `CreateCluster()`. It is not a free win. In Epic's measurement, reachability analysis dropped from roughly 17 ms to under 1 ms, but the stage that marks objects as unreachable grew by about 10 ms, and the net saving was closer to half in a shipping build. Clustering suits stable groups that really do live and die together, such as a level's data or an asset's subobjects. For objects that come and go independently, Epic's own advice is the blunt one: keep the `UObject` count low.

### Unity's Boehm-Demers-Weiser Collector

Unity's scripting runtimes (Mono and IL2CPP) use the Boehm-Demers-Weiser collector, a general-purpose library written to add garbage collection to languages that were never designed for it. It is conservative: with no exact map of where references live, it treats any word that looks like a heap address as a pointer, so a stray number can occasionally keep an object alive. It is non-moving: objects never relocate, which makes it easy to embed next to native code, but free space fragments over time (Unity's own manual says its strategy tends to fragment memory). And it is mark-and-sweep without generations: it marks from the roots, sweeps unmarked blocks into free lists, and every full collection traces the whole managed heap, not only recent objects. Incremental mode (available since 2019) splits the marking across frames in time slices, flattening the spike at the cost of tracking reference writes made mid-collection.

Compare that with the classic .NET collector, which is precise (the JIT emits maps of where references live), generational (new objects land in a small generation collected often and cheaply, since most die young), and compacting (survivors are moved together, so the heap doesn't fragment). That is why ordinary C# can allocate freely. Unity inherits the language but not that collector, so allocation discipline is stronger advice there, and the zero-allocation rule above isn't folklore in Unity. Unreal can't use the .NET design for the opposite reason: C++ code holds raw pointers the runtime can neither see nor patch, so a compacting collector has nothing safe to move. Unreal ends up non-moving and without generations like Unity, but precise, because reflection hands it the map that Boehm has to guess at.

</details>

A collector never knows that you are done with an object. It only knows whether something can still reach it, meaning a root (a global, a stack variable, an engine-owned object) leads to it through a chain of references. Unused and unreachable are different things, and the gap between them is where this bug lives: a hidden pooled projectile is unused, but if anything still points at it, it is reachable, so it stays. With smart pointers you had to write ownership down (`unique_ptr`, `shared_ptr`, `weak_ptr`), so it was at least visible in the code. A collector removes that ceremony, not the decision: every reference you leave behind is now an implicit vote to keep the object alive.

So the real question is an ownership question: who decided this stays reachable, and for how long? It fails in two directions.

**Retained too long.** A hard reference is a statement of ownership. In Unreal, a `UPROPERTY` pointer, a `TObjectPtr`, or a `TStrongObjectPtr` tells the collector that this object must live as long as the holder does. In Unity, static fields and event subscriptions say the same thing. Nobody writes them as ownership. They are written as convenience: remember the last target, keep the last hit payload, subscribe to an event. An inactive pooled object, a static event list, a cached payload: each one is a fair local decision, and the sum is a graph that grows with session length. That is also why the ticket gets marked "Can't reproduce". A ten-minute test never grows the graph enough to hurt, and a long soak does.

One detail changes where to look. Unreal clears references to destroyed actors for you, so what accumulates is whatever nobody destroys: pooled actors that were only hidden, non-actor `UObject`s such as per-hit payloads, widgets, and hard-referenced assets.

**Released too early.** The opposite failure comes from a pointer the collector can't see. A raw pointer or a `TSharedPtr` to a `UObject` doesn't keep anything alive, so the object can be collected while you still hold it. What you get is a dangling pointer, which usually shows up as a crash far from the cause rather than as a hitch. It has been reported even inside third-party SDK integrations that mixed smart pointers with `UObject`s.

Both directions share a cause: ownership expressed somewhere the collector, or the reviewer, can't see.

---

## The Fix: Give Every Lifetime an Owner

None of this calls for dropping pooling, lambdas, or caching. Each is the right tool in the right place. The fix is making sure each one has a named owner for what it keeps alive.

### 1. Give the pool a reset contract

A pool reduces allocation churn, but it also extends lifetimes: a pooled object may stay reachable for the whole match, so every reference inside it matters more than it did in a short-lived actor. Whoever owns the pool owns the reset. That means one place that clears everything, not every caller remembering to.

```cpp
// Owned: keeps the object alive on purpose.
UPROPERTY()
TObjectPtr<UHitPayload> LastHitPayload;

UPROPERTY()
TArray<TObjectPtr<AEnemyActor>> TrackedTargets; // pooled enemies are hidden, not destroyed

// Observed: does not keep anything alive.
TWeakObjectPtr<AActor> Instigator;
```

```cpp
void AProjectilePool::DespawnProjectile(AProjectileActor* Projectile)
{
    if (!IsValid(Projectile)) return;

    Projectile->SetActorHiddenInGame(true);

    // The pool owns the reset: every hard reference gathered while active
    // is released here, in one place.
    Projectile->ResetForPool();

    InactivePool.Push(Projectile);
}

void AProjectileActor::ResetForPool()
{
    LastHitPayload = nullptr;
    TrackedTargets.Reset();
    // Weak observers like Instigator need no reset.
}
```

The rule behind it is short: hard references for ownership, weak references for observation. A weak pointer never extends a lifetime, so a pooled object holding one can't turn into an accidental owner.

### 2. Make time visible

A bug whose signature is time needs evidence that has time on its axis. Run a long soak build and record `UObject` count over the session, broken down by class (Unreal's `obj list` command gives a per-class view, and Unity's Memory Profiler snapshots serve the same purpose). A flat line in a short run and a climbing line in a long one turns "can't reproduce" into a curve attached to the ticket. It also tells you which class is growing, which is most of the way to the owner.

### 3. Keep transient data out of the graph

For short-lived calculation state, a value type never enters the object graph at all. In Unreal, a `UCLASS` instance is a `UObject` the engine tracks, while a `USTRUCT` with no `UObject` pointers lives on the stack or inline inside its owner.

```cpp
// A UObject for temporary math: one more object for the collector to track.
UMyCombatCalculator* Calc = NewObject<UMyCombatCalculator>(this);
Calc->Execute(Target);

// A value type: lives on the stack and never enters the object graph.
FCombatParameters TempParams;
TempParams.Magnitude = 5.0f;
ProcessCombat(TempParams);
```

### 4. Know what a lambda keeps alive

A lambda is a small ownership statement that doesn't look like one. Whatever it captures, it keeps, and where it is stored decides who finds out. A raw `UObject` pointer, including `this`, is invisible to the collector: it won't keep the object alive, so a timer that fires after the object was destroyed runs against a dangling pointer. A plain lambda isn't tied to the object, so nothing cancels it when the object goes away. Capturing a strong pointer avoids that, but it turns a one-second timer into a one-second lifetime extension, and into a leak if the timer loops or is never cleared. Unity has the same shape: a closure that captures `this` and sits in a long-lived event keeps that object reachable for as long as the subscription exists.

```cpp
// The capture decides the lifetime, and nothing here says who owns it.
GetWorld()->GetTimerManager().SetTimer(Handle, [this, TargetId]()
{
    OnTimerComplete(TargetId); // raw this: invisible to the GC, dangling if destroyed first
}, 1.0f, false);

// Observed, not owned: the callback is skipped if the object is gone.
GetWorld()->GetTimerManager().SetTimer(Handle,
    FTimerDelegate::CreateWeakLambda(this, [this, TargetId]()
    {
        OnTimerComplete(TargetId);
    }), 1.0f, false);
```

Allocation is the smaller half of the story. A by-value capture lives inside the closure object, so it only reaches the heap when the closure is stored somewhere type-erased and too large for inline storage. In Unreal that is ordinary allocator churn, not collector work, since the GC only tracks `UObject`s. In Unity it is a managed allocation, which is the collector's problem. It is worth profiling in a hot path, but it isn't what makes a lambda risky.

### 5. Tune the collector last

Once the graph holds only what it should, the collector settings become a sensible final layer: running the pass at a natural pause such as a loading screen, grouping stable long-lived objects into clusters (Unreal then treats each group as a single unit during the reachability pass), and enabling incremental modes (which spread the marking work across several frames). Each comes with conditions. Unreal's incremental reachability analysis is documented as experimental in recent versions, requires `TObjectPtr` rather than raw pointers in reflected properties, and lists known limitations, so check the documentation for your engine version before enabling it. All of these lower the price of walking the graph. None of them changes what is in it, which is why they come after the ownership work and not instead of it.

---

## The Insight: Credit the Case, Track the Pattern

This is the same failure shape [Data-Driven Design Is an Architecture Boundary](DataDrivenDesign.md) and [Where Abstraction Meets The Hot Path](AbstractionMeetsTheHotPath.md) already named, here measured in lifetime instead of configuration layers or call depth: **credit the individual case, track the pattern across cases.**

Nobody who wrote the pool, the event subscription, or the timer callback made a bad decision. Each was a reasonable local call, reviewed on its own merits. What nobody owned was the sum: the lifetime of everything those decisions kept reachable. A pool doesn't remove the lifetime question, it moves it. The engine used to answer it when an object was destroyed, and now the pool's reset has to answer it, usually without anyone saying so out loud.

The ticket history follows the same logic. Every "can't reproduce" was a fair verdict on a short test. The recurrence across tickets was the signal, and the cheaper intervention was available all along: a soak run and a curve, before any escalation. That is the evidence-gated approach from [Matching Effort to Evidence](MatchingEffortToEvidence.md), applied to a bug that only shows up over time.

The trigger isn't foresight, since nobody predicts which pool will quietly outlive the match. **The trigger is catching the moment a long-lived object gains a reference**: a pool introduced, an event subscribed, a hard pointer added to something that persists. In review, the question is one line: who clears this, and when? That sits closer to the cause than any profiler spike three weeks after release, and it is the same placement rule the other performance posts apply: deciding, per system, whether a piece of code sits in the narrow part of the codebase where lifetime discipline has to be explicit.

---

## Production Bottom Line

> **Lifetime Is Someone's Job:** A pool, a cached reference, or an event subscription doesn't remove the lifetime question, it moves it to whoever owns the reset. A collector can only walk the graph you leave it.
>
> Tuning the collector lowers the price of the walk, and banning allocation shrinks one source of churn. Neither says who owns what stays reachable. The useful signal is the moment a long-lived object gains a reference: treat that moment, not a profiler spike weeks later, as the prompt to name an owner.