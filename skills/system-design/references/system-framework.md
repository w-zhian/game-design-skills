# System Design Framework

Use this reference when designing game systems, modules, and meta structures.

## 1. System Boundary Template

```
SYSTEM: [Name]
OWNS: [entities, states, verbs this system controls]
DOES NOT OWN: [what belongs to other systems]
TOUCHPOINTS:
  - Core loop: [how it connects]
  - Economy: [how it connects]
  - Combat: [how it connects]
  - Content: [how it connects]
  - Onboarding: [how it connects]
TUNING SURFACE: [what can be adjusted without code changes]
```

## 2. Entity-State-Verb Mapping

For each system, map:

| Entity | States | Player Verbs | System Verbs | Resources |
|--------|--------|-------------|---------------|-----------|
| (e.g.) Character | Locked → Available → Active → Upgrade → Max | Acquire, Equip, Upgrade, Unequip, Dismantle | Expire, Trigger, Reset | Gold, XP, Materials |

## 3. Dependency Graph Rules

- Draw dependencies as a DAG (directed acyclic graph)
- No circular dependencies between systems
- Each system should have at most 3 upstream dependencies
- If a system has more than 5 downstream dependents, it's too critical to change casually

## 4. Config Table Schema Standard

### Header Convention (3-row header)
```
Row 1: EnglishName    | LevelReq | CostGold | CostItem  | RewardExp |
Row 2: field_name     | level_req| cost_gold| cost_item | reward_exp|
Row 3: int            | int      | int      | string    | int      |
```

### Rules
- English name: PascalCase, no abbreviation
- Field name: snake_case, matches code variable
- Type: int / float / string / bool / enum / reference
- Every table has a primary key column (usually `id`)
- Foreign keys use format: `[target_table]_id`

## 5. System Design Doc Template

```markdown
## Summary
One paragraph explaining the system and why it exists.

## Goals And Non-Goals
- Goals: [what the system should achieve]
- Non-Goals: [what the system should not solve]

## Player Experience
Player journey from discovery to repeated use.

## System Model
- Entities / States / Player verbs / Resources / Rules / Rewards / Limits / Failure cases

## Loop Integration
How the system connects to core loop, meta loop, economy, content, onboarding, live ops.

## Progression
Unlocks, pacing, mastery curve, lifecycle stage differences.

## Economy And Rewards
Sources, sinks, caps, exchange paths, risk points.

## UX Requirements
Screens, feedback, player-readable states, tutorial needs.

## Balance And Tuning
Knobs, default assumptions, test ranges, side effects.

## Risks
False choices, dominant strategies, player confusion, production cost, content exhaustion, monetization pressure.

## Validation Plan
Playtest tasks, telemetry, expected behaviors, decisions to make after data.
```

## 6. System Architecture Red Flags

- System has no explicit owner in the game loop
- Adds a new currency, screen, or stat without a new decision
- Cannot be tuned without code changes
- Best strategy is obvious and stable after one session
- More than 5 parallel systems running simultaneously (cognitive overload)
- System that can be completely solved by a spreadsheet (no player agency)
- System that has no failure state (no tension)
- System that interacts with everything (no boundary = no system)

## 7. Meta Structure Patterns

### Vertical Meta
- Linear progression: each tier unlocks the next
- Good for: clear goals, easy to balance
- Risk: exhaustion when tiers are predictable

### Horizontal Meta
- Parallel tracks: multiple goals available simultaneously
- Good for: player choice, variety
- Risk: analysis paralysis, some tracks ignored

### Cyclical Meta
- Seasonal reset or prestige: progress resets but permanent bonuses remain
- Good for: long-term retention, fresh starts
- Risk: frustration if reset feels punitive

### Collection Meta
- Assemble sets or complete rosters
- Good for: completionist motivation, long-term goals
- Risk: FOMO pressure, too many gaps

## 8. UI Flow Design Principles

- One new decision at a time (don't dump complexity)
- Most important action should be the most visible
- State changes should be immediately readable
- Confirmation for irreversible actions
- Quick access to frequently used paths
- Tutorial teaches WHY before HOW
