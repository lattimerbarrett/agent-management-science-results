import numpy as np
from scipy.integrate import solve_ivp

class Billiard:
    def __init__(self,core,extra,pcoef,qcoef,h,left,right):
        self.core=np.asarray(core);self.extra=np.asarray(extra);self.pcoef=np.asarray(pcoef);self.qcoef=np.asarray(qcoef);self.h=h;self.left=left;self.right=right
        self.X=np.array([np.ones(len(core)),core,np.asarray(core)**2]).T
        self.Xe=np.array([np.ones(len(extra)),extra,np.asarray(extra)**2]).T
        self.d=1/np.prod(np.where(np.eye(len(core),dtype=bool),1,np.asarray(core)[:,None]-np.asarray(core)[None,:]),axis=1)
    def p(self,x):return np.polyval(self.pcoef,x)
    def q(self,x):return np.polyval(self.qcoef,x)
    def data(self,theta,a):
        L=self.core;X=self.X;h=self.h;p=self.p;q=self.q
        w=self.d*q(L)*(L-theta);wt=-self.d*q(L);H=(X.T*w)@X
        Z=np.vstack([np.ones(len(L)),X.T*p(L)])
        dw=np.linalg.lstsq(Z,np.r_[0.,-H@a],rcond=None)[0]
        E=np.dot(w,(X@a)*(p(L)-q(L)));wp=w*p(L)**2/h
        dwp=(dw*p(L)**2+2*w*p(L)*(X@a)+wp*E)/h
        b=-np.linalg.solve((X.T*wp)@X,H@a)
        Rc=q(L)*(X@a)+p(L)*(X@b)+E
        Re=q(self.extra)*(self.Xe@a)+p(self.extra)*(self.Xe@b)+E
        V=np.dot(wt,2*w*Rc/h)/np.dot(wt,wt)
        return w,wt,H,E,Rc,Re,V
    def mat(self,theta,interior=True):
        vs=[];ds=[];es=[]
        for j in range(3):
            w,wt,H,E,Rc,Re,V=self.data(theta,np.eye(3)[j]);vs.append(V);ds.append((4*E-2*Re)/self.h);es.append(E)
        vr=np.array(vs);D=np.array(ds).T;F=4*np.linalg.solve(H,self.Xe.T*self.p(self.extra));B=None
        if interior:
            R=self.h*wt/(2*w)
            C=np.linalg.solve(H,self.X.T@(w*R*R*self.p(self.core))/self.h**2)
            B=-np.outer(C,vr)
        return B,vr,D,F,np.array(es)
    def transport(self,tol=2e-9):
        gap=self.right-self.left;e=1e-8*gap
        ss=solve_ivp(lambda t,y:(self.mat(t)[0]@y.reshape(3,3)).ravel(),[self.left+e,self.right-e],np.eye(3).ravel(),rtol=tol,atol=tol*.01,dense_output=True)
        U=ss.y[:,-1].reshape(3,3)
        out={'U':U,'sol':ss}
        for side,t in [('L',self.left),('R',self.right)]:
            _,vr,D,F,E=self.mat(t,False)
            refl=[np.eye(3)-2*np.outer(F[:,j],D[j])/(D[j]@F[:,j])for j in range(len(self.extra))]
            out.update({side+'growth':D,side+'force':F,side+'energy':E,side+'reflect':refl})
        return out

def standard(h=18.,picks=(0,1,0),extra=None):
    core6=np.array([-3.,-2.,-1.,1.,2.,3.]);pol=np.poly(core6);pol[-1]+=h;r=np.sort(np.roots(pol).real)
    pc=np.poly(r[[2*j+picks[j]for j in range(3)]]);qc=np.poly(r[[2*j+1-picks[j]for j in range(3)]]);
    if extra is None:extra=np.array([0.,np.sqrt(7.)])
    return Billiard(np.delete(core6,1),extra,pc,qc,h,1.,2.)

if __name__=='__main__':
    b=standard();m=b.transport();print(m['U']);print(m['Lgrowth']@m['Lforce']);print(m['Rgrowth']@m['Rforce'])
