from pathlib import Path
root=Path('experiments/e1')
print('Exists:',root.exists())
if root.exists():
    for p in root.rglob('*completion*'):
        print('\nFILE',p)
        if p.is_file(): print(p.read_text()[:24000])
