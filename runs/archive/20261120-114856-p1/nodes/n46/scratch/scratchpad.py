from pathlib import Path
for x in ['experiments/e1','experiments/e4']:
 p=Path(x)
 print(x, p.exists())
 if p.exists(): print([str(y) for y in p.iterdir()][:15])
