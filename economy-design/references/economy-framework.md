# Economy Design Framework

Use this reference when designing game economy, resource flows, and monetization.

## 1. Resource Flow Mapping

For each currency/material, document:

```
RESOURCE: [Name]
TYPE: soft / hard / token / material / time
SOURCE:
  - [Activity]: [amount/day or per-completion]
  - [Activity]: [amount/day]
SINK:
  - [Activity]: [cost per use]
  - [Activity]: [cost per upgrade]
CAP: [hard cap / soft cap / unlimited]
EXCHANGE:
  - → [Target resource]: [rate, limit, condition]
  - ← [Source resource]: [rate, limit, condition]
CADENCE: daily / weekly / event / season / permanent
SEGMENT: beginner / mid-game / endgame / payer / non-payer
DECISION: What choice does this resource create for the player?
```

If a resource creates no decision, it should be removed or merged.

## 2. Economy Health Diagnostics

### Source/Sink Balance
```
Net flow = sum(sources) - sum(sinks)
```
- Net flow > 0 → inflation risk (stockpiling, content bypass)
- Net flow < 0 → deflation risk (frustration, grind perception)
- Net flow ≈ 0 → stable but check if the equilibrium is at the right pace

### Bottleneck Analysis
```
Time-to-target = target_cost / net_earn_rate
Bottleneck ratio = time_to_resource_A / time_to_resource_B
```
- Ideal: 2-3 parallel bottlenecks of similar weight
- Bad: single bottleneck dominates all progression
- Bad: no bottleneck (everything available immediately)

### Stockpile Risk
```
Max stockpile = source_rate * time_without_spending
Bypass potential = max_stockpile / next_content_cost
```
- If bypass potential > 3, players can skip content tiers
- Event rewards should not exceed 2x normal periodic income

## 3. Monetization Design Patterns

### Price Ladder Template
| Tier | Price (CNY) | Content | Value Type | Free Equivalent |
|------|-------------|---------|------------|-----------------|
| Entry | ¥6 | Starter pack | Acceleration | 3 days of grind |
| Small | ¥30 | Weekly pass | Acceleration | 2 weeks of grind |
| Medium | ¥68 | Monthly pass + battle pass | Acceleration + breadth | 1 month of grind |
| Large | ¥128 | Skin + currency | Expression + convenience | N/A (cosmetic) |
| Whale | ¥328 | Gem bundle | Acceleration | Varies |

### Fairness Check
- [ ] Free path time-to-target is reasonable for the genre
- [ ] Paid acceleration ratio ≤ 5x free path speed
- [ ] No exclusive power locked behind paywall
- [ ] PvP has compression mechanics (handicap, bracketing, counterplay)
- [ ] Cosmetic monetization doesn't fragment player base

## 4. Reward Pacing Design

### Cadence Patterns
| Cadence | Mechanism | Player Feel | Risk |
|---------|-----------|-------------|------|
| Per-action | Immediate drop | Gratifying | Can become expected/mandatory |
| Per-session | Daily quest | Habit-forming | Can become chore |
| Per-week | Weekly challenge | Goal-setting | Can dominate schedule |
| Per-event | Limited-time rewards | FOMO/excitement | Can cannibalize permanent goals |
| Per-season | Season pass | Long-term investment | Can feel like a second job |
| Per-milestone | Achievement/collectible | Pride/identity | Can become checklist grind |

### Pity System Design
```
Pity threshold = N pulls
Soft pity start = N * 0.7
Hard pity = N (guaranteed)
Rate-up probability = P%
Expected pulls to target = sum from i=1 to N of P(i) * i
```

Key questions:
- Is the pity threshold reachable within a free-player's monthly currency budget?
- Does soft pity create visible progress toward the hard pity?
- Is duplicate conversion fair (not punitive)?

## 5. Economy Red Flags

- Multiple currencies buy the same decision
- Paid spending removes the need to engage with the core loop
- Upgrade costs grow faster than earning rate without new gameplay
- Players can stockpile enough to ignore future content
- Scarcity is explained only by business need, not gameplay tension
- Event rewards destroy permanent economy pacing
- A currency has sources but no meaningful sinks
- Exchange rates make one activity strictly dominant
- The main bottleneck changes randomly without signaling
- Players hoard because spending choices are trap-laden

## 6. Battle Pass Design Template

### Structure
| Tier | Free Track | Paid Track | Cumulative Value |
|------|-----------|-----------|------------------|
| 1-10 | Basic materials | Premium currency | Entry value |
| 11-30 | Upgrade materials | Exclusive cosmetic | Break-even point |
| 31-50 | Mid-tier currency | Limited character/weapon | Value peak |
| 51-70 | Token rewards | Exclusive title/skin | Whale satisfaction |

### Design Principles
- **Break-even point**: Paid track should break even within 2 weeks of normal play
- **FOMO without frustration**: Exclusive items should be cosmetic or breadth, not power
- **Progress visibility**: XP bar should always show next reward
- **Catch-up mechanism**: Late purchasers can retroactively claim past tiers
- **Daily cap**: XP earning should have a daily cap to prevent "one weekend clear"

## 7. Gacha Design Template

### Probability Structure
| Rarity | Base Rate | With Soft Pity | Hard Pity |
|--------|-----------|----------------|-----------|
| SSR | 0.6% | Ramps from pull 70 | Pull 90 (guaranteed) |
| SR | 5.1% | No soft pity | Pull 10 (guaranteed) |
| R | 94.3% | — | — |

### Expected Value Calculation
```
Expected pulls to SSR = Σ(i=1 to 90) P(SSR at pull i) × i
Expected cost = expected_pulls × cost_per_pull
Free monthly pulls = (daily currency + event currency + quest currency) / cost_per_pull
```

Key check: Can a free player reach hard pity at least once per banner cycle?

## 8. Tuning Knob Reference

| Knob | Direction | What It Affects | Side Effects |
|------|-----------|-----------------|--------------|
| Daily source amount | ↑/↓ | Earn rate, stockpile | Inflation, content bypass speed |
| Sink cost | ↑/↓ | Time-to-target, frustration | Engagement, churn |
| Drop rate | ↑/↓ | Variance, excitement | Predictability, value perception |
| Pity threshold | ↑/↓ | Safety net, perceived fairness | Gacha revenue, player satisfaction |
| Exchange rate | ↑/↓ | Activity dominance | Player routing, engagement distribution |
| Price point | ↑/↓ | Conversion rate, ARPU | Accessibility, payer segmentation |
| Cap | ↑/↓ | Stockpile limit, hoarding | Frustration, engagement frequency |
