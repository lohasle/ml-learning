# Transformer 架构

## 概述
Transformer（2017, Vaswani et al.）是完全基于 Attention 机制的序列建模架构，用 Self-Attention 替代 RNN，实现了完全并行化和更好的长距离依赖建模。

## 核心组件

### 1. 多头注意力（Multi-Head Attention）
- 将 Q/K/V 投影 h 次，每个头独立做 Attention，拼接后再线性融合
- 每个头学不同的注意力模式（如语法关系、语义关联、位置关系）

### 2. 位置编码（Positional Encoding）
- 正弦/余弦编码：PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
- 为每个位置提供唯一标识，弥补 Self-Attention 的无序性

### 3. 残差连接 + LayerNorm
- 每个 sub-layer 都有残差连接，防止梯度消失
- LayerNorm 对单样本独立归一化

### 4. 前馈网络（FFN）
- 两层 MLP：d_model → d_ff → d_model
- 增加非线性表达能力

## 三种变体

| 变体 | 代表 | 特点 |
|------|------|------|
| Encoder-Only | BERT | 双向注意力，适合理解任务 |
| Decoder-Only | GPT | 单向注意力，适合生成任务 |
| Encoder-Decoder | T5, BART | 适合序列转换任务 |

## 关键公式

| 公式 | 说明 |
|------|------|
| MultiHead(Q,K,V) = Concat(head₁,...,headₕ)W^O | 多头拼接 |
| headᵢ = Attention(QWᵢ^Q, KWᵢ^K, VWᵢ^V) | 每个头独立计算 |
| FFN(x) = max(0, xW₁+b₁)W₂+b₂ | 两层 MLP |

## 关联概念
- 前置：Attention 机制（第15课）
- 后续：预训练语言模型 BERT/GPT（第17课）
- 关键论文：Attention Is All You Need (2017)
- 工程演进：FlashAttention、MQA、GQA 等优化
