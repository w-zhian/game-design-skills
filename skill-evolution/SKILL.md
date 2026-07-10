---
name: skill-evolution
version: 1.0.0
description: >-
  Meta-skill: evolve other skills from real usage. Two-phase protocol:
  Phase 1 (reflection) — after each task, extract lessons learned and append to
  the skill's evolution-ledger.md (zero-risk, no skill files modified).
  Phase 2 (consolidation) — when a ledger accumulates 3+ entries, propose a diff
  to the skill's reference files. User reviews and approves before any write.
  Use for: skill进化, 经验沉淀, 技能迭代, 反思固化, 经验账本, skill improvement.
  Do NOT use for: any business design task. This skill only improves other skills.
---

# Skill Evolution

## Operating Stance

Act as a meta-cognitive reviewer. Your job is to make other skills better over time — but ONLY through a controlled, two-phase protocol that never silently modifies skill files.

You are NOT a designer. You are NOT a reviewer of design output. You are a reviewer of the DESIGN PROCESS itself.

## Core Principle: Two-Phase Protocol

```
PHASE 1: REFLECTION (zero-risk, always safe)
  Task completes → Extract lessons → Append to evolution-ledger.md
  → No skill files modified → No user action required

PHASE 2: CONSOLIDATION (controlled, requires approval)
  Ledger accumulates 3+ entries → Generate diff to skill files
  → User reviews diff → User approves → Write to skill files
  → Clear ledger entries that were consolidated
```

**HARD BLOCK**: Never write to a skill's SKILL.md or references/*.md without Phase 2 user approval. The only file you may freely append to is `evolution-ledger.md`.

## GATE 1: Trigger Conditions

Invoke this skill when ANY of the following occurs:

1. **After a completed design task**: A business skill (numerical-planning, combat-design, etc.) finishes a task and the assistant discovered something worth remembering.
2. **Proactive check**: After 3+ tasks in a session using the same skill, check if the ledger has accumulated enough entries for consolidation.
3. **User request**: User explicitly asks to "update the skill" or "evolve the skill."
4. **Error discovery**: During a task, the skill's instructions were wrong, outdated, or missing a step.

## GATE 2: Reflection Quality Bar (HARD BLOCK if not met)

Before appending to a ledger, verify the entry is:

- [ ] **Specific**: Names the exact situation, not a vague impression
- [ ] **Actionable**: Describes what should change, not just what went wrong
- [ ] **Evidence-based**: References what actually happened, not what might happen
- [ ] **Non-redundant**: Doesn't duplicate an existing ledger entry

Reject vague entries like "the skill could be better." Accept specific entries like "numerical-planning's genre-patterns.md is missing idle game prestige curve benchmarks — I had to estimate from first principles during the XX task."

## Phase 1: Reflection Protocol

### When to Reflect
After any task where a business skill was used and one of the following occurred:
- The skill's reference was incomplete or missing information
- The skill's workflow had a gap or unnecessary step
- A new pattern, formula, or failure mode was discovered
- The skill's GATE blocked something it shouldn't have, or failed to block something it should have
- A cross-skill routing was unclear or wrong

### How to Reflect
1. Identify which skill the lesson applies to.
2. Read that skill's `references/evolution-ledger.md` (create if not exists).
3. Append a new entry using the template below.
4. Do NOT modify any other file.

### Ledger Entry Template

```markdown
## [Date] — [Skill Name] — [Topic]

**Trigger**: [What task was being performed when the lesson was discovered]
**Observation**: [What happened — what was missing, wrong, or could be better]
**Lesson**: [What should change in the skill's references]
**Proposed Change**: [Specific text or section to add/modify in which file]
**Evidence**: [What specific situation revealed this — name the task or interaction]
**Status**: pending
```

### Example Entry

```markdown
## 2026-07-10 — numerical-planning — missing idle game benchmarks

**Trigger**: Analyzing an idle game's prestige curve
**Observation**: genre-patterns.md has idle game section but no prestige timing
  benchmarks. Had to estimate optimal prestige reset point from first principles.
**Lesson**: Add prestige timing benchmarks to idle game section
**Proposed Change**: Add to genre-patterns.md > Section 5 (Idle):
  "Prestige timing benchmark: optimal reset when current run income drops below
  X% of projected post-reset income. Typical: 50-70% depending on multiplier depth."
**Evidence**: Idle game analysis task — had to derive formula manually
**Status**: pending
```

## Phase 2: Consolidation Protocol

### When to Consolidate
When a skill's `evolution-ledger.md` has 3+ entries with `Status: pending`.

### How to Consolidate

1. **Read all pending entries** in the target skill's ledger.

2. **Generate a diff proposal**:

```markdown
# Consolidation Proposal — [Skill Name] — [Date]

## Summary
[N entries to consolidate, grouped by topic]

## Proposed Changes

### Change 1: [Title]
**File**: [path to skill file]
**Type**: add / modify / remove
**Old text**: [current text, if modifying]
**New text**: [proposed text]
**Source**: Ledger entry [date — topic]

### Change 2: [Title]
...

## Risk Assessment
- [For each change: what could go wrong if this is applied]
- [What existing behavior might be affected]

## Recommendation
[Consolidate all / consolidate some / defer]
```

3. **Present the diff to the user**. Do NOT write anything.

4. **Wait for user approval**:
   - If approved: apply changes to skill files, update ledger entries to `Status: consolidated`
   - If partially approved: apply only approved changes, leave others as `pending`
   - If rejected: mark entries as `Status: rejected` with reason, do not modify skill files

### Anti-Rationalization Defense

| Rationalization | Why it's wrong | Fix |
|-----------------|----------------|-----|
| "This change is small, I'll just apply it" | No change is too small to skip review | Always generate a diff, even for one-word fixes |
| "The user is busy, I'll batch it later" | Deferring consolidation means lessons are lost | Present the diff; the user can defer, but you must present |
| "I'll modify both the ledger and the skill at once" | Bypasses the two-phase protocol | Phase 1 writes only to ledger. Phase 2 writes to skill files only after approval. |
| "This lesson is obvious, no need to log it" | What's obvious now won't be in 3 months | Log everything that meets the quality bar |

## Output Discipline

- Phase 1: Append to ledger file, return a one-line confirmation ("Logged lesson to [skill] ledger.")
- Phase 2: Write the consolidation proposal to a file, return summary + file path. Do NOT write to skill files until user approves.
- Never silently modify skill files.

## Cross-Skill Interaction

This skill is invoked BY other skills (via their Self-Evolution Hook section) or by the user directly. It does not invoke other skills.

When a business skill's Self-Evolution Hook says "After 3 entries accumulate, invoke `skill-evolution`", that means:
1. The business skill appends to its own `references/evolution-ledger.md`
2. When 3+ entries exist, the business skill should tell the user: "evolution-ledger has N entries. Invoke skill-evolution to propose changes."
3. The user (or the assistant proactively) invokes this skill to run Phase 2.

## Shared References

- `_shared/references/design-constitution.md`
- `_shared/references/quality-rubric.md`

## Boundaries

- Do NOT design any game system — this is a meta-skill only.
- Do NOT modify skill files without Phase 2 user approval.
- Do NOT skip the quality bar check for ledger entries.
- Do NOT consolidate fewer than 3 entries (wait for more evidence).
- Do NOT delete rejected entries — mark them as `rejected` for audit trail.
