import numpy as np, json, time, os
from scipy.optimize import minimize
rng=np.random.default_rng(15021)
def F(t):
 t=np.asarray(t,dtype=float);out=np.zeros_like(t);mask=t!=0;out[mask]=t[mask]*np.log(np.abs(t[mask]));return out

def metrics(z,n,p,details=False):
 a=z[:n];d=z[n:2*n];h=z[2*n:3*n];g=z[3*n:].reshape(n,2)
 aa=np.exp(a);dd=np.exp(d)
 x=aa[:,None]/aa[None,:];y=dd[:,None]/dd[None,:];b=aa[:,None]/dd[None,:]*(h[:,None]-h[None,:])
 fro=x*x+y*y+b*b;det=x*y
 K=np.sqrt((fro+np.sqrt(np.maximum(0,fro*fro-4*det*det)))/2)
 q=p/(p-1);Kq=K**q;chars=[]
 for L in range(1,n+1):
  idx=(np.arange(n)[:,None]+np.arange(L)[None,:])%n
  blocks=Kq[idx[:,:,None],idx[:,None,:]]
  chars.extend(np.mean(np.mean(blocks,axis=2)**(p-1),axis=1))
 A=max(chars)
 f=np.stack([g[:,0]/aa-h*g[:,1]/dd,g[:,1]/dd],axis=1)
 k=np.arange(n)[:,None]-np.arange(n)[None,:]
 H=(F(k+1)+F(k-1)-2*F(k))/np.pi
 hf=H@f
 out=np.stack([aa*(hf[:,0]+h*hf[:,1]),dd*hf[:,1]],axis=1)
 ng=np.sum(np.linalg.norm(g,axis=1)**p);no=np.sum(np.linalg.norm(out,axis=1)**p)
 R=(no/max(ng,1e-200))**(1/p)
 if details:return float(A),float(R),H
 return np.log(A),np.log(max(R,1e-100))
# Check exact compression kernel against numerical double integration and skew adjointness.
from scipy.integrate import quad
for k in [1,2,3,10]:
 exact=float((F(k+1)+F(k-1)-2*F(k))/np.pi)
 numerical=quad(lambda x:np.log((k+x)/(k+x-1)),0,1)[0]/np.pi
 assert abs(exact-numerical)<1e-10
print('Compression Hilbert kernel integral identities checked',flush=True)
results=[]
for p in [2.,3.]:
 for n in [8,16]:
  for Q in [3.,10.,30.,100.]:
   best=None
   for rep in range(4):
    z=np.concatenate([rng.normal(size=2*n)*.25*np.log(Q),rng.normal(size=n),rng.normal(size=2*n)])
    def fun(z):
     la,lr=metrics(z,n,p)
     return -lr+5*(la-np.log(Q))**2
    L=2*np.log(Q)+2
    bounds=[(-L,L)]*(2*n)+[(-4,4)]*n+[(-5,5)]*(2*n)
    res=minimize(fun,z,method='L-BFGS-B',bounds=bounds,options={'maxiter':250,'maxfun':60000,'ftol':1e-9,'gtol':1e-5})
    A,R,H=metrics(res.x,n,p,True)
    value=np.log(R)-5*(np.log(A)-np.log(Q))**2
    record={'p':p,'n':n,'target':Q,'rep':rep,'A':A,'R':R,'score':float(value),'nit':int(res.nit),'success':bool(res.success),'z':res.x.tolist()}
    results.append(record)
    if best is None or value>best['score']:best=record
    with open('workspace/agent1_variational_results.json','w') as f:json.dump(results,f)
    print('p',p,'n',n,'target',Q,'rep',rep,'A',round(A,5),'R',round(R,5),'nit',res.nit,flush=True)
   print('BEST',p,n,Q,best['A'],best['R'],flush=True)
open('workspace/agent1_variational_search.py','w').write(open('scratchpad.py').read())
