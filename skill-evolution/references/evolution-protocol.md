# Evolution Protocol Reference

Detailed protocol for the two-phase skill evolution mechanism.

## 1. Ledger File Standard

Each business skill maintains its own `references/evolution-ledger.md`. The file is:

- **Append-only**: New entries are added at the bottom, never overwrite
- **Never deleted**: Rejected entries stay for audit trail
- **Status tracked**: Each entry has `pending` / `consolidated` / `rejected` status

### Ledger File Header
```markdown
# Evolution Ledger — [Skill Name]

This file is append-only. Do not overwrite existing entries.
Entries with `Status: pending` are awaiting consolidation (Phase 2).
Entries with `Status: consolidated` have been applied to skill files.
Entries with `Status: rejected` were reviewed and declined.

---
```

## 2. Entry Quality Rubric

Before appending, check the entry against this rubric:

| Dimension | Accept | Reject |
|-----------|--------|--------|
| Specificity | Names the exact situation and file | "The skill could be better" |
| Actionability | Describes a concrete change | "Something should be added" |
| Evidence | References a real task or interaction | "I think this might be useful" |
| Non-redundancy | Doesn't duplicate existing entries | Same observation repeated |
| Scope | Applies to this skill only | Applies to a different skill (route there instead) |

## 3. Consolidation Decision Framework

When deciding whether to consolidate entries:

| Situation | Action |
|-----------|--------|
| 3+ entries, all on same topic | High consolidation priority — likely a real gap |
| 3+ entries, scattered topics | Medium — evaluate each individually |
| Entries contradict each other | Do NOT consolidate — flag for user discussion |
| Entry proposes removing existing content | High scrutiny — what breaks if removed? |
| Entry proposes adding new section | Medium — does it fit the existing structure? |
| Entry proposes modifying GATE | Critical — GATE changes affect all future tasks |

## 4. Diff Format Standard

```markdown
# Consolidation Proposal

## Metadata
- Skill: [name]
- Date: [date]
- Entries: [count]
- Reviewer: skill-evolution

## Changes

### Change [N]: [Title]

**File**: references/[filename].md
**Type**: [add / modify / remove]
**Location**: [section heading or line reference]

**Current content** (if modify/remove):
```
[exact current text]
```

**Proposed content**:
```
[exact proposed text]
```

**Rationale**: [Why this change, referencing the ledger entry]
**Risk**: [What could break]
**Source**: Ledger entry [date — topic]

---

## Overall Risk Assessment
[Summary of combined risk]

## Recommendation
[Consolidate all / Consolidate subset / Defer]
```

## 5. Post-Consolidation Audit

After applying approved changes:
1. Verify the skill file was modified correctly (read it back)
2. Update ledger entries from `pending` to `consolidated`
3. Add a note to the ledger:
```markdown
### Consolidation Log
- [Date]: Consolidated [N] entries into [files modified]. Changes: [summary]
```
4. If any entry was rejected, add reason:
```markdown
**Rejection reason**: [Why this was not applied]
```

## 6. Frequency Guidelines

| Phase | Frequency | Trigger |
|-------|-----------|---------|
| Phase 1 (reflection) | After every non-trivial task | Business skill's Self-Evolution Hook |
| Phase 2 (consolidation) | When ledger hits 3+ pending entries | Proactive check or user request |
| Full skill audit | Monthly | User explicitly requests |

## 7. Safety Guarantees

- **No silent writes**: Skill files are NEVER modified without user-approved diff
- **No data loss**: Ledger entries are NEVER deleted, only status-changed
- **No bypass**: GATE changes require explicit Phase 2 approval with risk assessment
- **Full audit trail**: Every change has a ledger entry, a proposal, and an approval record
