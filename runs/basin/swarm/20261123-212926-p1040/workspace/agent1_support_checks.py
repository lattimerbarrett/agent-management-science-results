"""Exact finite checks for support reduction of the degree-two Johnson kernel.
The universal proof is in agent1_support_lemma.txt. No modular rank inference.
"""
from itertools import product,combinations
from collections import defaultdict

def add(a,b,scale=1):
 c=dict(a)
 for w,v in b.items():
  c[w]=c.get(w,0)+scale*v
  if c[w]==0:del c[w]
 return c

def bracket(a,b):
 c=defaultdict(int)
 for u,x in a.items():
  for v,y in b.items():c[u+v]+=x*y;c[v+u]-=x*y
 return {w:x for w,x in c.items() if x}

def lyndon(w):return all(w<w[i:] for i in range(1,len(w)))
def lie(w):
 if len(w)==1:return {w:1}
 k=next(i for i in range(1,len(w)) if lyndon(w[i:]))
 return bracket(lie(w[:k]),lie(w[k:]))

def trace(i,p):
 c=defaultdict(int)
 for w,x in p.items():
  if w[0]==i:c[tuple(sorted(w[1:]))]+=x
 return {w:x for w,x in c.items() if x}

def deriv_apply(D,p):
 i,q=D;c=defaultdict(int)
 for w,x in p.items():
  for k,j in enumerate(w):
   if j==i:
    for v,y in q.items():c[w[:k]+v+w[k+1:]]+=x*y
 return {w:x for w,x in c.items() if x}

def deriv_bracket(D,E):
 i,p=D;j,q=E;c={}
 for k,v in [(j,deriv_apply(D,q)),(i,{w:-x for w,x in deriv_apply(E,p).items()})]:
  for w,x in v.items():
   key=(k,w);c[key]=c.get(key,0)+x
 return {w:x for w,x in c.items() if x}

def check(n):
 X=[{(i,):1} for i in range(n)]
 L3=[lie(w) for w in product(range(n),repeat=3) if lyndon(w)]
 traces=[]
 for i in range(n):
  for p in L3:
   t=trace(i,p)
   assert len(t)<=1 and all(abs(x)==1 for x in t.values())
   traces.append(t)
 for a in range(n):
  for b in range(a,n):
   if a!=b:r=a;p=bracket(bracket(X[a],X[b]),X[a])
   else:r=0 if a else 1;p=bracket(bracket(X[r],X[a]),X[a])
   t=trace(r,p)
   assert len(t)==1 and abs(t.get((a,b),0))==1
   assert p in L3 or {w:-x for w,x in p.items()} in L3
 V=[(i,bracket(X[a],X[b])) for i in range(n) for a,b in combinations(range(n),2)]
 for D,E in combinations(V,2):
  b=deriv_bracket(D,E)
  support={D[0],E[0]}|set().union(*(set(w) for w in D[1]))|set().union(*(set(w) for w in E[1]))
  if b:assert len(support)<=5
  t=defaultdict(int)
  for (i,w),x in b.items():
   if w[0]==i:t[tuple(sorted(w[1:]))]+=x
  assert all(x==0 for x in t.values())
 return len(L3),len(V),len(traces)
if __name__=='__main__':
 for n in range(2,8):print(n,check(n))
