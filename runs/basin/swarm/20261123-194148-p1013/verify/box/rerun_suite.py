from pathlib import Path
import shutil,runpy,sys,os
src=Path('workspace').resolve()
out=Path('copied')/'workspace'
out.mkdir(exist_ok=True,parents=True)
for p in src.iterdir():
 if p.is_file() and p.suffix in ('.py','.json'):
  shutil.copy2(p,out/p.name)
os.chdir('copied')
sys.path.insert(0,str(Path('workspace').resolve()))
runpy.run_path('workspace/agent2_all_checks.py',run_name='__main__')
