# Scheduling Is Architecture

One day I was optimizing an early-stage Rogue-like with hundreds of active enemies. Everything ran smoothly until the fights got crowded, and then the game thread stopped fitting in the frame. At a 60 FPS target the budget is about 16.7 ms, and in a crowded scene `World Tick Time` averaged **27.4 ms** in `stat game`, with worst frames at 52.8 ms.

`Tick Time` was the biggest line under it, and one of the things ticking was an area-of-effect aura actor. Its code looked completely innocent:

```cpp
// Simplified from the real actor. Many of these exist in a crowded fight.
void AAuraActor::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
    DoAuraJob(OverlappedActors);   // a BlueprintNativeEvent; the empty check lives inside
}

void AAuraActor::DoAuraJob_Implementation(const TArray<AActor*>& Targets)
{
    if (!HasAuthority() || Targets.IsEmpty()) return;   // the guard sits after the dispatch

    FDamageEffectParams ParamsCopy = DamageEffectParams;  // copied on every call
    FGameplayEffectContainer Container;                   // built on every call
    // ... fill the container and apply the effects to every target
}
```

The actor already had a tick interval, so its body did not run every frame, and it did almost nothing when no one was inside. Yet it sat near the top of the profile.

---

## The Blind Spot: The Profiler Named the Container

The usual explanation for a hot `Tick` is dispatch overhead. In Unreal, every registered tick function is queued each frame regardless of its body, and components register their own on top of the actor's. `stat game` shows this directly in the `Queue Ticks` line and the `Ticks Queued` counter, so the two suspects can be separated:

* **The registry:** `Queue Ticks` was 0.3 to 0.5 ms for roughly 500 to 740 queued ticks. That is a bit under a microsecond per tick function (derived by division, so approximate) and about **two percent** of `World Tick Time`.
* **The work under it:** `Tick Time` is inclusive, so it contains everything its callees do. The big lines were work: `Blueprint Time` at 7.7 ms over 348 calls and `GT Tickable Time` at 5.4 ms. For the aura, each pass copied damage parameters, built a new effect container, and searched an array with `Contains` and `AddUnique` on every overlap.

The empty check looked like protection, but it sat after the call dispatch, and with targets inside, every aura repeated that work at its interval. A large number under a tick says where time passes, not what is slow. This is the frequency side of [Where Abstraction Meets The Hot Path](AbstractionMeetsTheHotPath.md): nobody had decided how often this work should run.

Here is how the `stat game` inclusive averages changed across captures:

| Capture | World Tick | Tick Time | Blueprint Time | GT Tickable Time | Queue Ticks | Ticks Queued |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Initial | 27.43 ms | 21.05 ms | 7.74 ms | 5.41 ms | 0.53 ms | 591 |
| Iteration 1 | 16.79 ms | 14.83 ms | 3.04 ms | 1.46 ms | 0.33 ms | 706 |
| Iteration 2 | 13.57 ms | 11.53 ms | 2.72 ms | 1.62 ms | 0.26 ms | 568 |

### What the Numbers Do Not Show

* **Several changes landed together:** timers on the aura and projectiles, a set instead of an array, empty checks, and a fix for a damage multiplier that was applied twice, which also changes how fast enemies die. I did not isolate the tick change.
* **The captures are noisy:** three taken within twenty seconds of each other gave 11.4, 22.3 and 16.8 ms, and enemy counts and fight length differed. The honest reading is that the game thread cost roughly halved in most captures.
* **Registered ticks did not drop:** `Ticks Queued` went 591, 706, 568. The win did not come from fewer tick functions.
* **The forecast was rough:** I had estimated about 2x for the full list of optimizations, and I had implemented only part of it when the second capture showed roughly that.

---

## The Fix: Run Work Only When Someone Needs It

The change was to stop letting the engine's default schedule decide when the aura works. In order of effort:

### 1. Try the Cheap Option First

`SetActorTickInterval` lowers the rate but leaves the tick function registered, and it will not enable a tick function that is disabled. If the rate is the only problem, this is the whole fix.

### 2. Sleep When Idle

Set `PrimaryActorTick.bCanEverTick = false` and run the work from a timer that exists only while targets are inside. Only the idle-to-active transition starts it, and only the move back to idle stops it. The random initial delay keeps auras spawned in the same frame from waking on the same frame forever after.

```cpp
void AAuraActor::OnSphereOverlap(/* ... */ AActor* OtherActor /* ... */)
{
    if (!IsValidTarget(OtherActor)) return;

    const int32 PrevNum = OverlappedActors.Num();
    OverlappedActors.Add(OtherActor);

    if (PrevNum == 0)                  // idle -> active, and only then
    {
        const float Interval = FMath::Max(0.05f, AuraParams.Interval);
        const float InitialDelay = FMath::FRandRange(0.f, Interval);   // de-phase auras
        GetWorldTimerManager().SetTimer(AuraTimer, this, &AAuraActor::OnAuraTimer,
                                        Interval, true, InitialDelay);
    }
}

void AAuraActor::OnSphereEndOverlap(/* ... */ AActor* OtherActor /* ... */)
{
    OverlappedActors.Remove(OtherActor);

    if (OverlappedActors.IsEmpty())    // active -> idle
    {
        GetWorldTimerManager().ClearTimer(AuraTimer);
    }
}
```

In production you would typically go a step further and move this scheduling into one subsystem, so individual actors stay clean.

### 3. Track Overlaps in a Set

`Contains` and `AddUnique` on an array are linear scans, and they run on every overlap event. A `TSet` makes membership O(1), which is what the code above relies on.

### 4. Know When Waking Costs More

* **Components tick separately:** disabling the actor's tick does not silence its components, and a half-disabled actor keeps paying the registry cost.
* **Demand-driven is not automatically cheaper:** in a sandbox I wrote, once half of 5,000 objects were active, looping over a list of pointers cost roughly four times a flat loop over contiguous data. That is the layout argument from [Data Layout Is Architecture](DataLayoutIsArchitecture.md). Waking on demand pays off when most objects are idle most of the time.

### 5. Keep Tick Where Tick Is Right

Replacing every `Tick` is not a silver bullet, because it can break frame-perfect behavior. Use this table as a starting point:

| Scenario / Goal | Prefer Engine `Tick` | Prefer Demand-Driven / Events |
| --- | :---: | :---: |
| **Per-frame visual smoothing or interpolation** (`VInterpTo`, `Lerp`) | ✅ | ❌ |
| **Discrete, interval-based processing** (combat updates, scanning loops) | ❌ | ✅ |
| **Strict engine phase sequencing** (must run before or after physics) | ✅ | ❌ |
| **Idle-capable behaviors** (zone detection, environmental scanning) | ❌ | ✅ |
| **Rules whose order matters** (damage resolution, death) | ❌ | Direct calls, events only as notifications |

The quick litmus test:

> *"If this system ran 5 to 10 times per second instead of every frame, would the player notice a structural or visual issue?"*
> * **Yes** → keep a carefully managed engine `Tick`.
> * **No** → run it on demand.

---

## The Insight: A Default Is Still a Decision

The engine's tick schedule was a decision nobody made: it ran the work at a frequency that came with the framework. Moving the aura onto overlap events replaces that default with an explicit one, and for the aura it is a safe one. It has one handler, one owner and one writer. What changes when the same mechanism is used with many subscribers acting on shared state is the number of writers, and that is where the cost appears.

Martin Fowler's 2017 note "What do you mean by Event-Driven?" separates four patterns that people lump together. The one that matters in game code is event notification, where the sender does not care who listens. His warning is that the larger flow stops being explicit in any program text and often can only be reconstructed from a running system, and that events are often used as disguised commands.

**Encapsulation is not only private fields. It means the set of code that can change an object's state is knowable.** With a global bus or a deep subscription tree, it is not. I have seen one bug shape many times on an event-heavy Unity project: an object's state changed quietly because a distant or global dependency fired an event. I built a small synthetic model of the mechanism, with eight game rules (armor, shield, apply, thorns, lifesteal, last stand, regen, death) as independent subscribers:

* **Order is the hidden variable:** across all 40,320 registration orders of the same rules there were **8 different final states**. Only one order in six gave the designed outcome, and half left a unit marked dead with HP above zero, or the reverse. The cascade itself was identical in an explicit sequence (51 handlers, four levels deep), so events did not make it deeper. They hid the order.
* **Three facts carried it:** armor and shield must run before apply, and last stand must run before death. With events they are written nowhere. In a direct sequence they are three consecutive lines in one function.
* **Broadcast cost follows listeners, not interest:** when every listener on a global bus filters by id, 2,000 events per frame against 512 listeners took about 1.4 ms in the model, and engine delegates cost more per call.

So the rule I take from it is that **sequence is a direct call, and events are notifications.** In the model, listeners get an immutable view and no access to the world, so a listener that tries to write state does not compile. That is the price tag on the advice in [Ownership Tax in Unreal Engine](OwnershipTaxUE.md) to broadcast changes, and it applies the components-do-one-thing, orchestrators-sequence split from [The Engineer-Designer Boundary in Unreal Engine](BlueprintMess.md). 

A convention does not hold this line on its own. On a Unity project, a tree of controllers had been introduced to contain a growing number of signals. It restricted where controllers could be created, but subscribing to a signal stayed cheap, and people kept doing it. The feature the team pointed to as the clean example had the same bypasses once I traced it, and the architect agreed when I walked through it. A boundary holds only while bypassing it costs more than the shortcut, which is also the finding of [Backward Compatibility](BackwardCompatibility.md).

---

## The Production Bottom Line

> **A Default Is Still a Decision:** Scheduling is architecture because when code runs, how often and in what order are structural decisions, whether or not anyone makes them. The engine's tick gave the aura a schedule nobody chose, and its registry was a small line in the captures next to the work that ran at that frequency. Moving the work onto events replaces it with another default: an order and a writer set that live in subscriptions instead of in code.
>
> Own the wake-up in one place, keep sequence as direct calls, and make observers read-only.
