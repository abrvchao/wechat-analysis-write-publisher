#!/usr/bin/env python3
"""Deterministic Markdown to WeChat inline HTML renderer."""
import argparse, html, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
THEMES=json.loads((ROOT/'assets/themes.json').read_text(encoding='utf-8'))

def normalize(text):
    parts=re.split(r'(```[\s\S]*?```|`[^`]+`|https?://\S+)',text)
    for i,p in enumerate(parts):
        if p.startswith(('```','`','http://','https://')): continue
        p=re.sub(r'([\u4e00-\u9fff])([A-Za-z0-9])',r'\1 \2',p)
        p=re.sub(r'([A-Za-z0-9])([\u4e00-\u9fff])',r'\1 \2',p)
        p=re.sub(r'(?<=[\u4e00-\u9fff])[,;:!?](?=[\u4e00-\u9fff\s]|$)',lambda m:{',':'，',';':'；',':':'：','!':'！','?':'？'}[m.group()],p)
        p=re.sub(r'\*\*([^*]+?)([，。！？；：])\*\*',r'**\1**\2',p); parts[i]=p
    return ''.join(parts)

def inline(text,notes):
    text=html.escape(text,quote=False)
    text=re.sub(r'!\[([^]]*)\]\(([^)]+)\)',lambda m:f'<img src="{html.escape(m.group(2),quote=True)}" alt="{m.group(1)}" style="max-width:100%;height:auto;display:block;margin:20px auto 6px;border-radius:8px;" />',text)
    def link(m):
        notes.append((m.group(1),m.group(2))); return f'{m.group(1)}<sup style="font-size:10px;">[{len(notes)}]</sup>'
    text=re.sub(r'\[([^]]+)\]\((https?://[^)]+)\)',link,text)
    text=re.sub(r'\*\*([^*]+)\*\*',r'<strong style="font-weight:700;">\1</strong>',text)
    text=re.sub(r'\*([^*]+)\*',r'<em>\1</em>',text)
    text=re.sub(r'`([^`]+)`',r'<code style="background:#eef2f7;color:#be123c;padding:2px 5px;border-radius:4px;font-family:monospace;">\1</code>',text)
    return text

def component(kind,title,body,t,notes):
    a=t['accent']; s=t['surface']; r=t['radius']; rows=[x.strip() for x in body if x.strip()]
    if kind=='dialogue':
        items=[]
        for i,x in enumerate(rows):
            who,msg=(x.split(':',1)+[''])[:2] if ':' in x else ('',x)
            align='flex-end' if i%2 else 'flex-start'; bg=a if i%2 else s; color='#fff' if i%2 else t['text']
            items.append(f'<section style="display:flex;justify-content:{align};margin:9px 0;"><span style="max-width:82%;background:{bg};color:{color};padding:9px 12px;border-radius:14px;">{inline((who+"：" if who else "")+msg,notes)}</span></section>')
        return ''.join(items)
    if kind in ('steps','timeline'):
        return ''.join(f'<section style="display:flex;gap:12px;margin:12px 0;"><strong style="flex:0 0 28px;height:28px;line-height:28px;text-align:center;border-radius:50%;background:{a};color:#fff;">{i}</strong><span style="padding-top:3px;">{inline(x,notes)}</span></section>' for i,x in enumerate(rows,1))
    if kind=='stat':
        return '<section style="display:flex;flex-wrap:wrap;gap:10px;">'+''.join(f'<section style="flex:1;min-width:120px;background:{s};padding:14px;text-align:center;border-radius:{r};"><strong style="font-size:22px;color:{a};">{inline(x,notes)}</strong></section>' for x in rows)+'</section>'
    if kind=='compare':
        cols=''.join(f'<section style="flex:1;min-width:140px;background:{s};padding:14px;border-radius:{r};">{inline(x,notes)}</section>' for x in rows)
        return f'<section style="display:flex;gap:10px;flex-wrap:wrap;">{cols}</section>'
    if kind=='quote':
        return f'<section style="text-align:center;border-top:2px solid {a};border-bottom:2px solid {a};padding:22px;margin:24px 0;font-family:{t["font"]};font-size:19px;">{inline(" ".join(rows),notes)}</section>'
    if kind=='intro':
        return f'<section style="background:{s};border-radius:{r};padding:18px;margin:18px 0;"><strong style="color:{a};">{html.escape(title or "导读")}</strong><p>{inline(" ".join(rows),notes)}</p></section>'
    if kind=='end':
        return f'<section style="text-align:center;color:{t["muted"]};margin:32px 0;letter-spacing:.2em;">— END —<br><small>{inline(title or " ".join(rows),notes)}</small></section>'
    return f'<section style="background:{s};border-left:4px solid {a};padding:14px;border-radius:{r};margin:16px 0;">{inline(" ".join(rows),notes)}</section>'

def extract_components(text,t,notes):
    slots={}
    pat=re.compile(r':::(dialogue|steps|timeline|stat|compare|quote|intro|end)(?:\[([^]]*)\])?\n(.*?)\n:::',re.S)
    def repl(m):
        key=f'@@COMP{len(slots)}@@'; slots[key]=component(m.group(1),m.group(2) or '',m.group(3).splitlines(),t,notes); return key
    return pat.sub(repl,text),slots

def render(markdown,theme_name):
    t=THEMES[theme_name]; notes=[]; text,slots=extract_components(normalize(markdown),t,notes); out=[]; code=[]; in_code=False; list_kind=None; items=[]
    def flush():
        nonlocal list_kind,items
        for i,x in enumerate(items,1):
            mark=f'{i}.' if list_kind=='ol' else '•'; out.append(f'<section style="display:flex;gap:10px;margin:7px 0;"><span style="color:{t["accent"]};font-weight:700;">{mark}</span><span>{inline(x,notes)}</span></section>')
        list_kind=None; items=[]
    for raw in text.splitlines()+['']:
        if raw.strip().startswith('```'):
            flush()
            if in_code: out.append(f'<pre style="background:#111827;color:#e5e7eb;padding:16px;border-radius:8px;overflow-x:auto;"><code>{html.escape(chr(10).join(code))}</code></pre>'); code=[]
            in_code=not in_code; continue
        if in_code: code.append(raw); continue
        if raw.strip() in slots: flush(); out.append(slots[raw.strip()]); continue
        m=re.match(r'^\s*[-*]\s+(.+)',raw); n=re.match(r'^\s*\d+[.)]\s+(.+)',raw)
        if m or n:
            kind='ul' if m else 'ol';
            if list_kind and list_kind!=kind: flush()
            list_kind=kind; items.append((m or n).group(1)); continue
        flush(); s=raw.strip()
        if not s: continue
        h=re.match(r'^(#{1,4})\s+(.+)',s)
        if h:
            lv=len(h.group(1)); size={1:30,2:23,3:19,4:17}[lv]; border=f'border-left:4px solid {t["accent"]};padding-left:10px;' if lv>1 else ''
            out.append(f'<h{lv} style="font-size:{size}px;color:{t["text"]};{border}margin:28px 0 14px;line-height:1.4;">{inline(h.group(2),notes)}</h{lv}>'); continue
        if s=='---': out.append(f'<hr style="border:0;border-top:1px solid {t["accent"]};opacity:.3;margin:28px 0;" />'); continue
        q=re.match(r'^>\s*(?:\[!(tip|note|important|warning|caution)\]\s*)?(.*)',s,re.I)
        if q:
            label=(q.group(1) or 'quote').upper(); out.append(f'<section style="background:{t["surface"]};border-left:4px solid {t["accent"]};padding:14px 16px;margin:18px 0;border-radius:{t["radius"]};"><strong style="color:{t["accent"]};">{label}</strong><p style="margin:6px 0 0;">{inline(q.group(2),notes)}</p></section>'); continue
        if re.match(r'^>>+\s+',s): out.append(component('quote','',[re.sub(r'^>>+\s+','',s)],t,notes)); continue
        out.append(f'<p style="font-size:16px;line-height:1.85;color:{t["text"]};margin:12px 0;letter-spacing:.02em;">{inline(s,notes)}</p>')
    if notes:
        entries=''.join(f'<p style="font-size:12px;color:{t["muted"]};margin:4px 0;">[{i}] {html.escape(x)}：{html.escape(u)}</p>' for i,(x,u) in enumerate(notes,1)); out.append(f'<section style="border-top:1px solid {t["muted"]};margin-top:28px;padding-top:12px;">{entries}</section>')
    return f'<section data-theme="{theme_name}" style="max-width:680px;margin:0 auto;padding:4px 12px;background:{t["surface"] if theme_name=="midnight" else "#fff"};font-family:{t["font"]};">'+''.join(out)+'</section>'

def main():
    p=argparse.ArgumentParser(); p.add_argument('input',type=Path); p.add_argument('--theme',choices=THEMES,default='editorial-red'); p.add_argument('--output',type=Path,default=Path('content.html')); p.add_argument('--list-themes',action='store_true'); a=p.parse_args()
    if a.list_themes:
        print('\n'.join(f'{k}\t{v["label"]}' for k,v in THEMES.items())); return
    a.output.write_text(render(a.input.read_text(encoding='utf-8'),a.theme),encoding='utf-8'); print(a.output)
if __name__=='__main__': main()
