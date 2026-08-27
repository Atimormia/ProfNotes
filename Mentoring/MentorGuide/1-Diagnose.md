# Mentor Guide 01: Diagnostic Toolkit

## Purpose

This toolkit covers finding a Mentee's starting gaps and evaluating their progress against those gaps over time. Both are the same method, run at different moments: gather evidence, compare it against a defined expectation, classify what's found. What changes across moments is timing and stakes, not the underlying process.

## The Diagnostic Method

Run this four-step method at any diagnostic moment, whether a formal Baseline, a Checkpoint, or an informal check mid-module.

**1. Define what's being assessed.** State the specific competency or behavior in question before gathering any evidence. This is the toolkit's hard rule, applied at the method level: without this, evidence gathered next has nothing to be evidence of.

**2. Gather evidence from more than one source.** A single data point, especially a single self-report or a single constructed task, is the weakest form of evidence available. Combine sources where practical:

* **Self-report**, including the Mentee's own account of where they had to guess, improvise, or work past a gap under real delivery pressure. This is a richer signal than a general self-assessment, since it points at a moment the gap actually mattered, not a hypothetical.
* **Peer and colleague input.** People who work alongside the Mentee day to day, including the Mentor, form opinions about the Mentee's work in the normal course of collaboration. Surfacing that existing opinion, rather than manufacturing a new evaluation, is often cheaper and more honest than any constructed instrument.
* **Work archaeology.** The Mentor reviews the Mentee's existing work, commits, PRs, past decisions, from a diagnostic lens, looking for a specific pattern rather than general quality.
* **A designed task**, used sparingly and only where the other sources leave a real gap unconfirmed. A task should never be built around a single expected right answer or constructed specifically to expose one weakness. It should be a normal, low-risk unit of real or realistic work, observed for what it reveals, not a test with a pass condition.

**Where sources disagree, treat the disagreement as the signal.** A Mentee who reports confidence in an area where a peer or the Mentor's own archaeology suggests otherwise is more diagnostically useful than either source alone. Don't resolve the discrepancy by picking the source you trust more by default; raise it directly with the Mentee as a starting point for discussion.

**3. Classify the gap.** Once evidence points to something specific, name what kind of gap it is before deciding how to close it:

* **Knowledge gap:** the Mentee doesn't yet have the information or hasn't encountered the concept.
* **Practice gap:** the Mentee has the knowledge but hasn't done it enough, under real conditions, for it to be reliable.
* **Judgment gap:** the Mentee can execute the mechanics but struggles to decide when, whether, or how much to apply them.

This classification matters because the three types call for different responses. A knowledge gap is usually the cheapest to close and the least interesting to spend a full module on. A practice gap calls for repetition under realistic constraints. A judgment gap is the hardest to manufacture practice for and usually needs real, ambiguous, in-context work rather than an exercise. Which toolkit to reach for next (see Training Approach and Responsibility Transfer) depends on getting this classification right first.

**4. Note direction, leave intervention detail to planning.** At the diagnostic moment, the output is: here is the gap, here is its type, here is roughly how urgent it is. The specific exercise, task, or curriculum module built to close it is planning work, covered in the Training Approach Toolkit and the Mentoring Program's Phase 2, not this toolkit.

## The Three Moments

The method above runs identically at each of these; what changes is timing, stakes, and what the result gets compared against.

* **Baseline:** Run once, near the start of the mentoring relationship or a new curriculum area. Step 2's evidence has nothing prior to compare against yet; the output of Baseline becomes the comparison point for every later Checkpoint.
* **Checkpoint:** Run at minimum once per module, at whatever grain the module is sized. Step 2's evidence is compared directly against the Baseline and against the expectations set for that specific module.
* **Season Synthesis:** Not a new run of the method. A reading of the pattern across a season's Checkpoints, to understand trajectory rather than to re-diagnose a single point. If a season's evidence shows an earlier gap classification or urgency estimate was wrong, this is the right moment to revise it.

## A Caution on Stakes

By the time a Checkpoint runs, the Mentee has invested real effort and has something to lose in a way they didn't at Baseline. This mirrors a well-documented effect in evaluated performance generally: awareness of being judged measurably changes how someone performs, independent of their underlying skill. Frame Checkpoint conversations with this in mind, and actively resist any framing, from the Mentee, a Manager, or HR, that treats a Checkpoint as a graded test. See Guide 00's "Diagnosis Is Not Performance Review."

## Software Engineering Example

**Baseline:** A new Mentee joins claiming familiarity with SOLID principles. Rather than starting with a constructed task, the Mentor first checks two other sources: a conversation with the Mentee about a recent moment they had to make a structural decision under deadline pressure, and a quick review of the Mentee's recent commits for structural patterns. Both suggest the Mentee names principles correctly but defaults to duplicating logic rather than extracting it, under any time pressure. Only then is a small, realistic task used, not to test the Mentee, but to confirm the pattern directly. The gap is classified as a **practice gap**: the Mentee has the knowledge, but applying it reliably under pressure hasn't been rehearsed.

**Checkpoint:** At the end of a module built around that specific practice gap, the Mentor checks the same three sources again: does the Mentee's own account of a recent pressured decision show a different instinct now, has a peer noticed a change, does recent work show the pattern shifting. Direct comparison against the Baseline's specific finding, not a general re-test.

**Season Synthesis:** Across a season, the pattern across several such Checkpoints shows the practice gap closing under moderate pressure but reappearing under extreme deadline pressure specifically. That reveals the original classification was slightly wrong: what looked like a general practice gap is closer to a **judgment gap** about when to cut a corner and when not to, worth naming explicitly for the next season's planning.

## Result

A documented Baseline (with its evidence sources and gap classification), a series of Checkpoint records comparable against it, and a Season Synthesis that reads the set as a trajectory, feeding the Individual Goals Document, the Mentoring Strategy Document, and the Mentoring Program's Phase 4 review.