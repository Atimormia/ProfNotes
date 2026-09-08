# Mentoring Strategy Document

**Pairing:** Alex Chen (Mentee) and Marcus Webb (Mentor)
**Season:** Pilot Season 1, Weeks 1–12
**Access:** Mentor and Mentee; shared with Priya Fernandes and HR for alignment

---

## Key Topics and Gap Areas, and Why They're Prioritized This Way

* **Modern C++ idiom under real memory and performance constraints** (RAII, ownership, move semantics) is prioritized first because it is the more tractable, practice-type gap: closable through structured repetition, and a necessary foundation for the harder gap below.
* **Judgment on when interface-based abstraction is worth its structural and compile-time cost in C++** is expected to be a longer-horizon concern than a single season, since judgment gaps of this kind are typically formed through repeated exposure to real, varied pressure over time, not through one curriculum. This season treats it as a gap to open and begin narrowing, not a gap expected to close outright.
* Secondary, lower-priority observation: Alex's growing reliance on AI-suggested patterns without fully evaluating them before merging; tracked as part of the responsibility-transfer arc (Guide 03) rather than as its own module, and revisited in any future season regardless of how this one concludes.

This prioritization reflects a long-term view of the Mentee's development, not only what fits inside the current season. Where the current season cannot fully address a topic, that is stated here as an expectation from the outset, and the specific scoping of what this season will and will not cover is left to the Curriculum Record, which is revised more frequently than this document.

## Anticipated Exercise Types and Mentoring Style

Given Project Vanguard's pre-release stage, in-project tasks carry more delivery risk than this pairing's schedule can absorb. In-project material will be used for **discussion and critique rather than direct build practice**: examining real systems for structural cost, drawing boundaries, discussing failure cases already in production. The core skill-building work will run as a **Dedicated Exercise** in **Planned Mode**, using a personal performance-sandbox project (ParticleSim) as the spine, since it offers a domain (C++ performance and memory layout) where the cost of C#-style abstraction becomes measurable rather than theoretical.

Mentoring style: Marcus will default to Do Together review rather than Watch, given Alex already has professional coding experience; a brief Watch-stage session is planned for Week 1 specifically to model diagnostic reasoning aloud before shifting into review-based work.

## Anticipated Challenges

* Pre-release schedule pressure may compress mentoring time in Month 3 specifically, since Vanguard's stabilization milestones tend to cluster near the end of a quarter (see Guide 07 if this recurs beyond a single instance).
* Marcus's own judgment gap (teaching and delegation) may surface as over-correction in review rather than diagnostic questioning; flagged for tracking per Guide 06, not treated as a blocking risk to the season.
* **Neither party has prior experience producing structured educational documentation of this kind.** This is the company's first season under the framework, and both the Mentor and the Mentee are learning the documentation discipline (closure definitions, separate-before-reconciled outcome records) at the same time they are working through the actual mentoring content. Expect early records to need more HR support and revision than later ones; this is anticipated friction, not a sign the framework doesn't fit this pairing.
* This is a single pilot season with no committed continuation. Any goal understood from the outset to need more than one season, most notably Marcus's own architecture-track development, cannot be expected to show a complete result within this document's scope, and that limitation should be attributed to the pilot's scoping decision, not to the framework's toolkits or to either participant's effort.