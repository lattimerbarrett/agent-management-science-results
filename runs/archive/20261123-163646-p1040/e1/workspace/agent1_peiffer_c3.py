"""Genuine Peiffer relations via exact Aut action, truncated to class3."""
import json
from functools import lru_cache
from itertools import permutations
from sage.all import Matrix, ZZ
from agent1_degree3 import *
from agent1_degree3_closure import initial_vector

ONE={():1}
ID=tuple({(i,):1} for i in range(m))
def tmul(a,b):
 out={}
 aa=[[] for _ in range(4)];bb=[[] for _ in range(4)]
 for w,x in a.items():aa[len(w)].append((w,x))
 for w,x in b.items():bb[len(w)].append((w,x))
 for r in range(4):
  for s in range(4-r):
   for u,x in aa[r]:
    for v,y in bb[s]:out[u+v]=out.get(u+v,0)+x*y
 return {w:x for w,x in out.items() if x}
def subst(p,Q,cache=None):
 if cache is None:cache={():ONE}
 def mon(w):
  if w not in cache:cache[w]=tmul(mon(w[:-1]),Q[w[-1]])
  return cache[w]
 out={}
 for w,x in p.items():out=add(out,mon(w),x)
 return out

def ec(E,F):
 cache={():ONE}
 return tuple(subst(p,E,cache) for p in F)
def ei(E):
 A=Matrix(ZZ,[[p.get((j,),0) for j in range(m)] for p in E])
 Ai=A.inverse();assert Ai.base_ring()==ZZ or all(x in ZZ for x in Ai.list())
 Q=tuple({(j,):int(Ai[i,j]) for j in range(m) if Ai[i,j]} for i in range(m))
 L=Q
 for d in (2,3):
  PQ=ec(E,Q);new=[]
  for i,p in enumerate(PQ):
   err={w:x for w,x in p.items() if len(w)==d}
   new.append(add(Q[i],subst(err,L),-1))
  Q=tuple(new)
 assert ec(E,Q)==ID and ec(Q,E)==ID
 return Q

def ew(words):return tuple(add(expand(w),ONE,-1) for w in words)
def inner(i):
 out=[]
 for h in range(m):out.append(add(expand((i+1,h+1,-i-1)),ONE,-1))
 return tuple(out)

def main():
 data=json.load(open('workspace/agent2_nielsen_actions_n3.json'))
 act={name:ew(d['words']) for name,d in data['actions'].items()}
 # Signed permutation action on IA basis is exact, not just linear.
 names=[tuple(x) for x in data['names']]
 @lru_cache(None)
 def perm(perm):
  words=[]
  for name in names:
   if name[0]=='K':target=('K',perm[name[1]],perm[name[2]]);sgn=1
   else:
    i,j,k=[perm[x] for x in name[1:]];sgn=1 if j<k else -1
    target=('C',i,min(j,k),max(j,k))
   words.append((sgn*(names.index(target)+1),))
  return ew(words)
 @lru_cache(None)
 def R(i,j):
  pm=(i,j)+tuple(t for t in range(N) if t not in (i,j))
  ip=tuple(pm.index(t) for t in range(N))
  return ec(perm(pm),ec(act['T'],perm(ip)))
 @lru_cache(None)
 def I(i):
  pm=(i,)+tuple(t for t in range(N) if t!=i)
  ip=tuple(pm.index(t) for t in range(N))
  return ec(perm(pm),ec(act['I'],perm(ip)))
 out=[]
 for gi,name in enumerate(names):
  if name[0]=='K':
   _,i,j=name;r=ei(R(i,j));e=ec(I(i),ec(r,ec(I(i),r)))
  else:
   _,i,j,k=name;a=R(i,j);b=R(i,k)
   e=ec(a,ec(b,ec(ei(a),ei(b))))
  for h,p in enumerate(e):
   # phi_g(h) g h^-1 g^-1 is an actual identity in IA.
   ex=tmul(add(p,ONE),expand((gi+1,-h-1,-gi-1)))
   assert all(not x for w,x in ex.items() if len(w)==1)
   out.append(initial_vector(ex))
  print('built Peiffer relators for',gi+1,name,flush=True)
 json.dump(out,open('workspace/agent1_peiffer_vectors_c3.json','w'))
 print('saved',len(out),'exact class3 Peiffer vectors',flush=True)
 return out
if __name__=='__main__':main()
