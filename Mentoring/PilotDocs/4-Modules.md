# Module Plans

**Pairing:** Alex Chen (Mentee) and Marcus Webb (Mentor)
**Access:** Mentor and Mentee

---

## Module Plan 1: Naive Baseline and Benchmarking Harness (Weeks 1–4)

**Objectives and Key Concepts:** Build a naive Array-of-Structures particle system in modern C++, alongside a benchmarking harness to measure it, before any optimization. Key concepts: `TUniquePtr` vs. raw pointer ownership, `const` correctness, RAII lifecycle, why a benchmarking tool needs to exist before the thing it measures is optimized.

**Theoretical Material:** Marcus prepares two short worked examples from his own past code showing an ownership bug he personally introduced and how it was caught; Alex reviews existing team documentation on smart pointer semantics and prepares at least two questions before the Week 1 session.

**Exercise Requirements and Definition of Done:** A working particle struct and update loop compiles, runs, and produces correct output for a small particle count; a benchmarking harness reports update time per frame. Definition of Done is met when both exist and are reviewed once by Marcus.

**Agreed Closure Definition:** Not yet the full season's closure definition (see Individual Goals and Baseline Document); for this module specifically, Alex can explain, unprompted, why each pointer or reference in the code is owned the way it is.

**Meeting Cadence:** Two sessions per week for this module specifically (higher than the season default of one) given Week 1's Watch-stage session requires more direct modeling time.

---

## Module Plan 2: Structure-of-Arrays Rewrite and Spatial Partitioning (Weeks 5–8)

**Objectives and Key Concepts:** Rewrite Module 1's particle storage from Array-of-Structures to Structure-of-Arrays after a profiling result exposes the cost difference; implement a concrete spatial grid inside an interface boundary Marcus authors in advance. Key concepts: when polymorphism is worth its dispatch cost, cache locality, working inside a boundary someone else designed.

**Theoretical Material:** Marcus prepares the authored interface boundary and a short written rationale for why it's shaped the way it is; Alex reviews the profiling output from Module 1 in advance and prepares an initial hypothesis for what the SoA rewrite should look like.

**Exercise Requirements and Definition of Done:** The SoA rewrite passes the same benchmark harness from Module 1 with a measurable improvement; the grid implementation satisfies the authored interface and passes a basic correctness check (particles in the same cell are returned together). Definition of Done is met when both are reviewed once by Marcus.

**Agreed Closure Definition:** Alex can articulate why the interface boundary exists where it does, without needing to have designed it themselves, and does not attempt to add a second interface layer inside the boundary "for future flexibility" without being able to name a concrete, current reason for it.

**Meeting Cadence:** Season default (one session per week), plus one additional async written check-in given the Skeleton-Meat format's need for Alex to work more independently inside the boundary.

---

## Module Plan 3: Allocator Introduction and Transfer Step (Weeks 9–12)

**Objectives and Key Concepts:** Introduce custom allocator concepts (pool allocation vs. `new`/`delete` overhead) at an introductory level only, given reduced module scope (see Curriculum Record's Week 9 revision note); closing transfer step applies the season's judgment gap work to a real, unfamiliar system.

**Theoretical Material:** Short discussion only, given reduced scope; no new prepared material beyond a brief walkthrough of why allocation overhead matters.

**Exercise Requirements and Definition of Done (Allocator segment):** Reduced to a discussion and a small worked example rather than a full implementation; Definition of Done is a written summary from Alex of when a custom allocator would be worth the complexity for Vanguard's particle-heavy VFX systems specifically.

**Exercise Requirements and Definition of Done (Transfer Step, Critique Task):** Alex reviews Vanguard's existing ability-activation system and produces a short written critique identifying at least two places where an abstraction's cost does or doesn't justify itself, without proposing or shipping a code change.

**Agreed Closure Definition:** This is the module against which the season's full closure definition is tested (per Guide 01's hard rule and Guide 02's Planned Mode transfer requirement): Alex applies the same judgment from Modules 1 and 2 to code neither of them wrote, under real (not simulated) time pressure, since Vanguard's milestone moved up during this module.

**Meeting Cadence:** Reduced to biweekly given the milestone-driven schedule compression; explicitly recorded as a deliberate shrink per Guide 07, not an informal drop-off.