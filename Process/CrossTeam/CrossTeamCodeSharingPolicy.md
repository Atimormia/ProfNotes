# Cross-Team Code Sharing Policy

This is an illustrative policy written for two fictional teams: **Provider**, which owns a shared code repository, and **Consumer**, which builds a product on top of it. It is not a company document, and every name, window and threshold below is a placeholder to adapt. It demonstrates the approach from [Compatibility Is a Guardrail for the Next Engineer](../../Blog/BackwardCompatibility.md): make the correct path the easy one, rank controls by how little they depend on memory, and give every compatibility path an owner and an expiry.

---

## 1. Purpose and Scope

**Purpose:** let Provider change shared code without blocking Consumer's builds, and let Consumer adopt changes on its own schedule.

**In scope:** any code, interface or serialized data format that crosses the boundary between the two teams' repositories.

**Out of scope:** code that lives entirely inside one team's repository.

## 2. Roles

| Role | Responsibility |
|---|---|
| Provider | Owns the shared code, cuts releases, announces and stages breaking changes |
| Consumer | Pins to a release, migrates within the deprecation window, reports regressions |
| Policy owner | Has the authority to change repository settings and tooling, owns the weekly report, reviews overrides |

The policy owner role matters most. Rules that need server-side or repository-level enforcement cannot be installed by either team alone, so name one person who can.

## 3. Choosing How to Share

Copying is a reasonable default when the guess is that you will not need to repeat it. It stops being reasonable as soon as the first use shows that the shared piece will need maintenance, so decide on the first use, not the third.

| Situation | Method |
|---|---|
| You expect to need it once or twice and do not expect to maintain it | Copy it. A dependency costs more than a copy until the demand is proven. |
| The first use already shows it will need maintenance (a shared data format, a known second consumer, fixes that must reach every user) | Plan the boundary now: link to a released version and apply sections 4 to 10. |
| A third use | Turn it into a link regardless of the earlier guess. The repetition is the evidence. |
| Copying by hand beyond that | Treat it as a defect. The work grows with every team and every update. |

## 4. Consumption Rules

1. **Pin to a released reference** (a branch cut for consumers, or a tag), never to the working branch.
2. **Do not pin to a mechanism that downstream cannot override.** A pin should be something Consumer can move deliberately.
3. **Consume read-only where the tooling allows it**, so edits cannot land in code Consumer does not own.
4. **Change what you consume through one reviewed file**, and let automation apply the change.

## 5. Changing the Interface

Classify every change by the layer it can break:

| Layer | Question |
|---|---|
| Source | Does the consumer still compile? |
| Binary | Does it still link and load? |
| Behavior | Does it still act the same? |
| Data | Do assets and saved files still load with their values intact? |

Rules:

* Keep the interface **narrow**. Everything exposed will eventually be depended on, including behavior that was never documented.
* Back each locked interface with **tests that Consumer's CI also runs**.
* **Deprecate before removing.** The old call keeps working, and the warning names its replacement, a version and a removal date.
* At the removal milestone, **promote the warning to an error**.
* For renamed types or properties that appear in serialized data, ship a redirect so existing assets keep their values.

## 6. Code Practices That Keep Changes Compatible

The rules above govern how changes travel. These practices make the changes themselves cheaper to absorb.

| Practice | What it protects | Watch for |
|---|---|---|
| Defaults for new parameters and fields | Existing callers and old data keep working | In C++, a new defaulted parameter is source-compatible but changes the function's signature, so precompiled consumers need a rebuild. A default is also part of the contract: changing it changes behavior for everyone who relied on it. |
| An options struct in place of a growing parameter list | Call sites stay the same as options grow | The struct's layout changes, so precompiled consumers still need a rebuild. Its defaults need the same care. |
| Extension points (hooks, delegates, interfaces the consumer implements) | Consumers customize without editing provider code, which reduces the pressure to fork or patch | Every extension point is more surface that will be depended on. Add one when a second consumer needs it, not speculatively. |
| A save or serialization format chosen by how fast the data changes | Added or removed fields do not invalidate old data | Self-describing, key-based data (tagged properties, key-value tables) tolerates change, and tightly packed binary does not, so it needs an explicit version number. Use the tolerant format for volatile data and the packed one only where size or speed justify it. |
| A version stamp and ordered migration steps | Old data can be brought forward in a known order | Choose where migration runs: on load (lazy) or in a batch resave job (eager). Keep a sample file per past version as a test fixture, and retire each step at its expiry (section 10). |
| Safe fallbacks on read | A missing or unknown field loads as a default and not as a crash | Log every fallback, or silent data loss will hide behind it. |

```cpp
// Adding a defaulted parameter: existing source still compiles, but the signature changes
void Spawn(FName Id, float Delay = 0.f);

// Options struct: call sites stay the same as options grow
// (layout changes still require a rebuild of precompiled consumers)
struct FSpawnOptions { float Delay = 0.f; bool bPooled = false; };
void Spawn(FName Id, const FSpawnOptions& Options = {});
```

## 7. Cutting a Release

- [ ] Provider announces the cut and the candidate reference.
- [ ] The consumer build runs against the candidate.
- [ ] Known deprecations and their removal dates are listed in the release notes.
- [ ] The release reference is recorded in the Consumer's pinned configuration, through the reviewed file.

## 8. Making a Breaking Change

- [ ] Add the new path and keep the old one working (expand).
- [ ] Mark the old path deprecated with a message, a version and a removal date.
- [ ] Notify Consumer and agree the migration window.
- [ ] Track remaining uses of the old path per consumer.
- [ ] Remove the old path only when the count reaches zero or the window ends (contract).

## 9. Overrides

A rule with no way through gets bypassed or switched off, so provide one with an audit trail.

* An override requires a ticket reference and the engineer's name in the change description.
* Every override appears in the weekly report.
* The policy owner reviews overrides at the end of each cycle. A repeated override means the rule needs changing.

## 10. Retiring Compatibility Paths

Every shim, deprecated call, version pin and flag creates a period in which old and new coexist. Register each one:

| Path | Owner | Created | Expiry | Remaining uses |
|---|---|---|---|---|
| (example) Old config loader | Provider | (date) | (date) | (count) |

A path without an owner and an expiry should not be accepted.

## 11. What to Measure

Collect from the first week, even if the first numbers are rough:

* broken consumer builds attributable to shared-code changes, per month
* time to restore a blocked build
* number of consumers pinned to a working branch or to a pin they cannot override
* number of overrides, and who used them
* remaining uses of deprecated paths, per consumer

These numbers are what justify enforcement in section 12.

## 12. Rollout Plan

1. **Detect.** Run the read-only weekly report ([`shared_code_audit.py`](shared_code_audit.py), described in section 14). It needs no one's permission.
2. **Agree.** Review the report with both teams and adopt sections 3 to 6.
3. **Enforce.** Where the report shows repeated bypasses, ask the policy owner to move the rule up: from documentation, to a reviewed file, to read-only access, to removing the channel.
4. **Review.** Revisit this policy at the first recurrence of a blocked build, and again each quarter.

## 13. Tool Notes

Check each item against the tools in use, since behavior differs between versions.

| Tool | Equivalent of the rules above |
|---|---|
| Perforce streams | Import consumer code read-only, change imports through one reviewed spec file, point consumers at a release branch, and avoid pinning an import to a specific changelist where downstream streams cannot override it |
| Git | Pin a submodule or dependency to a tag or commit on a release branch, protect the release branch, assign code owners to interface paths, and use a dependency bot to propose updates |
| Unreal Engine | Use the deprecation macro with a version and a message, core redirects for renamed classes and properties, and custom serialization versions for versioned data |

## 14. Reference Script: Advisory Report

[`shared_code_audit.py`](shared_code_audit.py) is a small, read-only script for the "detect" step. It changes nothing, so it can run without anyone's permission, and its output gives the counts that section 11 asks for. It flags three things:

| Rule | What it means | Severity |
|---|---|---|
| `writable-import` | An import that allows edits to land in code the consumer does not own | High |
| `pinned-import` | An import pinned to a changelist or label, which may not be overridable downstream | Medium |
| `moving-branch` | An import of a branch that does not look like a release reference (the pattern is configurable) | Medium |

It reads Perforce stream specs (saved to files, or fetched with read-only commands) or the submodule settings of a Git repository, prints a summary count per rule, can emit JSON, and exits with a non-zero status when there are findings, so it can also run as a CI check.

It also answers the provider's question, which streams import from my code and how, with `--consumers-of`. That list is the set of known consumers for the consumer build in section 7, and the starting point for the per-consumer counts in section 10.

```
python shared_code_audit.py p4-specs ./specs
python shared_code_audit.py p4-specs ./specs --consumers-of //Core
python shared_code_audit.py git ./game-repo --release-pattern "release|v\d"
```

It was tested against sample spec files and a sample Git repository. The live Perforce mode was not run against a server, so treat it as a starting point and check it against your own tooling. It deliberately leaves out any script that writes (for example one that applies spec changes automatically), since that needs server-side permissions and a policy of its own, which belongs to the policy owner in section 2.