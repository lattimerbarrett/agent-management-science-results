import sys,time,json
from pathlib import Path
from functools import lru_cache
from collections import Counter
sys.path.insert(0,'workspace')
from agent2_lpres_cover import build,libgap
from agent1_degree3 import L3,lyndon,ld,add
reps=json.load(open('workspace/agent2_c3_torsion_reps.json'))
for v in reps:
 for i in range(3):
  out={}
  for w,c in zip(L3,v):
   if c:out=add(out,ld(w)[i],c)
  assert not out
H=build();libgap.SetInfoLevel(libgap.InfoLPRES,1)
t=time.time();Q=libgap.NilpotentQuotient(H,4)
print('H4 computed seconds',time.time()-t,flush=True)
QS=libgap.NilpotentQuotientSystem(H);epi=QS['Epimorphism']
y=[libgap.Image(epi,x) for x in libgap.GeneratorsOfGroup(libgap.Source(epi))]
def comm(a,b):return a*b*a**-1*b**-1
@lru_cache(None)
def LW(w):
 if len(w)==1:return y[w[0]]
 k=next(k for k in range(1,len(w)) if lyndon(w[k:]))
 return comm(LW(w[:k]),LW(w[k:]))
checks=[]
beta=comm(comm(y[2],y[8]),y[7]);bc=[bool(comm(beta,x)==libgap.One(Q)) for x in y]
print('BETA centrality 9:',bc,flush=True)
for k,v in enumerate(reps):
 a=libgap.One(Q)
 for w,c in zip(L3,v):
  if c:a=a*LW(w)**int(c)
 row=[bool(comm(a,x)==libgap.One(Q)) for x in y]
 checks.append(row);print('torsionrep',k,'centrality',row,flush=True)
L=list(libgap.LowerCentralSeriesOfGroup(Q));invs=[]
for i in range(len(L)-1):
 iv=list(map(int,libgap.AbelianInvariants(libgap.FactorGroup(L[i],L[i+1]))));invs.append(iv)
 print('actual layer',i+1,Counter(iv),flush=True)
Path('workspace/agent4_H4_torsion_centrality.json').write_text(json.dumps({'seconds':time.time()-t,'beta':bc,'all_reps':checks,'layer_invariants':invs}))
