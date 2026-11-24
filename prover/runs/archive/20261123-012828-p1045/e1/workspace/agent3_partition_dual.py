import numpy as np
from scipy.optimize import linprog
from itertools import combinations

def solve(theta,r=.03,a=.09,maxiter=3000,tol=1e-9):
 theta=np.array(theta,dtype=float);theta=theta/theta.sum()*(1-r);pairs=list(combinations(range(3),2));n=25
 def decode(x):
  Bs=[];mus=[]
  for j in range(3):
   y=x[5*j:5*j+5];Bs.append(np.array([[y[2],y[4]],[y[4],y[3]]]));mus.append(y[:2])
  muR=x[15:18];R=np.diag(x[18:21])
  for j,(u,v) in enumerate(pairs):R[u,v]=R[v,u]=x[21+j]
  return Bs,mus,muR,R,x[-1]
 def affine(x):
  Bs,mus,mr,R,c=decode(x);G=R.copy();mu=mr.copy();out=[];Ms=[]
  for j in range(3):
   ids=[i for i in range(3) if i!=j];B=Bs[j];m=mus[j];t=theta[j]
   G[np.ix_(ids,ids)]+=B;mu[ids]+=m
   Ms.append(np.block([[np.array([[t]]),m[None,:]],[m[:,None],B]]))
   out.extend(m-np.diag(B));out.extend([m[0]-B[0,1],m[1]-B[0,1],B[0,1]-sum(m)+t])
  Ms.append(np.block([[np.array([[r]]),mr[None,:]],[mr[:,None],R]]))
  out.extend(mr-np.diag(R))
  for u,v in pairs:out.extend([mr[u]-R[u,v],mr[v]-R[u,v],R[u,v]-mr[u]-mr[v]+r])
  rowstart=len(out)
  out.extend(2*mu-np.diag(G)-c)
  out.extend(a-G[u,v] for u,v in pairs)
  out.append(r*(a-r)-theta@np.diag(R))
  return np.array(out),Ms,rowstart
 base,M0,rowstart=affine(np.zeros(n));E=np.eye(n)
 terms=[affine(e) for e in E];C=np.stack([v[0]-base for v in terms],axis=1)
 Mcoef=[np.stack([terms[j][1][t]-M0[t] for j in range(n)],axis=2) for t in range(4)]
 Aub=list(-C);bub=list(base);meta=[None]*len(base)
 cobj=np.zeros(n);cobj[-1]=-1
 for it in range(maxiter):
  res=linprog(cobj,A_ub=np.array(Aub),b_ub=bub,bounds=(0,None),method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
  if not res.success:raise RuntimeError(res.message)
  worst=0
  for t in range(4):
   H=M0[t]+np.einsum('ijk,k->ij',Mcoef[t],res.x)
   ev,vec=np.linalg.eigh(H);worst=min(worst,ev[0])
   for j,e in enumerate(ev):
    if e < -tol:
     v=vec[:,j];Aub.append(-np.einsum('i,j,ijk->k',v,v,Mcoef[t]));bub.append(v@M0[t]@v);meta.append((t,v))
  if worst>=-tol:
   dual=-res.ineqlin.marginals
   Q=[np.zeros_like(m) for m in M0]
   for w,mt in zip(dual,meta):
    if mt is not None:
     t,v=mt;Q[t]+=w*np.outer(v,v)
   return dict(c=res.x[-1],theta=theta,r=r,a=a,rows=dual[rowstart:rowstart+3],pairs=dual[rowstart+3:rowstart+6],nu=dual[rowstart+6],Qs=Q,linear_dual=dual[:len(base)],x=res.x,iterations=it,worst=worst)
 raise RuntimeError('maxiter')

if __name__=='__main__':
 for th in [[1,1,1],[1.03,1,.97],[1.1,1,.9],[.4,.3,.27]]:
  z=solve(th);print(th,'c',z['c'],'lambda',z['rows'],'pairs',z['pairs'],'nu',z['nu'],'it',z['iterations'],flush=True)
