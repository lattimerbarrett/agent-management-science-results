from collections import defaultdict
from pathlib import Path
# Independent integer derivation verification in free associative algebra.
def pa(a,b):
 c=a.copy()
 for w,x in b.items():
  c[w]=c.get(w,0)+x
  if not c[w]:del c[w]
 return c
def pm(a,b):
 c=defaultdict(int)
 for w,x in a.items():
  for u,y in b.items():c[w+u]+=x*y
 return {w:x for w,x in c.items() if x}
def neg(a):return {w:-v for w,v in a.items()}
def pb(a,b):return pa(pm(a,b),neg(pm(b,a)))
def da(D,f):
 out={}
 for w,t in f.items():
  for k,i in enumerate(w):
   for v,c in D[i].items():out=pa(out,{w[:k]+v+w[k+1:]:t*c})
 return out
def db(D,E):return tuple(pa(da(D,e),neg(da(E,d))) for d,e in zip(D,E))
X=[{(i,):1} for i in range(3)];g=[];names=[]
for i in range(3):
 js=[j for j in range(3) if j!=i]
 for j in js:
  D=[{},{},{}];D[i]=pb(X[j],X[i]);g.append(tuple(D));names.append(('K',i+1,j+1))
 D=[{},{},{}];D[i]=pb(X[js[0]],X[js[1]]);g.append(tuple(D));names.append(('M',i+1,js[0]+1,js[1]+1))
def W(t):
 i,j,k,l=t;return db(db(db(g[i],g[j]),g[k]),g[l])
terms=[(3,(0,1,5,2)),(-4,(0,1,1,1)),(2,(0,2,5,1)),(-2,(1,2,3,1))]
out=[{},{},{}]
for c,t in terms:
 v=W(t)
 for i in range(3):out[i]=pa(out[i],{w:c*a for w,a in v[i].items()})
print('order',names);print('combined supports',list(map(len,out)));assert not any(out)
print('W0152 support sizes',list(map(len,W((0,1,5,2)))),'coeffs',sorted(set(v for a in W((0,1,5,2)) for v in a.values())))
