# 战斗遥测与验证

> 职责：定义最小事件字典、四层验证、Kill Criteria 与跨 Skill 验收路线；不代替数据团队的最终 schema、隐私审查或实验平台规范。

## 目录

- 测量原则
- 公共字段
- 最小事件字典
- 四层验证
- Kill Criteria
- A/B/C 所有权冲突检查
- 跨 Skill 验收路由
- 数据质量与边界

## 测量原则

- `[OBSERVED]` 本框架要证明的不是“有人进入战斗”，而是 Merge/经营选择能被看懂、归因、改变决策并把玩家带回核心循环。
- `[INFERRED]` 事件只记录能够回答产品问题的字段。没有预先声明分析用途的对象坐标、逐帧状态、完整背包快照或文本输入不应默认采集。
- `[HYPOTHESIS]` 首版以事件时间线加关键状态快照为主；只有在定位 AI、路径或窗口问题时，才对受控样本开启高频轨迹。
- `[HYPOTHESIS]` 所有测试同时保留版本、路线、遭遇、玩家生命周期与实验分组，否则曲线不能比较。

## 公共字段

所有事件至少继承下表的必需基础字段；命名可由数据团队调整，但语义不可丢失。准备实例、正式战斗和外置流程使用不同上下文 ID，不得互相冒充。

| 字段 | 用途 | 最小化说明 |
|---|---|---|
| `event_time` | 排序与计算相对时间 | 使用服务端/客户端统一时间约定 |
| `anonymous_player_id` | 会话与回流串联 | 不使用直接身份信息 |
| `session_id` | 区分单次会话 | 返回前后台的切分规则需统一 |
| `content_version` | 区分资源、逻辑和配置版本 | 必须能回溯参数集 |
| `experiment_group` | 对照实验 | 无实验写明确的默认组 |
| `route_id` | A / B / C 或经批准的新路线 | 用于所有权冲突分析 |
| `player_stage` | 生命周期/章节分群 | 不记录无用途的完整账号档案 |

条件字段不应为补齐 schema 而写入无意义值：`encounter_id` 只在事件属于准备、正式战斗，或某个外置阶段明确关联单一遭遇时填写；低压回流、跨遭遇恢复、章节/日与周活动阶段允许省略。外置事件即使携带 `encounter_id`，它也只是阶段关联字段，不能代替 `flow_instance_id`。

### 上下文 ID 生命周期

| ID | 生成时机 | 使用范围 | 连接规则 |
|---|---|---|---|
| `prepare_instance_id` | 每次准备页实际进入时新生成 | `combat_prepare_viewed/changed/exited`，并由 `combat_started` 原样携带 | 同一次准备内保持不变；退出后再次进入必须新建，不复用旧值 |
| `combat_run_id` | 仅在 `combat_started` 时新生成 | 正式开战至结算、重试、回写和返回 Merge | 一个正式开战一个 ID；原样重试也生成新 ID，并用 `previous_combat_run_id` 连接 |
| `flow_instance_id` | 会话、章节/日、周活动各自开始时生成 | `outer_flow_phase_changed` | 与 `flow_scale`、`outer_flow_curve_version` 共同唯一；允许关联多个准备实例和战斗局 |

- `[HYPOTHESIS]` 准备上下文因开战、关闭、返回、切后台超时或切换遭遇而结束时发送 `combat_prepare_exited`；只有 `exit_reason=started` 且随后同一 `prepare_instance_id` 出现 `combat_started` 才算转化为正式战斗，其余原因记为放弃/中断准备。
- `[HYPOTHESIS]` 同一会话再次进入同一遭遇仍生成新的 `prepare_instance_id`；`previous_prepare_instance_id` 只用于连接紧邻的同遭遇重进，不跨会话串联。
- `[HYPOTHESIS]` `combat_retry_selected` 指向失败局；若玩家选择改配，下一次 `combat_prepare_viewed` 同时携带 `source_combat_run_id`，但使用新的准备实例 ID。

## 最小事件字典

### `outer_flow_phase_changed` — 外置流程阶段进入 / 退出

- 最低字段：必需基础字段、`flow_scale`（session / chapter_day / week）、按尺度命名空间化的 `outer_flow_curve_version`（例如 `session:v1` / `chapter_day:v1` / `week:v1`）、`flow_instance_id`、`phase_id`、`transition`（entered / exited）、`elapsed_active_time`、退出时的 `completion_reason`（completed / paused / interrupted / expired）、可选的 `encounter_id` / `prepare_instance_id` / `combat_run_id`。
- 回答：三种外置尺度各阶段持续多久、完成/中断在哪里、风险检验频次、恢复与回写是否闭合。
- 不采集：阶段内每个普通 UI 行为；已有专项事件只通过 ID 关联。
- 时钟：这里的 `elapsed_active_time` 是当前 `flow_instance_id` 自开始以来的累计活跃时钟。前后台暂停、跨会话离线和超过统一无操作阈值的时间不累计；恢复后的值从暂停点继续，不能用墙钟差或当前 `session_id` 时长替代。
- 切分与恢复：暂停/会话切分时用 `exited(completion_reason=paused)` 结束当前活跃段；章节/日、周实例若尺度版本声明的身份与恢复窗仍有效，则下次会话沿用同一 `flow_instance_id` 和 `outer_flow_curve_version`，对同阶段重新发 `entered`。单次会话尺度在新会话新建实例。活动过期、版本变化或超出恢复窗时关闭旧实例并新建，不能拼接累计时钟。
- 派生：阶段活跃时长按同一 `flow_scale + outer_flow_curve_version + flow_instance_id + phase_id` 配对每个 entered/exited 活跃段，并求 `exit.elapsed_active_time - enter.elapsed_active_time` 后累加；暂停间隔因此天然排除，未配对段只计中断率。
- 完成口径：恢复完成率的分母是至少进入过 recovery 的 distinct `flow_instance_id`，分子是其中至少一次以 `completion_reason=completed` 退出 recovery 的 distinct 实例。相邻阶段转化只纳入前一阶段完成退出的 distinct 实例；`paused` / `interrupted` / `expired` 和重复 `entered` 单列。

### `combat_prepare_viewed` — 准备页进入

- 最低字段：基础字段、新生成的 `prepare_instance_id`、可选 `previous_prepare_instance_id` / `source_combat_run_id`、`entry_source`、`visible_objective_id`、`visible_threat_tags`、`current_loadout_signature`。
- 回答：玩家看到了什么目标/敌情，从哪里进入，初始配置是什么。
- 不采集：未展示给玩家的隐藏敌人参数。

### `combat_prepare_changed` — 准备修改

- 最低字段：基础字段、`prepare_instance_id`、`change_type`、`from_option_id`、`to_option_id`、`slot_or_route_id`、`source_object_id`、`preview_changed`。
- 回答：玩家是否做取舍，改的是单位/设施、器具、站位、资源还是路线；预览是否反馈。
- 不采集：每次拖拽像素路径；只有最终有效修改和撤销需要记录。

### `combat_prepare_exited` — 准备退出 / 放弃

- 最低字段：基础字段、`prepare_instance_id`、`exit_reason`、`elapsed_prepare_active_time`、`changed_flag`、`next_destination`。
- 回答：准备实例是进入战斗、主动返回、切换遭遇还是超时放弃；反复进入不会被误合并成一局。
- 不采集：离开后的页面路径明细；只保留直接去向类别。

### `combat_started` — 战斗开始

- 最低字段：基础字段、`prepare_instance_id`、新生成的 `combat_run_id`、`final_loadout_signature`、`objective_initial_state`、`resource_initial_state`、`resource_accounting_version`、`threat_tags_shown`、`total_duration_target`。
- 回答：最终选择、可见情报与起始状态是什么。
- `[HYPOTHESIS]` `total_duration_target` 是该版本的原型配置，不代表实际结束时间。

### `combat_phase_entered` — 阶段进入

- 最低字段：基础字段、`combat_run_id`、`phase_id`、`elapsed_active_time`、`phase_trigger`、`objective_state`、`resource_state`。
- 回答：阶段在实际活跃时间的何处发生、由什么状态触发。`tau` 不在运行时写入，结算后用实际 `T` 派生。
- 不采集：五个阶段点不承担完整压力曲线；曲线由版本化快照重建。

### `combat_choice_effect_triggered` — 配置 / 输入产生可见效果

- 最低字段：基础字段、`combat_run_id`、`contract_id`、`source_object_id`、`trigger_mode`（automatic / manual）、`elapsed_active_time`、`effect_type`、`feedback_cue_id`、`target_or_zone`、`result_code`。
- 回答：自动配置或手动输入何时第一次真实生效、给了什么反馈，以及首次有效反馈时间。
- 不采集：普通伤害逐跳；只记录合同定义的可归因触发。

### `combat_unit_became_damageable` — 单位首次可被处理

- 最低字段：基础字段、`combat_run_id`、`unit_instance_id`、`unit_archetype_id`、`elapsed_active_time`、`availability_reason`。
- 回答：单位 TTK 的起点，区分出生、入场、无敌结束或暴露窗口。
- 不采集：单位位置轨迹或逐帧属性。

### `combat_unit_resolved` — 单位死亡 / 失效 / 逃离

- 最低字段：基础字段、`combat_run_id`、`unit_instance_id`、`unit_archetype_id`、`elapsed_active_time`、`resolve_reason`、`credited_contract_id`。
- 回答：TTK 终点、击杀/失效序列和前后哨兵区间；逃离与非击杀失效不得混成击杀。
- 不采集：每次受击；公式审计另走受控轨迹。

### `combat_intervention_window_changed` — 干预窗口曝光 / 关闭

- 最低字段：基础字段、`combat_run_id`、`window_id`、`window_state`（opened / closed）、`elapsed_active_time`、`cue_id`、`close_reason`；关闭时增加 `input_occurred`。
- 回答：窗口曝光次数、可响应时长、未输入率和输入延迟。
- 边界：事件只能证明信号已曝光和玩家是否响应；“玩家认知上已识别”仍需访谈或受控任务确认。

### `combat_intervention_used` — 主动干预

- 最低字段：基础字段、`combat_run_id`、`intervention_id`、`target_id_or_zone`、`window_id`、`time_since_window_open`、`resource_cost`、`immediate_result_code`。
- 回答：窗口曝光后玩家是否响应、选择何种目标、输入是否改变过程；认知识别需结合质化证据。
- 不采集：无结果差异的装饰点击。

### `combat_pressure_snapshot` — 压力组件快照

- 最低字段：基础字段、`combat_run_id`、`elapsed_active_time`、`snapshot_reason`（fixed_interval / state_change）、`sampling_policy_version`、`pressure_normalization_version`、`component_raw_aggregates`、`component_normalized`、`objective_state`、`resource_state`。
- 回答：结算后重建压力曲线，并计算峰值位置、斜率、方差与 `CurveMAE`。
- 不采集：敌人逐个坐标或逐帧状态；`sampling_policy_version` 只在固定采样点和声明的关键状态变化时记录聚合快照。

### `combat_objective_damaged` — 目标受损

- 最低字段：基础字段、`combat_run_id`、`objective_id`、`damage_source_type`、`normalized_loss`、`remaining_objective_value`、`preventable_by_contract_id`。
- 回答：损失来自哪类压力，是否有已公开的可改准备/干预。
- 不采集：除非公式审计需要，不上传每次普通单位伤害明细。

### `combat_resource_supplied` — 局内资源补充

- 最低字段：基础字段、`combat_run_id`、`resource_type`、`amount`、`supply_reason`、`source_object_id`、`resource_accounting_version`。
- 回答：累计可用资源的分母，区分初始携带与局内补给。
- 不采集：与本局合同无关的钱包或仓库余额。

### `combat_resource_consumed` — 资源消耗

- 最低字段：基础字段、`combat_run_id`、`resource_type`、`amount`、`amount_from_initial_pool`、`consume_reason`、`remaining_amount`、`source_object_id`、`resource_accounting_version`。
- 回答：哪种准备被何时消耗，并与初始量/局内供给分别计算保留与消耗口径。
- 不采集：与设计无关的资产钱包余额。

### `combat_resolved` — 胜负

- 最低字段：基础字段、`combat_run_id`、`result`、`elapsed_active_time`（实际 `T`）、`last_phase_id`、`objective_final_state`、`resource_final_state`、`resource_accounting_version`、`failure_reason_code`、`attribution_cards_shown`、`near_fail_flag`、`near_fail_condition_version`。
- 回答：为何结束、代价如何、系统向玩家解释了什么。
- `[HYPOTHESIS]` `near_fail_flag` 必须引用 `near_fail_condition_version` 指向的版本化 `near_fail_condition`，不可由客户端随意判定。

### `combat_attribution_card_interacted` — 因果卡展示 / 展开 / 选项

- 最低字段：基础字段、`combat_run_id`、`card_id`、`contract_id`、`interaction`（shown / expanded / next_action_selected / dismissed）、`elapsed_since_resolve`。
- 回答：因果卡是否真正展示、被展开，以及玩家是否从卡片进入可改项。
- 不采集：卡片全文或玩家自由文本。

### `combat_retry_selected` — 重试 / 改配

- 最低字段：基础字段、`previous_combat_run_id`、`retry_mode`、`time_since_resolve`、`changed_contract_types`、`recovery_cost_type`。
- 回答：玩家是原样重试、改配、降低难度、撤退还是稍后返回；失败是否产生新决定。
- 不采集：没有行为差异的重复按钮曝光。

### `world_writeback_applied` — 世界回写

- 最低字段：基础字段、`source_combat_run_id`、`writeback_type`、`affected_world_object_id`、`next_action_ids_exposed`、`reversible_flag`。
- 回答：战斗如何改变人、空间、伙伴、车队、地图、生产或订单。
- 不采集：完整世界状态；只记录本局产生的变化。

### `merge_returned_after_combat` — 返回 Merge

- 最低字段：基础字段、`source_combat_run_id`、`return_delay_active_time`、`return_entry`、`first_merge_goal_id`、`goal_linked_to_writeback`。
- 回答：玩家是否回到主棋盘、为何回来、首个目标是否由战斗后果驱动。
- 不采集：与该回流问题无关的长期棋盘历史。

### 指标 → 最小事件对应

| 指标 / 问题 | 必需事件 | 派生边界 |
|---|---|---|
| 外置阶段时长、频次、恢复/回写 | `outer_flow_phase_changed` + 回写/返回事件 | 必须配对同 `flow_scale + outer_flow_curve_version + flow_instance_id + phase_id` 的进入/退出活跃段；恢复完成和相邻阶段转化按 distinct `flow_instance_id` 计算，只接受 `completion_reason=completed`，暂停/中断/重入单列；版本间不混算 |
| 准备转化、放弃与反复进入 | 准备 viewed/changed/exited + `combat_started` | `prepare_instance_id` 不复用；正式开战才有 `combat_run_id` |
| TTK | `combat_unit_became_damageable` + `combat_unit_resolved` | 同 `unit_instance_id`；按死亡/失效/逃离分组 |
| 击杀间隔与首尾哨兵 | `combat_started` + `combat_unit_resolved(resolve_reason=kill)` + `combat_resolved` | 无击杀局单列，不并入普通区间 |
| 首次有效反馈 / 自动配置触发 | `combat_started` + `combat_choice_effect_triggered` + 因果卡事件 | 首次触发不自动等于玩家理解，需质化复核 |
| 窗口曝光、未输入与延迟 | `combat_intervention_window_changed` + `combat_intervention_used` | 匹配同一 `window_id`；缺关闭事件视为数据缺失 |
| 两种资源口径 | `combat_started` + 资源 supplied/consumed + `combat_resolved` | 只比较同一 `resource_accounting_version` |
| 压力峰值、斜率、方差、CurveMAE | `combat_pressure_snapshot` + `combat_resolved` | 结算后派生 `tau`；只比较同采样/归一化版本 |
| 近失败占比 | `combat_resolved` | 只比较同 `near_fail_condition_version`；条件版本变化前后的历史 cohort 不混算 |
| 因果卡展开与进入可改项 | `combat_attribution_card_interacted` | `shown`、`expanded`、`next_action_selected` 分开计数 |

## 四层验证

### 1. 看懂（comprehension）

核心问题：玩家是否理解目标、威胁、可用输入和准备项对应关系？

- 量化：准备页进入→开始/放弃、目标首次受损前退出、窗口曝光/未输入、自动/手动配置首次有效反馈时间；事件只证明曝光与响应，不把它冒充认知理解。
- 质化：开战前复述“要保护/送达什么”；首次受损后指出危险来源。
- `[HYPOTHESIS]` 若事件显示触发但玩家复述错误，判为看懂失败，不得按“系统正常生效”放行。

### 2. 归因（attribution）

核心问题：玩家能否说明哪个 Merge/经营选择造成哪个战斗结果？

- 量化：`combat_choice_effect_triggered` 与目标损失/资源口径/阶段结果的关联、因果卡展示→展开→下一动作、失败原因与改配类型的一致性。
- 质化：战后请玩家说出“最有帮助的一项准备”“一个失败点”“下次改什么”。
- `[HYPOTHESIS]` 只说“战力不够”“等级低”视为核心接口归因失败，除非本次测试本来就在验证普通成长门槛。

### 3. 决策（decision）

核心问题：信息是否促成可替代选择，而非所有人复制同一最优解？

- 量化：准备实例内修改率、配置熵、同配置跨词缀表现、窗口曝光→输入时机分布、失败后改配与原样重试比例。
- 质化：玩家能否说出至少两种方案的收益/代价，且选择与路线所有权一致。
- `[HYPOTHESIS]` 选择分布集中不自动等于失败；必须结合对手/路线是否相同和该方案是否在所有场景支配。

### 4. 回流（return）

核心问题：战斗后果是否自然创造新的 Merge/经营行动？

- 量化：三尺度 `outer_flow_phase_changed` 的恢复/回写完成、世界回写→返回 Merge、首个 Merge 目标与回写关联、修复/补给/培育/重装行为、稍后自然回流。
- 质化：玩家是否认为“我要回去处理这个后果”，而不是只为领取奖励。
- `[HYPOTHESIS]` 返回棋盘但首个目标与战斗无关，只能证明导航，不证明三环闭合。

## Kill Criteria

### 登记模板

```markdown
假设：[HYPOTHESIS]
目标路线 / 玩家分群：
测试版本与流量来源：
对照版本：
样本与运行窗口：[HYPOTHESIS，由先导样本与实验能力设定]

看懂主指标 / 通过阈值：[HYPOTHESIS]
归因主指标 / 通过阈值：[HYPOTHESIS]
决策主指标 / 通过阈值：[HYPOTHESIS]
回流主指标 / 通过阈值：[HYPOTHESIS]
所有权护栏 / 否决阈值：[HYPOTHESIS]

失败属于：参数问题 / 结构问题
允许改变的旋钮：
本轮不改变的合同：
复测必须产生的预期移动：
未通过后的动作：调参 / 重构 / 降级 / 删除 / 延后解锁
```

### 参数问题

- `[HYPOTHESIS]` 玩家理解目标与因果，但某阶段过早/过晚、资源过松/过紧、窗口难度不合适或单一配置过强。
- `[HYPOTHESIS]` 可以点名可调旋钮，并能预言它会移动哪个指标而不改变接口语义。
- 处理：路由专项 Skill，做一次隔离变量的调整与复测。

### 结构问题

- `[HYPOTHESIS]` 玩家在表现调整后仍无法复述 Merge → 战斗 → 回写关系。
- `[HYPOTHESIS]` 战斗输入不改变行为/空间/时机，胜负只由战力解释。
- `[HYPOTHESIS]` 失败没有可改项，或回流只能靠奖励/强制任务。
- `[HYPOTHESIS]` 该形态持续违背 A/B/C 核心所有权。
- 处理：停止该形态、降级为可解释结算或回到接口合同重构；不通过继续加养成层补救。

## A/B/C 所有权冲突检查

| 路线 | 必须被遥测/访谈证明 | 冲突信号 | 建议动作 |
|---|---|---|---|
| A Cozy-first | `[HYPOTHESIS]` 玩家记得被保护的人/空间，失败后愿意修复而非感到被强制考试 | 只谈战力；因害怕永久损失而回避战斗；付费装修受损 | 降低损失、强化具体对象归因；持续冲突则改灾害结算或删除战斗 |
| B Collection-first | `[HYPOTHESIS]` 玩家能指出伙伴与器具如何协同，并愿意换编成尝试 | 只谈稀有度；Merge 只产经验；不愿让人格化伙伴成为耗材 | 恢复伙伴身份、强化行为合同；持续冲突则降级角色池和战斗深度 |
| C Logistics-first | `[HYPOTHESIS]` 玩家把胜负关联到装载、路线、货损和是否继续 | 只谈英雄/基地战力；路线选择不变；广告操作首周消失 | 让载荷/路线进入常驻战斗；持续冲突则停止向 4X 扩展 |

## 跨 Skill 验收路由

| 发现 | 主责 Skill | 必须交付给 QA 的证据 |
|---|---|---|
| 技能、敌人、阶段、AI、反馈不可读 | `combat-design` | 行为规格、信号、失败点、录像与事件对齐 |
| TTK、EHP、DPS、压力权重、曲线与阈值 | `numerical-planning` | 公式、输入口径、分布、边界和版本参数 |
| 资源来源/消耗、恢复成本、战斗奖励冲击 | `economy-design` | source/sink、余量、零资源路径、事件冲击 |
| 会话、日/周节奏、入口和内容消耗 | `gameplay-design` | 核心循环、入口频次、阶段解锁、内容复用 |
| 跨模块合同与状态边界 | `system-design` | 状态机、所有者、写入顺序、失败回滚 |
| 内部一致、边界、A/B/C 冲突和放行 | `qa-review` | 检查矩阵、P0/P1/P2、未通过项与负责人 |

## 数据质量与边界

- `[HYPOTHESIS]` 校验事件唯一性、顺序、丢失、重复、断线恢复、前后台时间和版本一致性后再计算曲线。
- `[HYPOTHESIS]` 准备事件按 `prepare_instance_id` 串联；`combat_started` 同时携带准备实例并生成 `combat_run_id`；战斗、回写与返回事件再按该正式战斗 ID 串联。不能满足这条链的数据不用于转化或闭环结论。
- `[HYPOTHESIS]` 压力曲线只使用能连接 `combat_pressure_snapshot → combat_resolved`，且 `sampling_policy_version` / `pressure_normalization_version` 完整的局；`tau` 一律在结算后派生。
- `[HYPOTHESIS]` 外置曲线只使用能按 `flow_scale + outer_flow_curve_version + flow_instance_id + phase_id` 配对进入/退出的活跃段；验证累计时钟不含暂停/跨会话离线且恢复时不倒退。缺失退出单独进入中断率，不用于完整时长占比；不同尺度或版本不直接并表。
- `[HYPOTHESIS]` 外置恢复完成率的进入与完成均按 distinct `flow_instance_id` 去重；相邻阶段转化只纳入 `completion_reason=completed` 的实例。`paused` / `interrupted` / `expired` 和重复进入单独报告，不得改变完成转化分子或分母。
- `[HYPOTHESIS]` 近失败指标只使用同一 `near_fail_condition_version` 的 `combat_resolved`；版本缺失的局进入数据质量报告，条件版本变化前后的历史 cohort 不混算。
- `[HYPOTHESIS]` 录像/高频轨迹只对明示测试样本启用；常规版本只采固定/状态变化聚合快照，并遵守目标市场隐私、年龄与数据最小化要求。
- `[HYPOTHESIS]` 不用单一均值放行；至少查看分布、生命周期、胜负、配置、设备性能和 A/B/C 路线差异。
- `[HYPOTHESIS]` 遥测显示相关性时不得直接声称因果；正式改动用对照实验、隔离变量或重复可控样本验证。
