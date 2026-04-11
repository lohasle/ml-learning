#!/usr/bin/env python3
"""
ml-learning 完整性验证脚本
输出 JSON 格式的检查结果，供子代理判断

用法: python3 skills/ml-daily/scripts/validate.py
退出码: 0=通过, 1=有错误
"""

import json, glob, os, re, sys

BASE = '/home/lohasle/.openclaw/workspace-ml-learning'
LESSONS = os.path.join(BASE, 'lessons')
DAILY = os.path.join(BASE, 'daily')
NOTES = os.path.join(BASE, 'notes')
DOCS = os.path.join(BASE, 'docs')
README = os.path.join(BASE, 'README.md')

results = {"pass": True, "errors": [], "warnings": [], "stats": {}, "gaps": []}

# === 1. Notebook 完整性 ===
notebooks = sorted(glob.glob(os.path.join(LESSONS, '*.ipynb')))
results["stats"]["notebooks"] = len(notebooks)

nb_numbers = []
for nb_path in notebooks:
    basename = os.path.basename(nb_path)
    m = re.match(r'(\d+)_(.+)\.ipynb', basename)
    if not m:
        results["warnings"].append(f"{basename}: 文件名不符合 NN_名称.ipynb 规范")
        continue
    
    num = int(m.group(1))
    name = m.group(2)
    nb_numbers.append(num)
    
    # 检查是否是合法 JSON
    try:
        with open(nb_path) as f:
            nb = json.load(f)
        cells = nb.get('cells', [])
        code_cells = [c for c in cells if c.get('cell_type') == 'code']
        md_cells = [c for c in cells if c.get('cell_type') == 'markdown']
        
        if len(cells) < 5:
            results["errors"].append(f"第{num}课 {basename}: 只有 {len(cells)} 个 cell（要求 ≥5）")
            results["pass"] = False
        
        if len(code_cells) < 2:
            results["warnings"].append(f"第{num}课 {basename}: 代码 cell 只有 {len(code_cells)} 个（建议 ≥3）")
        
        # 检查代码 cell 是否有实际内容
        empty_code = sum(1 for c in code_cells if not ''.join(c.get('source', [])).strip())
        if empty_code > 0:
            results["warnings"].append(f"第{num}课 {basename}: 有 {empty_code} 个空代码 cell")
            
    except json.JSONDecodeError as e:
        results["errors"].append(f"{basename}: JSON 解析失败 - {e}")
        results["pass"] = False
    except Exception as e:
        results["errors"].append(f"{basename}: 读取失败 - {e}")
        results["pass"] = False

# === 2. 课程编号连续性 ===
if nb_numbers:
    results["stats"]["max_lesson"] = max(nb_numbers)
    results["stats"]["lesson_numbers"] = sorted(nb_numbers)
    
    for i in range(1, max(nb_numbers) + 1):
        if i not in nb_numbers:
            results["errors"].append(f"课程编号不连续：缺少第 {i} 课")
            results["gaps"].append({"type": "missing_lesson", "number": i})
            results["pass"] = False

# === 3. Daily 记录检查 ===
daily_files = sorted([f for f in glob.glob(os.path.join(DAILY, '*.md')) if os.path.basename(f) != 'README.md'])
results["stats"]["dailies"] = len(daily_files)

for df in daily_files:
    basename = os.path.basename(df)
    size = os.path.getsize(df)
    if size < 500:
        results["warnings"].append(f"{basename}: 文件过小 ({size} bytes，建议 >1000)")
    with open(df) as f:
        content = f.read()
    if len(content.strip()) < 200:
        results["errors"].append(f"{basename}: 内容几乎为空")
        results["pass"] = False

# === 4. Docs HTML 片段同步 ===
generated_html = []
missing_html = []

for nb_path in notebooks:
    basename = os.path.basename(nb_path)
    name = basename.replace('.ipynb', '')
    html_path = os.path.join(DOCS, f'nb-{name}.html')
    if not os.path.exists(html_path):
        missing_html.append(f'nb-{name}.html')
    else:
        generated_html.append(f'nb-{name}.html')

if missing_html:
    results["errors"].append(f"缺少 Notebook HTML 片段: {', '.join(missing_html)}")
    for h in missing_html:
        results["gaps"].append({"type": "missing_nb_html", "file": h})
    results["pass"] = False

for df in daily_files:
    name = os.path.basename(df).replace('.md', '')
    html_path = os.path.join(DOCS, f'daily-{name}.html')
    if not os.path.exists(html_path):
        results["warnings"].append(f"缺少 daily HTML 片段: daily-{name}.html")

# 知识笔记 HTML 片段
for nf in sorted(glob.glob(os.path.join(NOTES, '*.md'))):
    name = os.path.basename(nf).replace('.md', '')
    html_path = os.path.join(DOCS, f'note-{name}.html')
    if not os.path.exists(html_path):
        results["warnings"].append(f"缺少笔记 HTML 片段: note-{name}.html")

# === 5. notes-lab.html 菜单项检查 ===
notes_lab = os.path.join(DOCS, 'notes-lab.html')
if os.path.exists(notes_lab):
    with open(notes_lab) as f:
        lab_content = f.read()
    
    nb_refs = re.findall(r'data-nb="([^"]+)"', lab_content)
    for ref in nb_refs:
        if ref and not os.path.exists(os.path.join(DOCS, f'{ref}.html')):
            results["errors"].append(f"notes-lab.html 引用了 {ref}.html 但文件不存在")
            results["gaps"].append({"type": "broken_lab_ref", "ref": ref, "file": f"{ref}.html"})
            results["pass"] = False
    
    note_refs = re.findall(r'data-note="([^"]+)"', lab_content)
    for ref in note_refs:
        if not os.path.exists(os.path.join(DOCS, f'{ref}.html')):
            results["errors"].append(f"notes-lab.html 引用了 {ref}.html 但文件不存在")
            results["gaps"].append({"type": "broken_lab_ref", "ref": ref, "file": f"{ref}.html"})
            results["pass"] = False
    
    # 检查菜单项数量与实际 notebook 数量是否匹配
    menu_items = re.findall(r'class="tree-item"', lab_content)
    lesson_menu_items = re.findall(r'data-nb="nb-\d+_', lab_content)
    if len(lesson_menu_items) != len(notebooks):
        results["warnings"].append(
            f"notes-lab.html 课程菜单项 ({len(lesson_menu_items)}) 与 notebook 数 ({len(notebooks)}) 不一致"
        )
else:
    results["warnings"].append("notes-lab.html 不存在")

# === 6. README 一致性 ===
if os.path.exists(README):
    with open(README) as f:
        readme_content = f.read()
    readme_lesson_links = readme_content.count('lessons/')
    if readme_lesson_links != len(notebooks):
        results["warnings"].append(
            f"README 课程引用 ({readme_lesson_links}) 与 notebook 数 ({len(notebooks)}) 不一致"
        )
else:
    results["errors"].append("README.md 不存在")
    results["pass"] = False

# === 7. index.html 课程列表检查 ===
index_html = os.path.join(DOCS, 'index.html')
if os.path.exists(index_html):
    with open(index_html) as f:
        idx_content = f.read()
    idx_lessons = re.findall(r'lesson-num', idx_content)
    if len(idx_lessons) != len(notebooks):
        results["warnings"].append(
            f"index.html 课程行数 ({len(idx_lessons)}) 与 notebook 数 ({len(notebooks)}) 不一致"
        )

# === 输出 ===
print(json.dumps(results, ensure_ascii=False, indent=2))
sys.exit(0 if results["pass"] else 1)
