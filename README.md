# Game Design Skills

游戏策划可自进化的 Skill 包，面向 Claude Code / Codex / WorkBuddy 等 AI Agent 工作台。

## 设计理念

每个 Skill 是**独立的、有边界的、可自进化**的能力单元：

- **独立**：一个 skill 只管一个领域，不交叉
- **有边界**：frontmatter 明确写 "Do NOT use for"，路由到正确 skill
- **可自进化**：通过 `skill-evolution` 元 skill 实现"反思→固化"两阶段学习

## Skill 清单

| Skill | 版本 | 职责 | 不负责 |
|-------|------|------|--------|
| `numerical-planning` | 2.0.0 | 属性/成长曲线/公式/经济/平衡设计（只设计不落表） | 配表落地（用 table-config）、战斗机制设计（用 combat-design） |
| `combat-design` | 1.0.0 | 战斗机制/技能/BOSS/伤害模型/战斗平衡 | 经济产出消耗（用 economy-design）、数值公式推导（用 numerical-planning） |
| `system-design` | 1.0.0 | 模块划分/UI流程/系统依赖/配表结构 | 数值平衡（用 numerical-planning）、核心循环设计（用 gameplay-design） |
| `economy-design` | 1.0.0 | 资源/货币/产出消耗/定价/商业化边界 | 战斗数值（用 numerical-planning）、系统架构（用 system-design） |
| `gameplay-design` | 1.0.0 | 核心循环/关卡/活动/奖励/难度曲线 | 系统模块设计（用 system-design）、数值推导（用 numerical-planning） |
| `qa-review` | 1.0.0 | 跨模块一致性/配表校验/边界检查 | 设计实现（各业务 skill 负责） |
| `skill-evolution` | 1.0.0 | 元 skill：从使用中反思→固化经验 | 任何业务设计 |

## 架构

```
game-design-skills/
├── README.md                        ← 本文件
├── _shared/                          ← 跨 skill 共享的引用
│   └── references/
│       ├── design-constitution.md    ← 设计宪法：个人设计原则与红线
│       ├── quality-rubric.md         ← 质量评分标准
│       ├── feature-brief-template.md    ← 功能简报模板
│       ├── system-design-doc-template.md ← 系统设计文档模板
│       └── playtest-report-template.md   ← 试玩报告模板
├── numerical-planning/               ← 数值规划（只设计不落表）
│   ├── SKILL.md
│   └── references/
│       ├── analysis-framework.md         ← 七层系统地图 + 九维审计透镜
│       ├── genre-patterns.md             ← 12品类数值模式库
│       ├── report-template.md            ← 快速/深度报告模板
│       ├── formula-toolkit.md           ← 五特性模型 + 公式选择决策 + 配表生成标准
│       ├── survivor-config-templates.md  ← 割草/幸存者类4张核心配表模板
│       ├── survivor-numeric-framework.md ← 三层DPS体系 + 涌现约束平衡 + 数字膨胀边界
│       ├── cross-genre-framework.md     ← 六维数值分析法 + 公式决策树 + 安全边界
│       └── idle-growth-framework.md     ← 海外Idle vs 国内放置 + 离线收益四模型 + Prestige
├── combat-design/                    ← 战斗设计
│   ├── SKILL.md
│   └── references/
│       ├── combat-framework.md          ← 伤害模型/TTK/角色差异/Boss设计
│       ├── monte-carlo-diagnostics.md  ← 六维诊断体系 + 模拟规模标准 + 报告结构
│       └── action-rpg-combat.md         ← 动作RPG战斗手感 + Boss四阶段 + 角色差异化
├── system-design/                    ← 系统设计
│   ├── SKILL.md
│   └── references/
│       ├── system-framework.md          ← 系统边界/依赖图/配表结构
│       └── cross-genre-mental-models.md ← 品类基因论 + 循环层级诊断 + 融合可行性矩阵
├── economy-design/                   ← 经济设计
│   ├── SKILL.md
│   └── references/
│       ├── economy-framework.md         ← 资源流/产出消耗/定价模型
│       └── slg-economy-framework.md     ← 五层资源分类 + 鲸鱼生态 + X+SLG融合 + 赛季重置
├── gameplay-design/                  ← 玩法设计
│   ├── SKILL.md
│   └── references/
│       ├── core-loop-framework.md      ← 核心循环/元循环/决策密度
│       ├── content-framework.md         ← 关卡节奏/内容配方/难度曲线
│       └── sanguo-troop-design.md       ← 一队三将/统帅值/武将协同矩阵/兵种差异化
├── qa-review/                        ← 质量审查
│   ├── SKILL.md
│   └── references/
│       ├── qa-checklist.md             ← 跨模块检查清单
│       └── config-table-analysis.md    ← 配置表分类规则 + 产出消耗模拟 + 割草类检查
└── skill-evolution/                  ← 元 skill：自进化
    ├── SKILL.md
    └── references/
        └── evolution-protocol.md    ← 两阶段学习协议
```

## 升级历史

- **v2.1.0** (2026-07-10): 整合 WorkBuddy 26个品类skill的核心内容到各skill的references/。新增13个引用文件，覆盖Monte Carlo诊断、配置表分析、跨品类框架、SLG经济、增量成长、动作RPG战斗、三国群英传设计等。
- **v2.0.0** (2026-07-10): 从单体 `wangzhao-game-design-director` 拆分为 7 个独立 skill + skill-evolution 元 skill。参照 WangHNoob/design-skills 架构，加入 GATE 硬门控、输出纪律、版本号、自进化机制。
- **v1.0.0**: 单体 `wangzhao-game-design-director` + `analyze-game-numerics`

## 作者

决明子 (w-zhian) — 3年数值策划，专注 MMO/RPG/SLG/塔防/卡牌/Roguelike 多品类数值设计。
