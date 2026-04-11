# Notebook 结构模板

每个课程 Notebook 必须包含以下 cell（按顺序）：

## 结构规范

1. **Markdown: 标题 + 学习目标**
   ```markdown
   # 第N课：课程名
   
   ## 学习目标
   - 目标1
   - 目标2
   - 目标3
   ```

2. **Markdown: 核心概念介绍**
   - 关键算法/模型的直觉解释
   - 在整个学习路线中的位置

3. **Code: 导入库**
   ```python
   import numpy as np
   import matplotlib.pyplot as plt
   # 其他必要库
   ```

4. **Code: 核心算法从零实现**
   - 不调 sklearn API，先手动实现
   - 关键步骤有注释

5. **Code: 可视化**
   - 至少一个图表（数据分布、决策边界、损失曲线等）

6. **Code: sklearn 对比验证**
   - 用库函数跑同样数据
   - 对比自己实现的结果

7. **Markdown: 总结 + 课后思考**
   ```markdown
   ## 总结
   - 要点1
   - 要点2
   
   ## 课后思考
   1. 问题1
   2. 问题2
   ```

## 质量底线

- 总 cell 数 ≥ 7
- 代码 cell ≥ 3（不含空的）
- markdown cell ≥ 3
- 文件大小 > 3KB
- 每个 code cell 有实际逻辑（不允许空壳）
