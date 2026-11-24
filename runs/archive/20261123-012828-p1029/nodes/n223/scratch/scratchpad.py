from pathlib import Path
for p in Path('experiments').rglob('*.md'):
    text=p.read_text()
    for i,line in enumerate(text.splitlines(),1):
        if any(s in line.lower() for s in ['cauchy', 'gluing', 'metric complete', 'monotone sequential']):
            print(f'{p}:{i}: {line}')
