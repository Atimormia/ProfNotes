# Game of Life Interview Ladder

## 1. Purpose

This document specifies a laddered take-home + live-discussion interview built around a single seed problem (Conway's Game of Life). It is designed to be used or adapted directly by a hiring team, not read as narrative. Everything here, prompts, rubrics, tooling, is a starting point to be customized to a specific team's stack and domain.

The design goals, in priority order:

1. Test architecture and engineering judgment, not typing speed or memorized syntax.
2. Allow AI assistance throughout the async portion, since restricting tools a candidate would use on the job doesn't produce a cleaner signal, just an artificial one.
3. Minimize observation-effect stress (per the research cited in [Live-Coding.md](Live-Coding.md)) by keeping the pressured, evaluative parts of the process asynchronous and reserving live time for discussion, not production.
4. Produce a scored rubric, not an interviewer's gut feeling.

---

## 2. Problem Design

Cellular automata show up in real game systems constantly: procedural generation, fog of war, fire/water spread, ecosystem simulation. It's a two-sentence rule set, so no candidate is blocked by unfamiliar domain knowledge, but it has genuine, well-documented algorithmic depth underneath.

### The Ladder

**Rung 1: Naive correctness.** Bounded 2D grid, brute-force neighbor counting, Conway's birth/survival rule. Baseline: does the candidate get the rule right and handle edges without reading out of bounds.

**Rung 2: Efficiency at scale.** Push to a 10,000×10,000 board, every frame. Two natural directions: active-frontier/candidate-cell tracking (only re-evaluate live cells, recently changed cells, and their neighbors) or bit-packing (64 cells per word, bit-tricks for neighbor counting). A candidate does not need to implement bit-packing to score strongly on Rung 2 if they benchmarked the naive version, identified the workload assumptions, and chose a simpler sparse/frontier approach with clear caveats. Which one they reach for first, and whether they can justify it against the alternative, is the actual signal, not which one they pick.

**Rung 3: Generalization.** An unbounded board forces a sparse representation: a hash set of live coordinates instead of a dense array. This is a real design fork, not an optimization of rung 1.

```cpp
struct CellCoord { long long x, y; bool operator==(const CellCoord&) const; };
struct CellCoordHash { size_t operator()(const CellCoord&) const; };

class SparseLife
{
public:
    void SetAlive(long long x, long long y);
    void Step(); // only touches live cells and their neighbors
private:
    std::unordered_set<CellCoord, CellCoordHash> LiveCells;
};
```

**Rung 4: Numerical/edge-case judgment.** No floats here, but two real hidden bugs: a naive XOR-based coordinate hash clusters badly for patterns near the origin (which is most patterns), silently degrading a hash set into something closer to a linked list at scale; and naive cycle detection (hashing the whole board) fails on a glider, whose cells move every tick even though the pattern itself is periodic: correct cycle detection needs translation-invariant canonicalization.

**Rung 5: Systems thinking (Hashlife).** A quadtree with hash-consed nodes, where each node caches its own future state some generations ahead, computed recursively from its children. Repeated/self-similar structure becomes near-free to simulate arbitrarily far forward (a dramatic, concrete illustration of architecture beating brute force). The key test isn't "can you implement this," it's "can you say what has to be true about the input for this to help": it does nothing for a fully random board.

**Rung 6: Live architectural extension.** Two directions: extending to a rule variant (e.g., HighLife's `{3,6}` birth rule) tests whether rule logic was ever separated from grid iteration in the first place; integrating into a per-frame tick budget tests whether the candidate recognizes that dense/frontier approaches can often be chunked incrementally across frames, while Hashlife's recursive structure resists slicing.

## 3. Process Overview

| Stage | Format | Duration | Candidate effort | Purpose |
|---|---|---|---|---|
| Step 1 | Async, written submission | Delivered async, ~1 hour of work | Solve + write up | Correctness + basic scale (Rungs 1–2) |
| Step 2 | Async, written submission | ~1 hour of work | Solve + write up | Generalization (Rung 3) |
| Step 3 | Async, written submission | ~45 min of work | Review + comment | Code review under real conditions (seeded mistakes) |
| Step 4 | Live, video call | 45–60 minutes | Conversation only, no coding | Numerical judgment, systems thinking, live extension (Rungs 4–6) |

Each async step unlocks the next only once submitted. This can be [automated](#10-environment--tooling) so no interviewer has to manually gate progress. Total candidate time investment: roughly 3 hours async + under an hour live, spread across as many days as the candidate needs.

---

## 4. Step 1: Candidate-Facing Prompt (Rungs 1–2)

> **Task: Simulate Conway's Game of Life**
>
> Conway's Game of Life is a cellular automaton on a 2D grid of cells, each either alive or dead. Each generation, every cell's next state is determined by its eight neighbors:
> - A live cell with fewer than 2 or more than 3 live neighbors dies.
> - A live cell with 2 or 3 live neighbors survives.
> - A dead cell with exactly 3 live neighbors becomes alive.
>
> **Part A.** Implement a simulation for a fixed-size grid (e.g. 200×200). Provide a way to seed initial live cells and advance the simulation by one generation.
>
> **Part B.** Your simulation needs to run against much larger grids (10,000×10,000) as part of a real-time system, advancing once per frame. The workload is intentionally underspecified: state what kind of patterns you are optimizing for, profile your Part A solution under that assumption, and improve it. You may take any approach you can justify.
>
> **Deliverable:** Code, plus a short written note (half a page is plenty) covering: what you measured, what you changed, and why. You may use AI assistants, search, documentation, and normal development tools. Be prepared to explain and defend anything you submit; do not fabricate benchmark results or submit code you cannot reason about.
>
> No time limit on Part A/B combined beyond keeping it to roughly an hour of focused work; submit whenever you're satisfied.

### Example Candidate Response

*(This is a reference response for calibration, not a "correct answer" key. Real submissions will vary widely and that variation is the point.)*

**Part A (excerpt):**

```cpp
class NaiveLife
{
public:
    NaiveLife(int width, int height)
        : Width(width), Height(height), Grid(width * height, false) {}

    void SetAlive(int x, int y, bool alive) { Grid[Index(x, y)] = alive; }

    void Step()
    {
        std::vector<bool> NextGrid(Grid.size(), false);
        for (int y = 0; y < Height; ++y)
            for (int x = 0; x < Width; ++x)
            {
                int Neighbors = CountLiveNeighbors(x, y);
                bool Alive = Grid[Index(x, y)];
                NextGrid[Index(x, y)] = Alive ? (Neighbors == 2 || Neighbors == 3)
                                               : (Neighbors == 3);
            }
        Grid = std::move(NextGrid);
    }
    // ...
};
```

**Part A write-up (excerpt):** "Straightforward dense-grid implementation. O(width × height) per step. Handles bounds by checking neighbor coordinates before indexing."

**Part B write-up (excerpt):** "At 10,000×10,000, Part A recomputes all 10^8 cells every frame regardless of how many are actually alive. I profiled and found we're allocating a full NextGrid every step too, which shows up in the allocator. I switched to active-frontier tracking: maintain a candidate set around live cells and cells that changed last step, and only re-evaluate those candidates and their neighbors. This assumes most of the board is stable most of the time, which held for our test patterns but would degrade if the whole board were chaotic. An alternative I considered was bit-packing 64 cells per word for cache density; I'd reach for that if the workload were dense and uniformly active rather than sparse."

---

## 5. Step 2: Candidate-Facing Prompt (Rung 3)

> **Follow-up:** Your simulation now needs to support an effectively unbounded board (patterns can move freely without wrapping or hitting an edge; assume coordinates fit in 64-bit integers). Adapt your solution. Include a few simple checks, such as a still life, an oscillator, and edge/corner behavior.
>
> Same deliverable format: code plus a short written note. If your Part B approach depended on a fixed board size, explain what has to change and why.

*(A strong response pivots to a sparse representation, e.g. a hash set of live coordinates, and explicitly discusses why a dense array or fixed-size frontier structure no longer applies. See Section 2 for a reference implementation shape.)*

---
## 6. Step 3: Async Code Review (Seeded Mistakes)

**Candidate-facing prompt:**

> Attached is a pull request against a teammate's branch, extending the simulation to support a new rule variant (HighLife: cells are also born with exactly 6 neighbors, in addition to 3). Review it as you would a real PR: leave comments on anything you'd flag before approving, and note anything you'd want changed.
>
> There's no single "correct" number of comments expected; we're interested in what you notice and how you'd communicate it.

**The seeded PR (illustrative excerpt, intentionally flawed):**

```cpp
// Reviewer note: this is what the candidate sees, unannotated.

// Rule now lives directly on the grid class as a hardcoded condition
// instead of being owned by a separate, swappable rule object.
class Grid
{
public:
    std::vector<bool>& GetCellsMutable() { return Cells; } // exposes internal storage directly

    void Step()
    {
        std::vector<bool> NextCells(Cells.size(), false);
        for (int y = 0; y < Height; ++y)
            for (int x = 0; x < Width; ++x)
            {
                int n = CountLiveNeighbors(x, y);
                bool Alive = Cells[Index(x, y)];
                NextCells[Index(x, y)] = Alive ? (n == 2 || n == 3 || n == 6) // bug: survival shouldn't include 6
                                                : (n == 3 || n == 6);
            }
        Cells = NextCells; // full copy every step instead of reuse/move
    }

private:
    std::vector<bool> Cells;
    int Width, Height;
    int CountLiveNeighbors(int x, int y) const { /* ... */ }
};
```

This excerpt is deliberately simplified to demonstrate the shape of the exercise, not to represent real-interview seeded bugs. In your own codebase, seed something closer to the subtlety of a real PR mistake, wrapped inside a change that otherwise reads as correctly solving the assigned problem, rather than an isolated, easily pattern-matched anti-pattern.

Three seeded issues, one per category, chosen to test different reviewing instincts:

- **A design-principle break:** `GetCellsMutable()` exposes the grid's internal storage directly, and the new rule condition is hardcoded inline rather than owned by a separate, swappable rule object. Neither of these is wrong in the sense of producing an incorrect result today, but both erode encapsulation and single-responsibility in ways that make the *next* change (a second rule variant, a different storage backend) more expensive. Tests whether a candidate reviews for maintainability, not just output correctness.
- **A correctness/safety break:** survival incorrectly includes 6; HighLife only changes the *birth* rule, not survival. Tests whether the candidate actually reasons about the specific rule change rather than skimming for style, and whether they'd catch a bug that produces a plausible-looking but wrong result rather than a crash.
- **A performance concern** (shown here in simplified form as a needless full-array copy every step): tests whether the candidate notices something that isn't wrong, just worse, which is a common and realistic PR-review scenario.

In your own version of this exercise, calibrate each seed to something you'd genuinely expect on your team: a real encapsulation violation your codebase has actually hit, a real off-by-one or edge-case class of bug, a real performance regression pattern from your own postmortems. The categories matter more than these specific examples.

Seeded PRs can be authored directly by the interviewer, or generated by taking the candidate's own Step 2 submission and asking an AI assistant to introduce one issue per category, this scales better across many candidates and avoids one hand-written PR becoming known/leaked over time.

---

## 7. Step 4: Live Discussion Guide (Rungs 4–6)

Facilitator talking points, not a script. Goal is open conversation, not quiz-and-check.

- "At 40,000 clustered live cells, your sparse structure's performance degrades. Any idea why, before I tell you?" (tests: hash quality intuition, prediction vs. diagnosis)
- "How would you know the simulation has stabilized, if a glider is present?" (tests: awareness of translation-invariant cycle detection)
- "I've heard of a technique called Hashlife that simulates huge patterns almost instantly. Can you reason about its utility, even if you aren't familiar with it by name?" (If the candidate hasn't heard of Hashlife, briefly explain the premise: a quadtree where identical subtrees are interned and each node caches future states. Then evaluate whether they can reason about when that structure helps or fails. Do not require the name "Hashlife" for credit.)
- "This needs to run inside a fixed per-frame time budget, not to completion. How would you adapt your approach?" (tests: incremental/resumable thinking, ties to real frame-budget constraints)
- "Suppose the same game needs to support both small dense levels and huge sparse ones, in the same shipped title. How would you architect that?" (deliberately open-ended, no clean answer, tests reasoning under ambiguity)

See [full rubric](#8-rubric) for this section.

---

## 8. Rubric

### A. Communication & Process Signals

| Signal | What to look for | Weak | Strong |
|---|---|---|---|
| Written reasoning clarity | Step 1/2 write-ups | Vague, or absent | States what was measured, what changed, and why, concisely |
| Honesty about limitations | Write-ups and live discussion | Claims a solution "just works" with no caveats | Names what would break the approach and under what conditions |
| AI usage transparency (if shared) | Optional chat log | N/A, opt-in only | Shows candidate questioning/correcting AI output rather than accepting it uncritically |
| Code review communication | Step 3 comments | Vague ("looks fine") or purely stylistic nitpicks | Specific, actionable, distinguishes correctness bugs from style/perf concerns |
| Response to pushback | Live discussion | Caves immediately when challenged on a correct decision | Holds reasoning, explains tradeoff calmly, revises only when actually persuaded |
| Comfort with ambiguity | The open-ended architecture question | Freezes, or asserts false certainty | Reasons aloud, commits to a defensible tradeoff, names what they're uncertain about |

### B. Technical / Architecture Signals

| Rung / Moment | Weak signal | Strong signal |
|---|---|---|
| Before Rung 1 | Codes directly against a raw array, no seam | Defines an interface (`IsAlive`, `Step()`) before implementation; representation is swappable later |
| Rung 1 → 2 | Waits to be told to optimize | Flags scale risk before being asked |
| Rung 2 | Picks bit-packing or active-frontier tracking, can't justify against the other | Explains why one fits this context better, grounded in the stated workload assumption |
| Rung 2 | Optimizes without measuring first | Benchmarks Part A at scale before changing it |
| Rung 3 | Treats "unbounded" as equivalent to "just a bigger fixed array" | Recognizes it requires a genuinely different (sparse) representation, not a bigger version of the dense one |
| Rung 3 | Requested checks (still life, oscillator, edges) are present but superficial or copy-pasted without understanding | Requested checks are meaningful, and the candidate adds further cases of their own (e.g. a glider, an empty board) |
| Rung 4 | Diagnoses the hash-clustering issue only after being shown it | Predicts the degradation before being told |
| Rung 5 | Proposes Hashlife reflexively as "the smart answer" | Names the precondition (repeated structure) it depends on |
| Rung 6 | Hardcodes the new rule inline, duplicates the loop | Adds it as a swappable rule object |
| Rung 6 | Assumes the simulation always runs to completion | Recognizes some approaches resist incremental slicing, others don't |
| Anywhere | Escalates sophistication even where a simple solution is already sufficient | States plainly when the simple version is already fine |
| Anywhere | Generic naming (`data`, `temp`, `helper2`) | Domain-specific naming (`LiveCells`, `CanonicalizePattern`) |
| Anywhere | Never asks about deployment context | Asks unprompted about threading, frame budget, determinism |

---

## 9. Role-Level Variants

This task is designed to focus on engineering judgment and architecture skills, and is best suited for senior+ levels. It can be adjusted for other levels and role expectations by trimming the process rather than lowering the evaluation bar informally; rubric weights should also be adjusted to match role expectations.

| Role level | Recommended scope | Primary signal |
|---|---|---|
| Junior | Step 1 + short live discussion | Correctness, tests, communication |
| Mid-level | Steps 1–3 + shorter live discussion | Representation choice, optimization judgment, code review |
| Senior | Full process | Architecture, scale tradeoffs, live systems reasoning |
| Staff+ | Full process with deeper live extension | Multi-representation architecture, operational constraints, cross-team design judgment |

---

## 10. Environment & Tooling

This section is directional, adapt to what a given team already runs.

**Submission and step-gating.** A private GitHub Classroom or a plain private repo per candidate works well: each step is a branch or a tagged commit, and a simple GitHub Action can auto-open the next step's issue/branch once a PR is opened, removing the need for a human to manually gate progress.

**Automated smoke checks, not automated grading.** A lightweight CI job (unit tests for the birth/survival rules, a basic performance benchmark with a generous, non-punitive threshold) can catch broken submissions early, but scoring judgment itself should stay human. Automating the rubric itself is a trap: the whole point of this format is judgment that a checklist can't capture.

**Code review step delivery.** A real PR against a private repo, opened by the interviewer's account or a bot account, with review comments left the same way they would be at work (inline, threaded). Avoids a bespoke review UI and tests the tool candidates will actually use on the job.

**AI chat log sharing.** No special tooling needed beyond asking candidates to optionally export and attach a chat transcript (most assistants support this natively); keep it clearly opt-in in the prompt language itself, not just in an internal policy doc.

**Live discussion.** Any standard video call tool; the only requirement is that no shared code editor is opened during this stage; if a candidate wants to sketch something, a shared whiteboard for diagrams is fine, but no live compilation.

---

*Open items for future revision: a second worked domain example (geometry/5-smooth numbers) with matching prompts and seeded-PR material; guidance on adapting Rubric B's scoring into a numeric scale for cross-candidate comparison; a short calibration guide for interviewers running Step 4 for the first time.*