# Attention 机制

## 概念定位
Attention 是从 RNN 时代到 Transformer 时代的关键桥梁。它解决了 Seq2Seq 架构中 encoder 必须将所有信息压缩到固定长度向量的信息瓶颈问题。

## 核心思想
让模型在处理序列的每一步，都能「回头看」所有位置的信息，自动学习哪些位置更相关。

## 关键公式

| 概念 | 公式 | 直觉 |
|------|------|------|
| 相关性 | QK^T | Query 与各 Key 的相似度 |
| 缩放 | ÷√d_k | 控制数值范围 |
| 权重 | softmax(·) | 归一化为概率分布 |
| 输出 | weights·V | 加权提取信息 |

## Q/K/V 类比

| 角色 | 图书馆类比 | 模型中 |
|------|-----------|--------|
| Query | 搜索词 | 当前需要的信息 |
| Key | 书名/标签 | 每个位置的特征 |
| Value | 书的内容 | 每个位置的实际信息 |

## 关键论文
- Bahdanau et al. (2014) - 首次提出 Attention 用于机器翻译
- Luong Attention (2015) - 简化计算
- Vaswani et al. (2017) - "Attention Is All You Need" → Transformer

## 关联概念
- **前置：** RNN/LSTM（第14课）- Attention 最初附着在 RNN 上
- **后续：** Transformer（第16课）- 纯 Attention 架构
- **延伸：** Self-Attention、Multi-Head Attention、FlashAttention
