"""Canonical IA3 edge lifts modulo gamma3, using certified c<=2 equality."""
import pickle
from pathlib import Path
from itertools import combinations,product
from sage.all import Matrix,vector,ZZ
from agent2_nielsen_actions import magnus
from degree2_certificate import compose,inv,red
from agent1_degree3 import expand,Ds,dbr

ident,gs,gis,names=magnus(3);pairs=list(combinations(range(9),2))
B=Matrix(ZZ,[[dbr(Ds[i],Ds[j])[k].get(w,0) for i,j in pairs] for k in range(3) for w in product(range(3),repeat=3)])
D,U,V=B.smith_form();rank=B.rank();assert rank==18
assert all(D[i,i]==1 for i in range(rank))
keys=[];sign=[]
for d in Ds:
 k=next(k for k,p in enumerate(d) if p);w=next(w for w in d[k] if w[0]<w[1]);keys.append((k,w));sign.append(d[k][w])

def evaluate(w):
 f=ident
 for x in w:f=compose(f,gs[x-1] if x>0 else gis[-x-1])
 return f

def powerword(w,n):return w*n if n>=0 else inv(w)*(-n)

def preimage(f):
 """Return a Magnus word w such that f*w^-1 is in A3=gamma3(IA3)."""
 f=tuple(map(tuple,f));ex=[expand(f[k]+(-k-1,)) for k in range(3)]
 assert not any(len(w)==1 for p in ex for w in p)
 aa=[ex[k].get(w,0)*s for (k,w),s in zip(keys,sign)]
 w1=tuple(x for i,a in enumerate(aa) for x in powerword((i+1,),a))
 # Residual r=f*w1^-1 is in A2=gamma2; compute its true tau2.
 r=compose(f,evaluate(inv(w1)));rx=[expand(r[k]+(-k-1,)) for k in range(3)]
 assert not any(len(w) in (1,2) for p in rx for w in p)
 y=vector(ZZ,[rx[k].get(w,0) for k in range(3) for w in product(range(3),repeat=3)])
 z=U*y
 assert all(x==0 for x in z[rank:])
 xx=V*vector(ZZ,list(z[:rank])+[0]*(36-rank));assert B*xx==y
 w2=()
 for (i,j),a in zip(pairs,xx):
  if a:w2+=powerword((i+1,j+1,-i-1,-j-1),int(a))
 w=red(w2+w1)
 return w

if __name__=='__main__':
 cache=pickle.loads(Path('workspace/agent2_rs_merged_edgecache.pkl').read_bytes())
 for f in list(cache)[:50]:
  w=preimage(f)
  r=compose(f,evaluate(inv(w)))
  assert all(not any(1<=len(t)<=3 for t in expand(r[k]+(-k-1,))) for k in range(3))
 print('PASS 50 actualSchreieredges matched moduloA3=gamma3')
