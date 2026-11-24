import numpy as np
from scipy.optimize import minimize
from itertools import combinations

def solve(theta,r=.03,a=.09,maxiter=10000):
 theta=np.array(theta,dtype=float);theta=theta/theta.sum()*(1-r)
 pairs=list(combinations(range(3),2))
 def decode(x):
  Bs=[];mus=[]
  for j in range(3):
   y=x[5*j:5*j+5];Bs.append(np.array([[y[2],y[4]],[y[4],y[3]]]));mus.append(y[:2])
  muR=x[15:18];R=np.diag(x[18:21])
  for j,(u,v) in enumerate(pairs):R[u,v]=R[v,u]=x[21+j]
  return Bs,mus,muR,R,x[-1]
 def cons(x):
  Bs,mus,muR,R,c=decode(x);G=R.copy();mu=muR.copy();out=[]
  for j in range(3):
   ids=[i for i in range(3) if i!=j];B=Bs[j];m=mus[j];t=theta[j]
   G[np.ix_(ids,ids)]+=B;mu[ids]+=m
   out.extend(np.linalg.eigvalsh(np.block([[np.array([[t]]),m[None,:]],[m[:,None],B]])))
   out.extend(m-np.diag(B));out.extend([m[0]-B[0,1],m[1]-B[0,1],B[0,1]-sum(m)+t])
  out.extend(np.linalg.eigvalsh(np.block([[np.array([[r]]),muR[None,:]],[muR[:,None],R]])))
  out.extend(muR-np.diag(R))
  for u,v in pairs:out.extend([muR[u]-R[u,v],muR[v]-R[u,v],R[u,v]-muR[u]-muR[v]+r])
  out.extend(2*mu-np.diag(G)-c)
  out.extend(a-G[u,v] for u,v in pairs)
  out.append(r*(a-r)-theta@np.diag(R))
  return np.array(out)
 x=[]
 for t in theta:x.extend([.4*t,.4*t,.2*t,.2*t,.15*t])
 x.extend([.02*r]*3+[.001*r]*3+[.0005*r]*3+[.25])
 res=minimize(lambda x:-x[-1],np.array(x),method='SLSQP',bounds=[(0,None)]*25,constraints=[{'type':'ineq','fun':cons}],options={'ftol':1e-11,'maxiter':maxiter})
 return res,cons(res.x).min()
if __name__=='__main__':
 for th in [[1,1,1],[.4,.3,.27],[.48,.48,.01],[.35,.32,.3]]:
  res,err=solve(th);print(th,res.x[-1],err,res.message,flush=True)
