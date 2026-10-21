# Compatibility Is a Guardrail for the Next Engineer

For a stretch of time, a game team's builds kept stopping for reasons that had little to do with what that team had changed. Code in the shared core repository would move (an interface that changed, a branch that advanced), and whoever imported it found out when their build failed. We worked in Perforce, where teams consume each other's code through stream imports, so a change in one depot could reach another team's workspace with no action from that team. It happened often enough to be a pattern, and in the cases I saw, the cause was a change that had been reasonable on the side that made it.

The history explains why. Core code had started as a separate repository that game teams consumed by copying from it. Later a core team formed and began working in that repository directly, which quietly turned a shared folder into a boundary between two teams (the setup is covered in [Matching Effort to Evidence](MatchingEffortToEvidence.md)). The first things that team built, analytics and similar pieces, needed almost no coordination with the game side, so the old way of working cost very little, and it went largely unnoticed that it had stopped fitting the structure. The first large feature built in parallel with a game team was the first real test, and it exposed the gap quickly.

---

## The Blind Spot: A Boundary in Structure, Not in Process

Separate repositories were the right structure here. They made the boundary real, and they were what eventually forced the process to catch up with it. What had not moved was the working model, which was still either "copy from core when you need something" or "work as if everyone shares one repository". A change that is safe inside one team's repository is only safe for a second team if something decides how it arrives, and at that point nothing in our setup did.

The failure has two parts, and it helps to keep them apart:

* **The cause:** a change that is compatible for its author and incompatible for its consumer. This is the part people usually mean by backward compatibility.
* **The channel:** the route by which that change reaches the consumer. In our case it was imports that pointed at a moving working branch, and changelist locks that pinned a version in a way downstream streams could not override, so the pin itself became a source of blocked builds. The same channel exists in Git as a submodule or dependency that tracks a branch instead of a commit.

Two instincts follow from this, and neither tends to hold up as the number of contributors grows:

* **The Discipline Approach:** write down the rule ("don't import the working branch", "review before you merge") and trust people to follow it. This works as long as you are the one who set the rule and the only one contributing, because then the rule and the habit live in the same head. As soon as a second contributor enters, let alone a second team, the rule depends on people who did not write it remembering it consistently, and the cost of one lapse tends to fall on someone else.
* **The Copy Approach:** share by copying the source, which removes the live link entirely. Copying is a sound default for the first one or two uses, since it avoids taking on a dependency before the demand is proven. By the third copy the demand is usually proven, and the repetition itself is the signal that it should become a link. Past that point, copying by hand tends to multiply the work with each team and each update, with drift as the price.

It is worth being honest about why so little had broken before. The earlier work had not put real load on the boundary, so **the absence of incidents mostly reflected the absence of the condition, not the safety of the process**. The same conditions were likely to return with the next large parallel feature, and the same failure with them.

---

## The Fix: Make the Right Path the Easy One

What stopped the blocking, as far as I can tell, was not one technique but three mechanisms, each of which changed what the easiest action was for the team on the other side of the boundary.

### 1. Pin to a Released Branch

The plugin team imported a branch cut specifically for them, rather than the working branch or a locked changelist. This did two things at once. The version in use became visible, since a named branch is something you can point at, and upstream work stopped landing in their build unless someone decided that it should. Cutting the branch required coordination between the teams, which was part of the point: creating a release branch is a natural moment for both sides to talk.

### 2. Lock a Narrow Interface

A smaller surface tends to mean fewer accidental dependencies. A locked signature is not the whole contract, though. By [Hyrum's Law](https://www.hyrumslaw.com/), once enough people use an interface, even its unintended observable behaviors tend to be depended on by somebody, whatever the documentation promises. Locking the interface therefore needs tests behind it, so that "what we promised" and "what consumers actually rely on" stay close together.

In an engine, the interface often includes serialized data. Renaming a property or a class can drop the values already saved in consumers' assets, so a change that the compiler accepts can still cost someone their work, which often makes game engine compatibility harder than it is for a typical service API (the core redirects item below covers the mapping).

### 3. Deprecate Before You Remove

The old call keeps working while a warning names its replacement (in Unreal, the deprecation macro carries both a version and a message). Consumers migrate on their own schedule instead of on the schedule of whoever changed the interface, and the removal date becomes an agreement and not a surprise. Once the agreed milestone arrives, the warning can be promoted to an error (for example by building with warnings treated as errors), so the removal date is enforced by the compiler and not only remembered by people.

Builds stopped blocking. I never had numbers to put on that, and I would rather leave the claim at what it is than reconstruct a figure after the fact.

### What I Recommended and Wasn't Built

The channel itself still needed closing, and I proposed a way to do it: imports set to read-only so that edits cannot land in a depot you do not own, changes to what a stream imports made through one reviewed file and applied by an automated script on submit and in CI, and no changelist locks, with older release branches used instead. Enforcing this needed server-side ownership beyond my own team, and it stayed a proposal.

Branching and deprecation turned out to be enough to stop the blocking, and that matters for how I would weigh the recommendation. The cause of the original failures was incompatible changes, and the trigger would not have prevented those on its own. What it addresses is the route they travel, which remains open: as far as I know, nothing today prevents someone from importing a working branch again. I cannot show that it would have prevented the next incident, only that it removes a way for the same failure to happen, and I would revisit it first.

### Ranking the Mechanisms

The mechanisms differ in how much they depend on anyone remembering, and ranking them by that is more useful than treating them as a flat list:

1. **Remove the channel.** Consume a built artifact or an automated, pinned snapshot instead of live source, so that wrong path is no longer available.
2. **Make it hard.** Read-only imports, a narrow interface, and changes made through one reviewed file. The wrong path still exists, but it costs effort and an explicit decision.
3. **Make it traceable.** A periodic report of imports that point at working branches, changelist locks, and remaining uses of deprecated calls. This prevents little by itself, but the wrong path leaves a record. This rung usually needs no one else's sign-off, and its numbers make the case for the rungs above it, which is the same logic as the lesson in [The Engineer-Process Boundary](EngineerProcessBoundary.md) about proving a problem before asking for funding.
4. **Warn.** Deprecation messages, which point the next engineer toward the replacement at the moment they need it.
5. **Document.** A written rule, which tends to ask the most of the reader and protect the least.

### What I Would Add Next

None of the following was built, and I am keeping it separate from what was.

* **A consumer build in CI:** before a change is promoted, build the known consumers against it. This is the idea behind what Google calls the Beyoncé Rule: if you depend on a behavior, you should have a test on it, and the test only counts if the shared CI actually runs it.
* **Expand and contract with a removal trigger:** add the new path, keep the old one, migrate consumers, then remove it. The last step needs a count of remaining uses per consumer, or the old path tends to become permanent.
* **Flags as consumer opt-in:** a breaking behavior change ships switched off, and each consumer turns it on when ready. The flag needs an expiry like the other mechanisms here (the lifecycle is covered in [Data-Driven Design Is an Architecture Boundary](DataDrivenDesign.md)).
* **Core redirects:** if the interface exposes `UObject` types, a rename can break the consumer's assets and not only their compile. Unreal's core redirects map old names to new ones on load.

If I had instrumented this from the start, the numbers I would want are broken builds attributable to cross-team imports per month, time to restore a blocked build, the count of imports pointing at a working branch, the count of changelist locks, and remaining uses of deprecated calls per consumer.

---

## The Insight: Compatibility Is How You Design the Next Engineer's Path

Compatibility is usually taught as a property of code: do not break the signature, version the format, keep the old field readable. The mechanisms above are also something else, a decision about which path is the easy one for whoever works next. A released branch, a narrow interface, and a deprecation warning do not ask the next engineer to understand the history of the boundary. They arrange things so that following the intended path is usually the cheapest one.

The idea is not new. Rico Mariani called it the [pit of success](https://blogs.msdn.microsoft.com/brada/2006/05/08/a-reminder-as-we-start-detailed-design-and-implementation/): design the platform so that people fall into good practice instead of climbing toward it. Safety engineering has a close equivalent in its hierarchy of controls, which ranks protections by how little they rely on human behavior, from removing the hazard, through guards and interlocks, down to procedures and training at the bottom. Don Norman's forcing functions describe the same spectrum for physical objects, along with a caution that applies here too: a constraint has a cost for normal behavior, so it has to distinguish legitimate violations from illegitimate ones. A guardrail therefore needs an escape hatch with an audit trail, a deliberate way through that records who used it and why, because one with no way through tends to get bypassed or disabled. That is why the "make it hard" rung is a better target than "make it impossible". I would also argue that "impossible" is really a price, and that everything between a convention and a physical constraint is a question of how expensive the bypass is and how cheap the shortcut is.

Two further points follow. First, **compatibility mechanisms tend to create a period in which old and new coexist**: a pinned branch next to head, a deprecated call next to its replacement, a flag next to the code it guards. Each of those periods needs an owner and an expiry date, or the shim tends to become the permanent interface. Second, the exposure here was less about the code itself than about a boundary that existed in the repository layout and not in the way people worked, and the first change that needed coordination found it.

---

## The Production Bottom Line

> **A Boundary in Structure Needs a Boundary in Process:** Separate repositories created a real boundary, but the working model stayed where it was, and the first large parallel feature exposed the gap. Documentation tells the next engineer what to do, while a guardrail decides what is easy to do, so close the channel a change travels through and not only the change that broke something.
>
> Match the guardrail to the risk. A pinned branch, a narrow interface, and a deprecation window were enough to stop the blocking, but none of them on its own prevents the next import of a working branch. Measure how often the shortcut is taken, and add the next rung when that number justifies it.