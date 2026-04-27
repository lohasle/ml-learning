# Agent 智能体

## 🎯 核心概念

### 1. 基础定义
- **类型**：AI 系统范式
- **适用场景**：需要多步推理、工具调用、自主决策的复杂任务
- **一句话定义**：LLM + 工具 + 规划 + 记忆 = 能自主行动的 AI 系统

### 2. 架构原理
- Agent 本质是一个**循环**：LLM 决策 → 调用工具 → 观察结果 → 再次决策
- ReAct 范式（Reasoning + Acting）是最经典的实现方式
- LLM 不直接执行操作，而是输出结构化指令（JSON），由框架层执行

### 3. 实践要点
- 必须设置最大步数，防止死循环
- 工具描述要清晰，LLM 靠描述选择工具
- 记忆管理是关键：上下文窗口有限，需要策略性裁剪
- 评估 Agent 比评估 LLM 更难：不只看最终答案，还要看过程

## 📊 关键概念

| 概念 | 含义 | 直觉 |
|------|------|------|
| ReAct | Thought → Action → Observation 循环 | 想一步做一步看一步 |
| Function Calling | LLM 输出结构化工具调用指令 | LLM 当指挥官，工具当执行者 |
| Tool Registry | 工具的注册和管理中心 | 工具箱，LLM 按需选取 |
| Memory | 短期 + 长期记忆管理 | 对话历史 + 知识库 |
| Planning | 任务分解和策略选择 | 大目标拆成小步骤 |

## 🔗 关联概念
- **前置知识**：LLM（第17课）、Prompt Engineering、RAG（第19课）
- **后续应用**：多模态 Agent、AI 系统、自主编程
- **同类对比**：RAG 是 Agent 使用"检索工具"的特例；Chatbot 是 Agent 的最简形式
- **关键论文**：ReAct (Yao et al., 2022)、Toolformer (Schick et al., 2023)、HuggingGPT (2023)

## 💡 记忆技巧
Agent 就像一个新员工：有大脑（LLM）但没经验，需要工具箱（Tools）、工作流程（Planning）、和笔记本（Memory）才能独立完成任务。
