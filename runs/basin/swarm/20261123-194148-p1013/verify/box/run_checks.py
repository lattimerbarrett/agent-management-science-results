from pathlib import Path
import runpy,os,sys
sys.path.insert(0,'/workspace')
p=Path('../workspace/final_checks.py')
if not p.exists():
    p=Path('workspace/final_checks.py')
print('cwd',os.getcwd(),'file',p.resolve())
exec(compile(p.read_text(),str(p),'exec'))
