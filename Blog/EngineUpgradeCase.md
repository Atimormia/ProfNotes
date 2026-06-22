# Upgrading Game Engines Safely

Mid-production engine upgrades are the ultimate engineering nightmare. You hit "Update," and suddenly half the project is broken, compiler errors number in the thousands, and the team’s velocity grinds to a halt for weeks or months.

I recently worked on a 10-year-old live-ops project where upgrading from Unreal Engine 4 to Unreal Engine 5 took *years*. The root cause wasn't just the massive architectural shift between engine versions; it was how historical custom engine modifications had been managed.

The project relied on a fragile patch script: developers needing access to an engine field would simply open the engine
source code, change the code, and tag it with a comment line. With no validation, no safety net, and hundreds
of these silent mutations scattered across a decade of development, it created an unmitigated upgrade bottleneck.

If you have a 10-year-old codebase, you can't afford to let it get broken by a new engine version. You must make an effort to structure your codebase to be safe from the engine's internal implementation and sometimes be ready to protect this technical priority from production pressure.

---

## The Blind Spot: Leaky Boundaries & Hacked Source

One day I was reviewing this CR (simplified and anonymized). The feature required data tightly locked inside an engine class. The immediate impulse is to force the door open: it unblocks the sprint, satisfies the feature request, and appears cheap in the moment.

### The Naive Code Review: Mutating the Engine

#### File: `/Engine/Source/Runtime/Engine/Classes/GameFramework/Character.h`

```diff
@@ -142,6 +142,10 @@ class ENGINE_API ACharacter : public APawn
 
+   // --- BEGIN CUSTOM PROJECT CHANGES ---
+   // Need this public so the Combat Telemetry system can pull it directly
+   // OLD: private:
+   public:
+   // --- END CUSTOM PROJECT CHANGES ---
    /** The max health threshold allowed before structural armor calculation triggers. */
    float MaxStructuralArmorPool;

```

#### File: `/MyProject/Source/MyProject/Combat/CombatTelemetry.cpp`

```cpp
void UCombatTelemetry::LogShieldData(ACharacter* TargetCharacter)
{
    // Directly reaching into a mutated engine variable
    float CurrentArmor = TargetCharacter->MaxStructuralArmorPool;
    SendTelemetryToBackend(CurrentArmor);
}

```

### The Cost of Upgrading a Compromised Engine

When the time comes to upgrade the engine, the engine creators completely refactor the internal pipelines. The automated upgrade script runs, pulls down the fresh, pristine source code for the new engine version, and attempts to apply the historical diffs. This is what the new version looks like:

#### File: `/Engine/Source/Runtime/Engine/Classes/GameFramework/Character.h` (New Engine Version)

```cpp
class ENGINE_API ACharacter : public APawn
{
    // The variable was completely removed, renamed, or packed into a compression struct!
    UPROPERTY()
    FCharacterDynamicAttributes PackedAttributes; 
};

```

### The Fallout:

1. **The Merge Script Fails:** The automated text-merging script looks for `float MaxStructuralArmorPool;` to re-apply the `public:` hack, but the variable no longer exists. The script crashes or silently skips the line.
2. **Cascading Compiler Errors:** Suddenly, `CombatTelemetry.cpp` fails to compile because `MaxStructuralArmorPool` is missing. If you have done this in 400 different places over 10 years, you are now facing weeks of manual code archeology just to figure out what data the original developer was trying to access, and how the new engine calculates it.

---

## The Fix: Governed Boundaries

A good tech lead does not treat engine sources as a convenient place to unblock every feature request. Even when a studio maintains an engine fork, modifications need to be deliberate, reviewed, isolated, and documented.

The goal is not “never touch the engine.” The goal is to prevent engine internals from becoming part of your gameplay architecture.

### 1. Prefer Sanctioned Extension Points

Before editing engine source, exhaust the extension mechanisms the engine already provides: subclassing, components, delegates, interfaces, plugins, subsystems, configuration, or data-driven hooks.

If a gameplay system needs additional state, keep that state in project-owned classes rather than exposing private engine fields directly.

### 2. Put a Project-Owned Boundary Around Engine Internals

If gameplay code needs information from the engine, do not let hundreds of systems reach directly into engine types. Create a narrow adapter or accessor layer owned by your project.

That way, when the engine changes, you update one boundary instead of performing archaeology across the entire codebase.

### 3. Govern Unavoidable Engine Fork Changes

Sometimes engine edits are unavoidable. To enforce considering other options before making an engine change, put additional control points in the development process:

- require code review from an engine owner
- document the reason for the change
- link the change to the consuming project system
- add tests or validation where possible
- keep a migration note for future engine upgrades
- fail CI if expected engine patches no longer apply

The real discipline is not avoiding every engine modification. It is making sure each modification has an owner, a purpose, and a controlled blast radius.

---

## The Production Bottom Line

> **Architectural Longevity:** Keeping a live-ops project maintainable over a decade takes immense discipline. Refusing to let the first "broken window" slide isn't about dogmatic purity — it's a critical production strategy. By strictly decoupling your gameplay systems and treating engine source as immutable, you ensure that upgrading your framework architecture remains a minor, predictable maintenance task rather than a multi-year engineering catastrophe.

 