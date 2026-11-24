from pathlib import Path
print('cwd',Path.cwd())
for p in Path('.').glob('*'): print(p)
for root in [Path('experiments'),Path('../experiments')]:
 print(root,root.exists())
 if root.exists():
  for p in root.rglob('*reduction*'): print(p)
