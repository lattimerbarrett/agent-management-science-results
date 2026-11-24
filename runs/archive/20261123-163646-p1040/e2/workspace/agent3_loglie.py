from collections import defaultdict
from math import factorial
import json,time
p=1000003;n=3;M=5

def add(a,b,s=1):
 d=a.copy()
 for w,v in b.items():
  d[w]=(d.get(w,0)+s*v)%p
  if not d[w]:del d[w]
 return d

def scale(a,s):return {w:v*s%p for w,v in a.items() if v*s%p}
def mul(a,b):
 d={}
 for u,x in a.items():
  for v,y in b.items():
   if len(u)+len(v)<=M:
    w=u+v;d[w]=(d.get(w,0)+x*y)%p
 return {w:v for w,v in d.items() if v}
def ex(i,sign=1):return {(i,)*k:pow(factorial(k),-1,p)*pow(sign,k,p)%p for k in range(M+1)}
def groupword(w):
 a={():1}
 for i,s in w:a=mul(a,ex(i,s))
 return a
def log(a):
 a=add(a,{():1},-1);ans={};b={():1}
 for k in range(1,M+1):
  b=mul(b,a);ans=add(ans,b,pow(k,-1,p)*(-1)**(k+1))
 return ans
X=[{(i,):1} for i in range(n)]
def subs(a,images):
 d={}
 for w,v in a.items():
  t={():1}
  for i in w:t=mul(t,images[i])
  d=add(d,t,v)
 return d
def autlog(images):
 ans=[]
 for i in range(n):
  t=X[i];a={}
  for k in range(1,M):
   t=add(subs(t,images),t,-1)
   a=add(a,t,pow(k,-1,p)*(-1)**(k+1))
  ans.append(a)
 return ans
G=[]
for i in range(n):
 for j in range(n):
  if i==j:continue
  images=X.copy();images[i]=log(groupword([(j,1),(i,1),(j,-1)]));G.append(autlog(images))
 for j in range(n):
  for k in range(j+1,n):
   if i in (j,k):continue
   images=X.copy();images[i]=log(groupword([(i,1),(j,1),(k,1),(j,-1),(k,-1)]));G.append(autlog(images))

def deriv(D,a):
 d={}
 for w,v in a.items():
  for k,i in enumerate(w):
   for u,z in D[i].items():
    if len(w)+len(u)-1<=M:
     ww=w[:k]+u+w[k+1:];d[ww]=(d.get(ww,0)+v*z)%p
 return {w:v for w,v in d.items() if v}
def bracket(D,E):return [add(deriv(D,E[i]),deriv(E,D[i]),-1) for i in range(n)]
def flat(D):return {(i,w):v for i,a in enumerate(D) for w,v in a.items()}
def unflat(d):return [{w:v for (j,w),v in d.items() if i==j} for i in range(n)]
class Space:
 def __init__(self):self.rows={}
 def insert(self,d):
  d=d.copy()
  while d:
   k=min(d,key=lambda k:(len(k[1]),k))
   if k not in self.rows:
    d=scale(d,pow(d[k],-1,p));self.rows[k]=d;return d
   d=add(d,self.rows[k],-d[k])
  return None
 def rank(self):return len(self.rows)
 def basis(self):return [unflat(d) for d in self.rows.values()]
S=Space()
for g in G:S.insert(flat(g))
W=[None,S]
for k in range(2,M):
 T=Space()
 for j,g in enumerate(G):
  for h in W[-1].basis():T.insert(flat(bracket(g,h)))
 W.append(T)
 print('W',k,T.rank(),flush=True)
for c in range(1,M):
 T=Space();U=Space()
 for k in range(c,M):
  for v in W[k].rows.values():
   T.insert(v);U.insert({key:x for key,x in v.items() if len(key[1])==c+1})
 print('gamma',c,T.rank(),'leading',U.rank(),flush=True)
json.dump({'W':[s.rank() for s in W[1:]]},open('workspace/agent3_trunc5.json','w'))
open('workspace/agent3_loglie.py','w').write(open(__file__).read())
