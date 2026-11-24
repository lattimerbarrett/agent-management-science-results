from fractions import Fraction as Q
from math import comb
import sympy as s

def add(a,b,c=Q(1)):
 for e,v in b.items():
  a[e]=a.get(e,Q(0))+c*v
  if not a[e]: del a[e]
 return a

def mul(a,b,cap):
 c={}
 for e,v in a.items():
  for f,w in b.items():
   if e+f<=cap: c[e+f]=c.get(e+f,Q(0))+v*w
 return {e:v for e,v in c.items() if v}

def binom(a,j):
 v=Q(1)
 for i in range(j): v*=Q(a-i,i+1)
 return v

def compute(g,b,alpha,d,verbose=False):
 k=g-(g+2)//3; N=2*g-2-d; P=2*g-1; H=4*g+2
 cap=max(0,-d)+(N//k+2)*P+H
 phi={-(2*g-1-2*j):Q(v) for j,v in enumerate(b) if v}
 powers=[{0:Q(1)}]
 for j in range(N//k+1):powers.append(mul(powers[-1],phi,cap))
 def ubasis(pole):
  if pole%2==0:return {-pole:Q(1)}
  return {-pole+j*H:binom(Q(1,2),j)*(-1)**j for j in range((cap+pole)//H+1)}
 def reduce(f,n):
  f=f.copy(); h={}; w={}; threshold=-n-d
  while f:
   e=min(f); v=f.pop(e)
   if not v:continue
   if e>=threshold:
    if e<=cap:w[e]=v
   elif e<=0 and ((-e)%2==0 or -e>=2*g+1):
    u=ubasis(-e); u.pop(e)
    add(f,u,-v)
   else:h[e]=v
  return h,w
 rows=[]
 for n in range(N+1):
  for e in range(-n-d): pass
  # H1 basis: all Laurent powers below threshold not leading U monomials
  for e in range(-(2*g-1),-n-d):
   if not (e<=0 and ((-e)%2==0 or -e>=2*g+1)):rows.append((n,e))
 index={z:i for i,z in enumerate(rows)}
 columns=[]
 def propagate(co,n,w,fac):
  for j in range(1,(N-n)//k+1):
   c=binom(Q(alpha)-Q(n,k),j)*k**j*fac
   if c:add(co[n+j*k],mul(w,powers[j],cap),c)
 for n in range(N+1):
  for pole in range(max(-1,n+d)+1):
   if pole%2 and pole<2*g+1:continue
   co=[{} for z in range(N+1)]
   propagate(co,n,ubasis(pole),Q(1))
   col={}
   for m in range(n+k,N+1):
    h,w=reduce(co[m],m)
    for e,v in h.items():col[index[m,e]]=v
    propagate(co,m,w,Q(-1))
   if col:columns.append(col)
 M=s.MutableSparseMatrix(len(rows),len(columns),{})
 for j,col in enumerate(columns):
  for i,v in col.items():M[i,j]=s.Rational(v.numerator,v.denominator)
 rank=M.rank();ans=len(rows)-rank
 if verbose:print('g,b,alpha,d,base,rank,h1=',g,b,alpha,d,len(rows),rank,ans)
 return ans

if __name__=='__main__':
 import shutil
 shutil.copyfile('scratchpad.py','workspace/agent4_cech.py')
 for g in range(6,7):
  r=(g+2)//3;k=g-r;N=2*g-2
  for j in range(r):
   b=[int(i==j) for i in range(r)]
   vals=[compute(g,b,a,d) for a,d in [(0,0),(1,0),(0,-N),(1,-N)]]
   print(g,b,vals,'lineDelta',vals[0]+vals[3]-vals[1]-vals[2],flush=True)
