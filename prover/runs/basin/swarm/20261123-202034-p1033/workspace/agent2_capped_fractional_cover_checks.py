from pathlib import Path
import itertools as it,random,time,json
import numpy as np
from scipy.optimize import linprog
rng=random.Random(371);start=time.time();results=[];counter=None
for r,n,N in [(3,6,1000),(4,8,3000)]:
 U=(1<<n)-1;E=[sum(1<<j for j in S) for S in it.combinations(range(n),r)];pairs=[(e,U^e) for e in E if e<(U^e)];small=[sum(1<<j for j in S) for S in it.combinations(range(n),r-1)];valid=0
 for z in range(N):
  fam=[p[rng.randrange(2)] for p in pairs]
  if any(all(F&C for F in fam) for C in small):continue
  valid+=1;A=-np.array([[int(F>>j&1) for j in range(n)] for F in fam],float);b=-np.ones(len(fam));c=np.ones(n)
  unc=linprog(c,A_ub=A,b_ub=b,bounds=[(0,None)]*n,method='highs');cap=linprog(c,A_ub=A,b_ub=b,bounds=[(0,1/(r-1))]*n,method='highs')
  assert unc.success and cap.success
  if cap.fun>unc.fun+1e-7:
   counter={'r':r,'n':n,'family':fam,'uncapped':unc.fun,'capped':cap.fun,'uncapped_cover':unc.x.tolist(),'capped_cover':cap.x.tolist()};break
 results.append({'r':r,'n':n,'samples':z+1,'valid_tau_r':valid,'counterexample':counter});print(results[-1],flush=True)
 if counter:break
Path('workspace/agent2_capped_fractional_cover_checks.py').write_text(Path('scratchpad.py').read_text());Path('workspace/agent2_capped_fractional_cover_checks.json').write_text(json.dumps(results,indent=2));print('seconds',time.time()-start)
