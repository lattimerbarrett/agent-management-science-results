"""Intrinsic S5s3 edge flight and minimal-wall scattering. Coefficients ASCENDING."""
import numpy as np
from scipy.integrate import solve_ivp

def edge_data(ob,theta):
    x=ob.nodes; H=x-theta; V=ob.V
    p=ob.N*H/(ob.d*ob.fv); pp=H*ob.fv/ob.d
    M=V.T@(p[:,None]*V); Mp=V.T@(pp[:,None]*V)
    DG=-np.linalg.solve(Mp,M)
    dN=ob.N**2*np.sum((H/(ob.d*ob.fv**2))[:,None]*V,axis=0)
    L=2*(ob.Vmu/ob.fm[:,None]+ob.Vmu@DG/ob.gm[:,None])-2*dN/ob.N
    F=-4*np.linalg.solve(M,ob.Vmu.T*ob.fm)
    j=np.argmin(abs(x-theta))
    q=ob.gv[j]*V[j]+ob.fv[j]*(V[j]@DG)-dN
    vt=np.array([theta**i for i in range(3)])
    p4=np.prod(theta-np.delete(x,j))
    # Intrinsic dw/dtheta=A(theta)w. This is smooth at gap endpoints;
    # closest j cancels the apparent P5(theta) zero analytically.
    A=np.outer(np.linalg.solve(M,vt),q)/(2*p4)
    # theta velocity b*w; vanishes proportionally at each endpoint.
    b=-2*H[j]*q/ob.N
    return A,F,L,dN,b

def flight(ob,a,b,rtol=1e-11,atol=1e-13):
    ff=lambda theta,T:(edge_data(ob,theta)[0]@T.reshape(3,3)).ravel()
    sol=solve_ivp(ff,[a,b],np.eye(3).ravel(),rtol=rtol,atol=atol)
    assert sol.success
    return sol.y[:,-1].reshape(3,3)

def effective_pair(ob,a,b,left,right):
    T=flight(ob,a,b)
    _,Fa,La,_,_=edge_data(ob,a); _,Fb,Lb,_,_=edge_data(ob,b)
    F0=Fa[:,left]; F1=np.linalg.solve(T,Fb[:,right])
    L0=La[left]; L1=Lb[right]@T
    C=np.array([[L0@F0,L0@F1],[L1@F0,L1@F1]])
    return T,C
