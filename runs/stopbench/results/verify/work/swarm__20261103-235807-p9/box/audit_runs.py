from pathlib import Path
import runpy, time, sys
sys.path.insert(0,'workspace')
for fn in ['agent2_cantor_checks.py','agent2_toeplitz_finite.py','agent1_cantor_checks.py','agent1_upper_checks.py','agent4_upper_checks.py']:
 print('\nRUN',fn,flush=True)
 s=Path('workspace',fn).read_text()
 s='\n'.join(l for l in s.splitlines() if not l.startswith("Path('workspace/"))
 exec(compile(s,fn,'exec'),{'__name__':'__main__','__file__':str(Path('workspace',fn))})
