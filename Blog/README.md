# Engineering Notes

Short essays on game engineering, architecture, performance, production workflows, and how AI changes the value of engineering judgment.

The common thread: a design decision is a bet on a workload (how often code runs, how long its objects live, how many people or threads change its state). Many problems that look like optimization, tooling, hiring, or workflow issues start as a bet that expired when that workload moved, with no boundary, owner, or process in place to notice.

## Start Here

>**An architecture is a bet on a workload. Technical symptoms are often where an expired bet gets settled.**

1. [The Bet Behind the Boundary](BetBehindTheBoundary.md) - The through-line of the blog: name the bet, name the trigger that ends it, and give the re-decision an owner. Links to the posts below.
2. [Data Layout Is Architecture](DataLayoutIsArchitecture.md) - AoS vs. SoA measured in ParticleSim, and how an interface over a volatile layout keeps the choice revisable per system.
3. [Ownership Tax in Unreal Engine](OwnershipTaxUE.md) - Chains of defensive `IsValid()` checks as a symptom of unowned state, fixed by owning the value where it changes.
4. [Code Review as Architecture Governance](CodeReview.md) - Code review hides several unnamed mechanisms; specify each on purpose, because process is architecture.
5. [Matching Effort to Evidence](MatchingEffortToEvidence.md) - An evidence-gated escalation ladder: spend political capital only when recurrence justifies it.
6. [Mentorship Shape Is a Substrate for Architecture](MentoringFramework.md) - Diagnose whether the gap is knowledge or judgment before choosing a mentoring structure.

## Content

### Game Engineering Architecture

From boundaries inside one codebase, through data and content, to inherited systems and boundaries between teams.

- [Engineer-Designer Boundary in Unreal Engine](BlueprintMess.md) - Where to draw the C++/Blueprint line, and why the shift toward Verse in UE6 exposes workflow habits more than it replaces node graphs.
- [Ownership Tax in Unreal Engine](OwnershipTaxUE.md) - Chains of defensive `IsValid()` checks as a symptom of unowned state, fixed by owning the value where it changes.
- [Data-Driven Design Is an Architecture Boundary](DataDrivenDesign.md) - Moving values out of code creates a hidden data spectrum; choose the layer on purpose and make it traceable.
- [The Silent Asset Loading Bottleneck](AssetLoadingBottleneck.md) - An inventory hitch that grew with every content pack, in Unity and in Unreal, and deciding fetch, virtualization, and eviction strategy on purpose.
- [The Invisible Rebuild Bottleneck](SilentBuildProblem.md) - A two-hour rebuild survives because waiting looks like working; it is chosen debt, and a visible process beats an unverified tool.
- [Upgrading Game Engines Safely](EngineUpgradeCase.md) - How untracked engine source edits turned a UE4 to UE5 upgrade into a multi-year effort, and how governed boundaries prevent it.
- [Refactoring a Legacy System at a Critical Point](RefactoringCase.md) - Compressing a textbook refactor of an undocumented settings system with system archaeology and a strangler fig.
- [Finding Seams in a Monolith](NoSeamsRefactoringCase.md) - A 30 MB monolithic scene that was right for one author: understand why the fence exists, then climb the modernization ladder only as high as needed.
- [Compatibility Is a Guardrail for the Next Engineer](BackwardCompatibility.md) - A boundary that existed in the repository layout but not in the way two teams worked, and the guardrails that closed the route a change travels.

### Performance as Architecture

From when and how often code runs, through what each call and byte costs, to lifetime, threads, and the network.

- [Scheduling Is Architecture](SchedulingIsArchitecture.md) - A profile that blamed `Tick` pointed at the work running at the tick's frequency: when to wake work on demand, and why sequence belongs in direct calls with events as notifications.
- [Where Abstraction Meets The Hot Path](AbstractionMeetsTheHotPath.md) - A stutter spread thin across a dozen small calls: watch frequency changes at opaque boundaries, not chain depth.
- [The Cost of a Virtual Function](VirtualFunctions.md) - What per-element dispatch does to a hot loop, and how to decide the variation once per batch, per value, or at compile time.
- [Data Layout Is Architecture](DataLayoutIsArchitecture.md) - AoS vs. SoA measured in ParticleSim, and how an interface over a volatile layout keeps the choice revisable per system.
- [The Zero-Copy Trap](ZeroCopyTrap.md) - Benchmarks showing when pass-by-value plus `std::move` costs more than it saves, and why trivial relocation matters.
- [Compile-Time Performance vs. Runtime Flexibility](CompileTimeVsRuntime.md) - C# resolves design intent at runtime, C++ at compile time; translating instincts between the two.
- [Garbage Collector Spikes](GarbageCollection.md) - Hitches that appear only in long sessions: pools, subscriptions, and timers keep objects reachable, so name who clears each reference and when.
- [Concurrency Is Architecture](ParallelArchitecture.md) - A frame arena that broke under threads: concurrency punishes ownership questions asked too late.
- [The Compounding Network Tax](NetworkTax.md) - Loading screens built from many "fast" backend calls; parallelize, triage the critical path, and own one layer to the wire.

### Engineering Judgment

From one engineer's decisions, through team mechanisms, to what an organization does with a fix.

- [Decomposition Is a Judgment Call](DecompositionIsAJudgmentCall.md) - Structure, flow, and failure as three decomposition axes, and how defaulting to one makes code rot.
- [Code Review as Architecture Governance](CodeReview.md) - Code review hides several unnamed mechanisms; specify each on purpose, because process is architecture.
- [AI Exposes Gaps in Architecture Design](AI&ArchitectureSkills.md) - AI made syntax free and exposed that boundary design, not typing, was the core engineering skill all along.
- [The Engineer-Process Boundary](EngineerProcessBoundary.md) - A proven fix that never got adopted: where line-engineer judgment ends and process has to take over.
- [The Refactor That Held](RefactorThatHeld.md) - A correct scene refactor that became a hard fork: technical quality is necessary but not sufficient when the organization around it is not ready to absorb it.
- [Matching Effort to Evidence](MatchingEffortToEvidence.md) - An evidence-gated escalation ladder: spend political capital only when recurrence justifies it.
- **Mentorship and Evaluation**
  - [Live-Coding Interview: What the Science Says About Our Favorite Technical Screen](Live-Coding.md) - What research says live-coding interviews actually measure, and what better predicts on-the-job performance.
  - [How to Hire Engineers When Syntax Is Free](TechInterview.md) - An interview format built around judgment: laddered async tasks with AI allowed, written answers, and code review.
  - [Architecture Is a Felt Contrast](ArchitectureIsaFeltContrast.md) - Architectural judgment is learned by building the rigid version first and feeling the contrast with planned growth.
  - [Training Juniors Is an Architecture Choice](TrainingJuniorsIsAnArchitectureChoice.md) - With safety-net roles gone and AI in the loop, teams must deliberately design how juniors build independent judgment.
  - [Mentorship Shape Is a Substrate for Architecture](MentoringFramework.md) - Diagnose whether the gap is knowledge or judgment before choosing a mentoring structure.
