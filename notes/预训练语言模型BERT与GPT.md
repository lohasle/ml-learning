# 预训练语言模型——BERT 与 GPT

## 核心概念

### 预训练 + 微调范式
先在海量无标注文本上学习语言规律，再用少量标注数据适配下游任务。这彻底改变了 NLP 的开发方式。

### BERT（Bidirectional Encoder Representations from Transformers）
- 架构：Transformer Encoder
- 训练目标：MLM（Masked Language Model）+ NSP
- 特点：双向注意力，能同时看到左右上下文
- 擅长：文本分类、命名实体识别、问答

### GPT（Generative Pre-trained Transformer）
- 架构：Transformer Decoder
- 训练目标：CLM（Causal Language Model）
- 特点：单向（因果）注意力，只能看到左边已生成的词
- 擅长：文本生成、对话、续写

## 关键公式

| 概念 | 公式 | 说明 |
|------|------|------|
| MLM 损失 | L = -Σ log P(masked \| context) | 完形填空 |
| CLM 损失 | L = -Σ log P(x_t \| x_{<t}) | 预测下一个词 |
| Scaling Law | L(C) ∝ C^(-α) | 计算量越大，损失越低 |

## 关键对比

| 维度 | BERT | GPT |
|------|------|-----|
| 方向 | 双向 | 单向 |
| 目标 | MLM | CLM |
| 参数 | 110M/340M | 117M→175B |
| 强项 | 理解 | 生成 |

## 关联概念
- [[Transformer 架构]] - BERT 和 GPT 的基础
- [[Attention 机制]] - Self-Attention 的具体应用
- [[大模型微调]] - 预训练后的适配方法
