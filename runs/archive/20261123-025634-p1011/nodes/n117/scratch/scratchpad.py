from pathlib import Path
import shutil, runpy, os
src=Path('experiments/e3/boundary_yamabe_verified').resolve()
dst=Path('verification_e3').resolve()
if dst.exists(): shutil.rmtree(dst)
shutil.copytree(src,dst)
print('Copied verification bundle to writable directory',dst,flush=True)
runpy.run_path(str(dst/'verify_all.py'),run_name='__main__')
