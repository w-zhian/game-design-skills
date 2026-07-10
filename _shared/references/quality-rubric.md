# Game Design Quality Rubric

所有 skill 在最终交付前必须过一遍此质量评分表。

## Quality Dimensions

| Dimension | Strong | Weak |
|-----------|--------|------|
| Player decision | Names concrete choices and tradeoffs | Talks about fun or engagement vaguely |
| Loop coherence | Shows how action, reward, progression, and return connect | Lists features without causal links |
| System boundary | Defines what the feature owns and how it touches other systems | Lets one feature sprawl into everything |
| Tunability | Names knobs and expected side effects | Suggests broad redesign with no control surface |
| Validation | Gives playtest tasks, metrics, or observations | Says "test it" without specifying what to learn |
| Risk awareness | Names player segment, lifecycle stage, and failure mode | Gives universal verdicts |
| Production realism | Respects content, UI, engineering, and live-ops constraints | Depends on unlimited content or perfect balance |
| Numerical specificity | Uses exact formulas, ratios, and breakpoints | Uses adjectives like "too fast" or "too expensive" |
| Cross-module impact | Names which other systems are affected and how | Designs in isolation |

## GATE: Final Check (MUST pass before output)

- [ ] Does the answer name at least one thing to cut, defer, or simplify?
- [ ] Does each recommended reward reinforce a player decision?
- [ ] Are assumptions labeled?
- [ ] Are exact metrics avoided unless supplied?
- [ ] Is the next artifact clear?
- [ ] Does every numerical claim have a formula, ratio, or breakpoint — not just an adjective?
- [ ] Are cross-module dependencies named?

If any check fails, revise before output.
