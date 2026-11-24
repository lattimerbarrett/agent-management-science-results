from pathlib import Path
import builtins
oldopen=builtins.open
def safeopen(file,mode='r',*args,**kwargs):
 if any(c in mode for c in 'wax+') and str(file).startswith('workspace/'):
  file='rerun_'+Path(file).name
 return oldopen(file,mode,*args,**kwargs)
builtins.open=safeopen
p=Path('workspace/agent2_combined_checker.py')
s=p.read_text().replace('ROOT=Path(__file__).resolve().parent', "ROOT=Path('workspace').resolve()")
s=s.replace("(ROOT/'agent2_combined_results.json').write_text", "Path('rerun_combined_results.json').write_text")
exec(compile(s,str(p),'exec'))
