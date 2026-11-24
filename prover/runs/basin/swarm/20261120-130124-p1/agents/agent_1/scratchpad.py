import numpy as np
from scipy.linalg import null_space
s=3;D=3
p=np.array([1.,0,-3,0]);q=np.array([1.,.8,-3,.2]);h=1.
pol=np.polymul(p,q);pol[-1]-=h;lam=np.sort(np.roots(pol));pv=np.polyval(p,lam)
M=np.vstack([np.ones(6)]+[pv*lam**j for j in range(s)]);m0=np.linalg.lstsq(M,[1,0,0,0],rcond=None)[0];N=null_space(M);B=null_space(np.vstack([np.ones(6),N.T]));Vander=lam[None,:]**np.arange(2*s+1)[:,None];diag=pv*pv/h-1

def mul(a,b):return np.array([sum(a[j]*b[k-j] for j in range(k+1)) for k in range(D)])
def div(a,b):
 out=np.zeros_like(a)
 for k in range(D):out[k]=(a[k]-sum(out[j]*b[k-j] for j in range(k)))/b[0]
 return out

def step(w):
 moms=w@Vander.T;G=moms[:,np.arange(s)[:,None]+np.arange(s)[None,:]];c=np.zeros((D,s))
 for k in range(D):c[k]=np.linalg.solve(G[0],-moms[k,s:2*s]-sum(G[j]@c[k-j] for j in range(1,k+1)))
 pp=c@Vander[:s];pp[0]+=lam**s
 ww=mul(w,mul(pp,pp));return div(ww,ww.sum(axis=1)[:,None])
def field(x):
 w=np.zeros((D,6));w[0]=m0+N@x[:2];w[1]=B@x[2:];d=step(step(w))-w
 return np.r_[N.T@d[1],B.T@d[2]]
def nullfunc(x):
 w=m0+N@x[:2];v=N@field(x)[:2]
 return sum(diag*v*v/w)
def deriv(fun,x,vel,eps=1e-5):return (fun(x+eps*vel)-fun(x-eps*vel))/(2*eps)

if __name__=='__unused__':
 A=np.column_stack([field(np.r_[np.zeros(2),np.eye(3)[j]])[:2] for j in range(3)])
 for di in [diag,1/diag,(diag+1)/diag,pv,np.polyval(q,lam),pv-np.polyval(q,lam),1/(pv-np.polyval(q,lam)),np.ones(6)]:
  diag=di
  g=N.T@(diag[:,None]*N/m0[:,None]);ev,U=np.linalg.eigh(g)
  if ev[0]*ev[1]>=0: print('definite',di,ev);continue
  v=U[:,0]/np.sqrt(-ev[0])+U[:,1]/np.sqrt(ev[1]);u=np.linalg.pinv(A)@v;k=null_space(A)[:,0]
  x=np.r_[np.zeros(2),u];f=field(x)
  print('test',di,'null',nullfunc(x),'deriv',deriv(nullfunc,x,f),flush=True)

if __name__=='__main__':
 print('normal derivative',np.column_stack([B.T@(step(step(np.array([m0,B@np.eye(3)[j],np.zeros(6)])))-np.array([m0,B@np.eye(3)[j],np.zeros(6)]))[1] for j in range(3)]))
 from itertools import combinations_with_replacement
 rng=np.random.default_rng(25);X=[];Ds=[];Es=[]
 pairs=list(combinations_with_replacement(range(3),2))
 for k in range(1600):
  while True:
   m=rng.normal(size=2)*.12;w=m0+N@m
   if min(w)>.005:break
  u=rng.normal(size=3);x=np.r_[m,u];ff=field(x);v=ff[:2];W=ff[2:]
  fs=np.r_[1,m,m[0]**2,m[0]*m[1],m[1]**2,1/w]
  dfs=np.r_[0,v,2*m[0]*v[0],m[0]*v[1]+m[1]*v[0],2*m[1]*v[1],-(N@v)/w**2]
  us=np.array([u[i]*u[j] for i,j in pairs]);dus=np.array([W[i]*u[j]+W[j]*u[i] for i,j in pairs])
  X.append(np.outer(fs,us).ravel());Ds.append((np.outer(dfs,us)+np.outer(fs,dus)).ravel());Es.append((pv*pv)@(B@u))
 X=np.array(X);Ds=np.array(Ds);Es=np.array(Es);XX=Es[:,None]*X
 scale=np.linalg.norm(X,axis=0);X/=scale;Ds/=scale;XX/=scale
 a=np.linalg.lstsq(XX,Ds,rcond=1e-10)[0]
 vals,vec=np.linalg.eig(a)
 for j in range(len(vals)):
  err=np.linalg.norm(Ds@vec[:,j]-vals[j]*XX@vec[:,j])/np.linalg.norm(Ds@vec[:,j])
  if err<.01:print('eig',vals[j],err,flush=True)
 print('best candidates',sorted([(float(np.linalg.norm(Ds@vec[:,j]-vals[j]*XX@vec[:,j])/np.linalg.norm(Ds@vec[:,j])),vals[j]) for j in range(len(vals))],key=lambda t:t[0])[:10])
 np.savez('linearfit.npz',X=X,D=Ds,XX=XX,scale=scale,vals=vals,vec=vec)

