# Mentor Guide 02: Training Approach Toolkit

## Purpose

This toolkit covers how a Mentor decides what a module should actually look like once a gap has been diagnosed and classified (see Guide 01). It addresses four separate decisions, taken in sequence: whether original material needs to be created at all, which design mode to use, what exercise format to build it around, and where the underlying task comes from.

## Step 0: Author or Curate

This decision applies twice, once for the theory material a module draws on and once for the exercise itself, since a Mentor may curate one and author the other for the same module.

Before creating anything, check whether usable material already exists: in the program's internal library from a past cycle, or as mature external material (documentation, a book, an established course, for theory; a previously authored exercise, for practice). Early in a program's life, little or no internal library exists, and most material will need to be authored from scratch. As cycles accumulate and modules are evaluated and promoted into the shared library (see Guide 04), a Mentor's role shifts progressively from author to curator: selecting existing material, adapting it to the specific Mentee's gap, and verifying the outcome, rather than creating new content each time.

Two factors inform this decision at any point in the program's maturity:

* **Where the gap sits on the proprietary-to-foundational spectrum.** A gap tied to fully proprietary, company-specific technology has no external source and must be authored internally, at least the first time. A gap in something foundational but uncommon in daily practice is more likely to have solid external material available, even early in the program's life.
* **Program maturity.** As the internal library grows, checking it first becomes the default step regardless of where a gap sits on the spectrum above, since material authored once in a past cycle is available for reuse in every later cycle facing the same gap.

If existing material covers the gap adequately, use it directly, noting the source per Guide 04. If it partially covers the gap, a smaller custom addition on top of existing material is often sufficient. If nothing suitable exists, proceed to author it, informed by Steps 1 through 3 below.

## Step 1: Choose the Design Mode

Where original exercise design is needed, two modes are available. Neither is the default; the choice depends on what the module needs to build in the Mentee, and follows directly from the gap type identified in Guide 01.

**Planned Mode:** A small number of high-signal constraints, chosen and sequenced by the Mentor from easiest to hardest, each gated behind a real, measurable result before the next is introduced. This mode suits building a specific, identifiable skill or instinct cleanly, and is generally the right default for a **practice gap**: the Mentee already has the knowledge and needs structured, escalating repetition to make it reliable.

Planned Mode is not complete once the final gated constraint is passed. A closing step is required: the Mentee applies the same judgment in a context meaningfully different from the one the module was built around, a different system, a different constraint combination, or a discussed hypothetical if a second real context isn't available. Without this step, a Mentee can pass every gate inside one narrow domain and still fail to recognize the same pattern the first time it appears somewhere unfamiliar.

**Reactive Mode:** A problem that widens unpredictably, with the number and shape of upcoming changes deliberately undisclosed, requiring the Mentee to reach a genuine, working resolution rather than stopping partway through. This mode suits building tolerance for and recognition of ambiguity, and is generally the better fit for a **judgment gap**: a Mentee who has the mechanics but struggles to decide when and how much to apply them typically needs exposure to genuine, unresolved ambiguity, not more structured repetition.

Reactive Mode has a firm precondition: it depends on the Mentee already having baseline fluency to draw on while working through the difficulty. Applied without that fluency, it produces discouragement rather than the intended effect.

Where a diagnosed gap is closer to a pure **knowledge gap**, neither mode is usually the right first move; direct instruction or curated material (Step 0) is typically more efficient than authoring an exercise of either kind.

**Combining Both Modes:** Where a Mentee's development calls for both a specific instinct and tolerance for ambiguity, run Reactive Mode before a related Planned Mode module, not the reverse. The Mentee's own experience of the first module's unpredictability sharpens their appreciation of the second module's deliberate structure; run in the opposite order, the Mentee has nothing yet to compare the structure against.

## Step 2: Choose the Exercise Format

Four formats are available. Each can be combined with either design mode above, and each suits a different point in Guide 03's responsibility transfer stages.

* **Paired Build:** The Mentor and Mentee design and implement together, in real time. Best suited to Guide 03's Watch and Do Together stages, since it is inherently collaborative rather than independent.
* **Revision Task:** The Mentee works on an existing artifact rather than a blank page, improving it against defined criteria. Valuable specifically because it forces contact with accumulated context the Mentee did not create themselves, which a from-scratch exercise cannot replicate.
* **Critique Task:** The Mentee evaluates someone else's existing work rather than producing new work. Isolates evaluative judgment from generative skill, and carries very low production risk, since nothing ships from it directly. Well suited to a Mentee approaching the Do Alone stage in Guide 03, where reasoning quality matters more than output.
* **Skeleton-Meat:** The Mentor authors the structural boundary (an interface, a contract, a composition) and the Mentee fills in what sits inside it. This isolates one specific decision by removing every other decision from scope, and is well suited to a Do Together stage where the Mentor wants to review reasoning on a narrow, specific choice without the Mentee also having to make every surrounding structural decision.

These generalize beyond programming directly: a Paired Build applies to joint design sketching or joint test-plan authoring; a Revision Task to reworking an existing document or asset; a Critique Task to design or document review; Skeleton-Meat to a wireframe a designer fills in, an outline a writer drafts from, or a coverage plan a tester implements against.

## Step 3: Choose the Task Source

Three sources are available for the underlying task, regardless of format or mode chosen above.

* **In-Project Task:** A piece of real, currently shipping work, selected because it happens to isolate the diagnosed gap. Use this when the current project has a piece of work available now that is low-priority, low-risk, and cleanly isolates the gap, per the original program's own pairing criteria.
* **Nice-to-Have Project:** Real work that would benefit the project or company but does not sit on the critical delivery path. Use this when no suitable in-project task exists at the current moment, or the diagnosed gap needs a format or timeline the active project cannot accommodate, but a lower-stakes, still-genuinely-useful alternative can be identified or proposed. This source sits deliberately between the other two: lower delivery risk than in-project work, higher realism and stake than a dedicated exercise.
* **Dedicated Exercise:** A task built or sourced specifically for mentoring purposes, with no other output. Use this when neither of the above sources is available, or when the exercise itself requires fabricated precision that real work cannot offer.

**Reactive Mode implies a Dedicated Exercise by default.** Reactive Mode depends on the Mentor controlling the timing and content of unannounced requirement changes, which is not ethically compatible with a task that also has to ship. In-Project and Nice-to-Have sources are generally reserved for Planned Mode.

**A Caution on Nice-to-Have Projects:** A manufactured project a Mentee can identify as manufactured loses much of its motivational value over a genuine one. Where this source is used, favor work with a real, stated beneficiary and a real, if lower, cost of not doing it, rather than inventing a project with no purpose beyond the mentoring exercise itself.

## The Hard Rule, Applied Here

Regardless of the choices made across all four steps, define what success looks like before the module begins, in terms specific enough that the Checkpoint diagnosis (Guide 01) has something concrete to compare against. For Planned Mode, this includes the closing transfer step, not only the final gated constraint. For Reactive Mode, this is the working resolution the Mentee is expected to reach, not a fixed intermediate checkpoint.

## Software Engineering Example

A Mentee's diagnosed gap (Guide 01) is a judgment gap: knowing when to generalize an interface versus when a simpler, narrower solution suffices. The Mentor selects Reactive Mode (judgment gap), which implies a Dedicated Exercise by default (Step 3's rule). No suitable material exists in the internal library, so the exercise is authored from scratch (Step 0). The Mentor selects a bounded problem and, working alone rather than in a Paired Build, has the Mentee build independently while the Mentor introduces a sequence of unannounced requirement changes (Step 2: closer to a standalone task than any of the four collaborative formats, since Reactive Mode's unpredictability is best experienced without a co-author present). The module concludes once the Mentee reaches an interface that survives the full sequence, with no further transfer step required, since Reactive Mode's own unpredictability already forces contact with an unfamiliar context by design.

## Result

A recorded decision, per Guide 04, on material source (authored or curated, for both theory and exercise separately), design mode, exercise format, and task source, together with the reasoning connecting these choices back to the gap type identified in Guide 01. This record feeds the module's eventual promotion into the shared library and gives a later Season Synthesis context for interpreting how the Mentee responded to the specific combination of choices made.