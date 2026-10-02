# Engineering Notes

Short essays on game engineering, architecture, performance, production workflows, and how AI changes the value of engineering judgment.

The common thread: many problems that look like optimization, tooling, hiring, or workflow issues often start as missing boundaries, unclear ownership, or weak process.

## Start Here

>**Technical symptoms often expose missing ownership, missing boundaries, or missing process.**

1. [Data Layout Is Architecture](DataLayoutIsArchitecture.md) - AoS vs. SoA measured in ParticleSim, and how an interface over a volatile layout keeps the choice revisable per system.
2. [Ownership Tax in Unreal Engine](OwnershipTaxUE.md) - Chains of defensive `IsValid()` checks as a symptom of unowned state, fixed by owning the value where it changes.
3. [Code Review as Architecture Governance](CodeReview.md) - Code review hides several unnamed mechanisms; specify each on purpose, because process is architecture.
4. [Matching Effort To Evidence](MatchingEffortToEvidence.md) - An evidence-gated escalation ladder: spend political capital only when recurrence justifies it.
5. [Mentorship Shape Is a Substrate for Architecture](MentoringFramework.md) - Diagnose whether the gap is knowledge or judgment before choosing a mentoring structure.

## Content
### Game Engineering Architecture

- [Engineer-Designer Boundary in Unreal Engine](BlueprintMess.md) - Where to draw the C++/Blueprint line, and why UE6's move to Verse is about lost discipline, not node graphs.
- [Ownership Tax in Unreal Engine](OwnershipTaxUE.md) - Chains of defensive `IsValid()` checks as a symptom of unowned state, fixed by owning the value where it changes.
- [Upgrading Game Engines Safely](EngineUpgradeCase.md) - How untracked engine source edits turned a UE4 to UE5 upgrade into a multi-year effort, and how governed boundaries prevent it.
- [The Invisible Rebuild Bottleneck](SilentBuildProblem.md) - Occasional multi-hour engine rebuilds go unnoticed because waiting looks like working; a visible process beats an unverified tool.
- [Data-Driven Design As Architecture Boundary](DataDrivenDesign.md) - Moving values out of code creates a hidden data spectrum; choose the layer on purpose and make it traceable.
- [Refactoring a Legacy System at a Critical Point](RefactoringCase.md) - Compressing a textbook refactor of an undocumented settings system with system archaeology and a strangler fig.
- [The Silent Asset Loading Bottleneck](AssetLoadingBottleneck.md) - An inventory hitch that grew with every cosmetics pack, and deciding fetch, virtualization, and eviction strategy on purpose.
- [Finding Seams in a Monolith](NoSeamsRefactoringCase.md) - A 30 MB monolithic scene: understand why the fence exists, then climb the modernization ladder only as high as needed.
- The Cost of Decoupling Everything (demand-driven pitfalls)
- Backward Compatibility (+ feature-flags?)

### Performance as Architecture

- [The `Tick()` Pitfalls](TickPitfalls.md) - Why an early-exiting `Tick()` still costs frame time at scale, and when to switch to demand-driven execution.
- [Garbage Collector Spikes](GarbageCollection.md) - GC spikes in Unreal and Unity, and zero-allocation habits that prevent them during early architecture work.
- [The Cost of a Virtual Function](VirtualFunctions.md) - The vtable and cache-miss tax of virtual calls at high instance counts, and when static polymorphism fits better.
- [Data Layout Is Architecture](DataLayoutIsArchitecture.md) - AoS vs. SoA measured in ParticleSim, and how an interface over a volatile layout keeps the choice revisable per system.
- [Concurrency Is Architecture](ParallelArchitecture.md) - A frame arena that broke under threads: concurrency punishes ownership questions asked too late.
- [Compile-Time Performance vs. Runtime Flexibility](CompileTimeVsRuntime.md) - C# resolves design intent at runtime, C++ at compile time; translating instincts between the two.
- [Where Abstraction Meets The Hot Path](AbstractionMeetsTheHotPath.md) - A stutter spread thin across a dozen small calls: watch frequency changes at opaque boundaries, not chain depth.
- [The Compounding Network Tax](NetworkTax.md) - Loading screens built from many "fast" backend calls; parallelize, triage the critical path, and own one layer to the wire.
- [The Zero-Copy Trap](ZeroCopyTrap.md) - Benchmarks showing when pass-by-value plus `std::move` costs more than it saves, and why trivial relocation matters.
- Architecture First, Optimization Second

### Engineering Judgment
- [AI Exposes Gaps in Architecture Design](AI&ArchitectureSkills.md) - AI made syntax free and exposed that boundary design, not typing, was always the core engineering skill.
- [The Engineer-Process Boundary](EngineerProcessBoundary.md) - A proven fix that never got adopted: where line-engineer judgment ends and process has to take over.
- [Matching Effort To Evidence](MatchingEffortToEvidence.md) - An evidence-gated escalation ladder: spend political capital only when recurrence justifies it.
- [The Refactor That Held](RefactorThatHeld.md) - Why a correct fix still isn't enough when the organization around it was never ready to absorb it.
- [Decomposition Is a Judgment Call](DecompositionIsAJudgmentCall.md) - Structure, flow, and failure as three decomposition axes, and how defaulting to one makes code rot.
- [Code Review as Architecture Governance](CodeReview.md) - Code review hides several unnamed mechanisms; specify each on purpose, because process is architecture.
- **Mentorship and Evaluation**
  - [Live-Coding Interview: What the Science Says About Our Favorite Technical Screen](Live-Coding.md) - What research says live-coding interviews actually measure, and what better predicts on-the-job performance.
  - [How to Hire Engineers When Syntax Is Free](TechInterview.md) - An interview format built around judgment: laddered async tasks with AI allowed, written answers, and code review.
  - [Architecture Is a Felt Contrast](ArchitectureIsaFeltContrast.md) - Architectural judgment is learned by building the rigid version first and feeling the contrast with planned growth.
  - [Training Juniors Is an Architecture Choice](TrainingJuniorsIsAnArchitechtureChoice.md) - With safety-net roles gone and AI in the loop, teams must deliberately design how juniors build independent judgment.
  - [Mentorship Shape Is a Substrate for Architecture](MentoringFramework.md) - Diagnose whether the gap is knowledge or judgment before choosing a mentoring structure.