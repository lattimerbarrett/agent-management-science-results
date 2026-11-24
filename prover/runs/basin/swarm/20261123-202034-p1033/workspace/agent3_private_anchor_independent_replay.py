from pathlib import Path
import z3,json,time,hashlib
files=[Path('workspace/agent3_t6_rank6_d2_private_'+x+'.smt2') for x in ['ext_same','ext_new']]+[Path('workspace/agent3_t6_rank6_d2_n26_private_'+x+'.smt2') for x in ['ext_same','ext_new','ext_both']]
rows=[]
for p in files:
 st=time.time();s=z3.Solver();s.set(timeout=60000);s.from_string(p.read_text());r=s.check();assert r==z3.unsat,(p,r)
 row=dict(file=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),assertions=len(s.assertions()),result=str(r),seconds=time.time()-st);rows.append(row);print(row,flush=True)
Path('workspace/agent3_private_anchor_independent_replay.json').write_text(json.dumps(rows,indent=2))
Path('workspace/agent3_private_anchor_independent_replay.py').write_text(Path('scratchpad.py').read_text())