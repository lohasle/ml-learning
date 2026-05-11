# Prompt Engineering

## 🎯 核心概念

### 1. 基础定义
- **类型**：LLM 交互接口设计
- **适用场景**：所有大模型应用开发
- **一句话定义**：Prompt 是激活大模型特定能力的结构化指令接口

### 2. 核心原理
- 大模型的参数空间中存储了海量能力，Prompt 决定激活哪些能力
- Prompt Quality = 角色设定 × 任务描述 × 约束条件 × 输出格式
- 关键论文：CoT (Wei et al. 2022)、ToT (Yao et al. 2023)、ReAct (Yao et al. 2022)

### 3. 实践要点
- 结构化 Prompt 用四要素模板：Role + Task + Constraints + Format
- Few-shot 示例重质量不重数量，3-5 个覆盖边界情况
- CoT 万能增强：加「一步步思考」即可提升推理质量
- Prompt 需要版本管理和测试驱动迭代

## 📊 关键公式

| 范式 | 公式/思想 | 直觉 |
|------|----------|------|
| Few-shot | $P(y\|x, E_1...E_k)$ | 给示例后预测更准 |
| CoT | $P(a\|q) = \prod P(r_i) \cdot P(a\|r)$ | 先推理再回答 |
| ToT | $\arg\max \sum V(\text{path})$ | 多路径探索选最优 |
| ReAct | $a_t = f(s_t, o_t)$ | 边想边做 |

## 🔗 关联概念
- 前置知识：Attention机制、Transformer架构、思维链(CoT)
- 后续应用：Agent系统、RAG系统、AI安全(prompt injection防御)
- 同类对比：微调(改模型参数) vs Prompt Engineering(不改参数改输入)

## 💡 记忆技巧
Prompt 就是给大模型的「API 接口」——好接口让系统稳定，差接口让系统随机崩溃。
