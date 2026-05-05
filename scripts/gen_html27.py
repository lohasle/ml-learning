#!/usr/bin/env python3
"""Generate HTML fragments for Lesson 27"""
import json, markdown, os

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

os.makedirs('docs', exist_ok=True)

# 1. Notebook HTML
nb_html = notebook_to_html('lessons/27_高效微调技术.ipynb')
with open('docs/nb-27_高效微调技术.html', 'w') as f:
    f.write(nb_html)
print(f"Generated: docs/nb-27_高效微调技术.html ({len(nb_html)} bytes)")

# 2. Daily HTML
with open('daily/2026-05-05.md') as f:
    md = f.read()
daily_html = markdown.markdown(md, extensions=['tables', 'fenced_code'])
with open('docs/daily-2026-05-05.html', 'w') as f:
    f.write(daily_html)
print(f"Generated: docs/daily-2026-05-05.html ({len(daily_html)} bytes)")

# 3. Note HTML
with open('notes/高效微调技术.md') as f:
    md = f.read()
note_html = markdown.markdown(md, extensions=['tables', 'fenced_code'])
with open('docs/note-高效微调技术.html', 'w') as f:
    f.write(note_html)
print(f"Generated: docs/note-高效微调技术.html ({len(note_html)} bytes)")
