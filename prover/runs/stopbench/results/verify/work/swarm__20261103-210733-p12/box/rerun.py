import os,sys,builtins,runpy
from pathlib import Path
print('cwd',os.getcwd(),flush=True)
os.makedirs('scratch',exist_ok=True)
orig=builtins.open

def op(path,mode='r',*a,**kw):
    s=str(path)
    if s.startswith('workspace/') and (any(x in mode for x in 'wax+') or os.path.exists('scratch/'+s[len('workspace/'):])):
        path='scratch/'+s[len('workspace/'):]
    return orig(path,mode,*a,**kw)
builtins.open=op
sys.path.insert(0,'workspace')
runpy.run_path('workspace/agent2_verify_support.py',run_name='__main__')
runpy.run_path('workspace/agent4_verify_lower.py',run_name='__main__')
runpy.run_path('workspace/agent3_validation.py',run_name='__main__')
