# 外置节奏、局内心流与可替换数值原型

> 职责：定义时间曲线、测量口径、原型假设替换方法与曲线级 Kill Criteria。伤害公式、成长曲线与最终配表仍归 `combat-design` / `numerical-planning`。

## 目录

- 证据纪律与统一时间轴
- 外置节奏曲线
- 局内五阶段心流
- 三种时长映射
- 可替换指标
- 压力指数与目标曲线
- 实测替换流程
- Kill Criteria

## 证据纪律与统一时间轴

- `[OBSERVED]` 当前项目没有竞品内部战斗遥测、隐藏公式或可比的精确阶段阈值。
- `[INFERRED]` 因此本文件的时间、阶段边界、目标压力、权重和阈值只能作为原型起点，不能称为行业基准。
- `[HYPOTHESIS]` 所有局内原型使用归一化时间 `tau=t/T`，其中 `t` 是自可操作战斗开始后的活跃时间，`T` 是该局在 `combat_resolved` 记录的实际总活跃时长。运行时只采集 `elapsed_active_time`；结算前不知道最终 `T`，因此 `tau` 必须在结算后派生，不能由客户端实时上报。
- `[HYPOTHESIS]` 原型先比较曲线形状，再比较绝对时长；拿到实测后允许整体替换 `T`，而不改五阶段语义。

## 外置节奏曲线

外置曲线的目标不是“战斗越多越好”，而是让低压准备、风险尖峰、恢复与世界回写交替，使下一次 Merge 有新问题。

### 单次会话

| 段落 | 玩家状态 | 系统动作 | 必须产生的下一步 |
|---|---|---|---|
| 低压回流 | `[HYPOTHESIS]` 重新理解库存、订单、居民/伙伴/车队状态 | 领取、整理、短链 Merge、查看上次回写 | 选择本次最重要的缺口 |
| 准备与取舍 | `[HYPOTHESIS]` 在空间、产能、携带和目标之间做选择 | 配置设施/阵容/载荷/路线 | 形成可预览的战斗假设 |
| 战斗尖峰 | `[HYPOTHESIS]` 识别压力并做少量关键干预 | 执行本文件五阶段曲线 | 产生可归因结果 |
| 恢复 | `[HYPOTHESIS]` 从高压降回可规划状态 | 查看因果卡、修复/治疗/整理战利品 | 选择接受损失、恢复或改配重试 |
| 世界回写 | `[HYPOTHESIS]` 看见人、空间、伙伴、路线或库存发生变化 | 生成新订单、关系、地图和生产条件 | 返回 Merge，而不是停在奖励弹窗 |

- `[HYPOTHESIS]` 会话内战斗应是一次清晰尖峰而非持续高压底色；若玩家回流后必须连续处理多个强制战斗入口，先合并入口再调时长。
- `[HYPOTHESIS]` 战后回 Merge 必须由具体缺口驱动，例如修门、补器具、治疗伙伴或重装货舱，不能只有泛用货币奖励。

### 章节 / 日循环

| 时段 | A Cozy-first | B Collection-first | C Logistics-first |
|---|---|---|---|
| 建立目标 | `[HYPOTHESIS]` 点名今晚要保护的人/房间 | `[HYPOTHESIS]` 展示生态目标与伙伴机会 | `[HYPOTHESIS]` 展示合同、货物与路线风险 |
| 低压准备 | `[HYPOTHESIS]` 生活、维修、防务订单争夺产能 | `[HYPOTHESIS]` 培育、器具、商队模块争夺容量 | `[HYPOTHESIS]` 补给、维修、武器、情报争夺车厢 |
| 风险检验 | `[HYPOTHESIS]` 守夜或灾害 | `[HYPOTHESIS]` 远征遭遇 | `[HYPOTHESIS]` 追逐/护送与连续损耗 |
| 恢复回写 | `[HYPOTHESIS]` 维修、治疗、关系与来客 | `[HYPOTHESIS]` 疲劳、发现、谱系与蓝图 | `[HYPOTHESIS]` 货损、伤员、残骸与绕路 |
| 新章钩子 | `[HYPOTHESIS]` 新居民/空间问题 | `[HYPOTHESIS]` 新生态/组合问题 | `[HYPOTHESIS]` 新路线/装载问题 |

### 周活动

- `[HYPOTHESIS]` 周活动采用“低压共同准备 → 多次递增检验 → 周中恢复/改配 → 周末高潮 → 世界永久回写”的波形。
- `[HYPOTHESIS]` 同一主题同时改变 Merge 订单、经营约束和战斗词缀；不为战斗复制独立棋盘、货币与通行证。
- `[HYPOTHESIS]` 周末高潮可以复用已验证主形态并增加一项组合压力；完整 Boss、实时 PvP 或跨服只在专项证据成立后解锁。
- `[HYPOTHESIS]` 周活动结束必须留下至少一种非数值世界变化，例如修复空间、生态记录、路线开放或角色关系；否则活动只在抽走主循环注意力。

### 外置曲线的可测合同

三种尺度统一发送 `outer_flow_phase_changed` 的进入/退出事件，使用 `flow_scale + outer_flow_curve_version + flow_instance_id` 分组；其中 `outer_flow_curve_version` 必须对应当前尺度的阶段顺序、目标和计算口径版本，事件最低字段见 `05-telemetry-and-validation.md`。

| 尺度 | 阶段 ID 顺序 `[HYPOTHESIS]` | 实例边界 | 必测输出 |
|---|---|---|---|
| 单次会话 | `low_pressure_return → prepare → combat_peak → recovery → writeback` | `session_id` 内第一次核心回流到退出/后台切分；新会话新建实例 | 各阶段活跃时长占比、准备→战斗转化、风险检验频次、恢复完成、回写完成、战后回 Merge |
| 章节 / 日 | `goal → preparation → risk_check → recovery_writeback → next_hook` | 一个版本化章节日/自然日目标实例；允许按同版本恢复跨会话实例 | 各阶段跨会话累计时长、风险检验次数与间隔、恢复完成、下一章钩子到达、未完成原因 |
| 周活动 | `joint_prep → escalating_checks → mid_recovery → climax → permanent_writeback` | 一个活动版本与玩家的参与实例；允许按同版本恢复跨会话实例 | 各阶段参与天数/活跃时长、检验频次与递增顺序、周中改配、高潮到达、永久回写完成 |

`elapsed_active_time` 在外置事件中专指当前 `flow_instance_id` 的累计活跃时钟，不是会话内时钟或墙钟。前后台暂停、会话之间的离线间隔和达到统一无操作阈值后的时间不累计；章节/日与周实例恢复时沿用暂停前的累计值，单次会话尺度则在新会话创建新实例。暂停/恢复用同阶段的 `exited(completion_reason=paused)` 与后续 `entered` 切成多个活跃段；阶段活跃时长为同实例、同版本、同 `phase_id` 的全部有效 `exit.elapsed_active_time - enter.elapsed_active_time` 之和。活动过期、口径版本变化或不满足恢复窗时关闭旧实例并新建实例，不跨实例拼接；缺少配对退出的段只进入中断率。

计算定义：

- `DurationShare_(s,v,p) = active_duration_in_phase_(s,v,p) / total_active_duration_(s,v)`，其中 `s=flow_scale`、`v=outer_flow_curve_version`；阶段进入后缺少退出事件的活跃段不进入完整时长样本，并单独报告中断率。
- `TransitionRate_(s,v,p→q) = distinct flow_instance_id entering q after a completed exit from p / distinct flow_instance_id exiting p with completion_reason=completed`；只有完成退出才进入相邻阶段转化口径。`paused` / `interrupted` / `expired`与重复进入分别报告，不混入完成转化，也不能被平均隐藏。
- `RiskFrequency_(s,v) = risk_checks_started / flow_instances_started`；同时报告相邻风险检验的活跃时间/自然时间间隔分布。
- `RecoveryCompletion_(s,v) = distinct flow_instance_id with at least one recovery exit where completion_reason=completed / distinct flow_instance_id with at least one recovery entered event`。同一实例的暂停后重入只保留一个分母资格；分子也按 distinct 实例去重。
- `WritebackCompletion_(s,v) = flow_instances_with_required_writeback_completed / flow_instances_with_risk_resolved`；“required”由 `outer_flow_curve_version` 声明。
- `FlowClosure_(s,v) = flow_instances_exiting_final_phase / flow_instances_entering_first_phase`。

目标与替换：

1. `[HYPOTHESIS]` 每个 `flow_scale + outer_flow_curve_version` 先声明阶段顺序、目标时长占比区间、风险检验频次/间隔、恢复与回写完成门槛，以及暂停、恢复窗和实例关闭规则；这些目标来自本项目原型，不引用竞品阈值。
2. 实测先按 `flow_scale + outer_flow_curve_version` 隔离，再按路线、生命周期和完成/中断分群，对比 `DurationShare` 向量误差、转移率差、风险频次/间隔分布、恢复完成与回写完成；不同尺度或版本不直接合并。
3. `[HYPOTHESIS]` 若阶段顺序和因果成立，只是时长/频次偏离，则替换目标占比或入口节奏；若大量实例跳过准备/恢复/回写，按结构问题重写外置循环，不能只拉长会话。
4. `[HYPOTHESIS]` 新目标版本必须记录旧目标、实测分布、替换原因和预期移动指标；会话、章节/日、周三层分别版本化，避免一层调优掩盖另一层断链。

## 局内五阶段心流

以下边界和目标均为 `[HYPOTHESIS]` 原型起点。

| 阶段 | `tau` 区间 | 玩家问题 | 压力目标 | 玩家输入 | 反馈 | 失败信号 |
|---|---:|---|---|---|---|---|
| 1. 识别目标 | `[HYPOTHESIS] 0.00–0.15` | “我要保护/击败/送达什么？危险从哪里来？” | 低；允许读场 | 确认目标、查看首个威胁、必要时微调初始优先级 | 目标轮廓、入口/路线、首个敌人信号与准备项对应关系 | 目标首次受损前玩家仍说不清胜利条件；首屏同时出现多个未教压力 |
| 2. 建立规则 | `[HYPOTHESIS] 0.15–0.35` | “我的准备如何作用？敌人的基本规则是什么？” | 低到中；用低代价验证规则 | 观察自动行为，完成一次低风险输入或看到一次配置触发 | 第一次有效反馈、行为因果、轻度成功/错误代价 | 首次反馈只显示数字；玩家把触发误认为随机；错误立刻不可恢复 |
| 3. 压力升级 | `[HYPOTHESIS] 0.35–0.65` | “哪个目标/资源先失控？我要保留什么？” | 持续上升；迫使取舍但保留恢复余地 | 转火、重分配、换道、消耗资源或接受局部损失 | 压力来源分层、资源余量、目标损失趋势、下一窗口预告 | 压力只来自 EHP 膨胀；所有输入都在冷却；最优解始终是全部即时释放 |
| 4. 关键干预 / 反转 | `[HYPOTHESIS] 0.65–0.82` | “现在用掉稀缺干预，还是承受损失等待更大机会？” | 局内峰值；允许玩家制造可见反转 | 使用关键器具/指令、抢修、打断、撤退或牺牲次要目标 | 强信号窗口、成功反转、失败原因和剩余退路 | 窗口不可读；不用干预也同样获胜；错一次直接无解且此前没有教学 |
| 5. 收束与可解释结算 | `[HYPOTHESIS] 0.82–1.00` | “我为何赢/输？代价是什么？下一次改什么？” | 从峰值快速回落；保留短尾风险，避免垃圾时间 | 完成收尾、选择追击/撤退或确认保留资源 | 胜负、关键贡献、目标损失、资源余量、世界回写预览 | 残敌拖延；结算只给星级/战力；玩家无法指出一个可改准备项 |

## 三种时长映射

表中全部时间均为 `[HYPOTHESIS]`。`75–90 秒`版本使用同一 `tau` 边界，允许按内容密度替换总时长。

| 阶段 | 45 秒原型 | 60 秒原型 | 75 秒原型 | 90 秒原型 |
|---|---:|---:|---:|---:|
| 识别目标 | `[HYPOTHESIS] 0–6.75s` | `[HYPOTHESIS] 0–9s` | `[HYPOTHESIS] 0–11.25s` | `[HYPOTHESIS] 0–13.5s` |
| 建立规则 | `[HYPOTHESIS] 6.75–15.75s` | `[HYPOTHESIS] 9–21s` | `[HYPOTHESIS] 11.25–26.25s` | `[HYPOTHESIS] 13.5–31.5s` |
| 压力升级 | `[HYPOTHESIS] 15.75–29.25s` | `[HYPOTHESIS] 21–39s` | `[HYPOTHESIS] 26.25–48.75s` | `[HYPOTHESIS] 31.5–58.5s` |
| 关键干预 / 反转 | `[HYPOTHESIS] 29.25–36.9s` | `[HYPOTHESIS] 39–49.2s` | `[HYPOTHESIS] 48.75–61.5s` | `[HYPOTHESIS] 58.5–73.8s` |
| 收束与结算 | `[HYPOTHESIS] 36.9–45s` | `[HYPOTHESIS] 49.2–60s` | `[HYPOTHESIS] 61.5–75s` | `[HYPOTHESIS] 73.8–90s` |

### 使用建议

- `[HYPOTHESIS]` 45 秒：验证单目标、单压力、单关键干预；优先用于 A 的日常守夜或 C 的单段追逐。
- `[HYPOTHESIS]` 60 秒：允许一种主压力与一种干扰压力组合；优先用于 B 的轻阵容展示。
- `[HYPOTHESIS]` 75–90 秒：只在前段规则已熟悉时用于章节高潮、护送或简化 Boss；不得用额外时长填充重复波次。
- `[HYPOTHESIS]` 若实测显示收束阶段持续高压或关键干预发生在随机位置，先重划事件时间线，再调整总时长。

## 可替换指标

### 1. TTK

定义：`TTK = EHP / effective_DPS`。EHP 与有效 DPS 的精确计算由 `combat-design` / `numerical-planning` 确认。

- 用途：比较同一敌人/目标在配置、阶段和玩家分群间的处理时间。
- `[HYPOTHESIS]` 原型只设置相对顺序：基础威胁 TTK < 干扰威胁 TTK < 阶段目标 TTK；不引用竞品精确秒数。
- 替换：实测用同一 `unit_instance_id` 的 `combat_unit_became_damageable` 到 `combat_unit_resolved` 的活跃时间分布替代公式估计，并按死亡/失效/逃离分组；停火、转火和无目标时间通过受控轨迹另行解释。

### 2. 首次有效反馈时间

定义：`T_first_feedback = t(first_effect_attributable_to_player_choice) - t(combat_start)`。

- “有效”要求玩家能把变化关联到战前配置或战中输入；纯伤害飘字不自动算有效。
- 替换：从首个 `combat_choice_effect_triggered`（包括 `trigger_mode=automatic` 的配置触发）计算，并结合反馈 cue、因果卡展开和访谈编码；若触发了反馈但玩家未识别，计为可见性失败而非时间达标。

### 3. 单位击杀间隔

定义：按 `combat_unit_resolved(resolve_reason=kill)` 的活跃时间排序。内部区间为 `Delta_kill_i = t_kill_i - t_kill_(i-1)`；另加入首尾哨兵：`Delta_open = t_first_kill - t_combat_start`，`Delta_tail = t_combat_resolved - t_last_kill`。无击杀局把整局活跃时长作为 `no_kill_interval` 单独报告，不伪造成普通击杀间隔。

- 用途：发现前段无反馈、阶段中垃圾时间或瞬时清屏。
- 替换：同时报告首尾哨兵、内部区间的中位数/分位数与最长空窗；目标并非固定间隔，而是与五阶段“建立规则—升级—反转—收束”的节拍一致。

### 4. 目标损失率

定义：`ObjectiveLossRate = lost_objective_value / initial_objective_value`。

- 目标价值可按人数、设施服务、货物、耐久或任务权重定义；不同单位不可直接相加，需先归一化。
- `[HYPOTHESIS]` A 应优先展示具体对象，B 展示伙伴/任务状态，C 展示货损/车况；不要只展示总耐久。

### 5. 资源余量

按资源类型和固定 `resource_accounting_version` 拆成两个口径：

- **初始资源保留率**：`InitialRetention_r = max(initial_r - consumed_from_initial_r, 0) / initial_r`。`consumed_from_initial_r` 按版本化的消耗分配规则计算；只回答出战携带的初始资源还保留多少，`initial_r=0` 时记为不适用。
- **累计供给消耗率**：`SupplyConsumption_r = consumed_r / (initial_r + supplied_in_run_r)`。只回答整局可用供给被消耗多少；分母为零时记为不适用。

- 用途：判断胜利是否过度富余、失败是否因单一资源耗尽、连续路线是否有后续选择。
- 跨局比较：同一资源必须固定单位、初始量定义、局内供给计入规则和消耗分配规则；只比较相同 `resource_accounting_version`。
- 替换：实测后分别检查两种口径与胜负、近失败、撤退和重试的关系，不把“越少越刺激”当目标。

### 6. 干预窗口

定义：用 `combat_intervention_window_changed` 记录窗口曝光/关闭，并与 `combat_intervention_used` 关联输入；总体可报告 `sum(valid_window_duration) / T`、窗口未输入率与输入延迟。事件只能证明 cue 已曝光和是否响应，认知上的“识别”需由访谈/受控任务确认。

- `[HYPOTHESIS]` 窗口数量不是深度指标；一个能改变目标/空间/资源的窗口优于多个同质点击。
- 替换：以识别率、选择差异、成功/失败后复述和策略分布校准窗口长度。

### 7. 近失败占比

定义：先由项目声明 `near_fail_condition`，再算 `NearFailShare = wins_meeting_near_fail_condition / all_wins`。

- `[HYPOTHESIS]` 条件可由目标最低安全度、关键资源耗尽、最后窗口成功或撤退边界组合；阈值必须公开为原型旋钮。
- 替换：用胜局轨迹聚类和玩家主观紧张度校准，避免把系统定义的“险胜”当成真实感受。

### 8. 压力指数

所有输入先映射到 `[0,1]`：

`P(t) = w_enemy*EnemyLoad(t) + w_objective*ObjectiveThreat(t) + w_resource*ResourceBurn(t) + w_control*ControlLoss(t) + w_input*RequiredInputDensity(t)`

约束：`w_i >= 0` 且 `sum(w_i)=1`。这是计算定义，不表示各维度同等重要。

- `[HYPOTHESIS]` 原型权重集合：`(w_enemy, w_objective, w_resource, w_control, w_input) = (0.20, 0.25, 0.20, 0.20, 0.15)`；全部是外露旋钮，必须由实测替换。
- `EnemyLoad`：活跃威胁的归一化处理需求，而非单纯敌人数。
- `ObjectiveThreat`：目标损失速度、接触风险或失败倒计时的归一化组合。
- `ResourceBurn`：关键资源消耗速度相对可持续速度。
- `ControlLoss`：不可用空间、被控单位、路线封锁或目标失控比例。
- `RequiredInputDensity`：单位有效时间内必须辨认并处理的不同决策窗口。

### 归一化与采样版本

- `pressure_normalization_version` 必须为每个组件声明：原始聚合量、单位、低/高锚点、方向、截断和缺失值规则。对“数值越高压力越高”的组件使用 `x_norm = clamp((x_raw-L)/(H-L), 0, 1)`；反向组件由版本显式声明，不在查询时临时翻转。
- `sampling_policy_version` 必须声明固定活跃时间采样策略与额外状态变化触发器；状态变化快照用于保留尖峰，固定采样用于保证不同局可比较。
- `combat_pressure_snapshot` 同时记录原始聚合量和归一化组件，不记录逐个单位位置。不同归一化或采样版本不直接并表；若必须比较，先用同一规则离线重算。
- 运行时所有快照只记 `elapsed_active_time`。收到 `combat_resolved.elapsed_active_time=T_actual` 后，离线派生每个快照的 `tau=elapsed_active_time/T_actual`。

## 压力指数与目标曲线

`[HYPOTHESIS]` 五阶段阶段均值目标向量可从 `(0.15, 0.30, 0.60, 0.90, 0.35)` 起步；它只描述“低—建立—上升—峰值—回落”的形状，不是竞品阈值。

### 对照方法

1. 用实际 `T` 把 `combat_pressure_snapshot.elapsed_active_time` 转换为 `tau`；缺少结算或有效快照的局只进入数据质量报告。
2. 按 `sampling_policy_version` 把固定采样与状态变化快照合并，在统一 `tau` 网格上采用版本声明的保持/插值规则重采样。`combat_phase_entered` 只标注阶段，不替代曲线采样。
3. 分玩家分群、胜负、配置和遭遇版本计算 `P_measured(tau)`，同时保留五个组件，避免平均值掩盖问题。
4. 从重采样曲线计算阶段均值、峰值位置、峰后回落斜率、阶段内方差；再与目标损失、两种资源口径和事件时间线联合解释。
5. 使用 `CurveMAE = mean(|P_measured(tau)-P_target(tau)|)` 作为形状误差；同时检查关键峰值和失败原因，不能用单一总分放行。
6. 把录像、访谈复述、配置触发、窗口和因果卡事件叠加。若曲线显示峰值但玩家没有识别，判为可读性问题。

## 实测替换流程

| 顺序 | 动作 | 替换对象 | 产出 |
|---|---|---|---|
| 1 | 灰盒录制最小事件与版本化压力快照 | 原型时长、事件时间、资源消耗 | 结算后派生的每局 `tau` 时间线 |
| 2 | 观察玩家并做战后复述 | 首次有效反馈、窗口识别、归因 | “触发”与“被理解”两套字段 |
| 3 | 按胜负与配置分群 | TTK、损失率、余量、近失败 | 分布而非单均值 |
| 4 | 拟合实际阶段边界 | 五阶段 `tau` 边界和目标压力 | 新版本曲线假设 |
| 5 | 只改一组旋钮复测 | 敌人时间线、资源量、窗口、目标耐久 | 因果可归因的版本差异 |
| 6 | 冻结语义、继续替换参数 | `T`、权重、阈值、阶段目标 | 可进入纵向切片的参数集 |

- `[HYPOTHESIS]` 若实测证明阶段顺序本身错误，可以替换结构；不得为了保留原型而曲解数据。
- `[HYPOTHESIS]` 每次替换记录“改变了什么、期待哪条曲线移动、可能伤害哪个路线所有权”。

## Kill Criteria

### 可调参数问题

满足以下特征时，路由给 `combat-design` / `numerical-planning` 进行一次有界调参：

- `[HYPOTHESIS]` 玩家理解目标与因果，但峰值过早/过晚、TTK 空窗、资源过松/过紧或窗口过窄。
- `[HYPOTHESIS]` 不同配置产生可观察差异，但某一方案在全部样本中支配。
- `[HYPOTHESIS]` 战后能复述正确原因，且修改敌人时间线、目标耐久、资源或窗口可预期地改变曲线。

### 结构停止条件

以下任一条件跨一次明确改变后的复测仍成立，应停止或降级该形态：

- `[HYPOTHESIS]` 玩家无法说清目标、准备与结果的关系，且有效反馈时间无法通过表现修正。
- `[HYPOTHESIS]` 压力峰值只来自数值堆叠，没有新的目标、空间、时机或资源判断。
- `[HYPOTHESIS]` 主动干预不改变过程，或不干预与最佳时机干预结果近似。
- `[HYPOTHESIS]` 结算无法回写下一轮 Merge/经营选择，战后回流只由奖励驱动。
- `[HYPOTHESIS]` A 持续破坏照料感、B 持续隐藏伙伴贡献、C 持续抹去装载和路线损耗。

### 阈值登记模板

```markdown
假设：[HYPOTHESIS]
目标路线 / 玩家分群：
战斗版本与总时长：[HYPOTHESIS]
目标曲线与阶段边界：[HYPOTHESIS]
主指标及通过阈值：[HYPOTHESIS，由内部基线/先导样本设定]
护栏指标及否决阈值：[HYPOTHESIS，由内部基线/先导样本设定]
对照版本：
样本与运行窗口：
允许调参范围：
结构停止条件：
下一动作：保留 / 调参 / 重构 / 降级 / 删除
```
