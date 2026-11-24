import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
from scipy.interpolate import CubicSpline
from pathlib import Path

def moment(Q,p,eps2=.02,N=3000):
 L=np.log(Q);X=np.linspace(0,L,N+1);dx=L/N;eps=np.sqrt(eps2);m=.5-eps2
 coeff={}; deriv={};zero=np.zeros(N+1)
 def get(i,j):return coeff.get((i,j),zero)
 def dget(i,j):return deriv.get((i,j),zero)
 for i in range(p,-1,-1):
  for j in range(p-i,-1,-1):
   # Only even powers of z appear from terminal u^p.
   if j%2:continue
   drift=m-j;pot=j*(j-1)/2
   A=lil_matrix((N+1,N+1));rhs=np.zeros(N+1)
   A[0,0]=1.;rhs[0]=1. if (i,j)==(p,0) else 0.
   inds=np.arange(1,N)
   for k in inds:
    A[k,k-1]=.5/dx**2-drift/(2*dx);A[k,k]=-1/dx**2+pot;A[k,k+1]=.5/dx**2+drift/(2*dx)
   rhs[1:N]=(-(i+1)*eps*np.exp(X/2)*(dget(i+1,j)+2*get(i+1,j))-.5*eps2*np.exp(X)*(i+2)*(i+1)*(get(i+2,j)+get(i+2,j-2))-.5*(j+2)*(j+1)*get(i,j+2))[1:N]
   A[N,N]=3/(2*dx);A[N,N-1]=-4/(2*dx);A[N,N-2]=1/(2*dx)
   rhs[N]=.5*Q*(i+2)*(i+1)*get(i+2,j)[-1]
   f=spsolve(A.tocsr(),rhs)
   coeff[i,j]=f;deriv[i,j]=CubicSpline(X,f)(X,1)
 f=coeff[0,0]
 val=float(CubicSpline(X,f)(np.log(2.)))
 return val**(1/p),float(np.min(f))
if __name__=='__main__':
 for p in [2,4,6]:
  prev=None
  for Q in [10.,30.,100.,300.,1000.]:
   val,mn=moment(Q,p)
   exp=None if prev is None else np.log(val/prev[1])/np.log(Q/prev[0])
   print('p,Q,norm,adjacent slope,min coefficient',p,Q,val,exp,mn,flush=True)
   prev=(Q,val)
 Path('workspace/agent3_output_moments.py').write_text(Path('scratchpad.py').read_text())
