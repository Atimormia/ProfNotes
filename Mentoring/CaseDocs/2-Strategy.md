# Mentoring Strategy Document

**Pairing:** Alex Chen (Mentee) and Marcus Webb (Mentor)
**Season:** Pilot Season 1, Weeks 1–12
**Access:** Mentor and Mentee; shared with Priya Fernandes and HR for alignment

---

## Key Topics and Gap Areas

* Modern C++ idiom under real memory and performance constraints (RAII, ownership, move semantics), the primary practice gap.
* Judgment on when interface-based abstraction is worth its structural and compile-time cost in C++, an emerging judgment gap distinct from the above.
* Secondary, lower-priority observation: Alex's growing reliance on AI-suggested patterns without fully evaluating them before merging; tracked as part of the responsibility-transfer arc (Guide 03) rather than as its own module.

## Anticipated Exercise Types and Mentoring Style

Given Project Vanguard's pre-release stage, in-project tasks carry more delivery risk than this pairing's schedule can absorb. In-project material will be used for **discussion and critique rather than direct build practice**: examining real systems for structural cost, drawing boundaries, discussing failure cases already in production. The core skill-building work will run as a **Dedicated Exercise** in **Planned Mode**, using a personal performance-sandbox project (ParticleSim) as the spine, since it offers a domain (C++ performance and memory layout) where the cost of C#-style abstraction becomes measurable rather than theoretical.

Mentoring style: Marcus will default to Do Together review rather than Watch, given Alex already has professional coding experience; a brief Watch-stage session is planned for Week 1 specifically to model diagnostic reasoning aloud before shifting into review-based work.

## Preliminary Timeline

* **Weeks 1–4 (Month 1):** ParticleSim Module 1 — naive AoS baseline and benchmarking harness. Establishes a felt, measurable baseline for what "correct but costly" looks like before any rewrite.
* **Weeks 5–8 (Month 2):** ParticleSim Module 2 — Structure-of-Arrays rewrite and a Skeleton-Meat exercise on spatial partitioning, where Marcus authors the partitioning interface boundary and Alex implements the concrete grid inside it.
* **Weeks 9–12 (Month 3):** ParticleSim Module 3 (partial; allocator work introduced but not completed within the pilot) plus the closing transfer step: a Critique Task on a real in-project system (Vanguard's existing ability-activation code), required by Planned Mode's closure rule (Guide 02, Step 1).

## Anticipated Challenges

* Pre-release schedule pressure may compress mentoring time in Month 3 specifically, since Vanguard's stabilization milestones tend to cluster near the end of a quarter (see Guide 07 if this recurs beyond a single instance).
* Marcus's own judgment gap (teaching and delegation) may surface as over-correction in review rather than diagnostic questioning; flagged for tracking per Guide 06, not treated as a blocking risk to the season.
* Three months may not be sufficient to fully close the emerging judgment gap (abstraction cost under pressure) even if the primary practice gap closes; this is treated as an acceptable, honestly-reported outcome rather than a failure condition for the pilot.