# The Cost of a Virtual Function

A projectile system ships with a clean hierarchy: `AProjectile`, `ABullet`, `AFireBullet`, each overriding a virtual `OnUpdate()`. It runs well in the first playtests with a few dozen projectiles in flight. Months later a new weapon type fires hundreds of pellets per shot, and the update loop starts showing up in captures. The profiler shows no single guilty function. It shows a loop that is slower than the sum of what its bodies do.

Nobody made a mistake here. The hierarchy was the right shape for the system the team believed it was building. What changed was the system's frequency, and nothing in the design said where the abstraction was supposed to stop.

---

## The Blind Spot: One Model for Every System

If you come from a managed-language background (C# or Java), polymorphism is the default tool. You create an abstract base class like `AEnemy`, mark a method `virtual`, override it in `AGoblin` and `AOrc`, and call it in a loop. That instinct is sound for most of a game's code, and there are two easy ways to get this topic wrong:

* **The Reactive Approach:** Use `virtual` everywhere and fix whatever the profiler flags. Usually fine, until a system that was never expected to be hot becomes hot, with a dozen features already built on its base class.
* **The Anti-Virtual Approach:** Treat `virtual` as a performance bug and strip it out on principle. That removes the seam designers and other programmers rely on, and buys nothing in the large part of the codebase that runs a few times per frame.

Why neither survives a real project is the subject of [Where Abstraction Meets The Hot Path](AbstractionMeetsTheHotPath.md). This post is about the mechanism underneath: what a virtual call actually does to a loop, and what the alternatives look like. Runtime polymorphism is not the problem. **Applying the same dispatch model to a UI manager and to 100,000 hot-loop entities is.**

When a class has a virtual function, the compiler generates a **Virtual Method Table (Vtable)**, and every instance carries a hidden pointer (the `vptr`) to it.

![vtable_layout.svg](misc/vtable_layout.svg)

Taken alone, one virtual call is cheap: a couple of dependent loads and an indirect jump. The cost appears when that call sits in a loop over many objects, and it has three separate sources:

1. **Scattered objects:** An array of base pointers usually points at heap objects allocated at different times. Reading each `vptr` means touching each object, so the loop pays for poor locality before any dispatch happens. This is the same memory-shape problem described in [Data Layout Is Architecture](DataLayoutIsArchitecture.md).
2. **Lost inlining:** The compiler cannot see through a call whose target is only known at runtime. A body that would collapse into a few instructions stays a real call, and every optimization that depends on seeing across that call (vectorization, hoisting, dead-code removal) is blocked.
3. **Unpredictable dispatch:** If `AGoblin` and `AOrc` are interleaved in the array, the indirect branch target changes from iteration to iteration. A branch predictor handles a stable pattern well and a shuffled one poorly. Different derived classes also live in different regions of code, which adds instruction cache pressure.

Each source is small per call. Multiplied by entity count and frame rate, they add up to the shape [Where Abstraction Meets The Hot Path](AbstractionMeetsTheHotPath.md) describes: frequency times a boundary the compiler cannot see across.

A [published case](https://realtimerendering.com/blog/?p=14) shows what that adds up to in production. On a PS3 project a physics programmer followed a simple rule: if one function in a class is virtual, make them all virtual. Physics code makes a lot of calls, and the extra dispatch added up. Eberly removed the unnecessary `virtual` modifiers and cut frame time by 5 ms, in a game targeting 30 fps (a 33 ms frame), so roughly 15% of the budget. Polymorphism stayed where it was needed. What went away was dispatch nobody had chosen.

> **The Unity / C# Perspective:** Managed environments make virtual methods, interfaces, and delegates feel like one abstract cost, and developers often build a habit of ignoring invocation overhead. In C++, where memory layout and dispatch model are explicit, that habit gets expensive in the narrow set of systems that run at high frequency. These costs are real in both worlds. C++ simply makes them visible and puts the decision in your hands.

---

## The Fix: Move the Dispatch Up a Level

If you are writing high-level systems like UI managers, quest logic, or GameMode rules, a standard `virtual` function is the right choice. Instance counts are low, designers and other programmers benefit from the seam, and the overhead is not measurable against everything else in the frame.

For high-frequency, high-count systems (a projectile manager processing thousands of active bullets per frame, mass AI agents, particle behaviors, inventory modifiers evaluated across a whole collection), there are options that keep the variation without paying per-element dispatch. The first four differ in where the decision is made and what they cost. The fifth is the check that comes before any of them.

| Option | Where the decision is made | Type set | Main cost |
|---|---|---|---|
| 1. Batch by type | Once per array | Open: a new type is a new batch | One container per type |
| 2. Flat data | As a value inside one loop | Open: a new type is a new data row | Branches multiply as behavior diverges |
| 3. Closed-set variants | Per element, but visible to the compiler | Closed | Element size, recompiles at every visit site |
| 4. CRTP and templates | Once per type, at compile time | Closed | Build times, diagnostics, no mixed array |

### 1. Batch by Type

Often the cheapest change is not removing polymorphism but moving it up a level. Keep one flat array per projectile type and call the update once per array, not once per element. The virtual call, or a plain function call, now happens a handful of times per frame, and the inner loop is a tight pass over contiguous data.

```cpp
// Before: one virtual call per element, mixed types behind base pointers
for (AProjectile* Projectile : AllProjectiles)
{
    Projectile->OnUpdate(DeltaTime); // indirect call, target changes per iteration
}

// After: the virtual call moves up to the batch
class IProjectileBatch
{
public:
    virtual ~IProjectileBatch() = default;
    virtual void UpdateAll(float DeltaTime) = 0;
};

template <typename T>
class TProjectileBatch : public IProjectileBatch
{
public:
    virtual void UpdateAll(float DeltaTime) override
    {
        // One concrete type over contiguous storage: the call is inlinable
        for (T& Item : Items)
        {
            Item.OnUpdate(DeltaTime);
        }
    }

private:
    TArray<T> Items;
};

// The manager pays a handful of virtual calls per frame, not thousands
for (IProjectileBatch* Batch : Batches)
{
    Batch->UpdateAll(DeltaTime);
}
```

The seam survives: adding a new projectile type means adding a new batch, and the manager does not change.

### 2. Flat Data

Instead of a deep inheritance chain (`AProjectile` $\rightarrow$ `ABullet` $\rightarrow$ `AFireBullet`), express variation as data: a flat `USTRUCT` with parameters, and a specialized system that processes them in a predictable loop. Behavior differences become values and small branches, not separate classes with separate code paths.

```cpp
// Variation lives in a row of data, one per projectile type
USTRUCT()
struct FProjectileParams
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere) float Gravity = 0.f;
    UPROPERTY(EditAnywhere) float BurnDamagePerSecond = 0.f; // 0 means no burn
};

// Per-projectile state is small, plain, and stored contiguously
struct FProjectileState
{
    FVector Position;
    FVector Velocity;
    float   BurnTimeRemaining = 0.f;
    int32   ParamsIndex = 0; // which row of FProjectileParams this one uses
};

void UProjectileSystem::Update(float DeltaTime)
{
    for (FProjectileState& P : Projectiles) // TArray<FProjectileState>
    {
        const FProjectileParams& Params = ParamsTable[P.ParamsIndex];

        P.Velocity.Z -= Params.Gravity * DeltaTime;
        P.Position   += P.Velocity * DeltaTime;

        // A fire bullet is a row with a non-zero value, not a subclass
        if (Params.BurnDamagePerSecond > 0.f)
        {
            P.BurnTimeRemaining -= DeltaTime;
        }
    }
}
```

This works while the variation is parameters and a few stable branches. Once the types need genuinely different code, the branches multiply and option 1 is the better fit. Designers also keep their seam, since a new projectile type is a new row in a data table, not a new class.

### 3. Closed-Set Variants

When the set of types is closed and small, `std::variant` keeps per-element variation but makes it visible to the compiler. The objects are stored by value in one array, and `std::visit` sees every alternative at compile time.

```cpp
using FProjectile = std::variant<FStandardBullet, FFireBullet, FPellet>;

TArray<FProjectile> Projectiles; // by value, contiguous, no pointer to chase

for (FProjectile& P : Projectiles)
{
    // The visitor is generated for each alternative, so each OnUpdate can be inlined
    std::visit([DeltaTime](auto& Bullet) { Bullet.OnUpdate(DeltaTime); }, P);
}
```

Against the three cost sources, a variant fixes two and leaves one:

* **Scattered objects (fixed):** The objects live in the array, so there is no `vptr` to load from a heap object.
* **Lost inlining (mostly fixed):** The compiler knows every possible target, so each call can be inlined into its own branch.
* **Unpredictable dispatch (still there):** The variant's index is still branched on per element, so an interleaved array gives you a shuffled switch instead of a shuffled indirect call. It gets cheap when the data is grouped by type, which is option 1 again.

Two costs come with it:

* **Element size:** Every element is as large as the biggest alternative, so one fat type inflates the whole array.
* **A closed set:** Adding a type changes the variant and recompiles every visit site, the same trade-off as CRTP below.

In engine code, UE5's own `TVariant` and `Visit` fill the same role.

### 4. CRTP and Templates

When the set of types is known at build time and you want polymorphic-looking code without runtime dispatch, the **Curiously Recurring Template Pattern (CRTP)** resolves calls at compile time (static binding), which lets the compiler inline them.

```cpp
// Base class template that uses compile-time static polymorphism
template <typename Derived>
class TProjectileBase
{
public:
    void Update(float DeltaTime)
    {
        // Static cast resolves the method at compile time: no Vtable lookup
        static_cast<Derived*>(this)->OnUpdate(DeltaTime);
    }
};

// Derived implementations
class FStandardBullet : public TProjectileBase<FStandardBullet>
{
public:
    void OnUpdate(float DeltaTime)
    {
        // Direct, inlinable machine instructions
    }
};
```

CRTP has costs of its own:

* **No mixed array:** Different `Derived` types are unrelated types, so you cannot keep them in one heterogeneous array, which is why it pairs with option 1 (one container per type).
* **Build times and diagnostics:** Heavy template use lengthens builds and makes error messages harder to read.
* **A locked type set:** The types are fixed at compile time, so designers cannot extend them without an engineer.

Those trade-offs are covered in [Compile-Time Performance vs. Runtime Flexibility](CompileTimeVsRuntime.md). Reach for it when a hot path has stopped changing, not as a default.

#### Smaller Tools

Three more things come up in this conversation, and none of them is a numbered option:

* **`final` on leaf classes:** It lets the compiler devirtualize calls it can already resolve statically. That is free, but it does nothing for a loop over base pointers, where the dynamic type is still unknown.
* **LTO and PGO builds:** They can devirtualize speculatively. That is a build setting, not an architecture decision, so it helps at the margin and should not be the plan.
* **`std::function` and type-erased callbacks:** These are not a way out. They are dynamic dispatch with an extra indirection, often an allocation too.

### 5. Measure First

Do not rewrite a working hierarchy on principle. Profile the loop at realistic entity counts, and compare against a batched or flat version of the same logic. A conversion that is not justified by a measurement is the same mistake in the other direction: a boundary removed on instinct. The 5 ms above is another team's number on another platform. A capture at your own entity counts is the only evidence that should drive the change.

---

## The Insight: Move the Decision Up, or Make It Visible

The options above look different, but they make one of two moves:

* **Change the level of the decision:** A virtual call per element decides the behavior N times per frame, at the point where the compiler cannot see the target, against objects scattered across the heap. Batching by type decides it once per array. Flat data decides it as a value inside a loop whose branches are stable. CRTP decides it once per type at compile time. In each case the inner loop ends up looking at one concrete behavior over contiguous data, which gives inlining, prefetching, and branch prediction something to work with again.
* **Make the decision visible:** A variant still branches on its index for every element, but the objects sit in the array and the compiler sees every alternative, so the call can be inlined. That fixes locality and inlining and leaves prediction to the data, which is why a variant over interleaved types behaves best once the array is grouped by type: the first move again.

So polymorphism is not removed. It is relocated to the level where the count is low and the seam is still useful, or kept where the compiler can see through it. The PS3 case is the simplest version of the same principle: the dispatch that went away was dispatch that had never been buying any variation.

This also explains why the hierarchy in the opening looked fine for months. The `virtual` keyword is a decision about where the behavior is chosen, and `OnUpdate()` per element is the lowest possible level to make it. That is a good default for code that runs a few dozen times. It stops being one when the count grows, and the fix is a change of level or of visibility, not a rewrite of the behavior.

The second move is the Boundary Type term from the formula in [Where Abstraction Meets The Hot Path](AbstractionMeetsTheHotPath.md): a variant does not lower the frequency, it changes how much of the boundary the compiler can see. Deciding when a system needs either move, and who notices that its frequency has changed, is a separate question. That post takes it up for whole call chains, and [The `Tick()` Pitfalls](TickPitfalls.md) does the same for scheduling.

---

## Production Bottom Line

> **Dispatch Belongs to the Batch, Not the Element:** A single virtual call costs a couple of loads and an indirect jump. The expense comes from paying it per element across scattered, mixed-type objects, where it blocks inlining, scatters memory access, and makes the branch target unpredictable. In a UI manager or a GameMode rule, none of that is measurable, and the seam is worth keeping.
>
> In a hot loop, the answer is rarely to give up polymorphism. Decide the variation once per array, once per value, or once per type at compile time, so the inner loop sees one concrete behavior over contiguous data, or keep it per element in a closed set the compiler can see through. Check the change against a capture at your own entity counts before making it.