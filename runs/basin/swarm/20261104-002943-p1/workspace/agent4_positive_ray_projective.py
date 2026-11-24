import numpy as np
from pathlib import Path
D=np.load('workspace/agent4_positive_ray_audit.npz');x=D['x'];p=D['p'];q=D['q'];C=float(D['C']);w0=D['w'];h0=D['h'];A0=D['A'];kap=float(D['kap']);V=x[:,None]**np.arange(4);T=np.r_[-w0[:6]/x[:6],0,0];Vm=V[6:];pm=p[6:];qm=q[6:]

def raw(pos,hc,A):
 w=w0+pos*T;h=V@hc;u=w*p*h;M=V.T@(w[:,None]*V);N=V.T@((w*p*p/C)[:,None]*V);ac=-C*np.linalg.solve(M,N@hc);aa=V@ac;F=np.dot(u,p*p);rat=2*(aa/p+C*h/q-F/C);b=w*rat;vel=np.dot(T,b)/np.dot(T,T)
 bb=-V@np.linalg.solve(M,V.T@(u*aa));e=np.dot(u,p*aa);zz=w*p*p/C;z1=(u*p*p+2*w*p*aa-zz*F)/C;z2=(w*(aa*aa+2*p*bb)+2*u*p*aa-z1*F-zz*e)/C
 aaa=C*h;bbb=-V@np.linalg.solve(N,V.T@(z2*q+z1*aaa));eee=np.dot(z2,q*q)+np.dot(z1,q*aaa);f2=(z2*q*q+2*z1*q*aaa+zz*(aaa*aaa+2*q*bbb)-(u+b)*F-w*eee)/C
 hd=np.linalg.solve(C*N,V.T@(p*(f2-b*p*h)));hd+=np.linalg.solve(N,Vm.T@(4*pm/C*A*A));ad=A*(-(pm*(C*(Vm@hc))+qm*(Vm@ac)+F)/C)
 c=(np.sum((C+p[:6]**2)*b[:6]**2/w[:6])/4+4*np.sum((C+pm**2)*A*A))/C
 return vel,hd,ad,c

def unpack(z):
 pos=z[0];hfree=z[1:4];A=z[4:];w=w0+pos*T;erow=-(w*p**3)@V/C;hc=np.r_[(1-erow[1:]@hfree)/erow[0],hfree];return pos,hc,A

def projective(z):
 pos,hc,A=unpack(z);vel,hd,ad,c=raw(pos,hc,A);return np.r_[vel,(hd+c*hc)[1:],ad+c*A]
E=-(w0*p**3)@(V@h0)/C;hc=h0/E;AA=A0/E;eq=np.r_[0,hc[1:],AA];print('E',E,'eq',eq,'normfield',np.linalg.norm(projective(eq)))
J=np.column_stack([projective(eq+1e-20j*np.eye(6)[j]).imag/1e-20 for j in range(6)]);print('J',J);print('EIGEN',np.linalg.eigvals(J));print('kapnorm',kap/E)
np.savez('workspace/agent4_positive_ray_jac.npz',eq=eq,J=J,eigs=np.linalg.eigvals(J),E=E)
