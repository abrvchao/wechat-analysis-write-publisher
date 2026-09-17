#!/usr/bin/env python3
import argparse,html,json
from pathlib import Path
from formatter import ROOT,THEMES,render

def main():
    p=argparse.ArgumentParser(); p.add_argument('input',type=Path); p.add_argument('--output',type=Path,default=Path('theme-gallery.html')); a=p.parse_args(); md=a.input.read_text(encoding='utf-8')
    cards=[]
    for key,t in THEMES.items():
        body=render(md,key)
        cards.append(f'<article><header><b>{html.escape(t["label"])}</b><code>{key}</code></header><div class="paper">{body}</div></article>')
    page='''<!doctype html><meta charset="utf-8"><title>WeChat Theme Gallery</title><style>body{margin:0;background:#e5e7eb;font-family:system-ui}.top{position:sticky;top:0;background:#111827;color:white;padding:14px 24px;z-index:2}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:22px;padding:22px}article{background:white;border-radius:12px;box-shadow:0 5px 20px #0002;overflow:hidden}header{display:flex;justify-content:space-between;padding:12px 16px;background:#f8fafc;border-bottom:1px solid #e5e7eb}.paper{height:680px;overflow:auto;padding:18px}</style><div class="top"><b>WeChat Theme Gallery</b> · 选择主题 ID 后使用 formatter.py --theme ID</div><main class="grid">'''+''.join(cards)+'</main>'
    a.output.write_text(page,encoding='utf-8'); print(a.output)
if __name__=='__main__': main()
