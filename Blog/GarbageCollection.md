# Garbage Collector Spikes

You are profiling your game, and everything looks perfect. The frame times are sitting at a buttery-smooth 16.6ms (60 FPS). Then, out of nowhere, the game hitches. A random, violent spike shoots up to 45ms, drops a frame or two, and immediately vanishes.

If you look closer via Unreal Insights or Unity’s Profiler, you’ll find the culprit hiding behind an innocent name: `Garbage Collection`.

We look at garbage collection as a magical janitor that runs quietly in the background. But in high-performance environments like Unreal Engine C++ or Unity C#, the GC is not a passive background worker—it is a stop-the-world process that can fundamentally ruin your game’s game-thread performance if you ignore how it works under the hood.

---

## The Core: Unreal’s UObject Clustering vs. Unity’s Managed GC

While both engines use automated memory management for their object hierarchies, they solve the problem in fundamentally different ways based on their low-level programming models.

### 1. Unreal Engine: The UObject Clustering Pipeline

Even though Unreal is written in native C++, it implements its own Garbage Collector specifically to manage `UObject` lifecycles and prevent memory leaks. Unreal’s GC uses a **Mark-and-Sweep** algorithm, but with a highly specialized optimization called **UObject Clustering**.

* **How it works:** Unreal groups related, long-lived assets (like a parsed level data asset, a material graph, or a blueprint template) into a static "Cluster." During the expensive **Mark** phase, the engine treats the entire cluster as a single node. Instead of verifying the lifecycle of 10,000 individual internal components, it checks the root of the cluster once.
* **The Trap:** Code that creates large numbers of transient `UObject`s, maintains unnecessary hard references, or prevents objects from being grouped efficiently can increase the amount of work the GC has to perform. In practice, this turns what should be a small reachability pass into a much larger traversal.
### 2. Unity: Generational and Incremental C# GC

In contrast, Unity relies on the managed C# garbage collection environment. Modern Unity versions can use Incremental GC, which spreads portions of the collection work across multiple frames, while older/non-incremental modes can cause more noticeable stop-the-world pauses.

* **How it works:** Unity's Incremental GC attempts to split the heavy Mark-and-Sweep work across multiple frames to avoid a single catastrophic spike. It tracks object references across a managed heap.
* **The Trap:** Unlike C++, where memory allocations are explicitly mapped to hardware boundaries, C# makes heap allocation invisible. Typing `new MyClass()` inside a high-frequency loop quietly requests space from the managed heap. If those allocations cross frame boundaries, the GC eventually *must* pause the main game thread to sweep the garbage.

---

## The Practice: Writing Zero-Allocation Gameplay Loops

To prove senior-level engineering capability to a Tech Lead, your code should never rely on the engine's GC to clean up after routine gameplay updates. High-frequency loops (like weapon fire systems, movement simulations, or particle tracking) must achieve **zero runtime allocation**.

Here are the strict production disciplines you must enforce in your modules:

### 1. Value Types vs. Reference Types (`USTRUCT` vs. `UCLASS`)

In Unreal C++, a `UCLASS` is instantiated on the heap and tracked by the `GUObjectArray` for garbage collection. A `USTRUCT`, however, behaves like a value type—it lives on the stack or inline inside the class that owns it.

```cpp
// ❌ NAIVE: Creating a full heap object for a temporary combat calculations struct
UMyCombatCalculator* Calc = NewObject<UMyCombatCalculator>(this);
Calc->Execute(Target); // Adds unnecessary UObject lifetime and GC tracking overhead.

//  SENIOR: Pure value type. Allocated on the stack, instantly popped when the block ends. Zero GC impact.
FCombatParameters TempParams;
TempParams.Magnitude = 5.0f;
ProcessCombat(TempParams); 

```

### 2. The Trap of Lambda Captures in Ticks and Timers

Lambda expressions are highly convenient for setting up quick callbacks or delayed functions, but they hide a massive allocation trap: **Variable Captures**.

```cpp
// ❌ NAIVE: Capturing by value creates a hidden heap-allocated copy of the structure
GetWorld()->GetTimerManager().SetTimer(Handle, [=]() {
    GEngine->AddOnScreenDebugMessage(-1, 5.f, FColor::Red, CapturedData.ToString());
}, 1.0f, false);

//  SENIOR: Pass explicit weak pointers or pointers to avoid closure state heap allocations
GetWorld()->GetTimerManager().SetTimer(Handle, FTimerDelegate::CreateUObject(this, &AMyActor::OnTimerComplete, CoreTargetID), 1.0f, false);

```

*Capturing variables by value (`[=]`) inside an anonymous closure creates a hidden capture-class instance on the heap. In hot paths, especially when the closure is stored in delegates, timers, async tasks, or type-erased containers, that state can contribute to hidden copies, lifetime complexity, and possible allocations.*

### 3. Object Pooling Pitfalls: Clean State Resetting

Everyone knows you should use Object Pools for high-count entities like projectiles or damage numbers instead of continuously calling `SpawnActor` and `Destroy`. However, juniors often create a secondary problem: **Memory Leaks via Stale References**.

When you return a `UObject` to a pool, you *must* explicitly null out its internal arrays and pointers. If an inactive pool object holds onto a reference to a dying combat target, Unreal's GC cannot free that target, causing a massive memory leak that quietly scales up over a play session.

```cpp
void AProjectilePool::DespawnProjectile(AProjectileActor* Projectile)
{
    if (IsValid(Projectile))
    {
        // CRITICAL: Clean state resetting prevents GC holding traps
        Projectile->SetActorHiddenInGame(true);
        Projectile->ClearTrackingReferences(); // Clear internal TMaps/TArrays completely!
        
        InactivePool.Push(Projectile);
    }
}

```
A pool reduces allocation churn, but it also extends object lifetimes. That means every retained reference inside a pooled object becomes more important, because the object may remain reachable for the entire match or level.

---

## The Production Bottom Line

> **The Discipline Heuristic:** Managing the Garbage Collector is a battle won during early architecture development, not during final optimization sweeps. By strictly utilizing `USTRUCT` for transient math processing, neutralizing hidden lambda allocations, and respecting the engine's internal object clustering logic, you prevent structural frame-time hitches before they ever manifest in production.
