# Individual Goals and Baseline Document

**Pairing:** Alex Chen (Mentee) and Marcus Webb (Mentor)
**Season:** Pilot Season 1 (3-month session), Weeks 1–12
**Access:** Mentor, Mentee, Mentee's Manager (Priya Fernandes), Mentor's Manager (David Okafor)

---

## Part A: Mentee Goals and Baseline

### Goals (Manager-Participant Meeting: Alex Chen and Priya Fernandes)

**Project-specific goal (Priya's framing):** Reduce review cycle time and rework on Alex's pull requests. Over the past two quarters, Alex's PRs have required an above-average number of review rounds, most commonly disputing structural choices rather than fixing defects.

**Personal goal (Alex's framing):** "Get fluent enough in modern C++ that I stop feeling like I'm translating from C# in my head every time I write a class."

### Baseline (Diagnostic Toolkit, Guide 01)

**Evidence Sources Used:**

* **Self-report:** Alex described a specific incident from six weeks prior: while building a weapon-pickup system ahead of a milestone, Alex built a four-level interface hierarchy anticipating future weapon types that didn't yet exist. The resulting header churn caused a circular-include problem that cost two days to resolve, ending with Alex asking a teammate for help under deadline pressure. Alex described the experience as feeling like "C++ fighting me for no reason," rather than as a structural choice that could have been made differently.
* **Peer input:** Two teammates independently noted that review cycles on Alex's PRs run long specifically because Alex re-argues structural decisions in review comments rather than addressing the underlying defect being flagged. A tools programmer separately noted that Alex's class shapes often resemble a C# dependency-injection or service-locator pattern translated literally into UE5 `UObject` hierarchies.
* **Work archaeology:** Marcus reviewed Alex's commits from the prior three months. Recurring pattern: `virtual` dispatch used on several per-frame, hot-path classes; three interfaces with exactly one production implementation each; manual `new`/`delete` used alongside engine-managed `UPROPERTY` pointers in the same class; no `const` correctness on read-only accessors. Two PRs included comments referencing an AI assistant's suggestion for "how to write a strategy pattern in C++," and the merged code matched the AI's suggested shape closely, including a virtual base class where a simpler, non-polymorphic solution would have served the actual (single-implementation) use case.
* **Designed task:** Not used at Baseline. The above three sources converged clearly enough that a constructed task wasn't needed to confirm the pattern; a task is reserved for the first module itself.

**Where sources disagreed:** Alex's self-report framed the difficulty as C++'s fault ("the language fighting me"). Peer input and work archaeology both pointed at a specific, repeatable structural habit instead. This discrepancy was raised directly with Alex during the Baseline conversation rather than resolved by picking one source over the other, and Alex's own recognition of the pattern once it was named (rather than defensiveness) was itself a useful data point about how the mentoring relationship was likely to go.

**Gap Classification:** Primarily a **practice gap** in modern C++ idiom (RAII, ownership semantics, move semantics, the specific mechanics that differ from C#'s garbage-collected model) — Alex can define these concepts when asked directly but has not rehearsed them under real delivery pressure. A secondary, emerging **judgment gap** is also present: knowing when an interface-first, SOLID-style abstraction is worth its structural and compile-time cost in C++, a cost that doesn't exist in the same form in C#. Urgency: moderate. Not blocking delivery outright, but actively slowing Alex's velocity and visibly affecting confidence.

**Agreed Definition of Closing This Gap:** Alex independently identifies, before writing a new class, whether a given piece of C++ code needs runtime polymorphism or can use a simpler, non-virtual structure, and can articulate the ownership and lifetime model for any pointer or reference used, without prompting, in both a reviewed setting and unprompted in real work.

---

## Part B: Mentor Goals and Baseline

### Goals (Manager-Participant Meeting: Marcus Webb and David Okafor)

**Organizational goal (David's framing):** Grow Marcus toward an architecture-track role: taking responsibility for decisions that scale through other engineers' work, not only through his own output. This requires developing comfort with teaching, delegation, and influence without direct authority.

**Personal goal (Marcus's framing):** "Help fix the C++ fluency gap on the floor — I keep seeing the same mistakes and it's faster if I just teach someone properly instead of fixing it in review every time." (Noted for the record: this framing is output- and reputation-oriented rather than teaching-oriented; worth monitoring per Guide 06 rather than treated as a problem to correct before the season starts.)

### Baseline

**Evidence Sources Used:**

* **Self-report:** Marcus has mentored informally in the past (unstructured, under the company's prior informal program) but has no experience running a structured curriculum, has not previously used a staged responsibility-transfer model, and has a stated preference for solving problems himself rather than facilitating someone else solving them.
* **Peer input:** David notes Marcus is highly respected technically but has a reputation for terse, sometimes discouraging review comments, and has previously declined opportunities to lead cross-team initiatives.

**Gap Classification:** A **judgment gap** specific to teaching and delegation: Marcus has the technical depth to mentor well but no rehearsed practice recognizing when to let a Mentee struggle versus when to step in, and no track record of taking responsibility for an outcome he isn't directly executing himself.

**Agreed Definition of Closing This Gap (for this season):** Not full architecture-role readiness, which is understood at the outset to be a multi-season goal. For this pilot specifically: Marcus asks diagnostic questions before offering solutions in at least the majority of Do Together sessions, and can articulate, unprompted, at least one instance where he deliberately let Alex struggle rather than intervening.

---

*Revision Note (Week 7):* Alex's personal goal statement was not revised, but the Baseline's secondary judgment-gap classification was flagged as likely to sharpen over the season; see Season Summary for the Week 12 reclassification.