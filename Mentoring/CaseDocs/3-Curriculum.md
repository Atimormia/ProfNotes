# Curriculum Record

**Pairing:** Alex Chen (Mentee) and Marcus Webb (Mentor)
**Season:** Pilot Season 1, Weeks 1–12
**Access:** Mentor and Mentee

**Scope of This Document:** Where the Mentoring Strategy Document sets the long-term priority order across gaps (practice gap first, judgment gap as a multi-season concern), this record scopes exactly what Season 1 covers within that order, and states explicitly what is deferred. This document is revised every module; the Strategy Document is revised only if the long-term priority itself changes.

---

## Module 1: Naive Baseline and Benchmarking Harness

* **Weeks:** 1–4
* **Module goal and gap addressed:** Practice gap (C++ ownership and memory semantics). Establish a felt baseline before any rewrite, and model diagnostic reasoning aloud (Watch stage, Guide 03) before shifting to reviewed practice.
* **Material source:** Theory curated (existing team documentation on `TUniquePtr`/`TSharedPtr` semantics, supplemented by Marcus walking through his own past code). Exercise authored (ParticleSim's Module 1 structure predates the internal library; this is the first cycle authoring it).
* **Design mode:** Planned Mode. Practice gap is the primary driver; the constraint sequence is chosen and gated by Marcus in advance.
* **Exercise format and task source:** Paired Build for the first session (Watch stage), transitioning to independent build reviewed by Marcus (Do Together). Dedicated Exercise; Vanguard's pre-release stage leaves no suitable In-Project or Nice-to-Have task at this grain.

## Module 2: Structure-of-Arrays Rewrite and Spatial Partitioning

* **Weeks:** 5–8
* **Module goal and gap addressed:** Practice gap continues (ownership under a more complex rewrite); judgment gap introduced directly (when is an interface boundary worth its cost).
* **Material source:** Exercise authored, extending Module 1 directly rather than starting fresh.
* **Design mode:** Planned Mode, continuing the same sequence.
* **Exercise format and task source:** Skeleton-Meat. Marcus authors the spatial-partitioning interface boundary in advance; Alex implements the concrete grid inside it. Chosen deliberately to isolate the interface-design decision, removing it from Alex's scope this round, so Marcus can review Alex's implementation reasoning without Alex also re-litigating whether an interface belongs there at all, which was the exact habit flagged at Baseline. Dedicated Exercise.

## Module 3: Allocator Work (Partial) and Transfer Step

* **Weeks:** 9–12
* **Module goal and gap addressed:** Practice gap consolidation; judgment gap tested under real time pressure (Vanguard's Month 3 milestone was moved up mid-module, see Module Outcome Record).
* **Material source:** Exercise authored (allocator segment); not completed within the pilot, carried forward as unfinished.
* **Design mode:** Planned Mode for the allocator segment; the closing transfer step is a Critique Task rather than a further Planned constraint, per Guide 02, Step 1's requirement that Planned Mode close with judgment applied in a different context.
* **Exercise format and task source:** Critique Task on Vanguard's existing ability-activation system (In-Project, but structured as review rather than a build task specifically because of pre-release delivery risk, per Guide 07). Selected because it required Alex to apply the same abstraction-cost judgment to real, unfamiliar code without shipping any change, keeping production risk near zero while still meeting Planned Mode's transfer requirement.

## Deferred to Future Iterations

Per the Strategy Document's long-term prioritization, the following are explicitly out of scope for Season 1 and are not implied to be resolved by this season's results:

* **Full allocator implementation** (ParticleSim's remaining scope for that module), reduced to an introductory discussion only after the Week 9 schedule compression.
* **Parallelization and further ParticleSim stages**, not reached at all within this season.
* **Judgment-under-pressure as an ongoing concern**, per the Strategy Document's framing that this gap is expected to need more than one season. Season 1 opens and narrows this gap; it does not close it, and no future document should read a lack of full closure here as a shortfall in this season specifically.
* **Marcus's architecture-track development goal**, understood from the outset (see Individual Goals and Baseline Document, Part B) as a multi-season goal that this single pilot season cannot be expected to complete.

## Library Note

None of this season's modules were drawn from an existing library entry; this is the first cycle building this specific curriculum. Module 1 and Module 2 are being submitted for library promotion review per Guide 02's promotion criteria, pending use with a second Mentee in a future season.

*Revision Note (Week 9):* Module 3's scope was reduced from a full allocator implementation to an introduction-only segment after Vanguard's Month 3 milestone moved up two weeks; this is a scope reduction per Guide 07's "shrink the module, don't cancel it" guidance, not a cancellation.