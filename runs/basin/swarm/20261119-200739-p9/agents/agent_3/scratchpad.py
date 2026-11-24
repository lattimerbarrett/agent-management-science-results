from pathlib import Path
import itertools
from fractions import Fraction as F
import numpy as np
import sympy as s

# Exact one-cycle martingale and shift algebra.
a,c,h,k,sa,sc,I=s.symbols('a c h k sa sc I',positive=True)
children=[]
for eps,zeta in itertools.product([-1,1],repeat=2):
 aa=a*(1+sa*zeta);cc=c*(1+sc*zeta);hh=h+eps*k/c
 children.append((aa,cc,hh))
for expr,target in [(lambda A,C,H:A,a),(lambda A,C,H:C,c),(lambda A,C,H:A*H,a*h),(lambda A,C,H:C*H,c*h)]:
 assert s.simplify(sum(expr(*z) for z in children)/4-target)==0
fp=sc*c*s.Matrix([-h-k/c,1]);fm=-sc*c*s.Matrix([-h+k/c,1])
gp=sa*a*s.Matrix([1,h+k/c]);gm=-sa*a*s.Matrix([1,h-k/c])
assert s.simplify(I*(fp.dot(gm)-fm.dot(gp))/2-2*I*a*k*sa*sc)==0
fe=s.Matrix([-k,0]);fz=sc*c*s.Matrix([-h,1]);ge=s.Matrix([0,a*k/c]);gz=sa*a*s.Matrix([1,h])
assert s.simplify(fe.dot(gz)-fz.dot(ge)+a*k*(sa+sc))==0
print('Exact martingale / sibling-shift / periodic-Hilbert cycle identities: passed')

# Independent exact rational finite-Cantor cross form, with explicit tail error.
m=6; atoms=[]
for signs in itertools.product([1,-1],repeat=m):
 x=sum((F(3-sig,8)*F(1,4)**j for j,sig in enumerate(signs)),F(1,2)*F(1,4)**m)
 H=sum((sig*F(1,2)**j for j,sig in enumerate(signs)),F(0))
 atoms.append((x,H,signs[0]))
left=[z for z in atoms if z[2]==1];right=[z for z in atoms if z[2]==-1]
S=F(2,4**m)*sum(((xH-yH)/(x-y) for x,xH,_ in left for y,yH,_ in right),F(0))
err_pi=12*F(1,2)**m+24*F(1,4)**m
assert S+err_pi < -2
print('Exact rational Cantor pi*cross:',float(S),'certified upper with tail:',float(S+err_pi),'< -2')

# Independent direct cell-Hilbert recurrence and weighted norm checks.
def cells(p,Q,L):
 t=1/Q;v=1/(p-1);ss=Q**(-v);r=2-t;z=2-ss;kk=Q**(v/p)
 leaves=[]
 def rec(left,length,a,c,h,lev,top):
  if lev==L:
   leaves.append((left,left+length,a,c,h,top));return
  for j,sign in enumerate([1,1,-1,-1]):
   good=j in [1,2];A=a*(r if good else t);C=c*(z if good else ss);H=h+sign*kk/c
   x=left+j*length/4;tag=j if lev==0 else top
   if good:rec(x,length/4,A,C,H,lev+1,tag)
   else:leaves.append((x,x+length/4,A,C,H,tag))
 rec(0.,1.,1.,1.,0.,0,-1)
 return np.array(leaves),r,kk

def raw_kernel(E):
 lo=E[:,0];hi=E[:,1]
 def phi(x):
  y=np.zeros_like(x);mask=x!=0;y[mask]=x[mask]*np.log(abs(x[mask]))-x[mask];return y
 K=phi(hi[:,None]-lo[None,:])-phi(lo[:,None]-lo[None,:])-phi(hi[:,None]-hi[None,:])+phi(lo[:,None]-hi[None,:])
 np.fill_diagonal(K,0.)
 return K/np.pi

def form(E):
 a,c,h,top=E[:,2],E[:,3],E[:,4],E[:,5]
 V=a[:,None]*c[None,:]*(h[:,None]-h[None,:])*raw_kernel(E)
 return V.sum(),V[top[:,None]!=top[None,:]].sum()

maxerr=0.;rng=np.random.default_rng(812)
for p in [2.1,2.5,3.,4.,7.]:
 for Q in [10.,100.,1000.]:
  prev=0.
  for L in range(1,6):
   E,r,kk=cells(p,Q,L);B,C=form(E)
   err=abs(B-C-r*prev/2)/(1+abs(B));maxerr=max(maxerr,err)
   assert err<1e-10
   lengths=E[:,1]-E[:,0];aa=E[:,2];cc=E[:,3];hh=E[:,4]
   assert abs(np.dot(lengths,aa)-1)<1e-12
   # Pointwise canonical weighted tests, checked at every leaf.
   for A,Cc,H in zip(aa,cc,hh):
    M=A**(1/p)*np.array([[1.,H],[0.,1/Cc]])
    f=Cc*np.array([-H,1.]);g=A*np.array([1.,H]);q=p/(p-1)
    assert abs(np.linalg.norm(M@f)**p/A-1)<1e-8
    assert abs(np.linalg.norm(np.linalg.solve(M.T,g))**q/A-1)<1e-8
   prev=B
print('75 independent exact-cell Hilbert recurrences and all terminal canonical norms: passed; max recurrence error',maxerr)
Path('workspace/agent3_lower_audit_checks.py').write_text(Path('scratchpad.py').read_text())
