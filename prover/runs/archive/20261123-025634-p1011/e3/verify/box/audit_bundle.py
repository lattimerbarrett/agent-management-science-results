from pathlib import Path
import shutil,runpy
src=Path('/mnt/workspace')
# Paths supplied by sandbox are relative to working directory's parent? resolve via actual provided relative paths.
src=Path('workspace/boundary_yamabe_verified').resolve()
print('source',src,src.exists())
dst=Path('bundle_copy').resolve()
if dst.exists(): shutil.rmtree(dst)
shutil.copytree(src,dst)
runpy.run_path(str(dst/'verify_all.py'),run_name='__main__')
