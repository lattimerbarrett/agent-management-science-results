import numpy as np
from scipy.optimize import minimize
from itertools import product
from math import sqrt

def solve(k,alpha,diag,status,tries=2):
    edges=[(i,j) for i in range(k) for j in range(i)]
    free=[e for e,s in zip(edges,status) if s==2]
    fixed=np.diag(diag).astype(float)
    for (i,j),s in zip(edges,status):
        if s!=2:fixed[i,j]=fixed[j,i]=s
    red=[(i,i) for i in range(k) if diag[i]==1]+[e for e,s in zip(edges,status) if s!=0]
    blue=[(i,i) for i in range(k) if diag[i]==0]+[e for e,s in zip(edges,status) if s!=1]
    def calc(z):
        x=z[:k]; P=fixed.copy()
        for p,(i,j) in zip(z[k:-1],free): P[i,j]=P[j,i]=p
        R=(P*x)@P.T; Q=1-P; B=(Q*x)@Q.T
        return R,B
    def con(z):
        R,B=calc(z); b=z[-1]
        return np.r_[[b-B[i,j] for i,j in blue],[alpha*b-R[i,j] for i,j in red]]
    best=None
    for t in range(tries):
        x=np.random.dirichlet(np.ones(k)*3)
        z=np.r_[x,np.random.uniform(.3,.8,len(free)),.47]
        res=minimize(lambda z:z[-1],z,method='SLSQP',bounds=[(.000001,1)]*k+[(.000001,.999999)]*len(free)+[(.01,1)],constraints=[{'type':'eq','fun':lambda z:sum(z[:k])-1},{'type':'ineq','fun':con}],options={'maxiter':150,'ftol':1e-9})
        if res.success and (best is None or res.fun<best.fun): best=res
    if best is None:return None
    return 1/best.fun,best.x

for a in [.18,.2,.21,.24]:
    k=3
    best=(max(2,(1+sqrt(a))**2,1+2*a/3+4*sqrt(a*(3-2*a))/3),None)
    for diag in [(0,0,0),(0,0,1),(0,1,1),(1,1,1)]:
        for status in product(range(3),repeat=3):
            result=solve(k,a,diag,status)
            if result is not None and result[0]>best[0]+1e-6:
                best=(result[0],(diag,status,result[1]))
                print('new best',a,best,flush=True)
    print('final best',a,best,flush=True)
