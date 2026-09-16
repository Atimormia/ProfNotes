# The Cost of a Third-Party Call

*(Working title, matching the "The Cost of a Virtual Function" naming pattern; happy to swap once the draft settles.)*

I keep running into the same complaint about loading screens on live-service games with multiple backends: **nobody can point to the one slow thing.**

QA files it as "loading takes too long." A network trace gets pulled, but it does not reveal a single guilty bottleneck. Instead, it exposes five or six separate calls, each taking a few hundred milliseconds, each pointing to a different service:

* **EOS** for player identity
* **PlayFab** for inventory state
* **Nakama** for social presence
* An **internal config service** for feature flags
* An **observability SDK** and a **chat filter** quietly initializing in the background

None of these calls is slow enough on its own to justify a bug report. Added together, **they are the loading screen.**

This is the exact problem dynamic I wrote about in [AbstractionMeetsTheHotPath.md](https://www.google.com/search?q=AbstractionMeetsTheHotPath.md): no single loudest function, just a little bit of everything, all at once. Except here, the hops are not reflection-backed attribute lookups inside one process. They are remote network calls to external services, each added at a different milestone for an individually reasonable reason.

---

## The Blind Spot: Why Every Integration Looked Free in Isolation

Two costs stack quietly across network integrations, and neither shows up if you evaluate an SDK in isolation.

* **The Connection Setup Tax:** Every new host demands a DNS lookup, a TCP handshake, and (almost universally) a TLS handshake before the actual request payload moves. Depending on region and routing, that cold-connection tax easily burns 100 to 300 ms per host. It is the network equivalent of what I covered in [TickPitfalls.md](https://www.google.com/search?q=TickPitfalls.md): an empty engine lifecycle hook is never free, and neither is an empty socket. The vendor SDK might execute quickly, but the network transport underneath cannot cheat physics.
* **The Chaining Tax:** When downstream services depend on an upstream token (e.g., PlayFab or Nakama requiring authentication from EOS), those calls cannot run concurrently. Total wait time shifts from the duration of the slowest single hop to the sum of every sequential setup time plus its round-trip latency.

Worse, sequential dependencies compound operational risk. When independent services each carry an isolated failure rate, chaining them multiplies their overall failure probability.

If three sequential services each boast an individual reliability of $90\%$, their combined end-to-end success rate drops sharply:

$$0.90 \times 0.90 \times 0.90 \approx 72.9\%$$

Running those same three calls in parallel and aggregating partial results pushes the odds of retrieving usable data beyond $99\%$. That is not a rounding error: it is the difference between a game that feels robust and one that feels constantly broken, dictated entirely by call orchestration rather than vendor downtime.

Underneath these taxes lies an even quieter problem: **nobody separates what must finish before input begins from what is merely along for the ride.** An observability client and a chat filter do not need to gate the main menu. They block the screen anyway simply because they were registered to the generic startup routine, because that is where initialization logic naturally accumulates.

None of this is apparent when reviewing a pull request for a single service. The EOS integration looks clean. The PlayFab SDK looks fine. The Nakama implementation passes review. Every addition makes sense on its own merits, much like the layered stat-resolution system in [AbstractionMeetsTheHotPath.md](https://www.google.com/search?q=AbstractionMeetsTheHotPath.md).

What went unowned was the total sequence.

Mobile performance guidelines explicitly warn against this dynamic during cold starts: accumulating lightweight, near-invisible SDKs remains one of the most common reasons an app launch stutters. Games rarely discuss it, perhaps because backend communication is often treated as platform plumbing rather than an explicit architecture. It mirrors the blind spot analyzed in [AI_ArchitectureSkills.md](https://www.google.com/search?q=AI_ArchitectureSkills.md): when tooling friction vanishes, the deliberate architectural decision often vanishes with it.

---

## The Solution: Triage, Parallelize, and Aggregate

The solution is not "avoid third parties." Building bespoke, in-house platforms for identity, economy, and social systems is an unforced error for most studios.

The fix is treating the startup sequence as an owned architectural domain, mirroring the argument from [DataDrivenDesign.md](https://www.google.com/search?q=DataDrivenDesign.md) regarding data layer distribution: having multiple layers was never the defect, the defect was leaving layer ownership undefined.

Three patterns address this bottleneck directly.

### 1. Parallelize Independent Calls and Declare True Dependencies

If inventory lookups and social state do not consume each other's data, they should never run sequentially. Only requests strictly requiring an EOS auth token should queue behind authentication, and that dependency should exist as an explicit, documented graph rather than an accidental byproduct of script execution order.

In Unreal Engine specifically, this meant replacing cascading, blocking logic with **custom asynchronous Blueprint nodes**. Modern game engines do not provide the dynamic data-loading primitives found in modern web frameworks out of the box; asynchronous orchestration must be built deliberately. This follows the push-model principle from [OwnershipTaxUE.md](https://www.google.com/search?q=OwnershipTaxUE.md): consumers should receive data as it lands, rather than blocking the thread waiting to pull it.

### 2. Evict Non-Essential Tasks from the Critical Path

Authentication genuinely blocks player progression, but chat moderation dictionaries, telemetry handshakes, and analytics sessions do not.

Deferring or lazy-loading auxiliary SDKs transforms a five-hop blocking sequence into a streamlined one- or two-hop transition. Secondary tasks complete asynchronously in the background while the player is already interacting with the lobby.

### 3. Place an Aggregation Layer Between Gameplay and the Wire

This adapts the Controller pattern from [BlueprintMess.md](https://www.google.com/search?q=BlueprintMess.md) to network boundaries: gameplay and UI code should remain decoupled from external provider topologies. A Slate widget or Gameplay Ability should not know that player identity, inventory, and guilds reside across three discrete cloud providers.

![owned_aggregation.svg](misc/owned_aggregation.svg)

An aggregation layer offers three distinct advantages:

* **Fan-Out / Fan-In:** It dispatches independent requests concurrently and shapes the responses into a unified structure before alerting client gameplay systems.
* **Warm Connection Pooling:** Hosted on dedicated backend infrastructure, it maintains pre-warmed sockets to third-party endpoints, sparing game clients repeated DNS and TLS handshakes.
* **Graceful Degradation:** If the chat filter provider times out, the aggregator delivers the chat payload anyway and flags it for background filtering, ensuring a transient third-party hiccup never blocks core gameplay data.

---

## Core Mechanic: Network Boundaries Are Hot Paths

The fundamental performance rule here mirrors [AbstractionMeetsTheHotPath.md](https://www.google.com/search?q=AbstractionMeetsTheHotPath.md): **systemic cost is execution frequency multiplied by boundary traversal overhead, constrained by concurrency.**

* A virtual call traverses a vtable that the compiler cannot inline across.
* An attribute lookup traverses reflection boundaries within Unreal's Gameplay Ability System.
* A third-party network call traverses the most unforgiving boundary in software: a physical network hop with discrete connection overhead and independent failure modes that client-side code cannot optimize away.

No engineer who integrated EOS, PlayFab, Nakama, or an analytics suite made an error in isolation. Each SDK addressed a concrete requirement and passed code review. The failure was an accounting failure: nobody tracked the cumulative system behavior.

This reflects the core principle from [DataDrivenDesign.md](https://www.google.com/search?q=DataDrivenDesign.md): **credit the individual implementation, but measure the global pattern.**

A dependency list that grows from one service to six does not flip from performant to unacceptable in a single commit. The degradation happens incrementally across milestones. The only way to prevent it is to treat the startup pipeline as an actively governed system, tracking which external calls are permitted to block the player before a QA ticket ever gets opened.

---

> **Key Architecture Rule:** Third-party SDKs are frequently treated as passive utility code because optimizing their internals belongs to someone else. Yet every remote call introduces an unyielding boundary: sockets, handshakes, and failure points. System performance depends on defining which calls must wait, stripping everything else off the critical path, and isolating gameplay systems behind an owned aggregation layer.