# Core Loop Framework

Use this reference when designing core loops, meta loops, and player motivation.

## 1. Core Loop Anatomy

```
ACTION → FEEDBACK → REWARD → UPGRADE/UNLOCK → NEW DECISION → RETURN
```

Every element must exist. If any is missing, the loop is broken.

### Element Checklist
| Element | Question | Red Flag |
|---------|----------|----------|
| Action | What does the player DO? | Loop begins with rewards instead of actions |
| Feedback | How does the player know it worked? | Feedback is delayed or ambiguous |
| Reward | What does the player GET? | Reward is disconnected from the action |
| Upgrade | What changes after? | Numbers go up but possibilities don't expand |
| New Decision | What becomes possible now? | No new choice = no progression, just accumulation |
| Return | Why come back? | Only reason is "more rewards" = chore loop |

## 2. Decision Density Audit

A healthy core loop has decision density at three time horizons:

| Timeframe | Decision Type | Example |
|-----------|--------------|---------|
| 10 minutes | Tactical | "Do I push or retreat?" |
| 10 hours | Strategic | "Which build do I invest in?" |
| 10 days | Meta | "Which goal do I prioritize this week?" |

If the 10-minute decision is the same as the 10-hour decision, the loop lacks depth.

## 3. Repeatability Engine

A loop needs one or more of these to sustain repetition:

| Engine | How It Works | Example |
|--------|-------------|---------|
| Variance | Random outcomes create different situations each run | Roguelike runs |
| Mastery | Player skill improves, revealing new depth | Action combat |
| Content | New authored content changes the context | Level progression |
| Social | Other players create dynamic pressure | PvP, guild wars |
| Economy | Resource management creates tradeoffs | City building |
| Buildcraft | Combinatorial possibilities create experimentation | Deck building |

Without at least one engine, the loop becomes a treadmill.

## 4. Meta Loop Design

### Meta Loop Components
- **Daily goals**: What does the player aim for today?
- **Weekly goals**: What spans multiple sessions?
- **Seasonal goals**: What defines a long-term arc?
- **Collection goals**: What can the player permanently complete?
- **Mastery goals**: What can the player endlessly improve at?
- **Social goals**: What requires or benefits from other players?

### Meta Loop Health Check
- Does the meta loop feed the core loop? (not replace it)
- Are goals visible and trackable?
- Does the player always have a near-term goal (reachable today)?
- Does the player always have a long-term aspiration (reachable in weeks)?
- Does completing a goal open new goals, not just close a chapter?

## 5. Core Loop Failure Modes

| Failure Mode | Symptom | Root Cause |
|--------------|---------|------------|
| Chore loop | Player repeats without deciding | Rewards without decisions |
| Treadmill | Numbers go up, gameplay doesn't change | No new decisions from upgrades |
| Content burn | Player finishes everything and quits | No repeatability engine |
| Stall | Player stops progressing | Difficulty cliff or economy bottleneck |
| Bloat | Too many parallel loops | No clear primary loop |
| Fragmentation | Activities don't connect | No shared reward currency or progression |

## 6. Prototype Design

The smallest playable test of a core loop:

1. **One verb**: What is the single action the player repeats?
2. **One decision**: What choice makes the action interesting?
3. **One reward**: What does the player get?
4. **One upgrade**: What changes after the reward?
5. **One return**: What brings the player back?

If the prototype needs more than one screen, it's too big.

## 7. Player Motivation Mapping

| Motivation | What the Player Wants | Loop Design |
|------------|----------------------|-------------|
| Achievement | To overcome challenges | Difficulty curve + mastery expression |
| Collection | To complete sets | Rarity tiers + collection meta |
| Social | To belong or compete | Guild systems + PvP + leaderboards |
| Exploration | To discover | Hidden content + branching paths |
| Expression | To customize | Cosmetic systems + build variety |
| Optimization | To min-max | Complex stat systems + tradeoffs |
| Relaxation | To unwind | Low-pressure activities + auto modes |

A single game can serve multiple motivations, but the core loop should serve ONE primary motivation first.
