# Upgrading Game Engines Safely

Mid-production engine upgrades are the ultimate engineering nightmare. You hit "Update," and suddenly half the project is broken, compiler errors number in the thousands, and the team’s velocity grinds to a halt for weeks or months.

I recently worked on a 10-year-old live-ops project where upgrading from Unreal Engine 4 to Unreal Engine 5 took *years*. The root cause wasn't just the massive architectural shift between engine versions; it was how historical custom engine modifications had been managed.

The project relied on a fragile patch script: developers needing access to an engine field would simply open the engine
source code, change the code, and tag it with a comment line. With no validation, no safety net, and hundreds
of these silent mutations scattered across a decade of development, it created an unmitigated upgrade bottleneck.

If you have a 10-year-old codebase, you can't afford to let it get broken by a new engine version. You must make an effort to structure your codebase to be safe from the engine's internal implementation and sometimes be ready to protect this technical priority from production pressure.

---

## The Blind Spot: Leaky Boundaries & Hacked Source

One day I was reviewing this CR. The feature required data tightly locked inside an engine class. The immediate impulse is to force the door open, it unblocks the daily sprint and just works with minimum effort.

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

### 💣 The Cost of Upgrading a Compromised Engine

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

## The Fix: Architectural Discipline and Tight Decoupling

A good tech lead treats the underlying game engine as an **immutable third-party library**. Maintaining a 10-year-old live-ops project requires strict architectural discipline to ensure engine changes are completely abstracted and never tightly coupled to your gameplay systems.

If you absolutely must access restricted engine data or alter native behavior, you enforce a strict code of conduct that keeps the core engine source code pristine:

### 1. Extensibility via Subclassing or Components

Instead of modifying base engine actors, handle your data extension within your own project modules. If you need a custom property or tracking state, inherit from the engine class or attach a modular actor component (`UActorComponent`) owned entirely by your project.

### 2. Runtime Memory Detouring (Hooks)

If a native engine function is not virtual and you *must* alter its logic, do not edit the source file. Use runtime memory detouring (function hooking) via lightweight engine-safe utilities or platform-specific libraries. This intercepts the execution flow at runtime, keeping your custom changes safely confined to your project directory.

### 3. Isolated Friend Accessors

If you maintain an internal engine fork and absolutely must bypass an access modifier, do not flip a block from `private` to `public`. Insert a single `friend class FMyProjectAccessor;` directive into the engine class. Then, handle all raw data extraction strictly within that isolated accessor class inside your project module.

This ensures that the engine's internal encapsulation details remain intact for the rest of your 400+ gameplay files, localizing the impact of any future engine refactoring.

---

## The Production Bottom Line

> **Architectural Longevity:** Keeping a live-ops project maintainable over a decade takes immense discipline. Refusing to let the first "broken window" slide isn't about dogmatic purity — it's a critical production strategy. By strictly decoupling your gameplay systems and treating engine source as immutable, you ensure that upgrading your framework architecture remains a minor, predictable maintenance task rather than a multi-year engineering catastrophe.

