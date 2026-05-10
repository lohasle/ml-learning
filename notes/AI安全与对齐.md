# AI 安全与对齐

> 第33课 | 阶段 6：前沿专题

## 核心概念

AI 安全关注的是确保 AI 系统的行为符合人类意图和安全边界。这不是一个单一问题，而是一个多维度挑战。

## 关键维度

| 维度 | 核心问题 | 代表方法 |
|------|----------|----------|
| 对抗鲁棒性 | 模型能否抵抗精心设计的输入扰动？ | FGSM、PGD、对抗训练 |
| 对齐 | 模型行为是否符合人类价值观？ | RLHF、Constitutional AI、DPO |
| 越狱防御 | 模型能否抵御绕过安全限制的尝试？ | 输入过滤、输出审查、系统提示加固 |
| 红队测试 | 系统是否有未被发现的漏洞？ | 自动化攻击、人工评估、基准测试 |

## 对齐技术演进

```
RLHF (2022) → Constitutional AI (2022) → DPO (2023) → KTO/ORPO (2024)
  ↓                    ↓                       ↓
人类标注偏好       AI 自我评判           直接偏好优化
奖励模型 + PPO    减少 human effort      跳过奖励模型
```

## DPO 核心思想

$$\mathcal{L}_{DPO} = -\mathbb{E}\left[\log\sigma\left(\beta\log\frac{\pi_\theta(y_w|x)}{\pi_{ref}(y_w|x)} - \beta\log\frac{\pi_\theta(y_l|x)}{\pi_{ref}(y_l|x)}\right)\right]$$

**直觉**：不需要训练奖励模型，直接用偏好数据让模型学会「好回答 > 坏回答」。

## 安全三要素

- **Helpfulness**：模型应该有用
- **Honesty**：模型应该诚实
- **Harmlessness**：模型应该无害

## 关联概念

- [[RLHF 与人类对齐]]（第26课）：对齐的基础方法
- [[高效微调技术]]（第27课）：LoRA/DPO 等训练方法
- [[向量数据库与嵌入检索]]（第32课）：安全检索的边界

## 关键论文与项目

| 论文/项目 | 核心贡献 |
|-----------|----------|
| Goodfellow et al. (2015) FGSM | 开创对抗样本研究 |
| Christiano et al. (2017) RLHF | 人类反馈强化学习 |
| Ouyang et al. (2022) InstructGPT | RLHF 首次大规模应用 |
| Rafailov et al. (2023) DPO | 直接偏好优化 |
| Anthropic Constitutional AI | AI 自我对齐范式 |
| HarmBench (2024) | 安全评估标准化 |