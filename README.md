# game-design-skills

面向游戏策划的可自进化 Qoder 技能包，转换自 GitHub 仓库
[w-zhian/game-design-skills](https://github.com/w-zhian/game-design-skills)。

## 功能概述

每个 Skill 是独立的、有边界的、可自进化的能力单元：

- **独立**：一个 skill 只管一个领域，不交叉
- **有边界**：frontmatter 明确写 "Do NOT use for"，路由到正确 skill
- **可自进化**：通过 skill-evolution 元 skill 实现"反思→固化"两阶段学习

## 包含技能

| Skill | 版本 | 职责 |
| --- | --- | --- |
| numerical-planning | 2.0.0 | 属性/成长曲线/公式/经济/平衡设计（只设计不落表） |
| combat-design | 1.0.0 | 战斗机制/技能/BOSS/伤害模型/战斗平衡 |
| system-design | 1.0.0 | 模块划分/UI流程/系统依赖/配表结构 |
| economy-design | 1.0.0 | 资源/货币/产出消耗/定价/商业化边界 |
| gameplay-design | 1.0.0 | 核心循环/关卡/活动/奖励/难度曲线 |
| qa-review | 1.0.0 | 跨模块一致性/配表校验/边界检查 |
| skill-evolution | 1.0.0 | 元 skill：从使用中反思→固化经验 |
| article-curation | 1.0.0 | 每日从 GameRes 游戏策划版块摘取系统/战斗/关卡/数值方向优质文章，生成日报 |

## 支持文件

- 每个技能均保留其 `references/` 目录（共 21 个引用文件，如
  `formula-toolkit.md`、`combat-framework.md`、`economy-framework.md` 等）。
- 跨技能共享引用放在 `skills/_shared/references/`：设计宪法、质量评分标准、
  功能简报模板、系统设计文档模板、试玩报告模板。
- 各 SKILL.md 中对共享引用的路径已由 `_shared/references/...` 改写为
  `../_shared/references/...`，以匹配 `skills/_shared/` 的新相对位置。
- GameRes 老文知识蒸馏（v2.3.0 新增，源自 27088 帖全量索引中评分最高的方法论文章）：
  - `numerical-planning/references/gameres-probability-and-change.md` — 概率期望
    递推/循环模拟、正态伪随机、导数视角建模
  - `combat-design/references/gameres-combat-formulas-and-feedback.md` — 战斗力
    因式模型、回合制伤害公式 11 步流程、打击感反馈清单
  - `gameplay-design/references/gameres-level-experience-quantification.md` — 关卡
    数值四维度框架、玩家思维六问分析
  - `system-design/references/gameres-system-architecture-and-abstraction.md` —
    核心系统五层架构、体验抽象五特性与六方法、优化三板斧

## 来源与署名

- **Source**: https://github.com/w-zhian/game-design-skills
- **Author**: 决明子 (w-zhian) — 3年数值策划，专注 MMO/RPG/SLG/塔防/卡牌/Roguelike 多品类数值设计
- **上游版本**: v2.1.0 (2026-07-10)
- **Logo**: 源仓库未提供 logo，`assets/avatar.svg` 为本插件生成的游戏手柄图标。

## 省略文件

- 源仓库 `README.md`（其内容已整合进本文件，技能清单表保留）。
- 源仓库 `.gitignore`（与插件分发无关）。

## 备注

- skill-evolution 会在各技能目录下生成/追加 `evolution-ledger.md`，
  属于技能自身的自进化机制，安装后按 SKILL.md 内协议执行。
