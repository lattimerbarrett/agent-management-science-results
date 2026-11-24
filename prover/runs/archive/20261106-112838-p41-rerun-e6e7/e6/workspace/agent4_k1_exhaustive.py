import sys,time,json
from itertools import combinations
from pathlib import Path
sys.path.insert(0,'workspace')
from agent4_decomposable_check import kd
n=6;d=3;k=1
allf=[sum(1<<v for v in c) for c in combinations(range(n),d+1)]
N=1<<len(allf);good=bytearray(N);ext=bytearray(N);good[N-1]=1;ext[N-1]=1
start=time.time();counts=[0,0]
for a in range(N-1,0,-1):
    fac=tuple(sorted(allf[j] for j in range(len(allf)) if a>>j&1))
    if kd(fac,k):
        good[a]=1;counts[0]+=1
        if a==N-1 or any(ext[a|1<<j] for j in range(len(allf)) if not a>>j&1):ext[a]=1
        else:
            counts[1]+=1
            Path('workspace/agent4_k1_obstruction.json').write_text(json.dumps({'n':n,'d':d,'k':k,'facets':fac,'mask':a}))
            print('FOUND',a,fac,flush=True);break
    if a%4096==0:print(a,counts,'sec',time.time()-start,flush=True)
print('RESULT',counts,'seconds',time.time()-start,'cache',kd.cache_info())
Path('workspace/agent4_k1_exhaustive.py').write_text(Path(__file__).read_text())
