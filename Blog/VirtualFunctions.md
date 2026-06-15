# The Cost of a Virtual Function

If you come from a pure software engineering or managed language background (like C# or Java), polymorphism feels natural. You create an abstract base class like `AEnemy`, mark a method as `virtual`, override it in `AGoblin` and `AOrc`, and call it in a loop. It feels clean, object-oriented, and safe.

But in high-performance game development using C++ and Unreal Engine, **virtual functions carry an invisible tax** that can quietly decimate your CPU cache efficiency if applied blindly to thousands of actors.

---

## The Blind Spot: The Vtable and Cache Misses


When a class in C++ contains a virtual function, the compiler creates a **Virtual Method Table (Vtable)** for that class. Every single instance of that object in memory receives a hidden pointer (the `vptr`) that points directly to this table.

```
[ Actor Instance in Memory ]
└── float Health
└── FVector Position
└── vptr ───────────────────────► [ Class Vtable ]
                                  └── OnTakeDamage() ──► Resolves to: AGoblin::OnTakeDamage()

```

When you iterate through an array of base pointers and call a virtual function:

1. **Double Pointer Indirection:** The CPU must read the object's memory to find the `vptr`. Then it must follow the `vptr` to find the Vtable. Finally, it must look up the function pointer inside the Vtable to jump to the actual machine instructions.
2. **The Cache Catastrophe:** Because different derived classes (`AGoblin`, `AOrc`) have their code compiled in different regions of executable memory, your CPU is forced to wildly jump around to execute instructions. This forces instruction cache (I-Cache) misses, kicking the CPU out of its highly optimized pipelined execution state.

> **The Unity / C# Perspective:** Managed environments and tooling like Unity, can make virtual methods, interfaces, and delegates costs feel abstract. As a result, developers often get a habit of ignoring invocation overhead – a habit that will quickly cause performance bottlenecks when writing high-performance C++ code, when memory layout and dispatch model are much more explicit.

---

## The Fix: Static Polymorphism via Composition or Templates

If you are writing high-level systems like UI managers or Quest logic, a standard `virtual` function is perfectly fine. The convenience outweighs the micro-overhead.

However, if you are writing low-level, high-frequency gameplay systems (like a projectile manager processing 2,000 active bullets per frame), you should be able to leverage CPU caching and avoid the cost of virtual function calls.

### 1. The Unreal Component-Driven Approach (Composition)

Instead of creating a deep inheritance hierarchy (`AProjectile` $\rightarrow$ `ABullet` $\rightarrow$ `AFireBullet`), handle the behavior variation statically via plain, non-virtual data processing. Keep your data flat, and let a specialized system process the logic in a predictable loop.

### 2. The C++ Compile-Time Approach (CRTP / Curiously Recurring Template Pattern)

If you truly need polymorphism but want zero runtime cost, use the **Curiously Recurring Template Pattern (CRTP)**. This forces the C++ compiler to resolve function calls at compile time (static binding) rather than runtime (dynamic binding), allowing the compiler to completely inline your functions.

```cpp
// Base class template that uses compile-time static polymorphism
template <typename Derived>
class TProjectileBase 
{
public:
    void Update(float DeltaTime) 
    {
        // Static cast resolves the method at compile-time—no Vtable lookup!
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

By leveraging flat structures (`USTRUCT`) and processing them uniformly in a dedicated `UActorComponent` subsystem, you can run thousands of specialized updates while maintaining continuous, sequential memory layout (L1/L2 cache-friendly).

---

## The Architecture Trade-offs

* **When to use Runtime Virtuals:** High-level gameplay systems with low instance counts (e.g., GameMode rules, GameState loops, complex UI interactions).
* **When to use Static Polymorphism:** High-frequency, high-count elements (e.g., custom particle behaviors, mass AI agents, trajectory calculations, inventory item modifiers).
