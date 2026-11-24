from pathlib import Path
print([p.name for p in Path('workspace').glob('*presentation*')])
for p in Path('workspace').glob('agent3*aut*'):
 print(p.name)
