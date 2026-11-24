from pathlib import Path
for p in sorted(Path('workspace').glob('*checks.py'))+sorted(Path('workspace').glob('*obstruction.py')):
 print('Executing',p.name,flush=True)
 exec(compile(p.read_text(),str(p),'exec'),{'__name__':'__main__'})
print('AUXILIARY CHECKS ONLY: no main completeness/exhaustivity assertion is encoded or verified.')