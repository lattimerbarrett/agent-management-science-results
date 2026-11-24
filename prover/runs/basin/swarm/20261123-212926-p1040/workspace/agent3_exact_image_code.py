from pathlib import Path
code=r'''from itertools import product

def add(a,b,scale=1,p=1000003):
 c=a.copy()
 for k,v in b.items():
  z=(c.get(k,0)+scale*v)%p
  if z:c[k]=z
  elif k in c:del c[k]
 return c

def apply(a,w,p):
 out={}
 for k,x in enumerate(w):
  for (i,v),t in a.items():
   if i==x:
    key=w[:k]+v+w[k+1:]
    out[key]=(out.get(key,0)+t)%p
 return {k:v for k,v in out.items() if v}

def bracket(a,b,n,p):
 out={}
 for (i,w),v in b.items():
  for t,z in apply(a,w,p).items():
   key=(i,t);out[key]=(out.get(key,0)+v*z)%p
 for (i,w),v in a.items():
  for t,z in apply(b,w,p).items():
   key=(i,t);out[key]=(out.get(key,0)-v*z)%p
 return {k:v for k,v in out.items() if v}

def generators(n,p):
 ans=[]
 for i in range(n):
  for j in range(n):
   if i!=j:ans.append({(i,(j,i)):1,(i,(i,j)):p-1})
  for j in range(n):
   for k in range(j+1,n):
    if i not in (j,k):ans.append({(i,(j,k)):1,(i,(k,j)):p-1})
 return ans

def basis(vectors,p):
 piv={}
 for a in vectors:
  a=a.copy()
  while a:
   k=min(a)
   if k in piv:a=add(a,piv[k],-a[k],p)
   else:
    inv=pow(a[k],-1,p)
    piv[k]={t:v*inv%p for t,v in a.items()}
    break
 return list(piv.values())

def ranks(n,maxdegree,p=1000003):
 gs=generators(n,p);bs=gs;out=[len(bs)]
 for d in range(2,maxdegree+1):
  bs=basis((bracket(a,b,n,p) for a in gs for b in bs),p)
  out.append(len(bs))
  print(n,p,d,len(bs),flush=True)
 return out
'''
Path('workspace/agent3_derivations.py').write_text(code)
exec(code)
from fractions import Fraction

def bracket_Q(a,b,n):
 out={}
 def app(a,w):
  z={}
  for k,x in enumerate(w):
   for (i,v),t in a.items():
    if i==x:
     key=w[:k]+v+w[k+1:];z[key]=z.get(key,0)+t
  return z
 for (i,w),v in b.items():
  for t,z in app(a,w).items():
   key=(i,t);out[key]=out.get(key,0)+v*z
 for (i,w),v in a.items():
  for t,z in app(b,w).items():
   key=(i,t);out[key]=out.get(key,0)-v*z
 return {k:v for k,v in out.items() if v}
def basis_Q(vectors):
 piv={}
 for a in vectors:
  a=a.copy()
  while a:
   k=min(a)
   if k in piv:
    t=a[k]
    for x,v in piv[k].items():
     z=a.get(x,0)-t*v
     if z:a[x]=z
     elif x in a:del a[x]
   else:
    t=a[k];piv[k]={x:Fraction(v,t) for x,v in a.items()};break
 return list(piv.values())
