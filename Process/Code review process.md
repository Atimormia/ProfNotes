---
title: "Code Review Process"
---

# Current Process

When code is ready for review, the following steps are taken:

1. **Creating a Review:** The author creates a review in Swarm and posts a Code Review (CR) request in the designated [**Slack channel**](https://offworldindustries.slack.com/archives/C8TAMPHDK). The request includes:

   1. A link to the JIRA ticket.
   2. A link to the Swarm review.
   3. A reviewer (optional).
   4. Urgency Level:

      1. **Low**: No rush, can be reviewed at convenience.
      2. **Medium**: Should be reviewed within the current sprint.
      3. **High**: Requires prompt attention to avoid delays.
      4. **Critical**: Must be addressed immediately to unblock key tasks or fixes.

   5. Comment: overview of what has been done and explanation for High/Critical urgency.

2. **Assigning Reviewers**

   1. The author can assign a reviewer, typically someone familiar with the codebase.
   2. If no reviewer is assigned, the review is picked up by a team member who is available for code review.

3. **Review Process:** The reviewer reviews the code in Swarm and either:

   1. **Approves**: Indicates the code is ready for merge. Press the "This Slaps" button in the CR request post on Slack to inform the team that the review has been completed and approved. Optionally, comment in the Slack thread with "Approved".
   2. **Leaves Comments**: Provides feedback that the author must address. Notify the author in Slack with a summary of what needs to be addressed.

4. **Addressing Feedback**

   1. The author updates the code to address comments and notifies the reviewer in Slack.
   2. The reviewer verifies that the changes meet expectations.

      1. If satisfied, they approve the review.
      2. If additional changes are needed, the reviewer provides more comments and updates Slack.

5. **Approve vs. Upvote**

   1. **Approve**: Formal approval for merging. Used by **assigned reviewers** or when feedback has been addressed, and the code is ready for merging.
   2. **Upvote**: Indicates the review looks good but is not necessarily ready for merge. Used for **unassigned reviews** to express agreement with the changes or as acknowledgment before a formal review.

## Clarification: Code Review Urgency Levels

To prioritize code reviews effectively, use the following urgency levels when submitting requests in the Slack channel:

#### **Low**

1. **Definition**: Optional priority. Can be reviewed at the reviewer's convenience without impacting the project timeline.
2. **When to Use**:

   1. Experimental work or prototypes.
   2. Side projects.
   3. Optional improvements or "nice-to-have" changes.

3. **Example**: *"Added a small utility script for internal use - review when you have time."*

#### **Medium (Normal)**

For requests that don't clearly fall into "High" or "Urgent."

1. **Definition**: Standard priority. Can be reviewed during regular code review cycles.
2. **When to Use**:

   1. Refactoring or optimization tasks.
   2. Improvements or bug fixes.
   3. Features that are not blocking other tasks or nearing deadlines.

3. **Example**: *"Refactored the logging system for better readability and maintainability."*

#### **High**

1. **Definition**: Needs attention soon. Delays may block other tasks or impact progress within the sprint.
2. **When to Use**:

   1. Key features nearing sprint deadlines.
   2. Integration tasks that unblock other team members.
   3. Issues causing significant but non-critical disruption.

3. **Example**: *"Feature X must be reviewed today to stay on track for this sprint's goals."*

#### **Critical (Urgent)**

Reserve this for the most critical cases to maintain credibility.

1. **Definition**: Immediate attention required. Critical for production, live issues, or hard deadlines.
2. **When to Use**:

   1. Hotfixes for live environments.
   2. Security vulnerabilities.
   3. Critical blockers for imminent release.

3. **Example**: *"Urgent: Fixes a crash on live servers impacting all users."*

When urgency level already indicates how fast it should be reviewed, in general, it's expected that any submitting request should be reacted to **the same day** it is requested or **the next day** at the latest.

# Code Review Workflow

## Clarification: Guidelines for Reviewers

- **Be Explicit**

  - Be clear about expectations. You may mark your comments with their priority level that is explained below, for example: `[Blocker]`, `[Required]`, `[Suggested]`, `[Future Note]`.
  - This helps the author prioritize and understand the severity of issues.

- **Provide Context**

  - Explain why the issue matters.
  - **Example**: *"This could lead to a crash under heavy load due to unbounded memory allocation."*
  - Context improves understanding and facilitates meaningful fixes.

- **Use Examples**

  - When applicable, provide suggestions or examples of how to address the issue.
  - **Example**: *"Consider using a TMap here for better lookup performance."*

- **Encourage Discussion**

  - For subjective comments, such as design preferences or alternative approaches, invite input from the author to foster collaboration.
  - **Example**: *"Would using dependency injection here better align with our architecture?"*

- **Address Potential Conflicts**

  - If conflicts or disagreements arise, involve an additional reviewer and tag a tech lead for resolution.
  - Ensure discussions remain respectful and focused on the technical issue at hand.

- **Acknowledge**

  - If you don't have specific feedback to offer, make sure to leave a confirmation comment like *"Looks good to me!" (LGTM).*

- **Celebrate Progress**

  - Even if you have no issues to raise, **constructive positive feedback** is always encouraged. It can go a long way in reinforcing good practices and motivating your peers. Examples of constructive positive feedback could include:

    - *"Efficient implementation! Using a hashmap here significantly improves lookup performance."*
    - *"Smart use of caching here - this will help reduce unnecessary calculations."*
    - *"Good job handling edge cases - this will make the code more robust."*
    - *"Great readability and use of the X approach - this improves maintainability."*

  - Providing positive feedback, even if brief, helps reinforce quality standards, motivates the team, and nurtures a culture of continuous improvement.

## Commenting and Addressing

### Proposal: Categories of Comments [Author 1]

Grading code review comments helps set clear expectations for the developer receiving the feedback and ensures focus on the most critical issues.

1. **Critical (Must Fix)**

   1. **Definition**: Issues that could break the code, cause crashes, security vulnerabilities, or major functionality failures.
   2. **Examples**:

      1. Incorrect logic that leads to incorrect results.
      2. Memory leaks or performance-critical issues.
      3. Security vulnerabilities like improper input validation.
      4. Breaking API contracts or incorrect synchronization in multithreaded code.

2. **Important (Should Fix)**

   1. **Definition**: Problems that don't break the code but can significantly affect maintainability, scalability, or consistency.
   2. **Examples**:

      1. Code that is difficult to read or understand due to poor structure.
      2. Violations of coding standards or best practices.
      3. Inefficient algorithms or unnecessary complexity.

3. **Nice to Have (Optional)**

   1. **Definition**: Improvements that enhance the code but aren't strictly necessary.
   2. **Examples**:

      1. Suggestions for alternative approaches that may improve clarity or elegance.
      2. Slight optimizations that aren't critical for performance.
      3. Improvements to comments or naming conventions for better readability.

4. **Future Recommendations**

   1. **Definition**: Insights or ideas for improving related areas in the future, but outside the scope of the current task.
   2. **Examples**:

      1. Highlighting potential areas of refactoring.
      2. Suggestions for new abstractions or patterns for upcoming features.
      3. Observations about technical debt.

5. **Discussion**

   1. **Definition**: Comments for clarifications, questions, or exploring alternate approaches without assuming action is required.

### Proposal: Addressing Comments with Tasks [Author 2]

- **Marking Comments as [Tasks](https://help.perforce.com/helix-core/helix-swarm/swarm/current/Content/Swarm/basics.comments.html#basics.comments.tasks)**:

  - **Blocker and Required Comments**: All Blocker and Required comments should be marked as tasks in Swarm. These tasks help track necessary revisions that must be made before the review can be approved.
  - **Suggested Comments**: If the author chooses to act on a Suggested comment, they should mark it as a task. This ensures that even non-mandatory changes are tracked and can be verified by the original commenter.

- **Addressing Tasks**: When a revision is made to address a task, the review author should mark the task as **Addressed** in Swarm. This signals to the reviewer that the required change has been completed and is ready for verification.

- **Verifying Tasks**: The reviewer should then mark the task as **Verified** if the fix meets expectations. This step confirms that the revision is satisfactory and closes the loop on that particular task.

- **Avoiding Overuse of "Mark Addressed"**: Authors should only mark a task as addressed when the corresponding revision has been posted.

### Comments Grades

Assign levels or labels to make the priorities clear:

| **Level** | **Label** | **Action** | **Marked as a task by** |
|---|---|---|---|
| 1 | 🛑 Blocker | Must be fixed. Blocks merging due to critical issues like crashes, breaking functionality, or security vulnerabilities. | Reviewer |
| 2 | ⚠️ Required | Should be fixed. If not fixed before merging due to deadlines, a tech debt task must be created and assigned for resolution. | Reviewer |
| 3 | 💡 Suggested | Nice to have. Fix if possible, but not mandatory. | Author |
| 4 | 📌 Future Note | For awareness. These are observations about potential risks or opportunities to improve code in future iterations, but no immediate action is needed. | No task |
| - | No label needed (Discussion) | For clarifications, questions, or exploring alternate approaches. | No task |

## Proposal: Reviewer Assignment [Author 3]

To improve the quality of code reviews, foster team collaboration, and ensure timely feedback, the following guidelines are proposed:

1. **Assign reviewer for High and Critical CRs**

   1. To guarantee that critical tasks don't get delayed, reducing risks to the project timeline and overall stability, a designated reviewer **must** be assigned to ensure immediate attention to pressing issues.

2. **Assign additional reviewer for Normal CRs**

   1. Sharing knowledge helps avoid bottlenecks by reducing reliance on specific individuals. Reviewing unfamiliar code exposes developers to new patterns and best practices, improving personal skill sets.
   2. Assign two reviewers:

      1. **One with Expertise**: Ensures the review process includes someone who deeply understands the context, minimizing oversights.
      2. **One Random Reviewer**: Encourages cross-functional knowledge sharing, team-wide awareness, and even distribution of review responsibilities.

3. **Avoid unassigned CRs**

   1. Assigning reviewers helps prevent delays, maintain momentum, and avoid overlooked tasks in the review queue.
   2. To ensure CR requests don't linger unresolved, **authors are encouraged to assign reviewers directly** whenever possible.
   3. Unassigned reviews can be picked up by any available reviewer, but be aware that it requires a more proactive position from team members.

      1. A **Slack reviewer randomizer tool** can be introduced to automatically select available team members. In this case, reviewer availability can be based on deadlined Slack statuses. [Author 4]
      2. Another option is to run locally a simple **Dice script** to help authors pick a random reviewer. [Author 5]

## Proposal: Review Participation

- **Minimum Participation**

  - Regular participation ensures workloads are balanced across the team, reduces review bottlenecks, and creates a shared sense of responsibility. Each developer is encouraged to participate in at least **two code reviews per week**.

- **Encourage Involvement**

  - Reviewing code from different domains helps developers broaden their understanding of the project, improving problem-solving and collaboration. Exposure to diverse approaches and ideas contributes to individual growth and a stronger team dynamic.
  - Team members are encouraged to **volunteer for reviews outside their domain**.

# Proposal: Code Review Gamification [Author 6]

To enhance engagement and participation in the code review process while balancing workloads, we may use a **Code Review Gamification** system. This system will incentivize active participation and recognize valuable contributions through **statistics collection** and **awards**. By promoting friendly competition and highlighting contributions, we aim to foster a collaborative environment, encourage knowledge sharing, and improve the overall code quality.

## Key Metrics to Track and Recognize

These can include:

- **Most Active Reviewer**: Awarded to the reviewer who contributes the most tagged comments, particularly important comments like `[Blocker]`, `[Required]`, and `[Suggested]`. This encourages thoughtful participation and use of comment tags.

- **Most Popular Reviewer**: Given to the reviewer who is most frequently assigned to code reviews, helping to acknowledge those who are often called upon for their expertise. This metric highlights team members who are consistently trusted with reviews, but it also draws attention to potential **bus factors**. If too few people are regularly assigned, this could indicate an imbalanced workload or the need for more reviewers to get involved.

- **Code Detective**: Recognizing reviewers who provide detailed `[Blocker]` comments and task resolutions to ensure critical issues are addressed.

- **Milestones**:

  - N amount of code review approved.

## Identifying and Addressing Inactivity

To ensure that all team members participate in the code review process and that workloads are balanced, we will monitor activity patterns:

- **Ignored by Team**: Team members who are not being assigned to reviews by others may be flagged. This might indicate they are not recognized as available or knowledgeable enough in certain areas.

- **Not Active**: Reviewers who both are not being assigned reviews and do not pick up unassigned reviews will also be flagged as not active.

These statistics are **NOT meant to measure individual programmer performance**. Instead, they are meant to provide **insights for the tech lead** to identify patterns in team collaboration. The goal is to improve engagement, balance workloads, and foster knowledge sharing - not to penalize individuals. If concerning trends emerge, the tech lead may take steps such as adjusting assignments, mentoring less-involved members, or encouraging more cross-functional review participation. [Author 7]

## Balancing Quality and Quantity

While participation is encouraged, we must ensure that the quality of reviews remains a priority. To prevent the focus from shifting purely to the number of reviews completed, the following will be emphasized:

### Meaningful Contributions Over Quantity

Rewards and recognition will be based on the impact and quality of reviews rather than just the number of reviews completed. Reviewers can be acknowledged for:

- Resolving `[Blocker]` comments and helping maintain code stability.
- Providing valuable insights that contribute to maintainability, performance, or readability.
- Suggesting improvements that align with coding best practices.

### Approving Without Comments

Reviews that are approved without any comments will be tracked and highlighted as an area for improvement. This ensures that reviews remain intentional and engaged, while also providing positive reinforcement to authors.

## Rewarding and Team Recognition

Acknowledging contributions in a positive way is vital for building a strong team culture:

- **Team Meetings and Newsletters**: Active contributors will be recognized in team meetings, such as Bi-Weekly Team Update, and/or Slack channels. This provides recognition for their efforts, promoting team cohesion and motivating others to participate.

- **Public Shout-Outs**: Special mention during company-wide Townhalls can be used to celebrate contributors who consistently go above and beyond.

- **Rewards**: Virtual and/or physical badges, gift cards, or bank days can be awarded based on various milestones.
