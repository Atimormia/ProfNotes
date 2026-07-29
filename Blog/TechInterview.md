Fair — you're right that AI&ArchitectureSkills.md itself doesn't strictly follow the "flowing paragraph" pattern either, it has its own numbered structure (Lock the Schema First, Treat AI Code Like an Engine Fork, etc.), so holding this post to a stricter standard than that one isn't really consistent. And for a post that's explicitly a "here's a proposed process with several concrete components" piece, numbered/labeled sections genuinely do make it easier to scan and reference back to, which matters if this is meant to be something a tech lead could actually action.

So let's go back to the previous version's structure (the `###` numbered sections), just keep the language pass we did on top of it, plainer phrasing, no colons-as-explanation, shorter sentences, since that part was a real improvement regardless of heading style.

Here's that combination:

# How to Hire Engineers When Syntax Is Free

A few years ago, I was given a take-home task that started as a simple algorithmic problem. I worked through it, wrote up my reasoning, submitted it, and got genuinely excited. My teaching experience hinted at how far this specific problem could go: harder constraints, generalization, memory limits, numerical edge cases, concurrency, live redesigns. It had real room for depth.

Going into the live round, I was curious what the interviewer actually wanted to explore, and hoping for a chance to show more architectural thinking than a first submission usually allows.

The live round asked one brief question about my code, dropped it, and switched to a completely unrelated live-coding puzzle.

Nothing about that was malicious. It looked like a planned part of their process. That's exactly what makes it worth writing about. The task had real depth. The process around it wasn't built to use any of it.

---

## The Blind Spot: A Good Task Isn't a Good Interview

I've written before about why [live-coding as a format measures the wrong thing](Live-Coding.md), performance under observation, not engineering judgment. This is a different problem, and a subtler one: even when a task is genuinely good, nothing about having it guarantees the process spends time where the depth actually is.

A rich task dropped into a format built for something else, verify they didn't cheat, then run a second, disconnected problem, gets almost none of its value extracted. The bottleneck isn't the task design anymore. It's whether the process is built to reach the parts of the task that actually reveal judgment.

There's a second piece to this, and it connects to something I've written about separately: [AI didn't remove the need for engineers, it removed the friction that used to force architectural thinking](AI_ArchitectureSkills.md). If AI makes syntax generation fast and easy to fake, testing "can you produce this code" measures a skill that's rapidly becoming free. What's left to test, designing boundaries, reasoning about tradeoffs, reading ambiguous requirements, communicating decisions clearly, is exactly what a live syntax round can't see.

I also spent four years teaching CS before moving fully into engineering, and I saw the same measurement gap play out there:

- A **written test** shows you an answer, not the reasoning behind it.
- **Live coding** shows you performance under pressure, not judgment.
- A **conversation** shows you communication and how someone frames a problem, not whether they can actually solve it.

None of these formats are wrong exactly, they're just each measuring something adjacent to the real target, and a person's actual understanding is almost always broader than whichever single format happens to catch. A rubric matters, but it's only as good as the process feeding it. You need enough different kinds of moments, written, live, reasoning under a new constraint, to actually see architecture and engineering judgment, rather than one of its shadows.

---

## The Fix: A Format Designed Around Signal

Rather than one intense live session, the format I'd propose is a short async sequence with a live discussion at the end, built around a single task with a laddered structure: each step raises the stakes on the same problem instead of introducing a new one, so nothing gets thrown away and nothing has to be re-explained from scratch.

### 1. Laddered Async Steps, AI Allowed

Break the task into 2-3 steps, delivered one at a time, each scoped to about an hour. A candidate submits a step and, this can be fully automated, receives the next one only once they have.

Each step deliberately assumes AI assistance is fine to use. If the goal is testing judgment rather than typing speed, prohibiting the tools a candidate would actually use on the job doesn't make the signal cleaner, it just makes the test artificial.

### 2. Written Submissions Graded as Communication

Require a short write-up with each step. How clearly someone explains their reasoning, flags a limitation, or outlines a tradeoff in a brief doc is a real, directly transferable proxy for how they'd write a PR description on the job, and it's a skill nobody tests in a live-coding round at all.

### 3. AI Chat Logs as a Rich, Opt-In Signal

Where a candidate is comfortable sharing it, their AI chat history alongside a submission is a genuinely rich signal: what they asked, whether they pushed back on a suggestion, whether they caught something the model got wrong. This should stay opt-in, plenty of strong candidates won't want to share raw chat logs, but where it's offered, it says more about judgment than the final diff does alone.

### 4. Asynchronous Code Review

Hand the candidate a small diff or PR, seeded with a few intentional issues, whether written by the interviewer or produced by feeding their own earlier step back through an AI with a deliberate mistake or two added, and have them leave review comments the way they would on a real repository. It's one good option among several here, not the centerpiece, but it's a rare chance to test something constant in the actual job and almost never tested anywhere: how someone reads and responds to somebody else's code under normal working conditions.

### 5. Live Discussion Over Live Coding

The live round contains zero new code. The conversation is entirely about the reasoning behind what the candidate already built: why this representation, what breaks at scale, how they'd extend it under a new constraint. This is where architectural judgment actually becomes visible, and it's the part a rushed, single live question can't get to if it never survives past the first five minutes.

### 6. Domain-Matched Task Customization

The task itself is a customization point, not a fixed choice. I built out a full worked example, a task with real mathematical and systems depth, walked through step by step across six rungs from naive correctness up to live architectural extension, along with branch points to watch for and a scoring rubric, as [a separate resource](../Process/TechTaskDesign.md). I'm giving the actual task material there rather than just describing it, so a reader can look at it directly and judge for themselves whether it fits their own team.

That resource uses a well-known algorithmic problem chosen mainly to demonstrate the shape. A geometry-heavy team, for instance, might get more out of a task built around finding the *n*-th 5-smooth number instead, same six-rung structure, different domain, chosen to match what the team actually builds day to day.

---

## The Insight: The Format Is the Point, Not the Puzzle

The specific task doesn't matter nearly as much as the shape: pick something with enough real depth, and enough relevance to what the team actually ships, that it can be re-entered from multiple angles without ever switching to an unrelated problem. Almost any well-chosen problem can be built into this shape, in whatever domain suits the team. What can't be retrofitted after the fact is a process willing to spend the time where the depth actually lives, and steps that look like the job itself, writing, reviewing, discussing, rather than a once-a-year performance under a clock.

---

## The Production Bottom Line

> **Wasted Depth:** A good take-home task is not the same thing as a good interview. The task I was given had genuine room to test correctness, scale, generalization, numerical judgment, systems thinking, and design extension, and the process used almost none of it. AI made syntax cheap enough that testing for it stopped being useful a while ago. What's left to test is judgment, and judgment only shows up if the process is deliberately built to reach it, through steps that resemble the actual job, not an accident of however much time happens to be left over after the first question.