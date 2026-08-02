# Data Layout Is Architecture

Before I moved fully into game systems work, most of my production experience was in C#. In that world, OOP paired with SOLID principles isn't just "clean code," it's the correct engineering default. Encapsulation, single responsibility, dependency inversion: these give you a framework for building something extensible, something a team can grow without it collapsing under its own weight. Performance was a secondary concern, a tax you'd pay later if you ever needed to, in exchange for a codebase that stayed sane.

I carried that assumption into game development. It felt reasonable right up until I measured it myself.

I built [ParticleSim](https://github.com/Atimormia/ParticleSim), a sandbox particle simulation, specifically to stop assuming and start measuring. The first thing I benchmarked was the most basic architectural decision in the whole project: how the particle data is laid out in memory. The result wasn't a rounding error. It was a 5 to 6x difference in update time, using the exact same logic, the exact same particle count, nothing changed except the shape of the data.

---

## The Blind Spot: Human Thinking vs. CPU Execution

A `Particle` struct that bundles position, velocity, acceleration, lifetime, and an alive flag into one block feels correct. It matches how you think about a particle conceptually: one thing, with properties. SOLID principles are built around relationships between concepts like this, and for years that mental model served me well.

The problem is that the CPU has no concept of a particle. It has cache lines.

A CPU doesn't load a single variable from memory. It loads a fixed-size cache line, typically 64 bytes, and pulls it up through a hierarchy: L1 cache first (a few dozen KB, fastest), then L2 (a few hundred KB to a few MB, slower), then L3 (shared across cores, several MB, slower still). If your particle struct is large and a hot loop only touches the position field, you still pay for every other byte riding along in that cache line. Iterate over 100,000 particles this way, and you're moving far more memory than the loop actually needs, most of it dead weight the CPU fetched for nothing.

Cache locality isn't the only mechanism at play, either. When a field's values sit in one contiguous array of the same type, the compiler has a much easier time auto-vectorizing the loop, issuing a single SIMD instruction across several particles at once instead of one instruction per particle. A scattered AoS loop can't do that as cleanly, since consecutive iterations aren't reading contiguous, uniformly-typed memory. The benchmark numbers later in this post are the combined effect of both: fewer wasted cache line bytes, and a loop shape the compiler can vectorize.

This is exactly why a framework can be right on one axis and silently wrong on another. SOLID never promised cache locality or vectorizable loops. It was never trying to.

---

## The Fix: Structure of Arrays

The first ParticleSim benchmark compared two implementations behind the same interface: `ParticleSystemDataAoS`, a plain `std::vector<Particle>`, against `ParticleSystemDataSoA`, where each field lives in its own contiguous array.

| Particle Count | AoS | SoA |
| ---: | ---: | ---: |
| 1,000 | 457 ns | 83.6 ns |
| 10,000 | 479 ns | 87.6 ns |
| 50,000 | 597 ns | 110 ns |
| 100,000 | 880 ns | 165 ns |
| 500,000 | 4,796,166 ns | 3,637,222 ns |
| 1,000,000 | 9,721,137 ns | 7,228,000 ns |

Same update logic. Same particle count. The only difference is memory shape, and SoA wins by 5 to 6x through 100,000 particles.

Look closer at the jump between 100,000 and 500,000, though. Update time per particle stays flat and low right up through 100,000, then explodes by roughly 4,000x at 500,000, for both layouts. That's the point where the working set stops fitting in L2 and the loop stops being compute-bound. It becomes bandwidth-bound: you're just waiting on memory to arrive, and no layout decision helps you once that's true. SoA still wins at that scale (3.6ms vs 4.8ms), but the margin shrinks from 5-6x down to about 24%, because both versions are now paying the same bandwidth tax.

That's the first lesson: **SoA isn't a universal win**. It's a win up to the point where you're bandwidth-bound regardless of layout, and past that point the honest answer is "neither layout saves you."

### Buying Parallelism

Contiguous, field-separated arrays don't just help the cache, they also make the update loop trivially parallel. Because each field lives in one contiguous array, splitting the loop across worker threads is just splitting an index range: each thread owns a slice of the array and never touches another thread's slice, so there's nothing to synchronize.

That paid off directly when I parallelized the particle update loop: raw pointers to each SoA array pulled once before the loop, chunked by thread, no locks, no shared mutable state. Just contiguous memory divided by thread count. Deeper concurrency tradeoffs, like what happens when the workload isn't this cleanly divisible, are their own topic for another post. But it's worth naming here: the same layout decision that wins on cache locality also removes the hardest part of going parallel.

### The Cost

This is the part that's easy to skip once the benchmarks look this convincing, and it's the part that actually matters for the architecture-first argument. **SoA is not free**. It costs you some of what SOLID was giving you in the first place.

- **Harder to size dynamically.** An AoS collection is just a `std::vector<Particle>`, it grows however it needs to. An SoA layout wants a known capacity up front, since every field array has to grow in lockstep, and a naive implementation either pre-allocates for a worst case or pays a resize cost across every array at once instead of one. `ParticleSystemDataSoA` takes a `capacity` in its constructor for exactly this reason.
- **Harder to generalize.** A `Particle` type with polymorphic behavior doesn't map cleanly onto parallel flat arrays. There's no natural place to hang per-type logic anymore, because there's no longer a single object to attach it to. Subclassing gets worse still: a derived type either has to reuse its parent's arrays and indices, or duplicate the whole layout for a handful of new fields.
- **Harder to read and extend.** Adding a field to an AoS struct is a one-line change. Adding a field to an SoA layout means touching every array, every loop, every call site that iterates the data, at least without something built specifically to prevent that. The encapsulation that made SOLID work, one point of change, is partly what you're trading away for throughput.

None of that is an argument against SoA. It's an argument against treating it as a default. The readability and extension costs above are real, but they're recoverable, at the price of a complexity layer that has to live somewhere. The boundary below is that layer.

---

## The Architectural Boundary: Interface Over a Volatile Layout

The actual architecture here is one decision, stated plainly: the interface doesn't change when the layout does. `update`, `add`, `size`, `positions` stay the same whether the data underneath is a `std::vector<Particle>` or five separate arrays. That's what lets the memory shape be revisited per system later without anything outside that boundary needing to know or care.

Let's look at the mechanics: the specific C++ techniques that make that boundary cheap to hold in this particular language. Tags, concepts, fold expressions, none of that is the point on its own. They're what it takes to keep the interface stable and readable at the same time, in a language without reflection to do it for you.

### Naming Fields Instead of Indexing Them

The naive version of SoA collapses every field into a raw array index: `storage[0]` for position, `storage[1]` for velocity, and so on. That's exactly the readability cost from above, since it turns every call site into something you have to cross-reference against a comment to understand.

The fix is a tag-struct pattern. Each field gets an empty struct as its compile-time identity:

```cpp
template <typename Tag>
struct FieldTag
{
    using tag = Tag;
};

template <typename Tag, typename First, typename... Rest>
struct FieldIndex<Tag, First, Rest...>
{
    static constexpr size_t value =
        is_same_v<typename First::tag, Tag>
            ? 0
            : 1 + FieldIndex<Tag, Rest...>::value;
};
```

`FieldIndex` walks the field list at compile time and resolves a tag like `Position` to its position in the tuple, so `particles.field<Position>()` reads like a named lookup but compiles down to a plain `get<N>(fields)` with no runtime cost at all. A companion fold expression, `HasField_v`, checks whether a tag exists among the fields, and gets used as a constraint on `field<Tag>()`:

```cpp
template <typename Tag>
    requires HasField_v<Tag, Fields...>
auto &field()
```

Ask for a field that doesn't exist, and the code fails to compile. That's a stronger guarantee than the AoS version ever gave you: a typo'd member name in a struct is also a compile error, so this doesn't buy safety SoA didn't already have, it buys back the readability that raw index access would have thrown away.

Put together, a real field list looks like this:

```cpp
struct Position {};
struct Velocity {};
struct Acceleration {};
struct Lifetime {};
struct Alive {};

using ParticleSoA = SoAContainer<
    SoAFieldVector2D<Position>,
    SoAFieldVector2D<Velocity>,
    SoAFieldVector2D<Acceleration>,
    SoAFieldScalar<float, Lifetime>,
    SoAFieldScalar<uint8_t, Alive>
>;
```

Five tags, five typed fields, and `particles.field<Position>()` reads exactly like the name says.

### One Container, Any Field Set

The second piece of the generalization is not writing a bespoke SoA class per data type. `SoAField` is a concept that defines the minimum contract any field must satisfy:

```cpp
template <typename F>
concept SoAField = requires(F f, size_t n) {
    { f.reserve(n) } -> same_as<void>;
    { f.resize(n) } -> same_as<void>;
    { f.size() } -> same_as<size_t>;
    { f.push_default() } -> same_as<void>;
};
```

Because that contract is a concept and not a base class, there's no vtable involved anywhere in the hot path, matching the same instinct behind [the true price of a virtual function](VirtualFunctions.md). `SoAContainer` then takes any number of fields satisfying that contract and stores them as a `tuple<Fields...>`, broadcasting operations across all of them with a fold expression instead of a loop:

```cpp
void reserve(size_t n)
{
    apply([&](auto &...f)
          { (f.reserve(n), ...); }, fields);
}

void push_back()
{
    apply([&](auto &...f)
          { (f.push_default(), ...); }, fields);
}
```

`(f.reserve(n), ...)` expands at compile time into one call per field, in order, with the field types and count baked in. Adding a new field to `ParticleSoA` means adding one line to the type alias, not touching `SoAContainer` at all. That's the one-point-of-change property the cost section above said SoA usually takes away, recovered through the type system instead of through an object model.

### Bounds Safety at Compile Time

The base storage for a field (`SoAFieldBase`) generalizes both scalar fields like `Lifetime` and multi-component fields like a `Vector2D` position under one implementation, using a fixed-size `array<vector<T>, Components>`. Component access is guarded by a concept rather than a runtime check:

```cpp
template <size_t K, size_t Components>
concept ComponentIndex = (K < Components);

template <size_t K>
    requires ComponentIndex<K, Components>
T *data() noexcept { return storage[K].data(); }
```

Asking for `data<2>()` on a two-component field fails to compile. There's no bounds check happening at runtime, because there's nothing left to check by the time the program runs.

### The Payoff

None of this machinery is visible to the code that actually consumes a `ParticleSystemDataSoA`. It exposes the same `update`, `add`, `size`, `positions` interface as the AoS version:

```cpp
class ParticleSystemDataSoA
{
public:
    ParticleSystemDataSoA(size_t capacity = 100000);

    void update(float dt, bool compact = false);
    size_t add(const Particle &p);
    size_t size() const;

    span<const core::Vector2D> positions();
};
```

Both classes expose the exact same interface. The caller never needs to know which layout it's talking to, and never touches `field<Tag>()` or `SoAContainer` directly at all, that machinery stays internal to the SoA implementation. That's the actual senior move here: not "SoA is correct now," but deciding the memory shape per system, behind a stable contract, so the decision can change later without rippling outward. `std::span` does real work in that contract too: it lets the SoA implementation hand out a non-owning view into its internal arrays without copying them out, so consumers get contiguous access without breaking encapsulation.

This is what keeps that cost contained: pay it once, in the container implementation, and let every caller keep reading like normal, structured code.

### C++ Limitations
Worth being honest about the limits of this, too. I originally wanted the container to generalize further, to handle a field that's itself a nested type (a `Vector2D` inside a `Particle`, for instance) without hand-declaring it as a special case. Doing that properly means the container needs to know a type's shape at compile time without being told, which is exactly what reflection is meant to give you. C++ is only just getting there: static reflection was voted into C++26, and as of this writing it's still experimental, available in an unofficial Clang fork rather than any shipping compiler. Getting there without reflection means either writing it by hand per type, as I did, or reaching for a macro-based code generator.

A few approaches other people have tried on the way to a more general SoA layout:

- **SoAx** is a limited version of this same generalization, built for one domain (particle-heavy HPC code) rather than for arbitrary types. Broader attempts exist and run into the same wall.
- Boost.PFR-based libraries like **AoAoAoTT** can decompose an arbitrary struct into SoA automatically, but they can't handle nested or empty types, the same gap I ran into.
- The most ambitious attempt I found is a 2025 proposal out of **Durham University** for a compiler extension that lets a developer annotate code so the compiler converts between AoS and SoA automatically, for arbitrary structures, based on context. It's a genuine research direction, and probably the closest thing to a real answer here, but the authors themselves note there's no automatic view construction available yet.

C++ is a lot slower to generalize this kind of problem than a language with built-in runtime reflection like C#, and I'd guess it's a couple more years before something like this is standard practice rather than a paper. Until then, hand-writing the field list per type, the way this container does, is the practical answer, not a shortcut around a solved problem.

_(Full source, including the SoA container, the particle system, and every benchmark referenced here, is in [ParticleSim](https://github.com/Atimormia/ParticleSim) repository.)_

---

## The Production Bottom Line

> **Architecture First:** We can still write clean code while optimizing for performance. Data layout is a design decision, not a surrender of design. The AoS version of ParticleSim wasn't buggy and wasn't unprofiled. It was architected for readability first, the same instinct SOLID trained into me, and it paid a 5x tax before anyone ever opened a profiler to find it. The fix wasn't abandoning that instinct everywhere. It was learning exactly where to spend it, and building a boundary clean enough that the decision can be revisited per system instead of once, for the whole codebase, up front.
