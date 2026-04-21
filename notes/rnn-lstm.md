# RNN / LSTM 与序列建模

## 核心思想

RNN 是处理**序列数据**的神经网络。核心机制是隐藏状态 $h_t$ 的循环传递：每一步的输出依赖当前输入和上一步的隐藏状态。

## 关键公式

| 概念 | 公式 | 直觉 |
|------|------|------|
| RNN | $h_t = \tanh(W x_t + U h_{t-1} + b)$ | 新输入+旧记忆压缩 |
| LSTM 遗忘门 | $f_t = \sigma(W_f [h_{t-1}, x_t] + b_f)$ | 0=全忘, 1=全留 |
| LSTM 输入门 | $i_t = \sigma(W_i [h_{t-1}, x_t] + b_i)$ | 新信息写入控制 |
| LSTM 细胞更新 | $C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$ | 擦旧+写新 |
| LSTM 输出 | $h_t = o_t \odot \tanh(C_t)$ | 从传送带读出 |

## RNN → LSTM → GRU 演进

- **RNN**（1986）：简单循环，梯度消失问题
- **LSTM**（1997）：加门控+细胞状态，解决长依赖
- **GRU**（2014）：简化 LSTM，合并门控，参数更少
- **Transformer**（2017）：去掉循环，用注意力机制处理全局依赖

## 关联概念

- 前置：CNN（空间局部性）→ 本课：RNN/LSTM（时间序列）→ 后续：Attention/Transformer
- 关键论文：Hochreiter & Schmidhuber, "Long Short-Term Memory", 1997
- 关键项目：Google Neural Machine Translation (2016) 使用 LSTM 做机器翻译
