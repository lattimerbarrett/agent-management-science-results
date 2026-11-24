"""Numerical small clique SDP relaxation, not a proof or certificate."""
import numpy as np
from scipy.optimize import minimize
from itertools import combinations

def solve(a=.09,r=.066918,maxiter=10000):
 s=1-r;pairs=list(combinations(range(3),2));ct=4*np.sqrt(a/3)-2*a
 def mats(x):
  mb=x[:3];mr=x[3:6];B=np.diag(x[6:9]);R=np.diag(x[9:12]);c=x[-1]
  for t,(i,j) in enumerate(pairs):B[i,j]=B[j,i]=x[12+t];R[i,j]=R[j,i]=x[15+t]
  return mb,mr,B,R,c
 def cons(x):
  mb,mr,B,R,c=mats(x)
  out=list(2*(mb+mr)-np.diag(B+R)-c)
  out += [a-B[i,j]-R[i,j] for i,j in pairs]
  out += [r*(a-r)/s-R[0,0],R[1,1]-R[0,0],r*(a-r)-(ct-r)*R[1,1]-(1-ct)*R[0,0]]
  m2=2*ct-s-2*np.sqrt(r)*(np.sqrt(max(R[0,0],0))+np.sqrt(max(R[1,1],0)))+R[0,0]+R[1,1]
  out.extend([m2,R[2,2]-R[0,0],r*(a-r)-m2*R[2,2]-(s-m2)*R[0,0]])
  out.extend(np.linalg.eigvalsh(np.block([[np.array([[s]]),mb[None,:]],[mb[:,None],B]])))
  out.extend(np.linalg.eigvalsh(np.block([[np.array([[r]]),mr[None,:]],[mr[:,None],R]])))
  out.extend(np.linalg.eigvalsh(2*np.diag(np.diag(B))-B))
  out.extend(mb-np.diag(B));out.extend(mr-np.diag(R))
  for mu,G,mass in [(mb,B,s),(mr,R,r)]:
   for i,j in pairs:out.extend([mu[i]-G[i,j],mu[j]-G[i,j],G[i,j]-mu[i]-mu[j]+mass])
  return np.array(out)
 # Interior-ish initial point; SLSQP is heuristic even though the feasible set is convex.
 qR=min(.001,r*(a-r)/(4*s));mR=np.sqrt(r*qR)*.5
 x0=np.r_[np.full(3,.31),np.full(3,mR),np.full(3,.18),np.full(3,qR),np.full(3,.08),np.full(3,qR/2),.3]
 bounds=[(0,s)]*3+[(0,r)]*3+[(0,s)]*3+[(0,r)]*3+[(0,s)]*3+[(0,r)]*3+[(0,1)]
 res=minimize(lambda x:-x[-1],x0,method='SLSQP',bounds=bounds,constraints=[{'type':'ineq','fun':cons}],options={'maxiter':maxiter,'ftol':1e-11})
 return res,cons(res.x).min(),mats(res.x)

if __name__=='__main__':
 res,err,mats=solve();print(res.success,res.message,'maxc',res.x[-1],'target',4*np.sqrt(.09/3)-2*.09,'mincon',err);print(mats)
