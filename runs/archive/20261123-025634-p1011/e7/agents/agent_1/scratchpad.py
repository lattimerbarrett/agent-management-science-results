from pathlib import Path
import runpy, contextlib,io,time
files=sorted(Path('workspace').glob('agent[1234]_*.py'))
for p in files:
 out=io.StringIO()
 with contextlib.redirect_stdout(out): runpy.run_path(str(p),run_name='__main__')
 print('PASS',p,flush=True)
Path('workspace/agent1_full_audit.txt').write_text('\n'.join(map(str,files))+'\n')
print('All',len(files),'suites executed as __main__; missing requested existence remains unproved.')
