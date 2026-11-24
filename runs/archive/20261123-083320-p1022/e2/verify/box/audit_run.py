from pathlib import Path
import runpy, time
p=Path('/workspace')
# tools expose repository files by relative workspace/
src=Path('workspace/unified_full_certificate.py')
print('Running', src, flush=True)
t=time.time()
runpy.run_path(str(src), run_name='__main__')
print('elapsed', time.time()-t)
