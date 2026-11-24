"""Finite monotone interior-Cantor triangular matrix weights."""
import numpy as np

def cantor(Q,p,N):
    q=p/(p-1);rho=1/8
    ea=1/Q;ec=Q**(-1/(p-1));r=Q**(1/p)
    sa=(1-ea)/rho;sc=(1-ec)/rho
    da=ea/(1-rho);dc=ec/(1-rho)
    assert min(sa,sc)>=4
    out=[]
    def rec(l,L,a,c,z,d,n):
        if n==0:out.append((l,l+L,a,c,z));return
        out.append((l,l+L/4,da*a,dc*c,z-2*d))
        rec(l+L/4,L/16,sa*a,sc*c,z-d,d/(sa**(1/p)*sc**(1/q)),n-1)
        out.append((l+5*L/16,l+11*L/16,da*a,dc*c,z))
        rec(l+11*L/16,L/16,sa*a,sc*c,z+d,d/(sa**(1/p)*sc**(1/q)),n-1)
        out.append((l+3*L/4,l+L,da*a,dc*c,z+2*d))
    rec(0.,1.,1.,1.,0.,r,N)
    out.sort()
    return np.array([(-1.,0.,da,dc,-2*r)]+out+[(1.,2.,da,dc,2*r)])

def all_endpoint_characteristics(cells,p):
    q=p/(p-1)
    L=cells[:,1]-cells[:,0]
    a,c,z=cells[:,2:].T
    B=np.zeros((len(L),2,2));C=B.copy()
    B[:,0,0]=a**(1/p);B[:,0,1]=a**(1/p)*z;B[:,1,1]=c**(-1/q)
    C[:,0,0]=a**(-1/p);C[:,0,1]=-z*c**(1/q);C[:,1,1]=c**(1/q)
    K=np.linalg.norm(np.einsum('iab,jbc->ijac',B,C),ord=2,axis=(-2,-1))**q
    mx=0.;arg=None
    for i in range(len(L)):
        for j in range(i+1,len(L)+1):
            w=L[i:j]/sum(L[i:j]);inner=K[i:j,i:j]@w
            val=np.sum(w*inner**(p-1))
            if val>mx:mx=val;arg=(i,j)
    return mx,arg

if __name__=='__main__':
    for p in (2.,3.,4.):
        for Q in (4.**max(1,p-1),10.**max(1,p-1)):
            cells=cantor(Q,p,4)
            assert np.min(np.diff(cells[:,4]))>=-1e-12
            inside=cells[(cells[:,0]>=0)&(cells[:,1]<=1)]
            length=inside[:,1]-inside[:,0]
            assert abs(np.sum(length*inside[:,2])-1)<1e-12
            assert abs(np.sum(length*inside[:,3])-1)<1e-12
            value,arg=all_endpoint_characteristics(cells,p)
            print('p,Q,N,cells,max endpoint Ap,ratio=',p,Q,4,len(cells),value,value/Q)
