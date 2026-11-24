from pathlib import Path
for d in ['e1','e2']:
 print('\nFILES',d)
 for p in (Path('experiments')/d).iterdir():
  if p.is_file(): print(p.name)
for fn in ['agent2_plateau_drift.py','agent3_plateau_drift.py','agent3_logvolume.py']:
 p=Path('experiments/e2')/fn
 print('\n###',p,'\n',p.read_text())
