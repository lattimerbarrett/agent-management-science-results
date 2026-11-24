from pathlib import Path
import shutil,runpy
src=Path('experiments/e3/boundary_yamabe_verified')
dst=Path('local_e3_verification')
if not dst.exists(): shutil.copytree(src,dst)
runpy.run_path(str(dst/'verify_all.py'),run_name='__main__')
