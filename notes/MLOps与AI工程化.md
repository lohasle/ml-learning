# MLOps 与 AI 工程化实践

## 概念定义

MLOps 是将 DevOps 原则应用于机器学习系统的实践，覆盖从数据管理到模型部署、监控的完整生命周期。

## 核心公式与机制

### MLOps 成熟度模型

| Level | 描述 | 关键能力 |
|-------|------|----------|
| 0 | 手动流程 | 无自动化 |
| 1 | ML Pipeline | 自动训练+部署 |
| 2 | CI/CD + CT | 代码/数据变更触发训练 |
| 3 | 全自动化+治理 | 特征商店、模型注册表、审计 |

### 数据漂移检测方法

| 方法 | 公式直觉 | 适用场景 |
|------|----------|----------|
| Z-Score | \|μ_new - μ_ref\| / σ_ref | 均值偏移检测 |
| KS Test | max\|F_ref(x) - F_new(x)\| | 分布整体偏移 |
| PSI | Σ(p_new - p_ref) × ln(p_new/p_ref) | 分箱后的分布差异 |
| JSD | KL(P\|M)/2 + KL(Q\|M)/2 | 概率分布距离 |

## 关键工具链

| 类别 | 工具 | 特点 |
|------|------|------|
| 实验追踪 | MLflow, W&B | 参数/指标/模型版本管理 |
| 数据版本 | DVC, LakeFS | 数据集版本化 |
| Pipeline | Kubeflow, Airflow, Dagster | DAG 编排 |
| Serving | vLLM, TGI, Triton | 高性能推理 |
| 监控 | Evidently, Arize | 漂移检测、性能监控 |

## LLM 时代的新挑战

- **Prompt 版本管理**：prompt 变更影响大，需要版本化和测试
- **幻觉监控**：LLM 产生虚假内容的概率需要持续监控
- **Token 成本控制**：推理成本可能远超训练成本
- **多组件协调**：模型 + RAG + Agent + Prompt 联合部署

## 关联概念

- [[量化推理技术]] — 部署优化手段
- [[向量数据库与嵌入检索]] — RAG 基础设施
- [[AI系统设计与部署]] — 系统层面设计
- [[Prompt Engineering高级技巧]] — Prompt 工程化

## 关键论文

- Sculley et al., "Hidden Technical Debt in ML Systems", NIPS 2015
- Google, "MLOps: Continuous Delivery for Machine Learning Models", 2020
