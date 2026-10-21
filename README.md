# ProfNotes

Working notes of Palina Freidlina, senior software engineer (C++/C#, systems architecture), with most of my production experience in games (Unreal Engine, Unity).

This repository is the source of my engineering blog and of a mentoring framework I designed for engineering teams. Everything here is written by me.

[LinkedIn](https://www.linkedin.com/in/pfreidlina/) | [Email](mailto:p.freydlin@gmail.com)

## About me

I am a senior C++ developer with a systems and architecture focus. Most of my cases come from games, where I have shipped titles and worked extensively in Unreal Engine and Unity, but the questions I care about are not specific to one industry: performance, ownership and lifetime, inherited codebases, build and content pipelines, and the way a team's process shapes its code. I follow how other industries handle the same problems and draw on them where they fit.

Alongside engineering I teach. I have mentored engineers, run code reviews as an architecture practice, taken part in hiring, and built a structured mentoring framework out of that experience. I also work on JoyBytes Vending, a project where I apply the same habits outside of studio work.

My resume is available on request.

## What I write about

One idea runs through every post:

> **Every architecture is a bet on a workload. The cost of the bet stays hidden until something changes the conditions, and the job is to know the bet, watch for the trigger, and own the decision to revisit it.**

Triggers are usually ordinary: a function that was called once a frame is now called per entity, a long-lived object picks up a reference, an asset list grows, a second thread appears, a team gets bigger, a dependency spreads. The posts show how to see these moments early, in runtime code and in team process. The examples are mostly from Unreal and Unity; the patterns apply well beyond them.

A second thread connects the technical and the human posts: people (and tools) often optimize a **proxy** for the real goal, such as friction instead of discipline, syntax instead of judgment, or a modern-looking mechanism instead of a measured need. Naming the proxy makes the real target visible.

## Where to start

If you have ten minutes, read these in order:

1. [Data Layout Is Architecture](Blog/DataLayoutIsArchitecture.md): how memory shape decides performance long before the profiler does.
2. [Ownership Tax in Unreal Engine](Blog/OwnershipTaxUE.md): how a convenient reference quietly becomes a lifetime and upgrade cost.
3. [Code Review as Architecture Governance](Blog/CodeReview.md): review as the place where boundaries are defended.
4. [Matching Effort to Evidence](Blog/MatchingEffortToEvidence.md): how much action a problem has earned, and how to escalate without drama.
5. [Mentorship Shape Is a Substrate for Architecture](Blog/MentoringFramework.md): how teaching structure produces architectural judgment.

The full catalog, grouped into game architecture, performance as architecture, and engineering judgment, is in [Blog/README.md](Blog/README.md).

## Repository map

| Folder | What is inside |
|---|---|
| [Blog/](Blog/README.md) | Engineering notes: about 30 posts on Unreal and Unity architecture, performance, refactoring, hiring, review, and mentoring. Every post follows the same five-part shape: Hook, Blind Spot, Fix, Insight, Production Bottom Line. |
| [Mentoring/](Mentoring/README.md) | A mentoring framework: concept, curriculum modules, mentor guides, and pilot documents showing how a season is run and documented. |
| [Process/](Process) | Team process drafts: a code review process, a technical task design for interviews, and a cross-team code sharing policy with an audit script. |

## How I work

- I look for the structural cause behind a local symptom, then check whether the evidence justifies acting on it.
- I prefer mechanisms that survive a change of people over heroics that depend on one person.
- I write down trade-offs, including the ones where the answer was "leave it alone".
- I try not to publish numbers I did not measure, and I label borrowed figures as borrowed.

## Notes on the content

Code in the posts is illustrative and written for clarity, not copied from any employer's codebase. Examples from studio work are described at the level of pattern, without internal names or proprietary detail. Published sources are cited where I rely on them.

## Questions

If you are hiring, or want to talk about any of the topics above, reach out through the contact details at the top of this file. I am happy to walk through any post or design decision in detail.