# Mentoring Framework

## Problem
Informal mentoring was inconsistent, hard to evaluate, and often collapsed into ad-hoc help or unstructured shadowing.

### Goal
Create a repeatable mentoring framework that supports skill growth, responsibility transfer, and mentor decision-making without turning mentoring into performance review.

### My Contribution
Designed the program structure, mentor toolkits, diagnostic model, responsibility-transfer model, and supporting documentation.

### Core Ideas
- Evidence-based diagnosis before intervention
- Knowledge/practice/judgment gap classification
- Planned vs reactive training modes
- Watch → Do Together → Do Alone → Own It responsibility transfer
- Diagnosis separated from performance review

## Content

This folder contains the full Mentoring Program: the structural framework for running mentoring at the company, and the Mentor Guide, the companion reference for Mentors making day-to-day judgment calls within that structure. The Program defines what happens and when. The Guide defines how a Mentor decides, at each recurring decision point, which approach fits their specific pairing.

### Program Documents

These four documents define the Mentoring Program itself: the concept, the goals, the phase-by-phase structure, and the setup process. They are specialization-agnostic and apply to any discipline running the program, not only software engineering.

* [Mentoring Program Introduction](MentoringFramework/Introduction.md) — the case for a structured program over informal or purely reactive mentoring, and what the full guide set covers.
* [Mentoring Program Concept](MentoringFramework/Concept.md) — goals, defined roles (Mentor, Mentee, Managers, HR), and the core strategies (pairing, curriculum creation, collaboration platform, mentor support, recognition).
* [Mentoring Program Structure](MentoringFramework/Structure.md) — the full phase-by-phase process: Phase 0 (Prepare), Phase 1 (Goal Setup), Phase 2 (Planning), Phase 3 (Module Iteration), Phase 4 (Evaluation), including the meetings, artifacts, and results expected at each phase.
* [Mentoring Program (slide overview)](MentoringProgram.pptx) — a condensed visual summary of the above, suitable for company-wide introduction and announcement.

### Mentor Guide

The Mentor Guide is the practical toolkit referenced throughout the Program's phases. Each document addresses one recurring decision a Mentor has to make, offering a menu of mechanisms rather than a single required method. Read the Overview first; the remaining toolkits can be read in any order, as the need arises during an actual mentoring relationship.

0. [Overview and How to Use This Guide](MentorGuide/Overview.md) — the shared vocabulary (iteration grain, signal language, the one hard rule) that every other toolkit assumes.
1. [Diagnostic Toolkit](MentorGuide/1-Diagnose.md) — finding and evaluating gaps, at the baseline, module, and season grain.
2. [Training Approach Toolkit](MentorGuide/2-TrainingApproach.md) — choosing between planned and reactive curriculum design.
3. [Responsibility Transfer Toolkit](MentorGuide/3-ResponsibilityTransfer.md) — deliberately fading support as competence grows, including AI-specific guidance.
4. [Document Templates and Content Guide](MentorGuide/4-Documents.md) — what belongs in each artifact named by the program and why each needs to exist as a written record.
5. [Mentoring Psychology Patterns](MentorGuide/5-Psychology.md) — a shared reference of recurring mentee patterns.
6. [Mentor Growth Toolkit](MentorGuide/6-MentorGrowth.md) — what a Mentor should watch for in their own development, including what to do when a Mentor shares the Mentee's gap.
7. [Balancing Teaching and Project Priorities](MentorGuide/7-TeachingInProduction.md) — deciding which tasks belong to mentoring versus dedicated exercises, and dividing time when the two compete.
8. [When Something Isn't Working](MentorGuide/8-Escalation.md) — an evidence-gated escalation path for mentor-mentee friction that does not resolve on its own.

### Mentoring Framework Pilot

This folder tracks the 12-week mentoring pilot pairing Mentee Alex Chen with Mentor Marcus Webb during Project Vanguard's pre-release phase (anonymized). It provides a complete, evidence-based trail tracing technical skill development, mentor pedagogy, and organizational evaluation from initial baseline diagnostics through post-season HR review.

1. **Diagnosis & Scoping:** Identify core practice and judgment gaps through work archaeology and team feedback before building a sandbox curriculum.
   1. [Individual Goals and Baseline Document](PilotDocs/1-Goals.md) – Establishes initial baseline diagnostic evidence, gap classifications, and agreed closure definitions for both Mentee and Mentor. 
   2. [Mentoring Strategy Document](PilotDocs/2-Strategy.md) – Outlines the high-level mentoring approach, topic prioritization between practice and judgment gaps, and anticipated delivery constraints. 
   3. [Curriculum Record](PilotDocs/3-Curriculum.md) – Scopes the 12-week progression across Modules 1 through 3, specifying deferred topics and shared library promotion criteria. 
2. **Execution & Checkpoints:** Execute planned exercises, capture unprompted evidence, and file independent feedback drafts prior to joint reconciliation sessions.
   1. [Module Plans](PilotDocs/4-Modules.md) – Details specific learning objectives, exercise requirements, meeting cadences, and module-level Definitions of Done. 
   2. [Module Outcome Records](PilotDocs/5-Records.md) – Tracks per-module progress using independent mentor and mentee feedback drafts reconciled with HR oversight. 
3. **Synthesis & Evaluation:** Reclassify unresolved gaps based on trajectory data, evaluate team impact, and assess framework viability for scaling.
   1. [Season Summary](PilotDocs/6-Summary.md) – Synthesizes the full-season trajectory, highlighting closed practice mechanics versus open judgment gaps under milestone pressure. 
   2. [Manager Comparison Record](PilotDocs/7-Assessment.md) – Documents the engineering manager's formal review of pull request improvements and ongoing development plan adjustments. 
   3. [HR Program Review](PilotDocs/Result.md) – Evaluates the organizational effectiveness of the mentoring framework pilot and recommends company-wide adoption.
