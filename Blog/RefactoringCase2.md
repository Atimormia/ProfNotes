# Finding Seams in a Monolith

The main scene was thirty megabytes of YAML text, and it held almost everything: level geometry, encounter logic, UI hookups, and most of the game rolled into one file, with almost no prefabs anywhere in sight. Two developers could not touch the repository in the same week without colliding. A small content change from one person and an unrelated fix from someone else routinely landed on the exact same lines of the exact same asset, because there was, structurally, nowhere else for either change to go.

From the outside, this looks like an obvious mistake: the kind of design a lead points at in a postmortem while declaring that nobody should ever build a scene this way.

That reaction skips a step. The scene did not end up in that state by accident, and the first productive move is never moral judgment. It is figuring out what question this structure was originally a correct answer to. **Nobody set out to build an unmergeable monolith. It was simply the optimal answer to an earlier reality.**

---

### The Blind Spot: The Fence Has a Reason

There is a principle worth borrowing here, even though it was not written for software. In 1929, G.K. Chesterton described an eager reformer who comes across a fence built across a road. Seeing no obvious purpose for it, the reformer demands it be torn down immediately. The wiser response is to refuse demolition until someone can explain, specifically, why it was erected in the first place. Only once you know what problem the fence was built to hold back does removing it become an informed decision instead of a reckless guess.

#### 1. The Ergonomics of the Solo Developer

Applied to a monolithic scene, the fence's purpose becomes obvious the moment you stop treating it as an error. A single developer, working alone, benefits enormously from having everything in one place.

Jumping between a dozen prefab files and separate sub-scenes to adjust one small interaction costs real time and cognitive context on every jump. Keeping everything inline, directly in the active scene, removes that friction entirely. There is no risk of two people colliding over the same asset, because there was only ever one person touching it.

Whether that shape came from deliberate systems design or simply from the path of least resistance during solo prototyping does not change the outcome: for an engineering team of exactly one, the monolithic scene was not a defect waiting to be noticed. It fit.

#### 2. Conway's Law in Reverse

The architectural breakdown occurred because of a dynamic Melvin Conway identified in 1967: software architectures naturally replicate the communication structures of the organizations that build them.

A team of one has exactly one communication path (itself). A design requiring zero cross-developer coordination is the structurally correct output for that team, whether or not anyone framed it that way at the start. What actually changed was not the scene. It was the studio sitting on top of it.

A larger team arrived behind the original prototype: more programmers, plus content creators who needed to check in material in parallel. Yet the scene's structure kept mirroring an organization of one long after the team had outgrown that footprint. Nobody asked whether the original architectural bet still held for a multi-track production team. The scene did not decay on its own; the studio outgrew what its earlier shape had produced, and nobody noticed the old answer no longer fit the new question.

#### 3. Proving Understanding Before Demolition

Knowing that a fence has a reason does not automatically tell you when you have actually uncovered it. Software engineering research into developer mental models has never converged on a single reliable method for comprehending unfamiliar code, and modifying a system on an incomplete mental model reliably makes things worse. Confidence is not evidence.

Rather than relying on abstract review, I relied on three practical operational proxies:

* **Paying the production tax firsthand:** I built several full levels inside the existing monolithic setup before proposing a single architectural change, experiencing its exact friction points directly.
* **The teaching test:** I took on the responsibility of teaching content creators how to place resources within the old pipeline. Being able to teach a system's quirks and real behavior to someone else is one of the oldest working tests for whether you actually understand it, rather than just having an opinion about it.
* **Manual migration parity:** When the new structure went in, I migrated every existing level into it personally, one at a time. Any discrepancy between what the old scene actually evaluated and what the new pipeline produced surfaced immediately on my own workstation, before it ever reached anyone else.

This process mirrors a fundamental principle of legacy system testing: you do not need access to the original author's private intentions, but you must be able to prove, deterministically, what the legacy code actually does under real conditions. That distinction has clear limits: this personal verification loop worked because the project had a small, manageable footprint of a few hand-crafted levels. At a scale of hundreds of levels, personal migration ceases to be viable, and automated behavioral suites must take its place.

---

### The Fix: Deciding How Much Fence to Tear Down

Once the workload mismatch was clear, the refactor could not be treated as a casual cleanup. It was an intentional re-architecture targeted at the workload the scene now had to support.

#### 1. The Cost of Missing Seams

The refactoring method was dictated by the coupling of the scene itself. In his work on legacy systems, Michael Feathers defines a **seam** as a place where you can alter program behavior without editing the source code directly in place.

The original scene had no seams. Level geometry, triggers, UI hookups, and encounter state were physically interleaved inside a single serialized asset. Without a seam, the Strangler Fig pattern (growing an isolated replacement alongside the original and migrating piece by piece) was impossible. When an asset is completely fused, attempting incremental, distributed edits across a team only magnifies merge conflicts. The honest options narrowed to a planned, single-owner cutover, executed deliberately during an agreed-upon maintenance window to protect the rest of the team from churn.

#### 2. Climbing the Modernization Ladder

A cutover does not mean burning down the entire codebase. Software engineering uses a well-established modernization ladder that ranks interventions from least invasive to most disruptive:

1. **Wrap:** Encase legacy components behind clean interfaces without altering their internals.
2. **Rehost (Migrate):** Move components to a new host or container with minimal changes.
3. **Refactor:** Restructure internal logic to reduce technical debt while preserving outward behavior.
4. **Rearchitect:** Redesign core subsystems to support new capabilities and access patterns.
5. **Rebuild or Replace:** Discard the legacy implementation entirely and engineer a ground-up solution.

The most successful architectural updates apply different rungs of this ladder to different subsystems simultaneously. That was the blueprint here:

* Gameplay logic was left alone entirely, wrapped behind interfaces where necessary.
* Peripheral systems around the edges received minor refactors and adjustments rather than full rewrites.
* The map organization, loading logic, and scene assembly pipeline was pushed all the way to a full rebuild, because it was the singular component lacking the seams required for anything cheaper.

#### 3. Declarative Tools Over Monolithic Blobs

The rebuild itself had three core components:

* **Decoupled scenes and explicit lazy loading:** Level assets were broken into distinct, modular chunks, loaded on demand rather than resolving the entire world synchronously on boot.
* **Explicit state machines:** Level transitions and initialization sequences were moved out of implicit script execution order and placed under structured state-machine control.
* **A declarative authoring tool:** Instead of hand-placing prefabs, triggers, and audio directly into a shared scene file, content creators configured levels through a dedicated editor tool. Levels were defined as structured data (specifying resources, enemy encounters, and VFX sequencing) that the engine parsed and instantiated at runtime.

Moving level authorship out of a fused scene file and into a referenced, data-driven pipeline eliminated merge collisions entirely. Multiple designers could author content across separate data files without touching a single shared scene.

#### 4. The Maintenance Tax of Custom Tooling

Trading an inline workflow for a custom authoring tool is not an unqualified victory, and presenting it as one would be dishonest. Internal tools are long-lived software assets that carry their own ongoing maintenance tax.

A custom level editor requires functional undo and redo stacks, robust validation to prevent invalid data states, intuitive UI design, and clear documentation. When you extract a problem out of a shared scene file and bury it inside a custom tool, you have not destroyed the underlying coordination tax: you have relocated it. The engineer who builds the tool becomes its de facto product owner, responsible for supporting content creators and patching editor edge cases across engine upgrades.

That trade was well worth making (the constant merge failures and blocked production pipelines of the monolithic scene were actively paralyzing the team), but trading one recurring cost for a smaller, different recurring cost is a more accurate description of engineering than calling the tool a magic fix.

#### 5. The Dual Failure Modes of Modernization

The modernization ladder highlights two distinct traps that lead teams astray:

* **Over-engineering through total replacement:** Rebuilding a legacy system that could have been cheaply wrapped burns immense time and introduces unnecessary stability risks.
* **Under-engineering through band-aids:** Applying superficial patches to a system that fundamentally lacks seams merely delays an inevitable collapse to a later, far more expensive date.

Neither mistake announces itself in advance. The only real defense is evaluating the choice of intervention with the exact same rigor applied to the initial decision to act.

---

### The Insight: Reconstructing the Original Question

Three foundational takeaways generalize past scene organization into any engineering project:

#### 1. Identify the Constraint Before Judging the Implementation

An architecture that looks absurd in hindsight was almost certainly an optimal solution to an earlier, unrecorded operational constraint. Reconstruct that initial constraint before proposing a change. If you cannot explain why the original team built the fence, you do not have the context required to tear it down safely.

#### 2. Track Workload Drift, Not Just System Health

Systems rarely decay in a vacuum; workloads change underneath them. As teams expand and feature complexity compounds, an architecture that delivered peak velocity for a solo developer will steadily turn into a bottleneck for a multi-disciplinary team. Revisit structural assumptions whenever team composition or concurrency patterns fundamentally shift.

#### 3. Require Operational Proof Over Subjective Confidence

Gaining a true mental model of unfamiliar systems cannot be validated by intuition alone. Establish concrete, domain-specific verification proxies: teaching the system's operational realities to a teammate, establishing behavioral parity through deterministic migrations, or isolating regressions with end-to-end integration tests. If you cannot demonstrate what the system actually does, you are not ready to rewrite it.

---

### The Production Bottom Line

> An architecture that looks wrong from the outside is very often a correct answer to a question nobody told you was being asked.
> The engineering discipline is not refusing to touch legacy systems, nor is it tearing them down on sight. It is reconstructing the original constraints before editing the design, acknowledging that personal confidence is not the same thing as verified understanding, and then climbing only as high on the modernization ladder as the real bottleneck requires.

---

The refactor held. It survived everything the team threw at it over the following months, except one thing.