from pathlib import Path
import shutil, runpy, sys
sys.dont_write_bytecode=True
source=Path('experiments/e3/boundary_yamabe_verified')
target=Path('audit_e3')
shutil.copytree(source,target,dirs_exist_ok=True)
runpy.run_path(str(target/'verify_all.py'),run_name='__main__')
