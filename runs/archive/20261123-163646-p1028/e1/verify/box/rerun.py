from pathlib import Path
import shutil, subprocess, sys
src=Path('workspace/complete_certificate_agent1')
dst=Path('certificate_rerun')
if dst.exists(): shutil.rmtree(dst)
shutil.copytree(src,dst)
p=subprocess.run([sys.executable,'RUN_ALL.py'],cwd=dst,text=True,capture_output=True)
print('exit',p.returncode)
print(p.stdout)
print(p.stderr)
