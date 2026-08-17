# Where Abstraction Meets The Hot Path

A player opens their bank tab and the game stutters for half a second. Not a crash, not a hitch anyone would file a bug over on its own, just a small, ugly pause every single time. QA flags it. I open the profiler expecting to find the usual suspect: one bloated function doing far too much work, the kind of thing [TickPitfalls.md](TickPitfalls.md)'s aura actor turned out to be.

There wasn't one. The frame's cost was spread across a dozen small functions, each taking a percent or two, each reasonable in isolation. The profiler was answering the question it is built to answer: _what's expensive?_ And the honest answer this time was: **a little bit of everything, all at once, three hundred times.**

---

## The Blind Spot: Frequency × Depth × Boundary

There are two easy answers to how much abstraction a performance-sensitive codebase should tolerate, and I've observed both of them at different points in my career:

* **The Reactive Approach:** Write clean code everywhere, and trust the architecture to stay flexible enough to fix whatever the profiler eventually flags. That's a reasonable instinct, and good architecture usually can absorb a fix. But a system can inherit a bottleneck nobody predicted simply because nobody expected it to become a hot path. By the time it is one, the cost is already load-bearing across a dozen features built on top of it. Worse, a profiler is built to find the loudest single function: a cost spread thin across many small, individually innocent functions doesn't reliably produce one.
* **The No-Abstraction Approach:** Abandon interfaces entirely and strip out boundaries everywhere in the name of performance. Eliminating boundaries triggers the exact failure [OwnershipTaxUE.md](OwnershipTaxUE.md) already named (just on purpose instead of by accident): nothing owns a clean seam anymore, so nothing is easy to isolate, whether the bug is a crash or a frame spike.

Neither extreme survives contact with what actually happened in the bank tab. The real mechanic sits underneath both:

$$\text{Cost} = \text{Frequency} \times \text{Depth} \times \text{Boundary Type}$$
where $BoundaryType$ is how visible each hop is to the compiler and runtime optimizer.

**Depth alone was never the enemy.** A five-hop chain of ordinary function calls sitting inside one translation unit often costs nothing: the compiler can see straight through every hop and inline the whole thing away.

The cost shows up specifically when a hop crosses a boundary the compiler can't see across:

* Virtual calls
* Function pointers
* Type-erased callbacks
* Plugin or module seams

In Unreal specifically, this is exactly what happens under a Gameplay Effect. Attribute resolution doesn't run as plain member access: it walks the reflection system, resolving `FProperty` pointers, matching gameplay tags, and reading scalable-float curve tables. None of that is a mistake. It's precisely the machinery that lets a designer add a new rarity tier or set bonus without anyone recompiling. It just isn't free, and it was never supposed to be evaluated three hundred times in a single frame.

That's what the bank tab was actually doing. An item's effective stats resolved through five layers built over five different milestones:

1. **Base stat lookup**
2. **Rarity multiplier**
3. **Affix chain** (from socketed gems)
4. **Set-bonus check** (against equipped gear)
5. **Temporary buff overlay** (from the last consumable used)

Every layer was added for a real feature, reviewed on its own merits, and crossed the same reflection-backed boundary GAS uses for flexibility. At equip time (once per item, once every few seconds at most), that cost is completely invisible. Rendered fresh for three hundred items at once, it's the stutter QA flagged.

---

## The Fix: Catch Frequency Shifts, Not Chain Depth

None of this calls for flattening the chain. The rarity, affix, set-bonus, and buff layers are all doing real work. Collapsing them into one function wouldn't make the game more maintainable: it would just make the next feature harder to add safely. The actual fix is catching the moment the chain's usage pattern changes, not auditing its depth on a schedule.

### 1. Trigger on frequency changes

The question worth asking in review isn't "how deep is this chain?", but **"did this call just move from something invoked rarely to something invoked per-item, per-frame, or across a whole collection at once?"** A stash tab rendering three hundred items, a raid-wide loot roll resolving stats for forty players, or a comparison tooltip wired to refresh continuously are all the same event: a call site's frequency changed underneath a chain designed for low frequency.

### 2. Cache at the boundary

This is the same move from [Ownership Tax in Unreal Engine](OwnershipTaxUE.md), just applied to computed stats instead of a fetched reference: don't re-derive the full chain on every read, resolve it once when the underlying data actually changes (an item equips, an affix rerolls, a buff expires) and cache the result. The stash tab reads three hundred cached snapshots instead of walking three hundred reflection-backed chains. The flexible authoring path stays intact, while only the frequently queried consumption path changes.

### 3. Account for caching trade-offs explicitly

Caching isn't free, and it's worth being honest about that before reaching for it as a default. The read cost goes away, but a synchronization problem takes its place: a cached snapshot is only correct as long as something reliably invalidates it the moment any layer changes. The set-bonus layer makes that harder than it looks, since a single item's snapshot depends on whatever else happens to be equipped. Unequip one piece of a set, and every other piece's cached snapshot needs invalidating too, not just the piece that moved. Get that wrong and the bug doesn't disappear: it just goes quiet, sitting as a stale stat in a tooltip until something forces a recompute. There's a second cost alongside it: precomputing a snapshot for every item spends memory to buy back CPU time. On memory-constrained platforms (such as mobile builds or consoles with fixed heaps), a few hundred cached snapshots carries a cost that shows up just as plainly as the stutter did.

### 4. Move resolution earlier when chains mature

If a specific chain turns out to be both hot and stable (behavior that stopped changing once the system matured), resolve it at compile time instead of runtime, using the trade-offs worked out in [Compile-Time Performance vs. Runtime Flexibility](CompileTimeVsRuntime.md). In practice, that might mean baking lookup tables during asset cooking, generating resolved modifier data, or replacing designer-authored indirection with a fixed representation once the design has stopped moving. That's rarely the first move, but it remains a valid option for the rare hot chain that has genuinely stopped needing to change.

---

## The Insight: Credit the Layer, Track the Chain

This is the same failure shape [Data-Driven Design Is an Architecture Boundary](DataDrivenDesign.md) already named, just measured in call-path depth instead of configuration layers: **credit the individual case, track the pattern across cases.**

Nobody who added the rarity multiplier, the affix chain, or the set-bonus check made a bad decision. Each was the correct call, reviewed and approved on its own: a local, well-bounded addition a healthy codebase should welcome. What nobody tracked was the combination: five independently reasonable layers stacking into one call path that nobody had designed together, because nobody owned the chain end to end the way each layer's author owned their own piece.

That's the placement rule [TickPitfalls.md](TickPitfalls.md), [GarbageCollection.md](GarbageCollection.md), [VirtualFunctions.md](VirtualFunctions.md), and [DataLayoutIsArchitecture.md](DataLayoutIsArchitecture.md) apply without stating directly: deciding, per system, whether a piece of code sits in the narrow, frequently executed fraction of the codebase or the much larger fraction where clean abstraction should simply win by default. Inventory items prove that decision isn't static. A system can start firmly in the flexible 80%, stay there through several honest feature additions, and cross into the hot 20% not because any single decision was wrong, but because frequency changed underneath a chain nobody was watching.

The trigger isn't foresight: nobody predicts at design time that a bank tab two years later will call an exact chain three hundred times in a frame. **The trigger is catching the moment usage changes**, at the point closest to when it actually shifts: during code review, not scheduled audits or waiting for the profiler to notice on its own.

---

## Production Bottom Line
> **Depth Was Never the Cost:** A chain of clean, well-reviewed abstraction layers can sit untouched and free for years, and every layer in it can be the right call. What turns it expensive isn't how deep it is, but whether a hop crosses a boundary the compiler can't see through, multiplied by how often that hop now runs.
>
> Flattening the chain on principle breaks the flexibility it was built for. Waiting for the profiler can miss a cost spread too thin to light up any single function. The useful signal is the moment a call's frequency changes: treat that moment, not a fixed depth limit or profiler alert, as the prompt to optimize.