from pathlib import Path
root=Path('experiments')
for p in list(root.rglob('*'))[:80]:
 print(p)
