# 幸存者/割草类配表模板

> 来源：survivor-config-simulator skill
> 用途：割草/幸存者-like数值配表生成与DPS模拟验证
> 依赖：vampire-survivors-numeric-perspective（数值公式基准）

## 核心配表模板（4张表）

### 表1：武器DPS配置表（Weapon_DPS_Config）

| 列名 | 类型 | 说明 | 公式/示例 |
|------|------|------|-----------|
| WeaponID | string | 武器唯一ID | WEP_001 |
| WeaponName | string | 武器名称 | 十字架 |
| WeaponType | string | 武器类型 | A类(范围持续)/B类(投射追踪)/C类(地面放置)/D类(召唤)/E类(环境强化) |
| BaseDamage | float | 基础伤害 | 10.0 |
| Cooldown | float | 冷却时间(s) | 1.5 |
| HitRate | float | 命中率(0-1) | 0.9 |
| DPS_Base | float | 基础DPS | =BaseDamage/Cooldown*HitRate |
| ProjectileCount | int | 投射物数量 | 1 |
| PierceCount | int | 穿透次数 | 0 |
| Duration | float | 持续时间(s) | 0(瞬发)/3.0(持续) |
| Radius | float | 作用半径 | 0(单体)/100(范围) |
| DPS_Actual | float | 实际DPS | =DPS_Base × ProjectileCount × (1+PierceCount×0.3) × 覆盖系数 |

**DPS_Actual 覆盖系数**：
```
A类(范围持续)：1.0（全程覆盖）
B类(投射追踪)：HitRate × 0.9（追踪损失）
C类(地面放置)：Duration / Cooldown（时间覆盖）
D类(召唤)：召唤数量 × 0.8
E类(环境强化)：1.0（不直接伤害）
```

### 表2：敌人HP波次配置表（Enemy_Scaling_Config）

| 列名 | 类型 | 说明 | 公式 |
|------|------|------|------|
| WaveID | int | 波次编号 | 1,2,3,... |
| EnemyType | string | 敌人类型 | 普通/精英/BOSS |
| HP_Base | float | 基础HP | 设计值 |
| ScalingFactor | float | 缩放系数 | 推荐1.12~1.15(主游戏)/1.20~1.25(无尽) |
| HP_Actual | float | 实际HP | =HP_Base × ScalingFactor^(WaveID-1) |
| KillTime_Target | float | 目标击杀时间(s) | 普通2-5s / 精英8-15s / BOSS 30-60s |
| PlayerDPS_Required | float | 所需玩家DPS | =HP_Actual / KillTime_Target |

**HP缩放参考基准**：
```
波次1 普通敌人：HP = 30
波次1 精英敌人：HP = 150
波次1 BOSS：HP = 2000
```

### 表3：经验曲线配置表（Exp_Curve_Config）

分段曲线推荐：
```python
def 标准经验曲线(等级):
    if 等级 <= 20:           # 新手期：快速成长
        return 100 × (1.15 ^ 等级)
    elif 等级 <= 60:         # 成长期：稳步发展
        return 20级经验 × (1.08 ^ (等级 - 20))
    else:                    # 后期：平缓增长
        return 60级经验 × (1.02 ^ (等级 - 60))
```

### 表4：Build协同系数表（Build_Synergy_Config）

```
总DPS = 武器层DPS × 属性乘区 × 协同乘区

属性乘区 = (1 + ATK%) × (1 + 暴击率% × 暴伤%) × (1 + 攻速% / CD)
协同乘区 = Π(1 + C_i) = (1+C₁) × (1+C₂) × ... × (1+Cₙ)
```

## 平衡性检查标准

| 指标 | 合理范围 | 异常信号 |
|------|---------|---------|
| 最优Build/最差Build DPS比 | ≤ 5倍 | >5倍说明Build严重失衡 |
| 总协同乘区 | ≤ ×5.0 | >5.0说明数值膨胀 |
| 最终DPS | ≤ 10^8 | 超出感知上限 |
| 每10级战力增幅 | 50%~80% | <50%成长感不足，>80%数值膨胀 |
