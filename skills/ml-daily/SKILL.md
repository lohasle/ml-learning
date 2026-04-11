---
name: ml-daily
description: ml-learning 每日课程生成与完整性维护流程。每次定时任务触发时使用。
---

# ML Learning 每日课程流程

本 Skill 定义 ml-learning-coach 子代理每次定时任务的**完整执行流程**。

## 核心原则

1. **不允许跳过任何 Phase**
2. **validate.py 是硬门槛** — 未通过不允许 push
3. **级联同步不可遗漏** — 新增内容必须同步到所有相关文件

---

## Phase 1: 健康检查（每次必做）

运行验证脚本：

```bash
python3 skills/ml-daily/scripts/validate.py
```

脚本输出 JSON，关键字段：
- `pass: true` → 无缺口，进入 Phase 3
- `pass: false` → 有错误，记录 `errors` 和 `gaps` 列表，进入 Phase 2

## Phase 2: 补齐缺口

根据 validate.py 的 `gaps` 列表逐项修复：

| 缺口类型 | 修复方式 |
|----------|----------|
| `missing_lesson` | 按 notebook-template.md 生成缺失编号的课程 Notebook |
| Notebook cell 不足 | 补充内容（代码 cell + markdown cell） |
| `missing_nb_html` | 从 ipynb 解析生成 `docs/nb-{name}.html` 片段 |
| `broken_lab_ref` | 生成缺失的 HTML 片段，或更新 notes-lab.html 菜单 |

### Notebook 渲染方法

```python
import json, markdown, base64, os

def notebook_to_html(nb_path):
    with open(nb_path) as f:
        nb = json.load(f)
    cells_html = []
    for cell in nb.get('cells', []):
        cell_type = cell.get('cell_type', '')
        source = ''.join(cell.get('source', []))
        if cell_type == 'markdown':
            content = markdown.markdown(source, extensions=['tables', 'fenced_code'])
            cells_html.append(f'<div class="nb-cell nb-markdown">{content}</div>')
        elif cell_type == 'code':
            escaped = source.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
            outputs_html = ''
            for out in cell.get('outputs', []):
                if out.get('output_type') == 'stream':
                    text = ''.join(out.get('text',[])).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
                    outputs_html += f'<div class="nb-output"><pre>{text}</pre></div>'
                elif out.get('output_type') == 'execute_result':
                    for dtype, data in out.get('data', {}).items():
                        if 'text/plain' in dtype:
                            text = (''.join(data) if isinstance(data, list) else data).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
                            outputs_html += f'<div class="nb-output"><pre>{text}</pre></div>'
            cells_html.append(f'''<div class="nb-cell nb-code">
  <div class="nb-label">In [{cell.get("execution_count","?")}]</div>
  <pre><code>{escaped}</code></pre>{outputs_html}
</div>''')
    return '\n'.join(cells_html)
```

### Daily MD 渲染方法

```python
import markdown
with open('daily/YYYY-MM-DD.md') as f:
    md = f.read()
html = markdown.markdown(md, extensions=['tables', 'fenced_code'])
with open('docs/daily-YYYY-MM-DD.html', 'w') as f:
    f.write(html)
```

补齐后**重新运行 validate.py**，直到 `pass: true`。

## Phase 3: 生成今日新课程

### 3.1 确定课程主题
- 检查学习路线图（roadmap/roadmap.md 或 README.md）
- 确定当前应学的下一课
- 使用 web_search 搜索相关资料辅助内容生成

### 3.2 生成文件（按模板）

| 文件 | 路径 | 参考 |
|------|------|------|
| Notebook | `lessons/NN_课程名.ipynb` | references/notebook-template.md |
| Daily 记录 | `daily/YYYY-MM-DD.md` | references/daily-template.md |
| 知识笔记 | `notes/主题.md`（如涉及新概念） | references/note-template.md |

### 3.3 渲染 HTML 片段

必须同步生成：
- `docs/nb-NN_课程名.html`（从 ipynb 渲染）
- `docs/daily-YYYY-MM-DD.html`（从 MD 渲染）
- `docs/note-主题.html`（如有新概念笔记）

## Phase 4: 级联同步

新增课程后，**必须逐一更新**以下文件：

1. **README.md** — 课程表格添加新行，更新快速入口
2. **docs/index.html** — 首页课程列表添加新课程行（含 Notebook 和课程链接）
3. **docs/notes-lab.html** — 菜单树添加新的 tree-item：
   ```html
   <a href="#" class="tree-item" data-note="daily-YYYY-MM-DD" data-nb="nb-NN_课程名" data-title="第 N 课：课程名">
     <span class="tree-icon">📖</span> N. 课程名
   </a>
   ```
4. **docs/daily.html** — 时间线添加新条目

同步检查项：
- 进度百分比 = 已完成课时 / 预计总课时（约30课）
- 已完成课时数 + 1
- 连续学习天数（如适用）

## Phase 5: 最终验证

再次运行 validate.py：

```bash
python3 skills/ml-daily/scripts/validate.py
```

- **通过** → 进入 git push
- **未通过** → 回到 Phase 2 修复，最多重试 2 次。仍不通过则不 push，报告错误。

## Git 操作

```bash
git add -A
git commit -m "lesson: 第N课 课程名 + 完整性同步"
git push origin main
```

## 输出格式（每次任务结尾必须输出）

```
## 执行报告

### validate 结果
- Phase 1: [通过/失败 - 错误数]
- Phase 2: [无需修复/已修复N项]
- Phase 5: [通过/失败]

### 今日新增
- 第 N 课：课程名
- 新增文件：[列表]

### 修复内容（如有）
- [修复的具体内容]

### Git 状态
- commit: [hash]
- push: [成功/失败]
```
