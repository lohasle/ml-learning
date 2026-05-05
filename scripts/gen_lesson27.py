#!/usr/bin/env python3
"""Generate Lesson 27: 高效微调技术 (LoRA / QLoRA / DPO)"""
import json, os

nb = {
    'metadata': {
        'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
        'language_info': {'name': 'python', 'version': '3.10.0'}
    },
    'nbformat': 4,
    'nbformat_minor': 5,
    'cells': []
}

def md_cell(source):
    return {'cell_type': 'markdown', 'metadata': {}, 'source': source.split('\n')}

def code_cell(source):
    return {'cell_type': 'code', 'metadata': {}, 'source': source.split('\n'),
            'execution_count': None, 'outputs': []}

# Cell 0: Title
nb['cells'].append(md_cell(
"""# 第27课：高效微调技术 — LoRA / QLoRA / DPO

## 学习目标
- 理解为什么全量微调大模型不现实（参数量爆炸、显存瓶颈）
- 掌握 LoRA 的核心思想：低秩矩阵分解
- 了解 QLoRA 如何进一步降低显存需求
- 理解 DPO 如何绕过奖励模型直接对齐
- 通过代码实验理解低秩适配的效果

## 前课衔接
- **第26课（RLHF）**：我们学会了三阶段对齐流程（SFT → RM → PPO）
- **本课**：聚焦工程实践——如何用最少的资源完成微调和对齐
- **为什么重要**：全量微调一个 7B 模型需要 100GB+ 显存，LoRA 只需 16GB——这让普通开发者也能微调大模型"""
))

# Cell 1: Concept explanation
nb['cells'].append(md_cell(
"""## 核心概念：为什么全量微调太贵？

一个大模型有数十亿参数。以 LLaMA-7B 为例：
- 7B 参数 × 4 bytes (FP32) = **28GB** 仅模型权重
- 训练需要存储梯度 + 优化器状态 ≈ 再来 2× 权重大小
- 总显存需求：**~80GB+**（单卡 A100 80GB 都很紧张）

**直觉类比**：你要翻新一栋 100 层大楼。全量微调 = 每层都拆了重建。LoRA = 只在关键楼层加装模块，效果差不多，成本降 100 倍。

**核心洞察**：微调过程中的权重变化矩阵 ΔW 具有很低的「内在秩」——也就是说，不需要改那么多参数就能达到很好的效果。"""
))

# Cell 2: LoRA mechanism
nb['cells'].append(code_cell(
"""# ========================================
# LoRA 核心机制：低秩矩阵分解
# ========================================
import numpy as np

# 原始权重 W ∈ R^(d×d)，比如 4096×4096
d = 4096
r = 8  # LoRA 秩，通常 4~64

# 原始参数量
full_params = d * d
# LoRA 参数量：两个矩阵 A ∈ R^(r×d), B ∈ R^(d×r)
lora_params = 2 * r * d

print(f"原始权重 W: {d}×{d} = {full_params:,} 参数")
print(f"LoRA: A({r}×{d}) + B({d}×{r}) = {lora_params:,} 参数")
print(f"压缩比: {full_params / lora_params:.0f}x")
print(f"LoRA 参数占比: {lora_params / full_params * 100:.2f}%")

# 模拟 LoRA 的效果
np.random.seed(42)
W = np.random.randn(d, d) * 0.02

# 低秩分解：ΔW = B @ A
A = np.random.randn(r, d) * 0.01
B = np.random.randn(d, r) * 0.01
delta_W = B @ A

print(f"\\nΔW 的秩: {np.linalg.matrix_rank(delta_W)} (远小于 {d})")
print(f"W + ΔW 的秩: {np.linalg.matrix_rank(W + delta_W)}")"""
))

# Cell 3: Rank analysis visualization
nb['cells'].append(code_cell(
"""# ========================================
# 秩 r 对效果的影响：实验分析
# ========================================
import numpy as np
import matplotlib.pyplot as plt

# 模拟一个「真实」的权重更新矩阵（低秩特性）
np.random.seed(42)
true_rank = 12
d = 512

U, _, Vt = np.linalg.svd(np.random.randn(d, d), full_matrices=False)
singular_values = np.zeros(d)
singular_values[:true_rank] = np.exp(-np.arange(true_rank) * 0.3)
true_delta = (U * singular_values) @ Vt

ranks = [1, 2, 4, 8, 16, 32, 64, 128]
errors = []
captured_energy = []

for r in ranks:
    U_r = U[:, :r]
    S_r = np.diag(singular_values[:r])
    Vt_r = Vt[:r, :]
    approx = U_r @ S_r @ Vt_r
    error = np.linalg.norm(true_delta - approx, 'fro') / np.linalg.norm(true_delta, 'fro')
    errors.append(error)
    total_energy = np.sum(singular_values[:true_rank]**2)
    captured = np.sum(singular_values[:min(r, true_rank)]**2) / total_energy
    captured_energy.append(captured)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(ranks, errors, 'o-', color='#C96442', linewidth=2, markersize=8)
ax1.set_xlabel('LoRA Rank (r)', fontsize=12)
ax1.set_ylabel('Relative Approximation Error', fontsize=12)
ax1.set_title('LoRA: Rank vs Approximation Error', fontsize=13, fontweight='bold')
ax1.axvline(x=true_rank, color='#888', linestyle='--', alpha=0.7, label=f'True rank={true_rank}')
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2.plot(ranks, captured_energy, 's-', color='#2E86AB', linewidth=2, markersize=8)
ax2.set_xlabel('LoRA Rank (r)', fontsize=12)
ax2.set_ylabel('Energy Captured', fontsize=12)
ax2.set_title('LoRA: Rank vs Information Captured', fontsize=13, fontweight='bold')
ax2.axhline(y=0.95, color='#888', linestyle='--', alpha=0.7, label='95% threshold')
ax2.axvline(x=true_rank, color='#C96442', linestyle='--', alpha=0.7, label=f'True rank={true_rank}')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('docs/lora_rank_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("图已保存: docs/lora_rank_analysis.png")"""
))

# Cell 4: QLoRA explanation
nb['cells'].append(md_cell(
"""## QLoRA：量化 + LoRA = 普通人也能微调

QLoRA（2023 年 Dettmers 等人提出）在 LoRA 基础上做了三件事：

| 技术 | 做什么 | 效果 |
|------|--------|------|
| **4-bit NormalFloat** | 新的量化数据类型 | 比 FP16 精度损失极小 |
| **双重量化** | 对量化常数再量化 | 每参数再省 0.37 bit |
| **分页优化器** | GPU 显存不够时用 CPU 内存 | 避免 OOM |

**显存对比**：

| 模型 | 全量微调 | LoRA (FP16) | QLoRA (4bit) |
|------|----------|-------------|--------------|
| LLaMA-7B | ~80GB | ~32GB | **~16GB** |
| LLaMA-13B | ~160GB | ~60GB | **~24GB** |
| LLaMA-65B | ~800GB | ~320GB | **~48GB** |

16GB 显存 = 一张 RTX 4090 就能微调 7B 模型！"""
))

# Cell 5: DPO vs PPO
nb['cells'].append(code_cell(
"""# ========================================
# DPO vs PPO 对比：从 RLHF 到直接偏好优化
# ========================================
import numpy as np
import matplotlib.pyplot as plt

def sigmoid(x):
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

beta = 0.1
log_ratios = np.linspace(-5, 5, 100)

# DPO loss
dpo_loss = -np.log(sigmoid(beta * log_ratios))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(log_ratios, dpo_loss, color='#C96442', linewidth=2.5)
ax1.set_xlabel('Log-Ratio (chosen vs rejected)', fontsize=12)
ax1.set_ylabel('DPO Loss', fontsize=12)
ax1.set_title('DPO Loss Function', fontsize=13, fontweight='bold')
ax1.axvline(x=0, color='#888', linestyle='--', alpha=0.5)
ax1.annotate('chosen > rejected', xy=(3, 0.1), fontsize=10, color='green')
ax1.annotate('chosen < rejected', xy=(-4.5, 3), fontsize=10, color='red')
ax1.grid(True, alpha=0.3)

# 方法对比柱状图
methods = ['PPO\\n(RLHF)', 'DPO', 'RLHF\\n(Full)']
x = np.arange(len(methods))
width = 0.18

components = [
    ('Reward Model', [1, 0, 1], '#C96442'),
    ('RL Training', [1, 0, 1], '#2E86AB'),
    ('Preference Data', [1, 1, 1], '#6B9F78'),
    ('SFT', [1, 1, 1], '#E8B059'),
]

for i, (label, vals, color) in enumerate(components):
    ax2.bar(x + i * width - 1.5*width, vals, width, label=label, color=color, alpha=0.85)

ax2.set_xticks(x)
ax2.set_xticklabels(methods, fontsize=11)
ax2.set_ylabel('Steps Required', fontsize=12)
ax2.set_title('Fine-tuning Method Complexity', fontsize=13, fontweight='bold')
ax2.legend(fontsize=9, loc='upper left')
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('docs/dpo_vs_ppo.png', dpi=150, bbox_inches='tight')
plt.show()
print("图已保存: docs/dpo_vs_ppo.png")"""
))

# Cell 6: LoRA training simulation
nb['cells'].append(code_cell(
"""# ========================================
# 实战模拟：LoRA 微调过程
# ========================================
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

d_in, d_out = 1024, 512
r = 8
alpha = 16

W = np.random.randn(d_out, d_in) * np.sqrt(2.0 / d_in)
A = np.random.randn(r, d_in) * 0.01
B = np.zeros((d_out, r))

n_steps = 20
losses = []
param_changes = []

for step in range(n_steps):
    x = np.random.randn(32, d_in)
    lora_update = (alpha / r) * B @ A
    y = x @ (W + lora_update).T
    target = np.random.randn(32, d_out) * 0.5
    loss = np.mean((y - target) ** 2)
    losses.append(loss)

    grad_scale = 0.001 * (1 + step * 0.1)
    B += grad_scale * np.random.randn(d_out, r)
    A += grad_scale * np.random.randn(r, d_in) * 0.1
    param_changes.append(np.linalg.norm(B @ A))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(losses, color='#C96442', linewidth=2.5, marker='o', markersize=5)
ax1.set_xlabel('Training Step', fontsize=12)
ax1.set_ylabel('Loss (MSE)', fontsize=12)
ax1.set_title('LoRA Fine-tuning: Loss Curve', fontsize=13, fontweight='bold')
ax1.grid(True, alpha=0.3)

ax2.plot(param_changes, color='#2E86AB', linewidth=2.5, marker='s', markersize=5)
ax2.set_xlabel('Training Step', fontsize=12)
ax2.set_ylabel('||dW|| = ||B @ A||', fontsize=12)
ax2.set_title('LoRA: Learned Update Magnitude', fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('docs/lora_training_sim.png', dpi=150, bbox_inches='tight')
plt.show()

print(f"可训练参数: {2 * r * (d_in + d_out):,}")
print(f"冻结参数: {d_in * d_out:,}")
print(f"训练参数占比: {2 * r * (d_in + d_out) / (d_in * d_out) * 100:.2f}%")
print(f"最终损失: {losses[-1]:.4f} (初始: {losses[0]:.4f})")"""
))

# Cell 7: Comparison table
nb['cells'].append(code_cell(
"""# ========================================
# 微调方法全景对比
# ========================================
import pandas as pd

data = {
    'Method': ['Full Fine-tune', 'LoRA', 'QLoRA', 'Adapter', 'Prefix-tuning'],
    'Trainable Params': ['100%', '~0.1%', '~0.1%', '~1-5%', '~0.1%'],
    'VRAM (7B)': ['~80GB', '~32GB', '~16GB', '~40GB', '~35GB'],
    'Speed': ['baseline', '~1.0x', '~0.8x', '~0.9x', '~0.95x'],
    'Inference Overhead': ['none', 'mergeable', 'dequant', 'yes', 'yes'],
    'Use Case': ['pretrain', 'general', 'consumer', 'multi-task', 'light'],
}

df = pd.DataFrame(data)
print('=' * 80)
print('Fine-tuning Methods Comparison')
print('=' * 80)
print(df.to_string(index=False))

print()
print('Key Papers Timeline:')
print('-' * 80)
papers = [
    ('2019', 'Adapter', 'Houlsby et al. - Parameter-Efficient Transfer Learning'),
    ('2021', 'Prefix-tuning', 'Li & Liang - Optimizing Continuous Prompts'),
    ('2021', 'LoRA', 'Hu et al. - Low-Rank Adaptation (ICLR 2022)'),
    ('2023', 'QLoRA', 'Dettmers et al. - Efficient Finetuning of LLMs'),
    ('2023', 'DPO', 'Rafailov et al. - Direct Preference Optimization'),
    ('2024', 'KTO', 'Ethayarajh et al. - Model Alignment as Prospect Theory'),
]
for year, name, ref in papers:
    print(f'  {year} | {name:15s} | {ref}')"""
))

# Cell 8: Practical recommendations
nb['cells'].append(md_cell(
"""## 实践建议：如何选择微调方法

### 决策树

```
你有 GPU 吗？
├── 没有 → 用云端 QLoRA（Google Colab 免费版）
├── 显存 < 24GB → QLoRA (4-bit) + LoRA (r=8~16)
├── 显存 24~48GB → LoRA (FP16, r=16~64)
└── 显存 80GB+ → 全量微调或大 LoRA

需要对齐吗？
├── 不需要 → 只做 SFT + LoRA
├── 需要，有偏好数据 → DPO（推荐）
└── 需要，有标注团队 → PPO/RLHF
```

### 推荐工具链（2025）

| 工具 | 用途 | 特点 |
|------|------|------|
| **PEFT** (HuggingFace) | LoRA/QLoRA 实现 | 最主流，与 transformers 无缝集成 |
| **TRL** (HuggingFace) | DPO/PPO 训练 | 支持 SFT → DPO 全流程 |
| **Axolotl** | 一站式微调 | 配置驱动，支持多种方法 |
| **unsloth** | 加速 LoRA 训练 | 2x 训练速度，节省显存 |"""
))

# Cell 9: Summary
nb['cells'].append(md_cell(
"""## 总结

### 核心要点
1. **LoRA 是工程突破**：低秩分解让微调参数量降 1000 倍，效果接近全量微调
2. **QLoRA 是民主化工具**：4-bit 量化 + LoRA 让消费级 GPU 也能微调 7B 模型
3. **DPO 简化了对齐**：跳过奖励模型训练，直接用偏好数据优化
4. **选择看资源**：显存决定方法，数据决定方向

### 关键公式

| 公式 | 含义 |
|------|------|
| ΔW = B·A (r << d) | LoRA 低秩分解，B in R^(d*r), A in R^(r*d) |
| h = Wx + (alpha/r)BAx | LoRA 前向传播，alpha 是缩放因子 |
| L_DPO = -log sigma(beta * (log pi_theta(y_w)/pi_ref(y_w) - log pi_theta(y_l)/pi_ref(y_l))) | DPO 损失函数 |

### AI 演进位置
- **2021** LoRA 论文 -> 参数高效微调的里程碑
- **2023** QLoRA -> 大模型微调民主化
- **2023** DPO -> 简化 RLHF 流程
- **趋势** -> 微调越来越轻量，效果越来越好

### 下一步预告
第28课我们将学习 **AI 安全与可解释性**——理解大模型为什么会产生幻觉，以及如何让 AI 系统更可信、更安全。"""
))

# Write
os.makedirs('lessons', exist_ok=True)
with open('lessons/27_高效微调技术.ipynb', 'w') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"Generated: lessons/27_高效微调技术.ipynb")
print(f"Total cells: {len(nb['cells'])}")
code_cells = sum(1 for c in nb['cells'] if c['cell_type'] == 'code')
md_cells = sum(1 for c in nb['cells'] if c['cell_type'] == 'markdown')
print(f"Code cells: {code_cells}, Markdown cells: {md_cells}")
