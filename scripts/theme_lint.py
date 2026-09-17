#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
path=Path(__file__).resolve().parent.parent/'assets/themes.json'
themes=json.loads(path.read_text(encoding='utf-8')); errors=[]
required={'label','accent','accent2','text','muted','surface','font','radius'}
for name,t in themes.items():
    missing=required-set(t)
    if missing: errors.append(f'{name}: missing {sorted(missing)}')
    for key in ('accent','accent2','text','muted','surface'):
        if key in t and not re.fullmatch(r'#[0-9a-fA-F]{6}',t[key]): errors.append(f'{name}: invalid {key}')
if len(themes)<10: errors.append('at least 10 themes required')
if errors:
    print('\n'.join(errors),file=sys.stderr); raise SystemExit(1)
print(f'{len(themes)} themes valid')
