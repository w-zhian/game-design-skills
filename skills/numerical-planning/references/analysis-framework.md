# Game Numerical Analysis Framework

Use this reference when performing a full teardown, balance diagnosis, formula audit, or pros/cons analysis of a game numerical system.

## Table Of Contents

1. Input inventory
2. System map
3. Audit lenses
4. Formula checks
5. Strength signals
6. Weakness signals
7. Tuning recommendations
8. Confidence labels

## 1. Input Inventory

Collect only what is needed for the user's goal. If unavailable, proceed with assumptions and label confidence.

| Input | Why it matters |
|---|---|
| Genre and platform | Defines acceptable session length, power gap, monetization pressure, and content cadence. |
| Target player segment | Casual, core, whale, competitive, collector, builder, and social players tolerate different curves. |
| Core loop | Reveals what actions generate resources and meaning. |
| Meta loop | Reveals long-term goals and retention structure. |
| Currency table | Shows sources, sinks, caps, conversion chains, inflation, and dead resources. |
| Stat/formula table | Shows power scaling, breakpoints, role balance, and runaway multipliers. |
| Reward table | Shows certainty, variance, pacing, pity, and aspiration. |
| Content unlock table | Shows whether power growth and content difficulty are aligned. |
| Monetization table | Shows pain-point placement, price ladder, fairness risk, and payer segmentation. |
| Telemetry | Validates whether the theoretical issue appears in real player behavior. |

## 2. System Map

Before judging, map the system in seven layers.

### Layer 1: Player Goals

- Short-term: next battle, next level, next chest, next upgrade.
- Mid-term: build completion, chapter clear, rank tier, deck archetype, city stage.
- Long-term: collection, mastery, PvP rank, guild status, prestige, seasonal identity.
- Social: cooperation, competition, gifting, guild obligation, leaderboard recognition.

### Layer 2: Core Loop

Write the repeated loop as verbs:

`enter activity -> consume resource/time -> perform skill/decision -> get reward -> upgrade/build -> unlock harder or richer activity`

Check whether every repeated action points back to a meaningful player goal.

### Layer 3: Economy Loop

For each currency or material:

- Source: where it enters.
- Sink: where it exits.
- Storage: whether players can hoard it.
- Cap: whether excess is lost or converted.
- Exchange: whether it converts into other resources.
- Cadence: daily, weekly, event, season, permanent.
- Segment: beginner, mid-game, endgame, payer, non-payer.

Healthy economy usually has a clear main bottleneck, secondary soft bottlenecks, and enough optional sinks to prevent dead stockpiles.

### Layer 4: Progression Loop

Track how effort converts to power and content access:

- Player level or account level.
- Character/card/equipment level.
- Skill/talent/tech tree.
- Content difficulty and rewards.
- Unlock gates and time gates.
- Reset/prestige loops.

The key question is not "does number go up" but "does marginal effort still create meaningful choice or emotion."

### Layer 5: Power Model

Identify the power layers:

- Base stat growth.
- Additive bonuses.
- Multiplicative bonuses.
- Critical/variance layers.
- Defense/mitigation layers.
- Control/healing/shielding layers.
- Team, synergy, element, faction, terrain, or counter systems.
- Caps, floors, diminishing returns, and breakpoints.

Most balance accidents come from hidden multiplicative stacking, uncapped mitigation, or thresholds that invalidate earlier choices.

### Layer 6: Monetization Loop

Map the monetization promise:

- What friction is created?
- What paid item relieves it?
- What is the free path?
- Is the paid path convenience, acceleration, expression, breadth, or direct power?
- Where is the fairness boundary for the genre?
- How does the system treat late joiners and non-payers?

### Layer 7: Live-Ops Knobs

Name the knobs designers can tune:

- Currency source amounts.
- Sink costs.
- Drop rates and pity thresholds.
- Enemy stats and stage requirements.
- Upgrade coefficients.
- Time-gate timers and stamina recovery.
- Event reward exchange rates.
- Matchmaking bands.
- Shop prices and bundle composition.

Prefer systems with many safe knobs and few hard-coded cliffs.

## 3. Audit Lenses

### Loop Coherence

Ask:

- Does the core loop feed the meta loop?
- Are rewards used soon enough to feel meaningful?
- Do long-term goals explain why short-term repetition matters?
- Is the player choosing or merely clearing chores?

Weakness signs:

- Many activities, no shared long-term purpose.
- Resources earned in one mode do not matter elsewhere.
- Daily tasks replace fun with obligation.
- Rewards are numerous but not decision-relevant.

### Curve Health

Audit:

- Time-to-next-upgrade by lifecycle stage.
- Marginal power gained per upgrade.
- Cost growth vs earning growth.
- Difficulty growth vs power growth.
- Catch-up speed for late players.
- Soft cap and hard cap placement.

Common curve shapes:

- Linear: predictable, easy to tune, can become flat.
- Exponential: exciting early, dangerous if compounded too long.
- Logarithmic: strong early catch-up, weak late aspiration.
- Logistic/S-curve: controlled lifecycle, good for caps and seasons.
- Step curve: milestone excitement, risk of cliffs.

### Economy Balance

Compute or estimate:

- Daily earn rate.
- Required spend rate.
- Stockpile growth.
- Time-to-target.
- Bottleneck ratio between parallel resources.
- Inflation after events and seasons.

Weakness signs:

- A currency has sources but no meaningful sinks.
- Main bottleneck changes randomly without signaling.
- Players hoard because spending choices are trap-laden.
- Event rewards destroy permanent economy pacing.
- Exchange rates make one activity strictly dominant.

### Combat And Stat Balance

Audit:

- Damage formula and defense formula.
- Effective HP, DPS, burst window, sustain, control uptime.
- Role compression: one unit does too many jobs.
- Counterplay: whether disadvantaged players have response options.
- Breakpoints: one threshold flips failure to trivial success.
- Variance: crit, dodge, proc, hit rate, random targeting.

Weakness signs:

- Multipliers stack without diminishing returns.
- Defense or healing creates immortality.
- Speed/action economy dominates all other stats.
- PvE requires exact stat checks with no tactical workaround.
- PvP snowballs too early and removes agency.

### Reward Psychology

Evaluate:

- Certainty vs variance.
- Visible progress toward a target.
- Near-term, mid-term, long-term goals.
- Pity or guarantee design.
- Duplicate handling.
- Bad-luck protection.
- Reward readability.

Weakness signs:

- Too much randomness without recovery.
- Reward reveal is exciting but reward utility is unclear.
- Pity thresholds are too far from natural session rhythm.
- Duplicate conversion feels punitive.
- Long-term goals require spreadsheet-level planning from casual players.

### Monetization Fairness

Separate revenue efficiency from system health:

- Pay-to-progress can be acceptable when non-payers still retain meaningful agency.
- Pay-to-win becomes dangerous when paid power removes counterplay or social legitimacy.
- Cosmetic or breadth monetization is safer but must still connect to identity.
- Subscription/battle pass needs regular perceived value, not just chores.

Weakness signs:

- First payer wall arrives before trust is established.
- PvP exposes raw spending gap too directly.
- Bundles hide real exchange rates.
- Paid acceleration creates permanent uncrossable gaps.
- Non-payer path becomes mathematically hopeless.

### Content Pacing

Check:

- How fast players consume authored content.
- Whether numerical gates protect content or merely block fun.
- Whether difficulty teaches new mechanics or only raises stats.
- How long a player waits between meaningful decisions.
- Whether events accelerate or cannibalize permanent goals.

### Strategy Diversity

Ask:

- How many builds are viable at each lifecycle stage?
- Are choices real or only illusions before an optimal path emerges?
- Do counters create a meta cycle or a solved hierarchy?
- Are support/defense/control roles valued numerically?

Weakness signs:

- One stat has best marginal value in all situations.
- One activity is best for all resources.
- One team archetype beats all content.
- Upgrades are irreversible but traps are not signaled.

### Operational Tunability

Ask:

- Can designers fix the issue by changing data?
- Which changes risk breaking older content?
- Are source/sink tables separated from formulas?
- Are event rewards isolated from permanent inflation?
- Are telemetry events granular enough to diagnose failure?

## 4. Formula Checks

Use these as audit prompts. Do not force them when the system does not use the concept.

### Combat

- Expected damage: `base * coefficient * attack_layer * skill_bonus * element_bonus * crit_EV * mitigation`
- Crit expected value: `1 + crit_rate * (crit_damage - 1)`
- Effective HP: `HP / (1 - damage_reduction)` when reduction is linear and capped.
- Time to kill: `enemy_EHP / player_DPS`
- Sustain pressure: `incoming_DPS - healing_or_shield_per_second`
- Control uptime: `control_duration / cycle_time`, adjusted by resistance and immunity.

Check for multiplicative stacking, uncapped mitigation, speed/action economy dominance, and breakpoints.

### Economy

- Net flow: `sources_per_period - sinks_per_period`
- Time to target: `target_cost / net_earn_rate`
- Bottleneck ratio: `time_to_resource_A / time_to_resource_B`
- Stockpile growth: `source_rate - natural_spend_rate`
- Event shock: `event_reward / normal_periodic_income`
- Exchange dominance: compare all activities by expected value per time, stamina, or attention.

### Gacha, Loot, And Drops

- Expected pulls to target.
- Probability to target by spend level.
- Pity threshold vs free earn rate.
- Duplicate conversion rate.
- Expected value per pull.
- Worst-case path and bad-luck recovery.

### Progression

- Cost growth rate vs income growth rate.
- Power gained per unit cost.
- Difficulty growth vs player power growth.
- Time between meaningful upgrades.
- Catch-up ratio for late joiners.
- Content unlock interval.

## 5. Strength Signals

Call these out when present:

- Core and meta loops reinforce one another.
- Main bottleneck is clear, fair, and readable.
- Upgrade choices create different strategies, not just bigger numbers.
- Early growth is fast enough to teach, late growth is slow enough to retain aspiration.
- RNG has visible safety nets and conversion value.
- Monetization relieves friction without deleting agency.
- PvP has compression, matchmaking, or counterplay to protect legitimacy.
- Live-ops has safe knobs for tuning without breaking old investments.
- New-player catch-up exists without invalidating veteran effort.

## 6. Weakness Signals

Prioritize these in critique:

- Hidden cliffs: a small requirement jump causes sudden failure.
- Runaway multipliers: stacked bonuses produce uncontrollable power gaps.
- Dead resources: currency accumulates with no valuable sink.
- False choices: many options exist but one dominates mathematically.
- Trap upgrades: irreversible investments with poor signposting.
- Pay wall before trust: monetization pressure arrives too early.
- Permanent whale gap: paid acceleration creates uncrossable competitive distance.
- Event inflation: temporary generosity damages permanent economy.
- Chore overload: daily systems optimize retention metrics while eroding fun.
- Opaque formulas: players cannot form reliable goals or strategies.

## 7. Tuning Recommendations

For each recommendation, specify:

- Knob: the exact parameter or table to change.
- Direction: increase, decrease, cap, split, flatten, steepen, convert, gate, or expose.
- Expected effect: what player behavior should change.
- Side effect: what may break.
- Validation metric: how to confirm whether the change worked.

Example:

| Knob | Direction | Expected effect | Side effect | Validation |
|---|---|---|---|---|
| Mid-game upgrade gold cost | Flatten levels 35-45 by 15-20% | Reduce time-to-next-upgrade cliff | Faster content consumption | Upgrade completion rate, chapter clear rate, day-7 retention |

## 8. Confidence Labels

Use confidence labels whenever data is incomplete:

- **High confidence**: directly supported by supplied tables, screenshots, formulas, or telemetry.
- **Medium confidence**: inferred from multiple visible system relationships but missing exact values.
- **Low confidence**: genre-informed hypothesis that needs data.

When confidence is low, convert the conclusion into a testable question.
