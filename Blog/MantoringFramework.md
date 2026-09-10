# Where Planned and Reactive Mentoring Meet

*(working title, not final)*

I combined my 4 years of teaching CS and whole IC experience together with participating in different mentoring processes on both sides to build a mentoring framework for my company. I kept running into the same wall from two directions at once. I had been on the receiving end of both extremes myself, a rigid, curriculum-first onboarding that taught me plenty of facts and none of the judgment to apply them, and later, informal, ask-when-stuck mentoring that taught real judgment in the moment and left nothing behind for anyone else to learn from. Neither one, on its own, was ever going to be the answer, and I wanted to understand why before I designed a third option.

The timing turned out to matter more than I expected. AI has quietly changed what a junior engineer's job actually is. When a tool can draft the architecture, propose the fix, and generate a plausible answer to almost anything, the one thing left that is unambiguously a person's job is deciding whether to accept it. That is a narrower, higher stakes position than writing code faster ever was, and it means the judgment underneath an engineer's decisions matters more now, not less, at the exact moment most companies have no real answer for how that judgment actually gets built.

Most companies default to one of two answers, and both fail in mirrored, structural ways. A formal mentoring program standardizes what it teaches, exactly what promotion and clear ownership need. Informal mentoring goes the other way: real proximity and real time reasoning produce real judgment, but leave no visible trace, no comparable record, no way for anyone above the pairing to tell whether it worked or where the gaps still are.

---

## The Blind Spot: Two Kinds of Knowledge, One Structure Forced on Both

Ask a company why its formal mentoring program produces engineers who can pass a design review on the exact principles they then violate under deadline pressure, and the honest answer is rarely "the curriculum was wrong." The curriculum usually did exactly what curricula do well: it made a body of knowledge explicit, standardized, comparable across people, easy to check off for a promotion packet. That is a real, valuable property, and it is also the whole problem, because judgment is not that kind of knowledge.

Decades of research across cognitive science, education, and organizational knowledge management converge on the same distinction, going back to the mid-1960s and running through modern accounts of expertise: explicit knowledge is what can be written down, taught as a rule, and transferred through content at scale. Tacit knowledge, the kind that shows up as expert judgment, pattern recognition, and situated decision making under real pressure, resists exactly that kind of transfer. It is not that nobody has tried to formalize it well enough yet. It is that the thing itself, by its nature, does not reduce cleanly to a rule someone can memorize and then correctly apply the first time reality diverges from the example. Expertise research describes this as a developmental progression, from following a rule toward intuitive, context sensitive action, and the second stage does not arrive by being told the rule more clearly. It arrives through direct exposure to situations a rule alone does not cover.

That is exactly why formal programs transfer knowledge well and judgment poorly, and it is not a fixable oversight in the curriculum design. It is what a uniform, rule based structure is and is not built to carry.

Informal mentoring fails for the mirrored reason. Direct proximity, watching someone reason through a real decision, absorbing how they think rather than only what they concluded, is precisely the mechanism tacit knowledge actually moves through. Informal mentoring often does build real judgment. What it does not do is leave anything behind. Nobody can compare one pairing's progress to another's. Nobody catches a structural gap in someone's foundation unless they happen to ask the right question at the right moment. And when something in the relationship itself stops working, there are no rails for solving it, no diagnostic method, no escalation path, just whatever informal goodwill the two people involved happen to have left.

---

## The Fix: Let the Structure Follow the Gap, Not the Program

Once judgment and knowledge are understood as needing opposite structures, planned for one, reactive for the other, the actual design question stops being which structure the whole program should use. It becomes: who decides, and when, which structure a specific diagnosed gap actually needs.

The framework I built puts that decision at the level of a single diagnosed gap, inside a visible, documented process, rather than baked into the program's design once for everyone.

**Diagnose before choosing anything.** Every gap starts by being classified as one of three kinds: a knowledge gap, where the person simply does not have the information yet; a practice gap, where they have the knowledge but have not rehearsed it under real conditions; or a judgment gap, where they can execute the mechanics but struggle to decide when and how much to apply them. This classification is not cosmetic. It is what tells a mentor which structure to reach for next, and it comes from more than one source deliberately, self report under real pressure, peer input, a review of existing work, sometimes a small task, since a single data point, especially a person's own confident self assessment, is the weakest evidence available on its own.

**Curate knowledge, design judgment.** For a knowledge gap or the knowledge portion of a larger one, the framework pushes a mentor toward the company's own growing library of proven material, or good external material, before authoring anything from scratch. This is the same instinct behind treating architecture as something you decide on purpose rather than by default: a value that changes rarely and only a specialist ever touches does not need a bespoke exercise built around it, it needs a good, reusable answer. Judgment gaps get the opposite treatment. They call for a genuinely designed exercise, chosen deliberately between two modes.

**Planned Mode** sequences a small number of high signal constraints from easiest to hardest, each one gated behind a real, measurable result before the next arrives. It builds a specific, identifiable instinct cleanly, and it is generally the right fit for a practice gap: the person already has the knowledge and needs structured, escalating repetition to make it reliable.

**Reactive Mode** widens a problem unpredictably, deliberately withholding how many changes are coming or what shape they will take, requiring a genuine, working resolution rather than a chance to stop partway through. It builds tolerance for and recognition of ambiguity, and it is the better fit for a judgment gap specifically, since a person who has the mechanics but struggles to decide when to apply them typically needs exposure to real, unresolved uncertainty, not more repetition of something they already know how to do.

**Make the whole thing visible without making it rigid.** Every one of these choices, which mode, which format, which task source, gets recorded, not to bureaucratize the relationship, but so a season's worth of decisions can be read later as a trajectory, and so a new person picking up the pairing, or a manager trying to understand whether the investment is working, has something real to look at instead of a vague impression. The record does not remove the individualization. A pairing still designs its own exercises around its own specific gap. What it removes is the total invisibility that makes informal mentoring impossible to evaluate or improve at scale.

---

## The Insight: Watching the Two Gaps Actually Diverge

I was able to watch a scenario: an engineer moving from C# into a C++ codebase, carrying real instincts that mostly do not transfer, alongside a mentor with deep technical depth and no real practice teaching anyone. The case demonstrated the separation of a practice gap from a judgment gap inside the same person, at the same time, so the two would not get diagnosed or treated identically by accident.

What that surfaced is the thesis proving itself rather than illustrating it after the fact. The practice gap, modern C++ ownership and memory mechanics, closed cleanly under Planned Mode, and held up even once real, unplanned deadline pressure hit later in the season. The judgment gap, knowing when an abstraction is actually worth its structural cost in a language where that cost is real, narrowed under the deliberately designed pressure of a Reactive exercise, and then partially reappeared the moment real, uncompressed time to think was taken away. Not a failure of the framework. Confirmation of exactly the asymmetry the whole design assumes: a practice gap becomes reliable through structured repetition, and a judgment gap needs sustained, repeated exposure to real pressure over more time than one structured season can fully provide.

The visibility this produced mattered as much as the diagnosis itself. Because the season's decisions were documented as they happened rather than reconstructed afterward from memory, the eventual review could separate two claims that get collapsed by default in almost every informal setting: one season was not long enough for this specific judgment gap to close, and no second season had actually been committed to in the first place. Those are different findings with different implications, and only one of them says anything true about how long judgment actually takes to form. An informal process would have produced a single, vague impression instead, something closer to "it sort of worked, mostly," with no way to tell which claim that impression was actually standing in for.

---

## The Production Bottom Line

> **Let the Structure Follow the Gap:** A formal mentoring program and an informal one are not two points on a quality spectrum, one disciplined, one lazy. They are two different structures, each genuinely well suited to one kind of knowledge and genuinely unsuited to the other. Formal buys standardization and loses judgment, by nature. Informal buys judgment and loses visibility, by nature. Building something better does not mean splitting the difference between them. It means diagnosing what a specific gap actually is before choosing how to close it, and keeping that choice, and its outcome, visible enough that the next pairing does not have to start from nothing. Judgment was always going to matter. What changed is how expensive it has become to leave its transfer to accident.