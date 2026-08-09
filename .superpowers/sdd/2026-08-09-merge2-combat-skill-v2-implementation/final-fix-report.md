# Final review fix wave 报告

## 状态

Final review brief 的四项缺口已在允许范围内关闭：冻结 v1 的五个 RED Prompt 已获得可审计的 fresh run 证据；恢复率/相邻阶段转化已改为 distinct instance 完成口径；研究文档的精确设计值已按证据层级标记并绑定项目数据替换；`near_fail_condition_version` 已进入事件、映射与数据质量规则。

## RED 五次有效运行

所有有效运行都使用 `fork_turns=none`、`gpt-5.6-terra`、`high`，只收到冻结 v1 Skill 定位、对应原始自然 Prompt；retry run 另有“不写文件、只在最终回答作答”的运行隔离。没有提供 v2、评分锚点、RED 预期或 intended fix。

| Prompt | Canonical run locator | 结果 | 字段分 |
|---|---|---:|---|
| P1 A 路线 60 秒夜间防守 | `/root/final_fix_wave/red_p1` | Pass | `2/2/2/2/2/1` |
| P2 武器链跨入战斗 | `/root/final_fix_wave/red_p2` | Pass | `2/2/2/2/2/2` |
| P3 B/C 同敌异构 | `/root/final_fix_wave/red_p3_retry` | Pass | B `2/2/2/2/2`；C `2/2/2/2/2`；不可共用/非换皮 `2/2` |
| P4 浪漫餐厅反例 | `/root/final_fix_wave/red_p4_retry` | Pass | `2/2/2/2/2` |
| P5 无项目数据的 TTK 曲线 | `/root/final_fix_wave/red_p5_retry` | **Fail** | `2/2/0/2/1` |

共 34 个必需字段，唯一 0 分是 P5 阶段目标：回答给出“教学/首局、常规局、高风险局/关底”等局际难度层，没有给出单局开局、中段、收束的曲线目标。P1 与 P5 的 1 分均保留真实数据缺口，没有事后补分。`01-red-baseline.md` 登记了每项原始回答摘录、字段理由和 Pass/Fail；`03-green-results.md` 只同步 RED→GREEN 对比，GREEN 原始回答与评分未修改。

### 污染运行隔离处置

- `/root/final_fix_wave/red_p3` 与 `/root/final_fix_wave/red_p5` 误写冻结 fixture，两次运行全部作废，不计入答案证据或评分。
- 使用污染前已知副本的逐行差异，通过 `apply_patch` 仅移除两处污染增量；没有用 shell 覆盖或猜测恢复。
- 恢复后 fixture 与副本逐行一致，二者 SHA256 均为 `4154CD71354E3A23979CD32F52A4B2000CFEBF390C43F03DBA16A4A0A194E8F8`。
- P3/P5 在恢复后加只读隔离重跑；为排除同波次时序疑点，P4 也在恢复后重跑。每轮之后 hash 均保持不变。

## 证据标签审计

- `00-research-plan.md`：固定 `[OBSERVED]` / `[INFERRED]` / `[HYPOTHESIS]` 定义，明确日期、章节、出版年份、官方版本号和来源计数不机械误标。
- `01-shared-market.md`：市场报告/商店事实与结构推断分离；区域顺序、跨系统数量、首周教学和首会话时限标为假设，并绑定分区域 cohort、机制到达与因果复述。
- `02-cozy-shelter.md`：完整复核受众、循环/战斗时长、订单/生产器/内容量、素材配比、价格、LiveOps 节奏、FTUE、MVP、D1/D7 与产能门槛。reviewer 点名的“每天一次、45–90 秒”已就近标假设，并以本项目会话、完成/退出和战后回流替换。
- `03-mythic-caravan.md`：受众、会话/战斗、主链/伙伴/模块规模、素材首日/首周承诺、价格/LiveOps、内容骨架、MVP 周期与否决线均就近标假设，并绑定行为、制作工时、内容消耗或分群数据。
- `04-wasteland-convoy.md`：受众、广告/战斗/远征时长、主链/车辆/事件规模、路线节点、联盟/赛季、素材数量、研发周期、D7 与立项门槛均就近标假设。reviewer 点名的 L0 `3—20 秒` 已绑定广告位时长、完播、规则识别和点击/安装数据。
- `05-failures-and-tensions.md`：创意真实性比例与 `3+2` 货币上限标假设，并绑定玩法时长、留存、货币识别和 UI 数据。
- `06-validation-and-timeline.md`：Stage 0—3 的素材数、闭环时长、内容量、D1/D7/D30、教程/跨系统门槛、运行周期与路线 Kill Criteria 均标假设并说明替换数据；市场时间线事实/推断分离。
- `07-synthesis.md`：来源统计为观察；货币、LiveOps 配比、阶段规模、首周承诺、D7/D30 与时间尺度等精确输出标假设并绑定替换数据。

审计原则是把无本项目实测支持的精确路线/素材/时长/比例/内容规模/门槛改为可替换假设，同时保留报告年份、官方版本与来源统计为观察事实。

## 公式与 schema 修复

- `RecoveryCompletion_(s,v)` 分母改为至少进入过 recovery 的 distinct `flow_instance_id`；分子是其中至少一次以 `completion_reason=completed` 退出 recovery 的 distinct 实例。暂停后重入不重复计数。
- `TransitionRate_(s,v,p→q)` 只使用从 p 完成退出的 distinct 实例；`paused` / `interrupted` / `expired` 与重复进入单列，不混入完成转化。
- 外置事件映射和数据质量规则使用同一分组/去重口径。
- `combat_resolved` 最低字段增加 `near_fail_condition_version`；指标映射和数据质量规则禁止把条件版本变化前后的历史 cohort 混算，缺版本局进入质量报告。

## 验证命令与输出

1. RED 结构检查：`red_locators_unique=5`；`red_field_scores=34 zeros=1 invalid=0`；RED summary `PASS`；GREEN 中 RED 对照 `PASS`。
2. Fixture：当前与污染前副本 `Compare-Object=IDENTICAL`；双方 SHA256 均为 `4154CD71354E3A23979CD32F52A4B2000CFEBF390C43F03DBA16A4A0A194E8F8`。
3. 公式/schema 定位：`RecoveryCompletion`、`TransitionRate`、distinct `flow_instance_id`、完成/暂停/中断分离，以及 `near_fail_condition_version` 的事件、映射、数据质量位置均命中。
4. 研究点名位置与代表性精确值定位：`02` 的每日/45–90 秒、`04` 的 L0 3–20 秒、`06` 的 80%/70% 与 D1/D7/D30、三路线内容/MVP 周期均命中 `[HYPOTHESIS]` 和替换数据。
5. 允许范围断言：`allowed_scope=PASS`。
6. Windows/macOS/Linux 本地绝对路径扫描：`absolute_paths=0`。
7. 真实占位符扫描（TODO/TBD/FIXME/CHANGEME/REPLACE_ME/PLACEHOLDER/XXX/angle-template）：`true_placeholders=0`。正文中“原型占位”或“品类占位”是被审计内容描述，不是未替换模板。
8. 首次 `git diff --check` 发现两处 trailing whitespace，定位修复后重跑退出码 0；仅有 Git 的 LF→CRLF 工作区提示，无空白错误。

仓库没有适用于这些 Markdown 合同的自动化测试套件；以上为 brief 指定的结构、内容、路径、fixture 与 diff 检查。

## 提交

- 消息：`fix: close merge2 release review gaps`
- 范围：上述允许文件与本报告；不修改主 `SKILL.md`、README、manifest 或 GREEN 原始回答/评分。
- 提交哈希不自写入同一提交，避免自引用导致哈希变化；最终哈希在交付回报中登记。
- 未 push。

## 顾虑

- 真实新 RED 只让 P5 失败；P1—P4 已由 v1 泛化能力答到 Pass，因此不能再声称这四项存在字段级 RED→GREEN 改善。文档已如实披露。
- P1 的正式样本/观察窗，以及 P5 的测试版本、主/护栏、样本/窗口和数值否决线仍须由先导样本登记；当前设计数字只能作为 `[HYPOTHESIS]`。
- 研究审计保证证据口径与替换路径，不证明路线规模、留存、经济或产能目标已经被项目数据验证。
