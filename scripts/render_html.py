#!/usr/bin/env python3
"""渲染今日课程所需的 HTML 片段"""
import json
import os
import sys

try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

BASE = '/home/lohasle/.openclaw/workspace-ml-learning'
DOCS = os.path.join(BASE, 'docs')

def notebook_to_html(nb_path):
    with open(nb_path) as f:
        nb = json.load(f)
    cells_html = []
    for cell in nb.get('cells', []):
        cell_type = cell.get('cell_type', '')
        source = ''.join(cell.get('source', []))
        if cell_type == 'markdown':
            if HAS_MARKDOWN:
                content = markdown.markdown(source, extensions=['tables', 'fenced_code'])
            else:
                content = source.replace('\n', '<br>\n')
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

def md_to_html(md_path):
    with open(md_path) as f:
        md = f.read()
    if HAS_MARKDOWN:
        return markdown.markdown(md, extensions=['tables', 'fenced_code'])
    else:
        return md.replace('\n', '<br>\n')

# 1. Notebook HTML
nb_path = os.path.join(BASE, 'lessons', '07_SVM支持向量机.ipynb')
nb_html = notebook_to_html(nb_path)
with open(os.path.join(DOCS, 'nb-07_SVM支持向量机.html'), 'w') as f:
    f.write(nb_html)
print(f"✅ Generated nb-07_SVM支持向量机.html ({len(nb_html)} bytes)")

# 2. Daily HTML
daily_path = os.path.join(BASE, 'daily', '2026-04-14.md')
daily_html = md_to_html(daily_path)
with open(os.path.join(DOCS, 'daily-2026-04-14.html'), 'w') as f:
    f.write(daily_html)
print(f"✅ Generated daily-2026-04-14.html ({len(daily_html)} bytes)")

# 3. Note HTML
note_path = os.path.join(BASE, 'notes', 'SVM支持向量机.md')
note_html = md_to_html(note_path)
with open(os.path.join(DOCS, 'note-SVM支持向量机.html'), 'w') as f:
    f.write(note_html)
print(f"✅ Generated note-SVM支持向量机.html ({len(note_html)} bytes)")

print("\n所有 HTML 片段生成完成！")
