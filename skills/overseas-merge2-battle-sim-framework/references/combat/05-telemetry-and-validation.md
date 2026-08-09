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

所有事件至少继承以下公共字段；命名可由数据团队调整，但语义不可丢失。

| 字段 | 用途 | 最小化说明 |
|---|---|---|
| `event_time` | 排序与计算相对时间 | 使用服务端/客户端统一时间约定 |
| `anonymous_player_id` | 会话与回流串联 | 不使用直接身份信息 |
| `session_id` | 区分单次会话 | 返回前后台的切分规则需统一 |
| `combat_run_id` | 串联一局及重试 | 每次正式开战唯一；预览不生成 |
| `content_version` | 区分资源、逻辑和配置版本 | 必须能回溯参数集 |
| `experiment_group` | 对照实验 | 无实验写明确的默认组 |
| `route_id` | A / B / C 或经批准的新路线 | 用于所有权冲突分析 |
| `encounter_id` | 遭遇模板 | 与难度/词缀分开 |
| `player_stage` | 生命周期/章节分群 | 不记录无用途的完整账号档案 |

## 最小事件字典

### 1. `combat_prepare_viewed` — 准备页进入

- 最低字段：公共字段（`combat_run_id` 可先使用准备实例 ID）、`entry_source`、`visible_objective_id`、`visible_threat_tags`、`current_loadout_signature`。
- 回答：玩家看到了什么目标/敌情，从哪里进入，初始配置是什么。
- 不采集：未展示给玩家的隐藏敌人参数。

### 2. `combat_prepare_changed` — 准备修改

- 最低字段：公共字段、`change_type`、`from_option_id`、`to_option_id`、`slot_or_route_id`、`source_object_id`、`preview_changed`。
- 回答：玩家是否做取舍，改的是单位/设施、器具、站位、资源还是路线；预览是否反馈。
- 不采集：每次拖拽像素路径；只有最终有效修改和撤销需要记录。

### 3. `combat_started` — 战斗开始

- 最低字段：公共字段、`final_loadout_signature`、`objective_initial_state`、`resource_initial_state`、`threat_tags_shown`、`total_duration_target`。
- 回答：最终选择、可见情报与起始状态是什么。
- `[HYPOTHESIS]` `total_duration_target` 是该版本的原型配置，不代表实际结束时间。

### 4. `combat_phase_entered` — 阶段进入

- 最低字段：公共字段、`phase_id`、`elapsed_active_time`、`tau_at_entry`、`phase_trigger`、`objective_state`、`resource_state`、`pressure_components`。
- 回答：阶段是否在目标位置发生、由什么状态触发、压力由哪些成分构成。
- 不采集：若压力组件没有对应调参或诊断用途，不扩展字段。

### 5. `combat_intervention_used` — 主动干预

- 最低字段：公共字段、`intervention_id`、`target_id_or_zone`、`window_id`、`time_since_window_open`、`resource_cost`、`immediate_result_code`。
- 回答：玩家是否识别窗口、选择何种目标、输入是否改变过程。
- 不采集：无结果差异的装饰点击。

### 6. `combat_objective_damaged` — 目标受损

- 最低字段：公共字段、`objective_id`、`damage_source_type`、`normalized_loss`、`remaining_objective_value`、`preventable_by_contract_id`。
- 回答：损失来自哪类压力，是否有已公开的可改准备/干预。
- 不采集：除非公式审计需要，不上传每次普通单位伤害明细。

### 7. `combat_resource_consumed` — 资源消耗

- 最低字段：公共字段、`resource_type`、`amount_normalized`、`consume_reason`、`remaining_normalized`、`source_object_id`。
- 回答：哪种准备被何时消耗，是否形成资源余量和连续路线判断。
- 不采集：与设计无关的资产钱包余额。

### 8. `combat_resolved` — 胜负

- 最低字段：公共字段、`result`、`elapsed_active_time`、`last_phase_id`、`objective_final_state`、`resource_final_state`、`failure_reason_code`、`attribution_cards_shown`、`near_fail_flag`。
- 回答：为何结束、代价如何、系统向玩家解释了什么。
- `[HYPOTHESIS]` `near_fail_flag` 必须引用版本化的 `near_fail_condition`，不可由客户端随意判定。

### 9. `combat_retry_selected` — 重试 / 改配

- 最低字段：公共字段、`previous_combat_run_id`、`retry_mode`、`time_since_resolve`、`changed_contract_types`、`recovery_cost_type`。
- 回答：玩家是原样重试、改配、降低难度、撤退还是稍后返回；失败是否产生新决定。
- 不采集：没有行为差异的重复按钮曝光。

### 10. `world_writeback_applied` — 世界回写

- 最低字段：公共字段、`writeback_type`、`affected_world_object_id`、`source_combat_run_id`、`next_action_ids_exposed`、`reversible_flag`。
- 回答：战斗如何改变人、空间、伙伴、车队、地图、生产或订单。
- 不采集：完整世界状态；只记录本局产生的变化。

### 11. `merge_returned_after_combat` — 返回 Merge

- 最低字段：公共字段、`source_combat_run_id`、`return_delay_active_time`、`return_entry`、`first_merge_goal_id`、`goal_linked_to_writeback`。
- 回答：玩家是否回到主棋盘、为何回来、首个目标是否由战斗后果驱动。
- 不采集：与该回流问题无关的长期棋盘历史。

## 四层验证

### 1. 看懂（comprehension）

核心问题：玩家是否理解目标、威胁、可用输入和准备项对应关系？

- 量化：准备页停留、目标首次受损前退出、阶段识别、窗口曝光后输入、首次有效反馈时间。
- 质化：开战前复述“要保护/送达什么”；首次受损后指出危险来源。
- `[HYPOTHESIS]` 若事件显示触发但玩家复述错误，判为看懂失败，不得按“系统正常生效”放行。

### 2. 归因（attribution）

核心问题：玩家能否说明哪个 Merge/经营选择造成哪个战斗结果？

- 量化：配置与目标损失/资源余量/阶段结果的关联、因果卡展开、失败原因与改配类型的一致性。
- 质化：战后请玩家说出“最有帮助的一项准备”“一个失败点”“下次改什么”。
- `[HYPOTHESIS]` 只说“战力不够”“等级低”视为核心接口归因失败，除非本次测试本来就在验证普通成长门槛。

### 3. 决策（decision）

核心问题：信息是否促成可替代选择，而非所有人复制同一最优解？

- 量化：准备修改率、配置熵、同配置跨词缀表现、窗口时机分布、失败后改配与原样重试比例。
- 质化：玩家能否说出至少两种方案的收益/代价，且选择与路线所有权一致。
- `[HYPOTHESIS]` 选择分布集中不自动等于失败；必须结合对手/路线是否相同和该方案是否在所有场景支配。

### 4. 回流（return）

核心问题：战斗后果是否自然创造新的 Merge/经营行动？

- 量化：世界回写完成、返回 Merge、首个 Merge 目标与回写关联、修复/补给/培育/重装行为、稍后自然回流。
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
- `[HYPOTHESIS]` `combat_resolved`、`world_writeback_applied` 与 `merge_returned_after_combat` 必须可通过 `combat_run_id` 串联；不能串联的数据不用于闭环结论。
- `[HYPOTHESIS]` 录像/高频轨迹只对明示测试样本启用，遵守目标市场隐私、年龄与数据最小化要求。
- `[HYPOTHESIS]` 不用单一均值放行；至少查看分布、生命周期、胜负、配置、设备性能和 A/B/C 路线差异。
- `[HYPOTHESIS]` 遥测显示相关性时不得直接声称因果；正式改动用对照实验、隔离变量或重复可控样本验证。
