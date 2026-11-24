import numpy as np
from scipy.signal import convolve2d
from scipy.optimize import differential_evolution
from numpy.polynomial import polynomial as P
from pathlib import Path


def clean(c,tol=1e-11):
 c=np.asarray(c,dtype=float).ravel();scale=max(1.,np.max(abs(c)))
 while len(c)>1 and abs(c[-1])<tol*scale:c=c[:-1]
 return c

def roots(c):
 c=clean(c)
 if len(c)<=1:return []
 return [z.real for z in P.polyroots(c) if abs(z.imag)<1e-6*(1+abs(z.real))]

def cubic_poly(Qs):
 z=[np.array([[1.,-1.],[-1.,0.]]),np.array([[0.],[1.]]),np.array([[0.,1.]])]
 out=np.zeros((4,4))
 for g in range(3):
  for a in range(3):
   for b in range(3):
    pp=convolve2d(convolve2d(z[g],z[a]),z[b])*Qs[g,a,b]
    out[:pp.shape[0],:pp.shape[1]]+=pp
 return out

def max_cubic(A,verts):
 # All vertices/edge critical points and all isolated interior stationary points.
 candidates=[np.array(v) for v in verts]
 def inside(pt):
  for i in range(len(verts)):
   v=verts[(i+1)%len(verts)]-verts[i];w=pt-verts[i]
   if v[0]*w[1]-v[1]*w[0]<-1e-7:return False
  return True
 for V,W in zip(verts,np.roll(verts,-1,axis=0)):
  xp=np.array([V[0],W[0]-V[0]]);yp=np.array([V[1],W[1]-V[1]])
  poly=np.zeros(1)
  for i in range(4):
   for j in range(4):
    if A[i,j]:poly=P.polyadd(poly,A[i,j]*P.polymul(P.polypow(xp,i),P.polypow(yp,j)))
  for t in roots(P.polyder(poly)):
   if 0<t<1:candidates.append(V+t*(W-V))
 f=np.zeros((3,3));g=np.zeros((3,3))
 for i in range(3):
  for j in range(3):
   f[i,j]=(i+1)*A[i+1,j];g[i,j]=(j+1)*A[i,j+1]
 a=f[0,2];d=g[0,2];b=f[:2,1];e=g[:2,1];c=f[:3,0];ff=g[:3,0]
 if abs(a)+abs(d)>1e-10:
  af_cd=P.polysub(a*ff,d*c);ae_bd=P.polysub(a*e,d*b);bf_ce=P.polysub(P.polymul(b,ff),P.polymul(c,e))
  resultant=P.polysub(P.polymul(af_cd,af_cd),P.polymul(ae_bd,bf_ce))
 else:
  resultant=P.polysub(P.polymul(b,ff),P.polymul(c,e))
 for x in roots(resultant):
  if not(-1e-6<=x<=1+1e-6):continue
  bb=P.polyval(x,b);ee=P.polyval(x,e);cc=P.polyval(x,c);fff=P.polyval(x,ff)
  if abs(a)+abs(d)>1e-10:
   denom=d*bb-a*ee
   if abs(denom)>1e-9:ys=[(a*fff-d*cc)/denom]
   else:ys=roots([cc,bb,a])+roots([fff,ee,d])
  else:
   ys=[-cc/bb] if abs(bb)>1e-9 else ([-fff/ee] if abs(ee)>1e-9 else [])
  for y in ys:
   pt=np.array([x,y])
   if inside(pt) and abs(P.polyval2d(x,y,f))+abs(P.polyval2d(x,y,g))<1e-5*(1+np.max(abs(A))):candidates.append(pt)
 vals=[P.polyval2d(v[0],v[1],A) for v in candidates]
 i=np.argmax(vals)
 return vals[i],candidates[i]

def interval_poly(K,lengths):
 # K is the pairwise kernel already raised to q=3/2; first and last cells are partial.
 n=len(lengths);mu=np.zeros(n);mu[1:-1]=lengths[1:-1]/sum(lengths[1:-1])
 V=np.column_stack([K@mu,K[:,0],K[:,-1]])
 Qs=np.empty((3,3,3));Qs[0]=(V.T*mu)@V;Qs[1]=np.outer(V[0],V[0]);Qs[2]=np.outer(V[-1],V[-1])
 A=cubic_poly(Qs)
 L=sum(lengths[1:-1]);a=lengths[0];b=lengths[-1]
 verts=np.array([[0,0],[a/(L+a),0],[a/(L+a+b),b/(L+a+b)],[0,b/(L+b)]])
 return A,verts

if __name__=='__main__':
 rng=np.random.default_rng(982)
 maxerr=0.
 for k in range(100):
  n=rng.integers(3,8);mats=[rng.normal(size=(2,2))+2*np.eye(2) for _ in range(n)]
  K=np.array([[np.linalg.norm(M@np.linalg.inv(N),2)**1.5 for N in mats] for M in mats])
  ll=np.exp(rng.uniform(-3,3,size=n));A,verts=interval_poly(K,ll)
  val,pt=max_cubic(A,verts)
  L=sum(ll[1:-1]);a,b=ll[0],ll[-1]
  def fun(uv):
   u,v=uv;den=L+u+v
   return -P.polyval2d(u/den,v/den,A)
  opt=differential_evolution(fun,[(0,a),(0,b)],popsize=10,maxiter=150,tol=1e-9,seed=k,polish=True)
  brute=-opt.fun
  if val<brute*(1-2e-6):raise AssertionError((k,val,brute,pt,opt.x))
  maxerr=max(maxerr,abs(val-brute)/(1+abs(val)))
 print('100 exact stationary/edge enumeration checks against independent DE passed; max relative discrepancy',maxerr)
 Path('workspace/agent3_p3_fractional.py').write_text(Path('scratchpad.py').read_text())
