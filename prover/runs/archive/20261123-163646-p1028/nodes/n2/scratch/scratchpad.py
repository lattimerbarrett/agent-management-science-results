import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import numpy as np, scipy.linalg as la
import networkx as nx
import random, math, time, json, multiprocessing as mp

def search(args):
 n,d,restarts,steps=args
 rng=random.Random(32123+n*100+d)
 best=-1.; bestedges=None
 start=time.time()
 ground=n-1; rhs=np.zeros(n-1);rhs[0]=1.
 def value(L):
  try:
   fac=la.cho_factor(L,lower=True,check_finite=False)
   x=la.cho_solve(fac,rhs,check_finite=False)
   r=x[0]
   return r if 0<r<n-1+1e-5 else -1.
  except la.LinAlgError:return -1.
 def update(L,a,b,change):
  if a!=ground and b!=ground:L[a,b]+=change;L[b,a]+=change
 for rep in range(restarts):
  G=nx.random_regular_graph(d,n,seed=rng.randrange(10**9))
  edges=list(G.edges()); masks=[sum(1<<v for v in G[u]) for u in range(n)]
  L=d*np.eye(n-1)-nx.to_numpy_array(G,nodelist=range(n))[:-1,:-1]
  val=value(L)
  for k in range(steps):
   i,j=rng.sample(range(len(edges)),2)
   a,b=edges[i];c,e=edges[j]
   if rng.randrange(2):c,e=e,c
   if len({a,b,c,e})<4 or (masks[a]>>c)&1 or (masks[b]>>e)&1:continue
   # swap a-b,c-e -> a-c,b-e
   update(L,a,b,1);update(L,c,e,1);update(L,a,c,-1);update(L,b,e,-1)
   newval=value(L)
   temp=.13*(1-k/steps)**3+.0002
   if newval>0 and (newval>=val or rng.random()<math.exp(max(-745,(newval-val)/temp))):
    # Explicit connectivity test only for accepted candidates.
    masks[a]^=(1<<b)|(1<<c);masks[b]^=(1<<a)|(1<<e)
    masks[c]^=(1<<e)|(1<<a);masks[e]^=(1<<c)|(1<<b)
    seen=1;todo=1
    while todo:
     bit=todo & -todo;todo^=bit;u=bit.bit_length()-1
     more=masks[u]&~seen;seen|=more;todo|=more
    if seen==(1<<n)-1:
     edges[i]=(a,c);edges[j]=(b,e);val=newval
     if val>best+1e-9:
      best=val;bestedges=list(edges)
     continue
    masks[a]^=(1<<b)|(1<<c);masks[b]^=(1<<a)|(1<<e)
    masks[c]^=(1<<e)|(1<<a);masks[e]^=(1<<c)|(1<<b)
   update(L,a,b,-1);update(L,c,e,-1);update(L,a,c,1);update(L,b,e,1)
 out={'n':n,'d':d,'R':best,'commute':n*d*best,'edges':bestedges,'seconds':time.time()-start}
 with open('best_%s_%s.json'%(n,d),'w') as f:json.dump(out,f)
 return out

if __name__=='__main__':
 cases=[(n,4,24,8000) for n in [15,17,19,21,23,25,27,29]]
 cases += [(n,3,10,6000) for n in [10,12,14,16,18,20]]
 with mp.Pool(2) as pool:
  for out in pool.imap_unordered(search,cases):
   print({k:v for k,v in out.items() if k!='edges'},flush=True)
