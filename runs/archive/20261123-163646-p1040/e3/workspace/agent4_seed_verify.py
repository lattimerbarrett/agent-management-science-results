import sys,json
from pathlib import Path
sys.path.insert(0,'workspace')
from agent4_derivations import *
g=generators(3)
def dw(t):
 i,j,k,l=t
 return deriv_bracket(deriv_bracket(deriv_bracket(g[i],g[j]),g[k]),g[l])
terms=[((0,1,5,2),3),((0,1,1,1),-4),((0,2,5,1),2),((1,2,3,1),-2)]
S=tuple({} for _ in range(3))
for t,a in terms:
 S=tuple(add(u,v,a) for u,v in zip(S,dw(t)))
assert all(not u for u in S)
tg=[{(1,):1},{(0,):1},{(0,):1,(1,):1},{(2,):1},{(0,):1},{(0,):1,(2,):1},{(2,):1},{(1,):1},{(1,):1,(2,):1}]
def tb(P,Q):
 out=set()
 for a in P:
  for b in Q:
   for w in [a+b,b+a]:
    if all(x!=y for x,y in zip(w,w[1:])):
     if w in out:out.remove(w)
     else:out.add(w)
 return out
P=tb(tb(tb(tg[0],tg[1]),tg[5]),tg[2])
print('target polynomial', [''.join('ABC'[x] for x in w) for w in sorted(P)])
assert P
for d in range(4,20):
 w=min(P); c=next(c for c in range(3) if c not in (w[0],w[-1]))
 P=tb(P,{(c,)})
 assert P and all(len(w)==d+1 for w in P)
 print(d+1,len(P),'bracket with','ABC'[c])
