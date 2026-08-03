# Game Numerics Report Template

Use this reference when the user asks for a structured teardown, review, audit, or professional report.

## Quick Diagnosis Format

Use this for short answers.

```markdown
**One-Sentence Diagnosis**
[The main numerical issue or strength in one sentence.]

**System Map**
- Genre / lifecycle stage:
- Core loop:
- Meta loop:
- Main resources:
- Main sinks:
- Power model:
- Monetization pressure:

**Strengths**
1. [Specific strength + why it works]
2. [Specific strength + why it works]

**Weaknesses / Risks**
1. [Specific weakness + affected player segment + lifecycle stage]
2. [Specific weakness + affected player segment + lifecycle stage]

**Recommended Tests**
- [Metric or table check that would confirm the diagnosis]
- [Gameplay or telemetry test]

**Confidence**
[High / Medium / Low] because [evidence available or missing].
```

## Deep Report Format

Use this for full analysis.

```markdown
# [Game/System] Numerical Design Teardown

## 1. Executive Summary

- Overall diagnosis:
- Best numerical strength:
- Biggest numerical risk:
- Most important missing data:
- Confidence:

## 2. System Map

| Layer | Current Structure | Design Purpose | Risk |
|---|---|---|---|
| Core loop |  |  |  |
| Meta loop |  |  |  |
| Economy |  |  |  |
| Progression |  |  |  |
| Combat/stat model |  |  |  |
| Monetization |  |  |  |
| Live-ops knobs |  |  |  |

## 3. Economy Flow

| Resource | Sources | Sinks | Cadence | Bottleneck Role | Health |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

Key findings:
- 

## 4. Progression And Curve Health

| Curve | Observed / Inferred Shape | Good Sign | Risk |
|---|---|---|---|
| Player level |  |  |  |
| Power growth |  |  |  |
| Cost growth |  |  |  |
| Difficulty growth |  |  |  |
| Reward growth |  |  |  |

Key findings:
- 

## 5. Combat / Stat / Power Model

| Component | Role | Balance Question | Risk |
|---|---|---|---|
| Damage |  |  |  |
| Defense / mitigation |  |  |  |
| Healing / shields |  |  |  |
| Crit / variance |  |  |  |
| Speed / action economy |  |  |  |
| Synergy / counters |  |  |  |

Key findings:
- 

## 6. Reward And Motivation

- Short-term goals:
- Mid-term goals:
- Long-term goals:
- Variance and safety nets:
- Collection or mastery pressure:

Strengths:
- 

Risks:
- 

## 7. Monetization And Fairness

| Paid Mechanism | Player Pain Relieved | Free Path | Fairness Risk | Health |
|---|---|---|---|---|
|  |  |  |  |  |

Key findings:
- 

## 8. Genre Fit

Compare the design against expected genre patterns:

- What fits the genre:
- What deviates in a useful way:
- What deviates dangerously:

## 9. Pros And Cons

### Strengths

| Strength | Why It Works | Evidence | Fragility |
|---|---|---|---|
|  |  |  |  |

### Weaknesses

| Weakness | Player Impact | Root Cause | Severity | Confidence |
|---|---|---|---|---|
|  |  |  |  |  |

## 10. Recommendations

| Priority | Knob | Change | Expected Effect | Side Effect | Validation Metric |
|---|---|---|---|---|---|
| P0 |  |  |  |  |  |
| P1 |  |  |  |  |  |
| P2 |  |  |  |  |  |

## 11. Missing Data

- [Data needed]
- [Why it matters]
- [How to collect or estimate it]
```

## Severity Scale

| Level | Meaning |
|---|---|
| P0 | Breaks core loop, fairness, retention, or economy health. Fix before expansion. |
| P1 | Meaningfully harms one lifecycle stage or player segment. Tune soon. |
| P2 | Local issue, polish problem, or future risk. Monitor and test. |

## Confidence Scale

| Confidence | Use when |
|---|---|
| High | The conclusion is directly supported by supplied tables, screenshots, formulas, or telemetry. |
| Medium | The conclusion follows from visible system relationships but exact values are missing. |
| Low | The conclusion is a genre-informed hypothesis and should be validated before acting. |
