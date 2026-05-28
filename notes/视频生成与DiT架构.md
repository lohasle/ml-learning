# 视频生成与 DiT 架构

## 🎯 核心概念

### 1. 基础定义
- **类型**：生成模型 / 扩散模型变体
- **适用场景**：图像生成、视频生成、多模态内容创作
- **一句话定义**：用 Transformer 替代 U-Net 做扩散模型的去噪网络，实现视觉内容的生成

### 2. 核心架构
- **DiT = Diffusion + Transformer**
- Patchify 将图像/视频转为 token 序列
- AdaLN-Zero 用时间步条件动态调制归一化参数
- Transformer Blocks 做全局自注意力去噪
- Unpatchify 将输出重组为图像/视频

### 3. 实践要点
- patch_size 选择：4×4 常用，更小更精细但更慢
- 大规模训练需要潜空间压缩（如 VAE）
- 视频生成需 3D patchify 处理时空联合维度
- 扩散步数通常 50-1000 步

## 📊 关键公式

| 公式 | 含义 | 直觉 |
|------|------|------|
| L = E[‖ε - ε_θ(x_t, t)‖²] | 扩散训练损失 | 让模型从噪声图中认出原始噪声 |
| x → Conv2d(k=p, s=p) → flatten | Patchify | 把图像切成小方块变成 token |
| y = γ(t)·Norm(x) + β(t) | AdaLN | 时间步告诉噪声多强，调整归一化 |
| x → Conv3d(k=(tp,p,p)) | 3D Patchify | 在时空三维同时切块处理视频 |

## 🔗 关联概念
- 前置知识：扩散模型、Transformer、ViT
- 后续应用：多模态统一架构、AI 视频创作
- 同类对比：U-Net（传统扩散去噪网络）

## 💡 记忆技巧
DiT 就是把扩散模型的「放大镜工匠」U-Net 换成「全局规划师」Transformer——先切 patch 再全局看，像拼图一样从噪声中还原画面。
