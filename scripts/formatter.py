#!/usr/bin/env python3
"""Small deterministic Markdown-to-WeChat inline HTML renderer."""
import argparse, html, re
from pathlib import Path

THEMES = {
    "editorial": {"accent":"#9f1239","text":"#292524","muted":"#78716c","bg":"#fffaf5","font":"Georgia,'Noto Serif SC',serif"},
    "minimal": {"accent":"#334155","text":"#1f2937","muted":"#6b7280","bg":"#ffffff","font":"-apple-system,BlinkMacSystemFont,'PingFang SC',sans-serif"},
    "tech": {"accent":"#2563eb","text":"#172033","muted":"#64748b","bg":"#f8fafc","font":"-apple-system,BlinkMacSystemFont,'PingFang SC',sans-serif"},
}

def normalize(text):
    parts=re.split(r'(```[\s\S]*?```|`[^`]+`|https?://\S+)',text)
    for i,p in enumerate(parts):
        if p.startswith(('```','`','http://','https://')): continue
        p=re.sub(r'([\u4e00-\u9fff])([A-Za-z0-9])',r'\1 \2',p)
        p=re.sub(r'([A-Za-z0-9])([\u4e00-\u9fff])',r'\1 \2',p)
        p=re.sub(r'(?<=[\u4e00-\u9fff])[,;:!?](?=[\u4e00-\u9fff\s]|$)',lambda m:{',':'，',';':'；',':':'：','!':'！','?':'？'}[m.group()],p)
        parts[i]=p
    return ''.join(parts)

def inline(text, footnotes):
    text=html.escape(text,quote=False)
    text=re.sub(r'!\[([^]]*)\]\(([^)]+)\)',lambda m:f'<img src="{html.escape(m.group(2),quote=True)}" alt="{m.group(1)}" style="max-width:100%;height:auto;display:block;margin:18px auto;" />',text)
    def link(m):
        footnotes.append((m.group(1),m.group(2))); return f'{m.group(1)}<sup style="color:#64748b;">[{len(footnotes)}]</sup>'
    text=re.sub(r'\[([^]]+)\]\((https?://[^)]+)\)',link,text)
    text=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',text)
    text=re.sub(r'`([^`]+)`',r'<code style="background:#eef2f7;padding:2px 5px;border-radius:4px;font-family:monospace;">\1</code>',text)
    return text

def render(markdown, theme_name):
    t=THEMES[theme_name]; lines=normalize(markdown).splitlines(); out=[]; footnotes=[]; in_code=False; code=[]; list_kind=None; list_items=[]
    def flush_list():
        nonlocal list_kind,list_items
        if not list_items:return
        rows=[]
        for n,item in enumerate(list_items,1):
            mark=str(n)+'.' if list_kind=='ol' else '•'
            rows.append(f'<section style="display:flex;gap:10px;margin:7px 0;"><span style="color:{t["accent"]};font-weight:700;">{mark}</span><span>{inline(item,footnotes)}</span></section>')
        out.extend(rows); list_kind=None; list_items=[]
    for raw in lines+['']:
        if raw.strip().startswith('```'):
            flush_list()
            if in_code:
                out.append(f'<pre style="background:#111827;color:#e5e7eb;padding:16px;border-radius:8px;overflow-x:auto;"><code>{html.escape(chr(10).join(code))}</code></pre>'); code=[]
            in_code=not in_code; continue
        if in_code: code.append(raw); continue
        m=re.match(r'^\s*[-*]\s+(.+)',raw); n=re.match(r'^\s*\d+[.)]\s+(.+)',raw)
        if m or n:
            kind='ul' if m else 'ol'; item=(m or n).group(1)
            if list_kind and list_kind!=kind: flush_list()
            list_kind=kind; list_items.append(item); continue
        flush_list(); s=raw.strip()
        if not s: continue
        h=re.match(r'^(#{1,3})\s+(.+)',s)
        if h:
            level=len(h.group(1)); sizes={1:28,2:22,3:18}; out.append(f'<h{level} style="font-size:{sizes[level]}px;color:{t["text"]};border-left:4px solid {t["accent"]};padding-left:10px;margin:28px 0 14px;">{inline(h.group(2),footnotes)}</h{level}>'); continue
        if s=='---': out.append(f'<hr style="border:0;border-top:1px solid {t["muted"]};opacity:.35;margin:28px 0;" />'); continue
        q=re.match(r'^>\s*(?:\[!(tip|important|warning)\]\s*)?(.*)',s,re.I)
        if q:
            label=(q.group(1) or 'quote').upper(); out.append(f'<section style="background:{t["bg"]};border-left:4px solid {t["accent"]};padding:14px 16px;margin:18px 0;"><strong style="color:{t["accent"]};">{label}</strong><p style="margin:6px 0 0;">{inline(q.group(2),footnotes)}</p></section>'); continue
        out.append(f'<p style="font-size:16px;line-height:1.85;color:{t["text"]};margin:12px 0;letter-spacing:.02em;">{inline(s,footnotes)}</p>')
    if footnotes:
        items=''.join(f'<p style="font-size:12px;color:{t["muted"]};margin:4px 0;">[{i}] {html.escape(label)}：{html.escape(url)}</p>' for i,(label,url) in enumerate(footnotes,1))
        out.append(f'<section style="border-top:1px solid #e5e7eb;margin-top:28px;padding-top:12px;">{items}</section>')
    return f'<section style="max-width:680px;margin:0 auto;font-family:{t["font"]};">'+''.join(out)+'</section>'

def main():
    p=argparse.ArgumentParser(); p.add_argument('input',type=Path); p.add_argument('--theme',choices=THEMES,default='editorial'); p.add_argument('--output',type=Path,default=Path('content.html')); a=p.parse_args()
    a.output.write_text(render(a.input.read_text(encoding='utf-8'),a.theme),encoding='utf-8'); print(a.output)

if __name__=='__main__': main()
