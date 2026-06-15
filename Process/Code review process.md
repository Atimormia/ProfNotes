---
title: "[]{#_lg2lkfy03ats .anchor}Code Review Process"
---

# Current Process

When code is ready for review, the following steps are taken:

1.  **Creating a Review:** The author creates a review in Swarm and posts a Code Review (CR) request in the designated [**[Slack channel]{.underline}**](https://offworldindustries.slack.com/archives/C8TAMPHDK). The request includes:

    a.  A link to the JIRA ticket.

    b.  A link to the Swarm review.

    c.  A reviewer (optional).

    d.  Urgency Level:

        i.  **Low**: No rush, can be reviewed at convenience.

        ii. **Medium**: Should be reviewed within the current sprint.

        iii. **High**: Requires prompt attention to avoid delays.

        iv. **Critical**: Must be addressed immediately to unblock key tasks or fixes.

    e.  Comment - overview on what has been done and High/Critical urgency explaining

2.  **Assigning Reviewers**

    a.  The author can assign a reviewer, typically someone familiar with the codebase.

    b.  If no reviewer is assigned, the review is picked up by a team member who is available for code review.

3.  **Review Process:** The reviewer reviews the code in Swarm and either:

    a.  **Approves**: Indicates the code is ready for merge. Press the \"This Slaps\" button in the CR request post on Slack to inform the team that the review has been completed and approved. Optionally, comment in the Slack thread with "Approved".

    b.  **Leaves Comments**: Provides feedback that the author must address. Notify the author in Slack channel with a summary of what needs to be addressed.

4.  **Addressing Feedback**

    a.  The author updates the code to address comments and notifies the reviewer in Slack.

    b.  The reviewer verifies that the changes meet expectations.

        i.  If satisfied, they approve the review.

        ii. If additional changes are needed, the reviewer provides more comments and updates Slack.

5.  **Approve vs. Upvote**

    a.  **Approve**: formal approval for merging. Used by **assigned reviewers** or when feedback has been addressed, and the code is ready for merging.

    b.  **Upvote**: indicating the review looks good but not necessarily ready for merge. Used for **unassigned reviews** to express agreement with the changes or as acknowledgment before a formal review.

## Clarification: Code Review Urgency Levels

To prioritize code reviews effectively, use the following urgency levels when submitting requests in the Slack channel:

#### **Low**

a.  **Definition**: Optional priority. Can be reviewed at the reviewer's convenience without impacting the project timeline.

b.  **When to Use**:

    i.  Experimental work or prototypes.

    ii. Side projects.

    iii. Optional improvements or \"nice-to-have\" changes.

c.  **Example**: *\"Added a small utility script for internal use - review when you have time.\"*

#### **Medium (Normal) -** for requests that don't clearly fall into \"High\" or \"Urgent.\" {#medium-normal---for-requests-that-dont-clearly-fall-into-high-or-urgent.}

a.  **Definition**: Standard priority. Can be reviewed during regular code review cycles.

b.  **When to Use**:

    i.  Refactoring or optimization tasks.

    ii. Improvements or bug fixes.

    iii. Features that are not blocking other tasks or nearing deadlines.

c.  **Example**: *\"Refactored the logging system for better readability and maintainability.\"*

#### **High**

a.  **Definition**: Needs attention soon. Delays may block other tasks or impact progress within the sprint.

b.  **When to Use**:

    i.  Key features nearing sprint deadlines.

    ii. Integration tasks that unblock other team members.

    iii. Issues causing significant but non-critical disruption.

c.  **Example**: *\"Feature X must be reviewed today to stay on track for this sprint\'s goals.\"*

#### **Critical (Urgent) -** reserve this for the most critical cases to maintain credibility

a.  **Definition**: Immediate attention required. Critical for production, live issues, or hard deadlines.

b.  **When to Use**:

    i.  Hotfixes for live environments.

    ii. Security vulnerabilities.

    iii. Critical blockers for imminent release.

c.  **Example**: *\"Urgent: Fixes a crash on live servers impacting all users.\"*

When urgency level already indicates how fast it should be reviewed, in general, it's expected that any submitting request should be reacted **the same day** it is requested or **the next day** at the latest.

# Code Review Workflow

## Clarification: Guidelines for Reviewers

- **Be Explicit**

  - Be clear about expectations. You may mark your comments with their priority level that is explained below (e.g., \[Blocker\], \[Required\], \[Suggested\], \[Future Note\]).

  - This helps the author prioritize and understand the severity of issues.

- **Provide Context**

  - Explain why the issue matters.

  - **Example**: *\"This could lead to a crash under heavy load due to unbounded memory allocation.\"*

  - Context improves understanding and facilitates meaningful fixes.

- **Use Examples**

  - When applicable, provide suggestions or examples of how to address the issue.

  - **Example**: *\"Consider using a TMap here for better lookup performance.\"*

- **Encourage Discussion**

  - For subjective comments (e.g., design preferences or alternative approaches), invite input from the author to foster collaboration.

  - **Example**: *\"Would using dependency injection here better align with our architecture?\"*

- **Address Potential Conflicts**

  - If conflicts or disagreements arise, involve an additional reviewer and tag a tech lead for resolution.

  - Ensure discussions remain respectful and focused on the technical issue at hand.

- **Acknowledge**

  - If you don\'t have specific feedback to offer, make sure to leave a confirmation comment like *\"Looks good to me!\" (LGTM).*

- **Celebrate Progress**

  - Even if you have no issues to raise, **constructive positive feedback** is always encouraged. It can go a long way in reinforcing good practices and motivating your peers. Examples of constructive positive feedback could include:

    - *\"Efficient implementation! Using a hashmap here significantly improves lookup performance.\"*

    - *\"Smart use of caching here - this will help reduce unnecessary calculations.\"*

    - *\"Good job handling edge cases - this will make the code more robust.\"*

    - *\"Great readability and use of the X approach - this improves maintainability.\"*

  - Providing positive feedback, even if brief, helps reinforce quality standards, motivates the team, and nurtures a culture of continuous improvement.

## Commenting and Addressing

### Proposal: Categories of Comments \[[[Paulina Freidlin]{.underline}](mailto:paulina.freidlin@offworldindustries.com)\]

Grading code review comments helps set clear expectations for the developer receiving the feedback and ensures focus on the most critical issues.

1.  **Critical (Must Fix)**

    a.  **Definition**: Issues that could break the code, cause crashes, security vulnerabilities, or major functionality failures.

    b.  **Examples**:

        i.  Incorrect logic that leads to incorrect results.

        ii. Memory leaks or performance-critical issues.

        iii. Security vulnerabilities like improper input validation.

        iv. Breaking API contracts or incorrect synchronization in multithreaded code.

2.  **Important (Should Fix)**

    a.  **Definition**: Problems that don\'t break the code but can significantly affect maintainability, scalability, or consistency.

    b.  **Examples**:

        i.  Code that is difficult to read or understand due to poor structure.

        ii. Violations of coding standards or best practices.

        iii. Inefficient algorithms or unnecessary complexity.

3.  **Nice to Have (Optional)**

    a.  **Definition**: Improvements that enhance the code but aren\'t strictly necessary.

    b.  **Examples**:

        i.  Suggestions for alternative approaches that may improve clarity or elegance.

        ii. Slight optimizations that aren\'t critical for performance.

        iii. Improvements to comments or naming conventions for better readability.

4.  **Future Recommendations**

    a.  **Definition**: Insights or ideas for improving related areas in the future, but outside the scope of the current task.

    b.  **Examples**:

        i.  Highlighting potential areas of refactoring.

        ii. Suggestions for new abstractions or patterns for upcoming features.

        iii. Observations about technical debt.

5.  **Discussion**

    a.  **Definition**: Comments for clarifications, questions, or exploring alternate approaches without assuming action is required.

### Proposal: Addressing Comments with Tasks \[[[Bronson Bouchard]{.underline}](mailto:bronson.bouchard@offworldindustries.com)\]

- **Marking Comments as [[Tasks]{.underline}](https://help.perforce.com/helix-core/helix-swarm/swarm/current/Content/Swarm/basics.comments.html#basics.comments.tasks)**:

  - **Blocker and Required Comments**: All Blocker and Required comments should be marked as tasks in Swarm. These tasks help track necessary revisions that must be made before the review can be approved.

  - **Suggested Comments**: If the author chooses to act on a Suggested comment, they should mark it as a task. This ensures that even non-mandatory changes are tracked and can be verified by the original commenter.

- **Addressing Tasks**: When a revision is made to address a task, the review author should mark the task as **Addressed** in Swarm. This signals to the reviewer that the required change has been completed and is ready for verification.

- **Verifying Tasks**: The reviewer should then mark the task as **Verified** if the fix meets expectations. This step confirms that the revision is satisfactory and closes the loop on that particular task.

- **Avoiding Overuse of \"Mark Addressed\"**: Authors should only mark a task as addressed when the corresponding revision has been posted.

### Comments Grades

Assign levels or labels to make the priorities clear:

| **Level** | **Label** | **Action** | **Marked as a task by** |
|----|----|----|----|
| 1 | 🛑Blocker | Must be fixed. Blocks merging due to critical issues like crashes, breaking functionality, or security vulnerabilities. | Reviewer |
| 2 | ⚠️Required | Should be fixed. If not fixed before merging due to deadlines, a tech debt task must be created and assigned for resolution. | Reviewer |
| 3 | 💡Suggested | Nice to have. Fix if possible, but not mandatory. | Author |
| 4 | 📌Future Note | For awareness. These are observations about potential risks or opportunities to improve code in future iterations, but no immediate action is needed. | No task |
| \- | No label needed (Discussion) | For clarifications, questions, or exploring alternate approaches. | No task |

## Proposal: Reviewer Assignment \[[[Paulina Freidlin]{.underline}](mailto:paulina.freidlin@offworldindustries.com)\]

To improve the quality of code reviews, foster team collaboration, and ensure timely feedback, the following guidelines are proposed:

1.  **Assign reviewer for High and Critical CRs**

    a.  To guarantee that critical tasks don't get delayed, reducing risks to the project timeline and overall stability a designated reviewer **must** be assigned to ensure immediate attention to pressing issues

2.  **Assign additional reviewer for Normal CRs**

    a.  Sharing knowledge helps avoid bottlenecks by reducing reliance on specific individuals. Reviewing unfamiliar code exposes developers to new patterns and best practices, improving personal skill sets.

    b.  Assign two reviewers:

        i.  **One with Expertise**: Ensures the review process includes someone who deeply understands the context, minimizing oversights.

        ii. **One Random Reviewer**: Encourages cross-functional knowledge sharing, team-wide awareness, and even distribution of review responsibilities.

3.  **Avoid unassigned CRs**

    a.  Assigning reviewers helps prevent delays, maintain momentum, and avoid overlooked tasks in the review queue.

    b.  To ensure CR requests don't linger unresolved, **authors are encouraged to assign reviewers directly** whenever possible.

    c.  Unassigned reviews can be picked up by any available reviewer, but be aware that it requires a more proactive position from team members.

        i.  A **Slack reviewer randomizer tool** can be introduced to automatically select available team members. In this case reviewer availability can be based on deadlined Slack statuses \[[[Patrick Fischer]{.underline}](mailto:patrick.fischer@offworldindustries.com)\]

        ii. Another option is to run locally a simple **Dice script** to help authors to pick a random reviewer \[[[Paulina Freidlin]{.underline}](mailto:paulina.freidlin@offworldindustries.com)\]

## Proposal: Review Participation

- **Minimum Participation**

  - Regular participation ensures workloads are balanced across the team, reduces review bottlenecks, and creates a shared sense of responsibility. Each developer is encouraged to participate in at least **two code reviews per week**.

- **Encourage Involvement**

  - Reviewing code from different domains helps developers broaden their understanding of the project, improving problem-solving and collaboration. Exposure to diverse approaches and ideas contributes to individual growth and a stronger team dynamic.

  - Team members are encouraged to **volunteer for reviews outside their domain**.

# Proposal: Code Review Gamification \[[[Brad Fix]{.underline}](mailto:brad.fix@offworldindustries.com)\]

To enhance engagement and participation in the code review process while balancing workloads, we may use a **Code Review Gamification** system. This system will incentivize active participation and recognize valuable contributions through **statistics collection** and **awards**. By promoting friendly competition and highlighting contributions, we aim to foster a collaborative environment, encourage knowledge sharing, and improve the overall code quality.

## Key Metrics to Track and Recognize

These can include:

- **Most Active Reviewer**: Awarded to the reviewer who contributes the most tagged comments (particularly important comments like \[Blocker\], \[Required\], and \[Suggested\] comments). This encourages thoughtful participation and use of comment tags.

- **Most Popular Reviewer**: Given to the reviewer who is most frequently assigned to code reviews, helping to acknowledge those who are often called upon for their expertise. This metric highlights team members who are consistently trusted with reviews, but it also draws attention to potential **bus factors** (if too few people are regularly assigned), which could indicate an imbalanced workload or the need for more reviewers to get involved.

- **Code Detective**: Recognizing reviewers who provide detailed \[Blocker\] comments and task resolutions to ensure critical issues are addressed.

- **Milestones**:

  - N amount of code review approved

## Identifying and Addressing Inactivity

To ensure that all team members participate in the code review process and that workloads are balanced, we will monitor activity patterns:

- **Ignored by Team**: Team members who are not being assigned to reviews by others may be flagged. This might indicate they are not recognized as available or knowledgeable enough in certain areas.

- **Not Active**: Reviewers who both are not being assigned reviews and do not pick up unassigned reviews will also be flagged as not active.

These statistics are **NOT meant to measure individual programmer performance**. Instead, they are meant to provide **insights for the tech lead** to identify patterns in team collaboration. The goal is to improve engagement, balance workloads, and foster knowledge sharing - not to penalize individuals. If concerning trends emerge, the tech lead may take steps such as adjusting assignments, mentoring less-involved members, or encouraging more cross-functional review participation.\[[[Brendan Miller-Young]{.underline}](mailto:brendan.milleryoung@offworldindustries.com)\]

## Balancing Quality and Quantity

While participation is encouraged, we must ensure that the quality of reviews remains a priority. To prevent the focus from shifting purely to the number of reviews completed, the following will be emphasized:

### Meaningful Contributions Over Quantity

Rewards and recognition will be based on the impact and quality of reviews rather than just the number of reviews completed. Reviewers can be acknowledged for:

- Resolving \[Blocker\] comments and helping maintain code stability.

- Providing valuable insights that contribute to maintainability, performance, or readability.

- Suggesting improvements that align with coding best practices.

### Approving Without Comments

Reviews that are approved without any comments will be tracked and highlighted as an area for improvement. This ensures that reviews remain intentional and engaged, while also providing positive reinforcement to authors.

## Rewarding and Team Recognition

Acknowledging contributions in a positive way is vital for building a strong team culture:

- **Team Meetings and Newsletters**: Active contributors will be recognized in team meetings (e.g., Bi-Weekly Team Update) and/or Slack channels. This provides recognition for their efforts, promoting team cohesion and motivating others to participate.

- **Public Shout-Outs**: Special mention during company-wide Townhalls can be used to celebrate contributors who consistently go above and beyond.

- **Rewards**: Virtual and/or physical badges (gift cards, bank days) can be awarded based on various milestones.
