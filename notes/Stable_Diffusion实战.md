# Stable Diffusion 实战：部署与调参

## 核心架构

Stable Diffusion 由三大组件组成：

1. **VAE（变分自编码器）**：图像 ↔ 潜在空间的桥梁
   - 编码器：512×512×3 → 64×64×4（压缩 48 倍）
   - 解码器：64×64×4 → 512×512×3

2. **UNet**：去噪引擎
   - 接收：带噪声的 latent + 时间步 t + 文本条件
   - 输出：预测的噪声
   - 关键结构：对称编码-解码 + 跳跃连接 + Cross-Attention

3. **CLIP Text Encoder**：文本理解
   - 将 prompt 编码为 768 维向量
   - 通过 Cross-Attention 注入 UNet

## 推理管线

```
Prompt → CLIP → text_embedding
噪声 latent → UNet × N steps → 去噪 latent → VAE Decoder → 图像
```

## 关键调参

| 参数 | 推荐范围 | 作用 |
|------|----------|------|
| Steps | 20-30 | 去噪精度 |
| CFG Scale | 7-9 | Prompt 遵循度 |
| Sampler | Euler A / DPM++ 2M Karras | 去噪算法 |
| Negative Prompt | 必填 | 排除不想要的内容 |

## CFG 公式

```
noise_pred = noise_uncond + cfg_scale × (noise_cond - noise_uncond)
```

## LoRA 微调

- 冻结 UNet，在 Cross-Attention 层添加低秩矩阵
- 只需几 MB 权重，少量图片即可学到新风格

## 关联概念

- 第40课：扩散模型理论（DDPM/DDIM）
- 第11课：CNN（UNet 的基础）
- 第13课：Attention（Cross-Attention 机制）
- 第24课：LoRA（低秩适配）
