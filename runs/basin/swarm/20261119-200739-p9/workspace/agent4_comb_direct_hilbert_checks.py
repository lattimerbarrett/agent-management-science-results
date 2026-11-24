import numpy as np
from pathlib import Path

def tree(Q,p,depth):
    v=1/(p-1);la=1/Q;lc=Q**(-v);ra=2-la;rc=2-lc;k=Q**(v/p)
    out=[]
    def rec(left,length,a,c,h,d,top):
        if d==0:
            out.append((left,left+length,a,c,h,top));return
        # B+,G+,G-,B- ; rotation left+,right-
        q=length/4
        out.append((left,left+q,a*la,c*lc,h+k/c,0 if top<0 else top))
        rec(left+q,q,a*ra,c*rc,h+k/c,d-1,1 if top<0 else top)
        rec(left+2*q,q,a*ra,c*rc,h-k/c,d-1,2 if top<0 else top)
        out.append((left+3*q,left+4*q,a*la,c*lc,h-k/c,3 if top<0 else top))
    rec(0.,1.,1.,1.,0.,depth,-1)
    return np.array(out),ra,k

def bilinear(Q,p,depth):
    z,ra,k=tree(Q,p,depth)
    left,right,a,c,h,top=z.T
    phi=lambda x:np.where(x!=0,x*np.log(np.maximum(abs(x),1e-300)),0.)
    K=(phi(right[:,None]-left[None,:])-phi(left[:,None]-left[None,:])-phi(right[:,None]-right[None,:])+phi(left[:,None]-right[None,:]))/np.pi
    D=a[:,None]*c[None,:]*(h[:,None]-h[None,:])*K
    B=D.sum()
    Cross=np.where(top[:,None]!=top[None,:],D,0).sum()
    scale=sum((ra/2)**j for j in range(depth))
    return B,Cross,B/(k*scale),Cross/k,len(z)
res=[]
for p in [2.,3.,5.]:
 for Q in [10.,100.,10000.]:
  for n in [3,5,7,8]:
    r=bilinear(Q,p,n); print(p,Q,n,r,flush=True);res.append((p,Q,n,*r))
Path('workspace/agent4_comb_direct_hilbert_checks.txt').write_text(str(res))
Path('workspace/agent4_comb_direct_hilbert_checks.py').write_text(Path(__file__).read_text())
