from pathlib import Path
import shutil, runpy, os
src=Path('experiments/e3/boundary_yamabe_verified').resolve()
dst=Path('verification_e3').resolve()
shutil.copytree(src,dst,dirs_exist_ok=True)
runpy.run_path(str(dst/'verify_all.py'),run_name='__main__')
