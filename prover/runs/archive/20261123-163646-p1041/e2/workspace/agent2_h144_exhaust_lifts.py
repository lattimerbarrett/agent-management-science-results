import itertools,json,time,sys
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese
from collections import Counter

def kernel(S,m,d=4):
 vs=veronese(m,d);basis={};rels=[]
 for i,p in enumerate(S):
  v=vs[p];c=1<<i
  while v:
   j=v.bit_length()-1
   if j not in basis:basis[j]=(v,c);break
   b,bc=basis[j];v^=b;c^=bc
  if not v:rels.append(c)
 return rels

def extra_basis(S,m,rels):
 basis={};extra=[]
 def ins(v):
  while v:
   j=v.bit_length()-1
   if j in basis:v^=basis[j]
   else:basis[j]=v;return True
  return False
 assert ins((1<<len(S))-1)
 for j in range(m):assert ins(sum(1<<i for i,p in enumerate(S) if p>>j&1))
 for v in rels:
  if ins(v):extra.append(v)
 return extra

S=[x for x in range(256) if 1^((x>>0&1)&(x>>1&1))^((x>>2&1)&(x>>3&1))^((x>>4&1)&(x>>5&1))]
assert len(S)==144
stats=Counter();nodes=0;maxm=8;t0=time.time();cache={}
def walk(S,m,path):
 global nodes,maxm
 rels=kernel(S,m);extra=extra_basis(S,m,rels);D=len(extra);nodes+=1;maxm=max(m,maxm);stats[m,len(rels),D]+=1
 if D==0:return
 if D>8:raise RuntimeError(('too large',m,D))
 for bits in range(1,1<<D):
  label=0
  for j,v in enumerate(extra):
   if bits>>j&1:label^=v
  SS=[p|(((label>>i)&1)<<m) for i,p in enumerate(S)]
  walk(SS,m+1,path+[bits])
walk(S,8,[])
A={sum(((u>>i)&1)<<i for i in range(6)) for u in range(64)}
B={sum(((u>>i)&1)<<j for i,j in enumerate([0,1,2,3,6,7])) for u in range(64)}
C={16^sum(((u>>i)&1)<<j for i,j in enumerate([0,1,2,8,9,10])) for u in range(64)}
SS=sorted(A^B^C);assert len(SS)==144
print('second seed Kdim',len(kernel(SS,11)),flush=True)
walk(SS,11,[])
print('nodes',nodes,'maxm',maxm,'stats',stats,'sec',time.time()-t0)
json.dump({'nodes':nodes,'maxm':maxm,'stats':{str(k):v for k,v in stats.items()}},open('workspace/agent2_h144_exhaust_lifts.json','w'))
from pathlib import Path
Path('workspace/agent2_h144_exhaust_lifts.py').write_text(Path(__file__).read_text())
