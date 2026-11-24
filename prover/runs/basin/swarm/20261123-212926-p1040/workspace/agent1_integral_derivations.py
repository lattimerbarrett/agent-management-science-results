"""Exact integral derivation arithmetic; unit pivots certify primitive sublattices."""
from itertools import combinations

def generators(n):
 return [{(i,(a,b)):1,(i,(b,a)):-1} for i in range(n) for a,b in combinations(range(n),2)]
def apply(a,w):
 out={}
 for k,x in enumerate(w):
  for (i,v),t in a.items():
   if i==x:
    z=w[:k]+v+w[k+1:];out[z]=out.get(z,0)+t
 return {z:t for z,t in out.items() if t}
def bracket(a,b):
 out={}
 for A,B,s in [(a,b,1),(b,a,-1)]:
  for (i,w),v in B.items():
   for z,t in apply(A,w).items():
    key=(i,z);out[key]=out.get(key,0)+s*v*t
 return {k:v for k,v in out.items() if v}
def bezout(a,b):
 old_r,r=a,b;old_s,s=1,0;old_t,t=0,1
 while r:
  q=old_r//r;old_r,r=r,old_r-q*r;old_s,s=s,old_s-q*s;old_t,t=t,old_t-q*t
 if old_r<0:return -old_r,-old_s,-old_t
 return old_r,old_s,old_t
def combine(a,x,b,y):
 z={k:x*v for k,v in a.items() if x*v}
 for k,v in b.items():
  t=z.get(k,0)+y*v
  if t:z[k]=t
  else:z.pop(k,None)
 return z
class UnitLattice:
 def __init__(self):self.b={};self.blocked=0;self.pending=[]
 def insert(self,v):
  v=v.copy()
  while v:
   p=min(v);a=v[p]
   if p not in self.b:
    self.b[p]={k:x*(1 if a>0 else -1) for k,x in v.items()};return True
   w=self.b[p];d=w[p]
   if a%d==0:v=combine(v,1,w,-a//d)
   else:
    g,s,t=bezout(d,a)
    self.b[p]=combine(w,s,v,t)
    v=combine(v,d//g,w,-a//g)
  return False

def image(n,d):
 g=generators(n);bs=g
 for k in range(2,d+1):
  L=UnitLattice()
  for a in g:
   for b in bs:L.insert(bracket(a,b))
  old=-1
  while old!=len(L.b):
   old=len(L.b);todo=L.pending;L.pending=[]
   for a in todo:L.insert(a)
  bs=list(L.b.values())
  if k==2:expected=n*n*(n*n-1)//3-n*(n+1)//2
  elif k==3:expected=n*(n**4-n*n)//4-(n**3+2*n)//3
  else:expected=None
  if expected is not None:print("expected",expected,"accepted",len(bs),"blocked",L.blocked,flush=True)
  print('integral image',n,k,len(bs),'pivot sizes',sorted(set(v[p] for p,v in L.b.items())),flush=True)
 return bs
if __name__=='__main__':
 for n in range(2,7):image(n,3)
