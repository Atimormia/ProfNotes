# Matching Effort to Evidence

A newly formed core team owed us a plugin: a wrapper around a third-party library, handed to the game side so we could build a UI on top of it. Before I was even staffed on the feature, the plugin I inherited was already copying the entire backend interface, every field, every method, just in case. Nobody had decided what the game side actually needed. The interface conversation between the two teams had stalled, so someone filled the silence the only way available to them: mirror everything, and figure out the real shape later.

That instinct wasn't wrong. Iterating against a fast, disposable copy to discover real requirements is a legitimate way to get unstuck when nobody above you has drawn the boundary yet. The problem showed up later, when "figure out the real shape later" never happened. Nobody ever declared the mirror finished and the real contract designed. It kept growing, absorbing whatever the game side needed next, one addition at a time, until the plugin was less an interface and more a second copy of the backend wearing a different name.

---

## The Blind Spot: A Team With a Purpose and No Mechanism

The core team's reason to exist was never really in question: centralize solutions that more than one game needed, instead of every team reinventing them separately. What was missing was the mechanism. Nobody had decided whether generalization was supposed to flow upward, a game builds something, a second use case appears, core adopts and generalizes it, or downward, core designs something game-agnostic from the start and hands it down finished. There was no manager attached to the team either, just a couple of senior engineers carrying an informal mandate to work on agnostic solutions. A team can have an obvious purpose and still have no charter, if nobody ever decided how it was supposed to do its job.

Two things filled that gap instead, and neither showed up as a crisis, which is exactly what let it run so long. On the core side, the engineer building the plugin was guessing at the interface: mirroring whatever piece of the backend looked like it would be needed, without a design conversation to base that on, because the conversation wasn't happening. On my side, I was writing my own Jira tickets for a feature with no planning behind it, because if I didn't, the feature simply wouldn't move.

Neither of us stayed inside our own lane, either. When waiting for the other side would have blocked the work, we didn't wait. He patched game code directly. I wrote Go scripts against the backend. Not because either of us lacked a boundary to respect, but because respecting it meant stalling, and stalling wasn't an option on a feature already short on planning and long on deadline pressure.

Neither of us knew, at the time, that we were solving the same problem from opposite sides. Two people, on two different teams, independently absorbing the same missing coordination function, occasionally reaching across into each other's territory to keep the whole thing moving at all. From outside, that should have read as a loud signal: if two competent engineers are both guessing at a boundary and crossing it in both directions just to avoid blocking each other, the boundary was never actually drawn. Instead it read as two people doing their jobs well. The redundancy canceled into silence instead of becoming evidence, because nothing in the organization was positioned to notice it was the same gap, seen twice, from both sides at once.

---

## The Fix: Escalate on Evidence, Not on How It Feels

The natural response to noticing a gap like this is to push harder: build more, document more, make the case more forcefully. That instinct is what put both of us into unplanned overtime on a feature nobody had properly scoped. It also doesn't change anything on its own, because an organization doesn't fund a horizontal seat just because one line engineer worked hard enough to deserve one.

The question that actually matters isn't how to convince them. It's what the evidence in front of you justifies doing, and what it doesn't. I eventually wrote a formal proposal to company leadership for a chartered architect role, with a specific person in mind, after talking to enough people across the org to confirm the gap wasn't just mine. That's the most expensive move available to a line engineer. The role got created about a year later, filled by someone other than the person I'd proposed, and I never learned whether it worked, because by then I'd moved to another project.

That result reads as failure if the measure is whether leadership acted. It isn't the right measure. The proposal answered a different question than the one I asked. I asked whether leadership would fund this. The org answered, through a year of silence and then a decision made without me, that this wasn't where its attention actually was, whatever the org chart implied about being big enough to need it. That's real information, delivered through a channel that wasn't built to say so directly.

Escalating anyway, regardless of cost, isn't the lesson here. The cost of escalating should track the evidence you actually have, not how strongly you feel about the gap. A ladder makes that concrete: not a checklist to complete, but a way to match effort to evidence and know honestly when to stop.

---

## The Practice: A Ladder Gated by Evidence

### 1. Leave a Record, Not a Request

The cheapest rung costs a paragraph. When I inherited the mirrored plugin, the move was writing, in the ticket, that this was a placeholder meant to unblock development, not a designed contract, and naming what was still undecided. That's not a request for process. It's a dated fact, sitting where a future version of you, or anyone doing archaeology later, can find it. There's no reason not to do this by default. It asks nothing of anyone and costs almost nothing to write.

### 2. Name the Transition Point Once

At some point the mirror should have graduated into an actual interface. That transition never got named out loud. The move at that stage isn't building the real abstraction alone on your own time, that repeats the absorption problem one level deeper. It's a short, neutral note to whoever's closest to owning the plugin: this started as a placeholder, real requirements are visible now, a proper contract is needed before another consumer arrives. Said once, on record. If nobody acts on it, that absence is now on record too, and it didn't cost you the feature to say it.

### 3. Recognize Recurrence Before You Escalate Further

This is the actual gate, and it's the rung that separates a private frustration from something worth spending real capital on. The first time the plugin's thin abstraction cost someone unplanned work, it read as one bad boundary. The second time, when a different game's auth requirements didn't fit the interface at all, it stopped being a single incident and became a pattern. Recognizing the parallel with the core engineer's guesswork did the same thing from a different angle: once I understood he'd been making the same kind of unowned scope decision I had, on his own side of the boundary, the gap stopped being something specific to my feature and became something true about the organization.

Neither recurrence required anyone's permission to notice. Both are what license the next rung. Without them, escalation is conviction dressed up as evidence.

### 4. Widen the Aperture, After Checking You're Not the One Missing Something

The expensive move: proposing a structural fix to someone who can fund it, rather than documenting a boundary for the next engineer to find. Before writing that proposal, I talked to people across several teams, specifically to test whether I was the one missing context, not to gather allies. That step matters as much as the proposal itself. Spending the one expensive move you get on a gap you haven't verified is the same overinvestment as building the whole abstraction alone: well intentioned, and still a bet placed with your own standing instead of the organization's resources.

This rung isn't available, or worth using, on every gap a line engineer notices. It's for the ones that survived rung three: recurrence confirmed, and confirmed by more than your own read of it.

### 5. Read the Answer for What It Actually Says

Whatever comes back, a rejection, a year of silence, a fix that lands without you and that you never get to see work, isn't a verdict on whether you did enough. It's data about where the organization's attention already lives, delivered through a channel that wasn't built to say so directly. The proposal didn't fail to get funded because it was weak. It didn't get funded because leadership's priorities sat somewhere else, and the response revealed that plainly, whether or not anyone ever said it out loud.

This rung runs backward too, onto yourself, not just onto the org. Writing about a stalled effort with enough rigor to make the argument to a stranger is sometimes the only way to see clearly what you actually did, separate from what it felt like in the moment. I believed, right up until I tried to build a structured argument out of an earlier stalled migration, that I hadn't pushed hard enough. Building the argument showed the opposite: the stopping point had been correct, and what felt like failure was restraint, working exactly as it should have. That's a harder thing to trust in the moment than in hindsight, but it holds up better than the feeling of not enough does while you're still standing inside it.

---

## The Insight: The Ladder Isn't Meant to Be Climbed

Most of this ladder isn't about reaching the top. Rungs one and two cost so little there's no reason not to do them by default, on almost anything. Rung three is the actual decision point, and it's evidence, not effort or feeling, that earns the right to go further. Most gaps a line engineer notices should stop at rung two and never need to become a proposal to leadership. That's not a lesser outcome. It's the correct one, given what the evidence supported.

Rung five is the part most advice on this topic skips. Plenty of writing exists on how to escalate clearly. Very little exists on how to read what comes back, including silence, without converting it into a verdict on your own judgment. An organization that isn't built for technical priorities will not reliably fund the fix, no matter how correctly you ask. What stays inside your control is not burning yourself out trying to personally substitute for that funding, and not mistaking the org's inaction for evidence that you failed to do enough. That distinction sits close to the one at the center of [The Engineer-Process Boundary](EngineerProcessBoundary.md), just earlier in the sequence: not what to do after a stall becomes visible, but how to pace yourself, rung by rung, before it ever gets there.

---

## The Production Bottom Line

> **Match the Climb to the Evidence:** An organization that hasn't chartered a function will not fund it just because an engineer worked hard enough to deserve one. What a line engineer actually controls is how much they spend chasing that gap, and how accurately they read whatever comes back, including nothing at all. Leave the cheap record by default. Name the transition once. Wait for recurrence before spending real capital. And when the answer arrives, read it as information about the organization's priorities, not as a grade on personal effort. Stopping at the second rung because the evidence never justified a third isn't giving up. It's the whole point of building the ladder in the first place.