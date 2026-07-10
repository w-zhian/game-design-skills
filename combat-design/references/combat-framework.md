# Combat Design Framework

Use this reference when designing combat mechanics, skill systems, and encounters.

## 1. Combat Paradigm Decision Tree

```
Is combat real-time?
├── Yes → Player skill matters
│   ├── Action-heavy (souls, musou) → Frame data, i-frames, hitboxes
│   ├── Tactical (tower defense) → Placement, timing, target priority
│   └── Hybrid (action card) → Real-time + build preparation
└── No → Strategy matters
    ├── Turn-based (JRPG) → Action economy, turn order, team comp
    ├── Card battler → Hand management, resource sequencing
    └── Auto-battler → Build composition, stat thresholds
```

## 2. Damage Model Library

### Subtract Formula (减法公式)
`damage = attack - defense`
- Good for: linear power growth, readable breakpoints
- Risk: defense stacking creates immortality at high values
- Use when: you want clear "defense breaks" as progression gates

### Multiply Formula (乘法公式)
`damage = attack * (1 - defense / (defense + constant))`
- Good for: smooth scaling, no immortality, common in modern designs
- Risk: marginal value of defense is non-linear (hard for players to read)
- Use when: you want long-term scaling without hard caps

### Divide Formula (除法公式)
`damage = attack * attack / (attack + defense)`
- Good for: symmetric attack/defense, elegant at all scales
- Risk: identical damage ratio at all power levels (boring if not varied)
- Use when: you want elegant mathematical properties and symmetric combat

### Hybrid Formula
`damage = (attack - flat_reduction) * (1 - percentage_reduction)`
- Good for: layered defense, multiple counterplay paths
- Risk: complexity spiral, hard to tune
- Use when: you need both flat breakpoints and percentage scaling

## 3. Skill Design Checklist

For each skill/ability, answer:

| Dimension | Question |
|-----------|----------|
| Decision | What choice does this skill create? When does the player choose to use it? |
| Cost | What does it cost? (mana, cooldown, positioning, risk) |
| Effect | What does it do? (damage, control, utility, buff, debuff) |
| Counter | What beats this skill? (interrupt, dodge, cleanse, out-range) |
| Progression | How does it change with investment? (new tier effect vs bigger number) |
| Readability | Can the player understand it in one use? |
| Synergy | What does it combo with? What does it conflict with? |
| Differentiation | Why would I pick this over another skill in the same slot? |

## 4. Boss Design Template

### Phase Structure
| Phase | HP Range | Behavior Change | New Mechanics | Intensity |
|-------|----------|-----------------|---------------|-----------|
| Phase 1 | 100-70% | Slow, telegraphed attacks | Basic dodge pattern | Low |
| Phase 2 | 70-40% | Faster, adds projectiles | AoE + positioning check | Medium |
| Phase 3 | 40-10% | Enrage, mechanic overlap | Combined mechanics | High |
| Phase 4 | 10-0% | Final check | DPS race or survival | Extreme |

### Encounter Design Principles
- **Teach then test**: Phase 1 teaches the mechanic, Phase 2 adds pressure, Phase 3 combines
- **Punish, don't kill**: Failure should cost resources, not instant death (unless genre demands it)
- **Readable telegraphs**: Color, audio, and animation must all signal the same thing
- **Multiple solutions**: If there's only one way to win, it's a puzzle, not a fight

## 5. Role Differentiation Matrix

| Role | Core Fantasy | Primary Stat | Unique Decision | Counter Role |
|------|-------------|---------------|-----------------|--------------|
| Tank | "I protect" | Defense/HP | When to absorb vs when to reposition | Burst DPS |
| DPS | "I destroy" | Attack/Crit | When to commit vs when to disengage | Control |
| Healer | "I sustain" | Healing/Shield | When to heal vs when to buff | Burst |
| Control | "I dictate terms" | CC/Debuff | When to lock down vs when to spread | Tank |
| Utility | "I enable" | Buffs/Utility | What to enable vs what to save | (varies) |

## 6. Combat Balance Red Flags

- **One-stat dominance**: Speed or crit invalidates all other stat choices
- **Immortality stacking**: Defense/healing creates unkillable builds
- **Burst meta**: One-shot combos remove counterplay
- **Sponge enemies**: Difficulty = HP inflation, not mechanic complexity
- **Action economy abuse**: Extra turns/actions invalidate balance
- **Mandatory builds**: One team comp beats all content
- **Trap choices**: Skills that look good but are mathematically inferior

## 7. TTK Calibration Reference

| Genre | Expected TTK (normal enemy) | Expected TTK (elite) | Expected TTK (boss) |
|-------|---------------------------|---------------------|---------------------|
| Action RPG | 3-8 sec | 15-30 sec | 2-5 min |
| Turn-based JRPG | 2-4 turns | 6-10 turns | 15-30 turns |
| Card battler | 3-6 turns | 8-12 turns | 15-25 turns |
| Tower defense | Varies by wave | Varies | N/A (base defense) |
| Musou/horde | 1-3 sec (mobs) | 10-20 sec (officers) | 3-8 min |

These are genre benchmarks, not rules. Always calibrate to the specific game's pacing.
