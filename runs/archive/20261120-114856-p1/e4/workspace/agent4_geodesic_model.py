import numpy as np
from scipy.integrate import solve_ivp

class GeodesicModel:
    """Experimental leading CG slow geodesic; NOT a convergence/counterexample proof.
    Coefficients q,r descending; v,xi coefficients ascending. tau ascending 0..2,
    with monic cubic leading term. q*r-H must have 8simple real roots.
    """
    def __init__(self,q,r,H):
        self.q=np.array(q);self.r=np.array(r);self.H=float(H)
        self.P=np.polymul(q,r);self.P[-1]-=H
        roots=np.sort_complex(np.roots(self.P));assert max(abs(roots.imag))<1e-7
        self.x=roots.real;self.f=np.vander(self.x,4,increasing=True)
        self.qv=np.polyval(q,self.x);self.rv=np.polyval(r,self.x)
        pd=np.polyval(np.polyder(self.P),self.x)
        self.C=(self.rv/pd)[:,None]*self.f[:,:3]
        self.wb=self.rv/pd*self.x**3;self.Ci=np.linalg.pinv(self.C)
        Sy=np.zeros((8,8))
        for j in range(4):
            Sy[3-j:8-j,j]=r;Sy[3-j:8-j,4+j]=q
        rhs=np.zeros(8);rhs[-1]=-H
        self.vb=np.linalg.solve(Sy,rhs)[:4]
    def weights(self,tau):return self.wb+self.C@tau
    def maps(self,tau,xi):
        w=self.weights(tau);f=self.f;qv=self.qv;rv=self.rv;H=self.H
        G=f.T@(w[:,None]*f);Gp=f.T@((w*qv*qv/H)[:,None]*f)
        dr=-np.linalg.solve(Gp,G@xi)
        df=rv*(f@xi)+qv*(f@dr);dh=w@df;ee=df-dh
        dW=2*w*ee/H
        K=np.linalg.solve(G,f.T@(w*qv*ee*ee))/H**2
        cc=np.sum(w*(H+qv*qv)*ee*ee)/H**3
        return self.Ci@dW,-K+cc*self.vb,dh,w
    def field(self,t,Z):
        tt,dx,_,_=self.maps(Z[:3],Z[3:]);return np.r_[tt,dx]
    def shoot(self,T,angle,tol=1e-9,maxtime=20,margin=1e-10):
        tau=np.array([0.,T,0.])
        assert min(self.weights(tau))>0
        Lmap=np.column_stack([self.maps(tau,np.eye(4)[j])[0]for j in range(4)])
        dhrow=np.array([self.maps(tau,np.eye(4)[j])[2]for j in range(4)])
        vel=np.array([np.cos(angle),0.,np.sin(angle)])
        if vel[0]<0:vel=-vel
        xi=np.linalg.solve(np.vstack([dhrow,Lmap]),np.r_[0.,vel])
        xi/=np.linalg.norm(self.C@vel)
        def bound(t,Z):return min(self.weights(Z[:3]))-margin
        bound.terminal=True;bound.direction=-1
        def cross(t,Z):return Z[0] if t>1e-7 else 1e-8
        cross.terminal=True;cross.direction=-1
        sol=solve_ivp(self.field,[0.,maxtime],np.r_[tau,xi],events=[bound,cross],rtol=tol,atol=tol*1e-3,dense_output=True)
        Z=sol.y[:,-1];tt,_,dh,w=self.maps(Z[:3],Z[3:])
        return {'residual':np.array([Z[2],tt[1]]),'returned':len(sol.t_events[1])>0,'time':sol.t[-1],'Z':Z,'sol':sol,'minweight':min(w),'deltah':dh,'velocity':tt}
