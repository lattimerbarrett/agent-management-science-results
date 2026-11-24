import numpy as np

def make_field(rec):
    x=np.r_[rec['act'],rec['mus']];p=np.r_[rec['p'],rec['pm']];q=np.r_[rec['q'],rec['qm']];C=float(rec['C']);w0=np.r_[rec['w'],0,0];V=x[:,None]**np.arange(4);T=np.r_[-w0[:6]/x[:6],0,0];Vm=V[6:];pm=p[6:];qm=q[6:]
    def raw(pos,hc,A):
        w=w0+pos*T;h=V@hc;u=w*p*h;M=V.T@(w[:,None]*V);N=V.T@((w*p*p/C)[:,None]*V);ac=-C*np.linalg.solve(M,N@hc);aa=V@ac;F=np.dot(u,p*p);rat=2*(aa/p+C*h/q-F/C);b=w*rat;vel=np.dot(T,b)/np.dot(T,T)
        bb=-V@np.linalg.solve(M,V.T@(u*aa));e=np.dot(u,p*aa);zz=w*p*p/C;z1=(u*p*p+2*w*p*aa-zz*F)/C;z2=(w*(aa*aa+2*p*bb)+2*u*p*aa-z1*F-zz*e)/C
        aaa=C*h;bbb=-V@np.linalg.solve(N,V.T@(z2*q+z1*aaa));eee=np.dot(z2,q*q)+np.dot(z1,q*aaa);f2=(z2*q*q+2*z1*q*aaa+zz*(aaa*aaa+2*q*bbb)-(u+b)*F-w*eee)/C
        hd=np.linalg.solve(C*N,V.T@(p*(f2-b*p*h)));hd+=np.linalg.solve(N,Vm.T@(4*pm/C*A*A));ad=A*(-(pm*(C*(Vm@hc))+qm*(Vm@ac)+F)/C)
        c=(np.sum((C+p[:6]**2)*b[:6]**2/w[:6])/4+4*np.sum((C+pm**2)*A*A))/C
        return vel,hd,ad,c
    def field(z):
        pos=z[0];hfree=z[1:4];A=z[4:];w=w0+pos*T;erow=-(w*p**3)@V/C;hc=np.r_[(1-erow[1:]@hfree)/erow[0],hfree]
        vel,hd,ad,c=raw(pos,hc,A);return np.r_[vel,(hd+c*hc)[1:],ad+c*A]
    E=float(rec['E']);eq=np.r_[rec['pos'],rec['h'][1:]/E,rec['A']/E]
    return field,eq

def screen(rec,step=1e-5):
    field,eq=make_field(rec)
    J=np.column_stack([field(eq+1e-20j*np.eye(6)[j]).imag/1e-20 for j in range(6)])
    eig,vec=np.linalg.eig(J);left=np.linalg.inv(vec)
    radial=np.sqrt(rec['kap2'])/rec['E'];idx=np.argmin(abs(eig-radial));ell=left[idx].real
    def Hdir(u):
        eta=1e-20
        return (field(eq+step*u+1j*eta*u).imag-field(eq-step*u+1j*eta*u).imag)/(2*step*eta)
    actions=[]
    for j,ev in enumerate(eig):
        if ev.imag>1e-4:
            u=vec[:,j].real;v=vec[:,j].imag;actions.append((ev,ell@(Hdir(u)+Hdir(v))))
    return dict(eig=eig,actions=actions,residual=np.linalg.norm(field(eq)),radial=radial,J=J,eq=eq)

if __name__=='__main__':
    import pickle
    data=pickle.load(open('workspace/agent4_broad_positive_rays.pkl','rb'))
    for rec in data:
        if rec['L'] in [5,10] and rec['ratio']==.98:
            ans=screen(rec);print(rec['L'],rec['ratio'],rec['bits'],'res',ans['residual'],'eigs',ans['eig'],'actions',ans['actions'])
