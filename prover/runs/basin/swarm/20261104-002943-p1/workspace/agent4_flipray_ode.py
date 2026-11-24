import numpy as np
from scipy.optimize import root
from pathlib import Path
xi=np.sqrt(5-np.sqrt(8+2*np.sqrt(2)));x=np.r_[[-3,-np.sqrt(5),-1,1,np.sqrt(5),3],[-xi,xi]]/3
s=4;n=8;V=x[:,None]**np.arange(s);p=x**4-10*x*x/9+11/81;q=x**4-10*x*x/9+23/81;C=28/6561
w0=np.r_[[7/32,1/16,7/32,7/32,1/16,7/32],[0,0]];wt=np.r_[-w0[:6]/x[:6],0,0]
assert max(abs(p[:6]*q[:6]-C))<1e-14 and max(abs(p[6:]*q[6:]+C))<1e-14

def jet(ws,ref):
 N=len(ws);Ms=[V.T@(w[:,None]*V) for w in ws];ps=[ref];cs=[np.zeros(s)]
 for j in range(1,N):
  rhs=V.T@(ws[j]*ref)
  for l in range(1,j):rhs+=Ms[l]@cs[j-l]
  cs.append(-np.linalg.solve(Ms[0],rhs));ps.append(V@cs[j])
 raw=[np.zeros(n) for _ in range(N)]
 for j in range(N):
  for a in range(j+1):
   for b in range(j-a+1):raw[j]+=ws[a]*ps[b]*ps[j-a-b]
 den=[sum(a) for a in raw];out=[]
 for j in range(N):out.append((raw[j]-sum((den[l]*out[j-l] for l in range(1,j+1)),np.zeros(n)))/den[0])
 return out

def ode(t,z):
 pos=z[0];w=w0+pos*wt;hco=z[1:5];a=z[5:7];h=V@hco;u=w*p*h;w2=-sum(a*a)*w;w2[6:]=a*a
 out=jet(jet([w,u,w2,np.zeros(n)],p),q);b=out[1]-u;G=V.T@((w*p*p)[:,None]*V);hd=np.linalg.solve(G,V.T@(p*(out[2]-w2-b*p*h)));ad=np.divide(out[3][6:],2*a,out=np.zeros(2),where=a!=0);vel=np.dot(wt,b)/np.dot(wt,wt)
 return np.r_[vel,hd,ad]

def res(zz):
 h0,h2,k=zz;d=ode(0,np.r_[0,h0,0,h2,0,1,1]);return [d[1]+k*h0,d[3]+k*h2,d[5]+k]
sols=[]
for i in range(100):
 rng=np.random.default_rng(i);st=rng.normal(size=3)*[200,200,5];sol=root(res,st)
 if sol.success and np.linalg.norm(res(sol.x))<1e-6 and not any(np.linalg.norm(sol.x-v)<1e-2 for v in sols):sols.append(sol.x);print('RAY',sol.x,'res',res(sol.x),flush=True)
d0=ode(0,np.r_[0,0,0,0,0,1,1]);e0=ode(0,np.r_[0,1,0,0,0,1,1]);e2=ode(0,np.r_[0,0,0,1,0,1,1]);ee=ode(0,np.r_[0,1,0,1,0,1,1]);a0=e0[5]-d0[5];a2=e2[5]-d0[5]
co=[]
for ind,hind in [(1,0),(3,1)]:
 c00=e0[ind]-d0[ind]-(a0 if hind==0 else 0);c22=e2[ind]-d0[ind]-(a2 if hind==1 else 0);c02=ee[ind]-e0[ind]-e2[ind]+d0[ind]-(a2 if hind==0 else a0);co.append([d0[ind],c00,c02,c22])
print('reducedco',co,'adcoef',a0,a2)
c1,b1,b2,b3=co[0];c2,d1,d2,d3=co[1];rr=np.roots([c2*b3-c1*d3,c2*b2-c1*d2,c2*b1-c1*d1]);print('ratiocandidates',rr)
for rrr in rr:
 hsq=-c1/(b1+b2*rrr+b3*rrr*rrr);print('ratio',rrr,'h0square',hsq)
print('rays',len(sols));np.savez('workspace/agent4_flipray_params.npz',x=x,p=p,q=q,C=C,w0=w0,wt=wt,rays=np.array(sols))
