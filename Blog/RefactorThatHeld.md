# The Refactor That Held

The company had bought an indie game for one reason: it tested well in marketing. The plan was a reskin: swap the narrative and the environment for an IP we owned, and keep everything else intact. From the outside, it looked like low-effort work: change some models, write some new levels, ship it.

I joined after that decision was already made. My first weeks were spent analyzing the project alongside the CTO, the two of us figuring out what we had actually bought. Together with an artist and a designer, we pushed the reskin and the first levels to an MVP. It worked, but it was inefficient in a way that was hard to ignore: we were colliding constantly, stepping on each other inside the exact same files on a near-daily basis.

Right after the MVP shipped, the CTO left. There was no explanation given, no handover plan, nothing. The collision problem that had been merely annoying a week earlier was suddenly mine to solve, and there was no one left above me to solve it with.

I eventually fixed it. The refactor held, technically, for as long as the project existed. This isn't that story; that one is told in [Finding Seams in a Monolith](NoSeamsRefactoringCase.md). **This is the story of everything surrounding that fix that had nothing to do with its quality, and why a correct refactor was never going to be enough on its own.**

---

## The Blind Spot: A Fix Doesn't Get Absorbed by Being Correct

A refactor doesn't land in a vacuum. It lands inside an organization, and that organization's condition at the time decides whether the fix actually gets to compound, or whether it gets overwhelmed by forces that have nothing to do with the code. Several of those conditions were already broken before I ever touched the scene file.

**1. The acquisition gap:** An indie game, finished and frozen, was bought because it tested well with players. The business then needed it to behave like something else entirely: a living platform that could absorb an ongoing stream of content, and eventually reconcile with a separate version being developed in parallel. Nobody checked whether what we bought was built to do that. There is a real, named category in software acquisitions for this exact failure: **architecture that does not match the growth thesis**. No refactor executed after the fact could change what was true at the moment of purchase.

**2. The succession vacuum:** A single person, the CTO, held the entire technical continuity. When they left days after the MVP, the organization did not have a successor ready; it simply had a vacancy. I spent weeks trying to get direction from the studio director before realizing the actual problem: I wasn't being denied direction, there was simply no one left positioned to give it. That structural gap above me existed regardless of what I did below it.

**3. The task-switching tax:** Right after the refactor landed, the director pulled me onto a second project for about a month. It was work I didn't want and knew was an inefficient use of my time, but I lacked the standing to refuse it outright. The cost of that diversion was concrete: research on task switching puts an engineer split across two simultaneous projects at roughly 40% effective time on each, with the remaining 20% lost entirely to context switching. A month of critical runway disappeared into pure overhead for reasons that had nothing to do with the refactor's design.

None of these three problems could be resolved by a better technical plan. They were organizational facts sitting underneath the project the entire time, and code quality was never going to be the variable that decided whether they mattered.

---

## The Fix: Engineering Authority and Process

Getting the refactor built was never solely an engineering task; treating it as one would have left it unable to survive. What shifted the situation first was not a technical insight, but a change in how I communicated.

I stopped framing my proposal as a question for the director and started presenting it as a decision I had made: here is what we are doing, here is the schedule, and here is the overtime approval I need so I can do the surgery over the weekend without blocking the team. In that same conversation, I stated plainly that if I was taking responsibility for calls of this scale while the team grew under me, I needed a title that reflected it.

Nobody stopped the plan. The director approved the overtime. The promotion followed the refactor, and it mattered for a practical reason: **it gave subsequent decisions real organizational standing instead of borrowed authority.**

Authority alone was still only half the scaffolding. I had to build out the operational infrastructure so the team could actually absorb the technical changes:

* I built a CI/CD pipeline and an explicit branching strategy where there had been none.
* I introduced Scrum to a team that had never run it, which meant coaching our producer on Jira workflows while learning to run the board myself.
* I fought leadership for predictable sprint goals, because the team had told me directly that arbitrary ambiguity was wearing on them far more than the workload itself.

Every one of these was necessary scaffolding. A correct scene architecture cannot help a team that has no predictable cadence, no shared process, and no clear chain of decision-making sitting on top of it.

---

## The Practice: When Upstream Drift Collided with Downstream Reality

The CI/CD pipeline, the Scrum rollout, and handing Jira to the producer were not optimizations for their own sake, nor was I holding the reins out of reflex. It was an active, gradual handoff: moving planning and task decomposition off of me and onto the team, piece by piece, as fast as the work allowed.

It simply hadn't finished. The month right after the refactor, the window that should have gone toward completing that handoff, was swallowed by the second project. Looking back, I cannot fully separate how much of what remained unfinished was due to that stolen month, and how much came from the instinct to hold onto control during a crisis. What I can say honestly is that the effort to build team autonomy was real and in motion, not something I was avoiding.

Meanwhile, the refactor had always been a trade-off, not a free win. Decoupling the monolithic scene and handing content creators their own configuration layer bought massive internal throughput. The cost was mergeability with anything still touching the original structure. **We had executed a permanent hard fork, whether we named it at the time or not.**

The first real test of that fork arrived in the worst possible way. The original indie team had continued developing their version in parallel, and they eventually shipped a major feature that leadership demanded we merge into our project, urgently, on a short deadline.

A git merge was impossible. The two projects no longer shared a common scene graph, initialization lifecycle, or asset structure. The only honest path forward was rebuilding the feature from scratch inside our new architecture.

A ground-up redevelopment under a compressed deadline does not decompose cleanly even for a team with established planning muscle; the true scope stays uncertain until implementation begins. For a team that had never been given the space to practice decomposition independently, it was an impossible first assignment. Every piece of work still had to route through me: the exact same single point of failure the team had leaned on since the CTO left, just with cleaner infrastructure underneath.

It was a textbook systems constraint: **a system's actual throughput is strictly capped by its tightest bottleneck, regardless of how much capacity improves around it.** In the vocabulary of Team Topologies, the team cognitive load was completely saturated. I was trying to manage architectural translation, task breakdown, and core implementation simultaneously, and none of them could be done well under that pressure.

---

## The Insight: Why the Architecture Couldn't Save Us

We did not make the deadline.

What we delivered was a partial implementation: real technical progress, but an incomplete, unstable version of the feature compared to what the business expected on what it had treated as a routine merge timeline. To leadership, the feature was already running on another screen; our inability to drop it in looked like engineering failure.

The project lost its financing shortly after. My team was laid off, and the studio closed its doors permanently soon behind that.

The architecture could support the feature, authored cleanly within the new pipeline. The team's own planning capacity was still being handed over, in motion, not stalled. What wasn't ready was the business's own model: it had assumed a frictionless soft fork, while the team's actual way of working had required a hard fork to function at all. Stabilizing a team in crisis and building an organization that can absorb an external shock without you are two entirely different jobs. When the shock arrived, I was still doing the first.

---

## The Production Bottom Line

> **A refactor's technical quality is necessary, but never sufficient.**
> 
> Whether an architectural fix gets absorbed depends on conditions that code cannot solve: whether the business model matches the architecture it bought, whether succession planning protects technical continuity when leaders leave, and whether an engineering team is given the runway to build its own planning autonomy rather than routing every decision through the person who stepped up to resolve the initial crisis.
> 
> Claiming the authority to decide, and building the process around a fix so a team can actually use it, is real, demanding work. But stabilizing a system yourself is not the same thing as building an organization that can survive the next shock without you standing underneath the entire structure.