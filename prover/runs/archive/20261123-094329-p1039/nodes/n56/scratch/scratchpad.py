from pathlib import Path
root=Path('experiments')
files=[p for p in root.rglob('*') if p.is_file()] if root.exists() else []
print('Available shared files:',len(files))
for p in files[:100]: print(p)
