import sys,contextlib,io,json,time
sys.path.insert(0,'workspace')
with contextlib.redirect_stdout(io.StringIO()):import fz25_upper as F
from functools import lru_cache
from fractions import Fraction as Q
P=1000000007
@lru_cache(None)
def basis(d):return tuple((p,t) for t in range(d+1) for p in F.partitions(d-t))
@lru_cache(None)
def unrel(h,r,sigma):
 F.k0=2*h-1
 return F.rel(r,sigma)
@lru_cache(None)
def pointed_relation(h,r,sigma,a):
 out={}
 for t in range(r+1):
  c=(F.A if a==0 else F.B)[t]
  for q,v in unrel(h,r-t,sigma).items():
   q0=Q(v*c);out[(q,t)]=q0.numerator*pow(q0.denominator,-1,P)%P
 return out

def relation_rows(h,d,cap=4):
 idx={x:i for i,x in enumerate(basis(d))}
 for r in range(1,d+1):
  for a in (0,1):
   for sz in range(min(cap,3*r-h-a-1)+1):
    if (3*r-h-1-a-sz)%2:continue
    for sigma in F.partitions(sz):
     if any(s%3==2 for s in sigma):continue
     rr=pointed_relation(h,r,sigma,a)
     for extra,psi in basis(d-r):
      row=[0]*len(idx)
      for (kp,t),c in rr.items():row[idx[(tuple(sorted(kp+extra,reverse=True)),t+psi)]]=c
      yield row

def echelon(rows,n):
 piv={}
 for row in rows:
  row=list(row)
  for j in range(n):
   v=row[j]
   if not v:continue
   if j in piv:
    c=row[j];row=[(x-c*y)%P for x,y in zip(row,piv[j])]
   else:
    inv=pow(v,-1,P);row=[x*inv%P for x in row];piv[j]=row;break
  if len(piv)==n:break
 return piv
if __name__=='__main__':
 T=time.time()
 for h in [1,2,3,4,6,12,13,23,24]:
  dims=[]
  for d in range(13):
   e=echelon(relation_rows(h,d),len(basis(d)));dims.append(len(basis(d))-len(e))
  print(h,dims,'time',time.time()-T,flush=True)
