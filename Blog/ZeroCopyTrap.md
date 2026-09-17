# The Zero-Copy Trap

Somewhere along the way, "pass by value and `std::move` it" became the modern C++ default answer to whatever `const Type&` used to handle. It is a reasonable-sounding rule, and it comes from real, well-argued guidance. What it does not come with is a guarantee that adding move machinery to a small, hot type is free, or even a wash.

I wanted to know whether that assumption actually holds at the point where it is supposed to matter: a small type, moved constantly, in a hot loop. Instead of debating the theory, I wrote two benchmarks to measure the hardware reality directly.

---

## The Blind Spot: Moving Isn't a CPU Instruction

The CPU does not have a native "move" operation. It copies bytes, or it passes a pointer. Everything C++ calls a move is an abstraction built on top of that physical reality. The gap between the language's promise and the hardware's execution shows up in two specific places.

### 1. The ABI Tax: Registers vs. Stack Spills

The first penalty is how a type gets passed to a function. Under both the Itanium and MSVC x64 ABI rules, a **trivially copyable type** (one with no user-defined copy constructor, move constructor, or destructor) is passed directly in CPU registers (`%xmm0`, `%rax`, `%rdx`), provided it fits within 8 or 16 bytes.

The moment you add a custom move constructor, even a trivial one, the type stops being trivially copyable. The ABI immediately refuses to pass it in registers. It gets passed indirectly instead, via a hidden pointer or spilled onto the stack frame, regardless of how small the payload actually is.

I tested this with two eight-byte structs holding the exact same two floats. The first was a plain, trivially copyable pair:

```cpp
struct TrivialPair
{
    float x;
    float y;
};

```

The second held the same two floats, plus a user-defined move constructor that does what a real move constructor typically must do: copy the values across and write zeros into the source so its destructor can safely execute:

```cpp
struct MovablePair
{
    float x;
    float y;

    MovablePair(MovablePair&& other) noexcept
        : x(other.x), y(other.y)
    {
        other.x = 0.0f; // The "tombstone" write-back
        other.y = 0.0f;
    }

    ~MovablePair() {}
};

```

Both structs were passed by value into a non-inlined function, run ten million times each:

| Passing Strategy | Latency | Relative Performance |
| --- | --- | --- |
| **Trivially copyable pass-by-value** | 2.175 ns/call | **Baseline (Registers)** |
| **Move-constructible pass-by-value** | 10.707 ns/call | **4.92x slower** |

Nothing about that move constructor was performing heavy computation. The cost was entirely the calling convention's response to the type no longer being trivial: fast register passing was traded away for memory indirection and stack writes before a single byte of actual work took place.

### 2. The Silent Fallback: Missing `noexcept` and Reallocation

The second penalty is what `std::vector` does when a move constructor is not marked `noexcept`. Vector growth relies on `std::move_if_noexcept`, which exists to preserve the strong exception guarantee: if a move constructor throws partway through resizing a buffer, the container cannot roll back safely, so it silently falls back to deep-copying every single element instead.

An engineer can write a fully functional move constructor, watch their code compile, and never realize the standard container has quietly chosen to ignore it.

I benchmarked this using a small heap-owning handle. The only difference between these two implementations is a single keyword:

```cpp
// Falls back to copying every element on reallocation
struct NotNoexceptHandle
{
    char* data = nullptr;
    NotNoexceptHandle(NotNoexceptHandle&& other) /* not noexcept */
    {
        data = other.data;
        other.data = nullptr;
    }
    ~NotNoexceptHandle() { std::free(data); }
};

// Actually moves elements on reallocation
struct NoexceptHandle
{
    char* data = nullptr;
    NoexceptHandle(NoexceptHandle&& other) noexcept
    {
        data = other.data;
        other.data = nullptr;
    }
    ~NoexceptHandle() { std::free(data); }
};

```

Alongside those, I tested a raw buffer that relocates elements with a single `std::memcpy` without invoking any constructors or destructors at all, matching how `TArray` and `folly::fbvector` operate internally:

```cpp
// No constructors, no destructors, just move the raw bytes
auto* newBuffer = static_cast<RelocatableHandle*>(
    std::malloc(sizeof(RelocatableHandle) * newCapacity));
std::memcpy(newBuffer, buffer, sizeof(RelocatableHandle) * size);

```

Growing a buffer of 100,000 elements from capacity $N$ to $2N$:

| Container Strategy | Reallocation Time | Relative Speedup |
| --- | --- | --- |
| **`std::vector` (non-`noexcept` move)** | 23.602 ms | Baseline (Silent copy fallback) |
| **`std::vector` (`noexcept` move)** | 3.820 ms | **6.18x faster** |
| **Manual buffer (`memcpy` relocation)** | 0.654 ms | **36.08x faster overall** |

Stack those two gaps together, and the naive, unmarked type is roughly **36x slower** than the trivially relocated version for growing the exact same 100,000 elements.

Neither gap is about how much work the move constructor body performs. Both are about whether the type or the container was ever structured to bypass the constructor-and-destructor dance entirely.

---

## The Fix: Design for Trivial Relocation

None of this is an argument against move semantics. It is an argument against treating a move constructor as a default modernization pattern instead of an explicit architectural decision.

### 1. Keep Small Data Trivially Copyable

Pass small, plain structs by value or by `const&`, and stop there. If a type is purely data (coordinates, colors, small math primitives), giving it a user-defined move constructor does not make it faster. It disqualifies the type from CPU register passing and buys nothing in return, because there was never an allocated heap resource to transfer in the first place.

### 2. Reserve `std::move` for True Ownership Transfer

A move constructor earns its keep when it is genuinely handing off an expensive, non-shareable resource: a heap buffer, an OS handle, or an exclusive lock.

This mirrors the ownership discussion in [Ownership Tax in Unreal Engine](https://www.google.com/search?q=OwnershipTaxUE.md). Once you move an object, you create a "moved-from" tombstone state that must be handled safely everywhere it is accessed afterward. That is an architectural burden you introduce on purpose for large resources, not a micro-optimization to spray across plain data.

### 3. Mark Every Real Move Constructor `noexcept`

This is a near-free performance win. It is the sole difference between a standard container utilizing your move logic or silently discarding it. If you cannot mark a move constructor `noexcept` in good faith, treat that as an architectural warning sign that the type's ownership boundaries are blurred, not merely as a missing keyword.

### 4. Treat Relocatability as an Architectural Choice

For hot collections of many objects, determine whether your type can be **trivially relocated** (moved in memory via a bitwise `memcpy` without needing fixups or destructors).

This aligns directly with [Data Layout Is Architecture](https://www.google.com/search?q=DataLayoutIsArchitecture.md): memory shape is an intentional choice, not a language default.

* **Facebook Folly (`fbvector`):** Uses an explicit type trait, `folly::IsRelocatable`, allowing the container to bypass calling thousands of move constructors in favor of `std::memcpy`.
* **EASTL:** Implements `has_trivial_relocate` for high-throughput container resizing.
* **Unreal Engine (`TArray`):** Relies on `TIsTriviallyCopyConstructible` and `FMemory::Memmove` by default during reallocations, sidestepping standard C++ move overhead entirely.
* **ISO C++ (P1144 / P2786):** The proposed `std::is_trivially_relocatable` aims to bring this exact engine-level hardware reality into standard C++.

---

## The Architectural Insight: Ownership Model vs. Hardware Reality

The recurring mistake is treating "idiomatic modernization" as synonymous with "hardware optimization."

A move constructor is an **ownership contract**: it declares that one object now exclusively owns a resource that another object used to hold. Ownership is a boundary decision that belongs at the point where system responsibilities change. Plain data does not need an ownership model: it needs an intentional memory layout.

When you add custom move semantics to plain data, you force the hardware to treat simple bytes as an ownership negotiation. You pay for stack allocations, tombstone writes, and lost register slots, all to simulate moving something that was already trivial to copy.

And when a type does genuinely own a heap resource, it still owes the container an explicit `noexcept` contract. Without it, you are paying the maintenance and cognitive cost of move machinery that the compiler quietly ignores at runtime.

---

## The Production Bottom Line

> **The CPU Doesn't Move; It Copies:** Hardware moves data by copying bytes or passing pointers. Every abstraction built on top of that (move constructors, container growth algorithms, and ABI calling conventions) is a choice about how much hardware reality to hide, and at what performance cost.
> Adding a move constructor to an eight-byte struct did not make it faster; measured directly, it made passing the exact same data **4.92x slower** simply by disqualifying it from CPU registers. And a genuine move constructor without a `noexcept` specifier is an invisible instruction to standard containers to fall back to deep copies, paying a **6.18x penalty** on reallocations.
> Trivial relocation, the pattern game engines and low-latency libraries rely on, is not a micro-optimization layered on top of move semantics. It is the architectural recognition that most data was never an ownership problem to begin with, and shouldn't be dressed up as one.