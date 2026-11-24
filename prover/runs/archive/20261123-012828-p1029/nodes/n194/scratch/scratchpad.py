from pathlib import Path
root=Path('experiments/e1')
print('directory exists:',root.exists())
if root.exists():
    hits=list(root.rglob('*ultraproduct*'))
    for p in hits:
        print('\nFILE',p)
        if p.is_file() and p.suffix in ('.md','.txt'):
            text=p.read_text()
            print(text[:20000])
