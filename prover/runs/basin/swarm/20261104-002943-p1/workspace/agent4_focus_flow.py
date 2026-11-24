import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import expit
from pathlib import Path
D=np.load('workspace/agent4_positive_ray_audit.npz');x=D['x'];p=D['p'];q=D['q'];C=float(D['C']);w0=D['w'];hc0=D['h'];A0=D['A'];V=x[:,None]**np.arange(4);T=np.r_[-w0[:6]/x[:6],0,0];Vm=V[6:];pm=p[6:];qm=q[6:]
def chart(u):
 t=np.tanh(u);w=w0+t*T;w[2]=2*w0[2]*expit(2*u);w[3]=2*w0[3]*expit(-2*u);return t,w

def flow(tau,z):
 t,w=chart(z[0]);hc=z[1:5];A=z[5:];h=V@hc;u=w*p*h;M=V.T@(w[:,None]*V);N=V.T@((w*p*p/C)[:,None]*V);ac=-C*np.linalg.solve(M,N@hc);aa=V@ac;F=np.dot(u,p*p);rat=2*(aa/p+C*h/q-F/C);b=w*rat;ud=-rat[3]/(1+t) if z[0]>=0 else rat[2]/(1-t)
 bb=-V@np.linalg.solve(M,V.T@(u*aa));e=np.dot(u,p*aa);zz=w*p*p/C;z1=(u*p*p+2*w*p*aa-zz*F)/C;z2=(w*(aa*aa+2*p*bb)+2*u*p*aa-z1*F-zz*e)/C
 aaa=C*h;bbb=-V@np.linalg.solve(N,V.T@(z2*q+z1*aaa));eee=np.dot(z2,q*q)+np.dot(z1,q*aaa);f2=(z2*q*q+2*z1*q*aaa+zz*(aaa*aaa+2*q*bbb)-(u+b)*F-w*eee)/C
 hd=np.linalg.solve(C*N,V.T@(p*(f2-b*p*h)));hd+=np.linalg.solve(N,Vm.T@(4*pm/C*A*A));ad=A*(-(pm*(C*(Vm@hc))+qm*(Vm@ac)+F)/C)
 E=-F/C;c=(np.sum((C+p[:6]**2)*b[:6]**2/w[:6])/4+4*np.sum((C+pm**2)*A*A))/(C*E)
 return np.r_[ud,hd+c*hc,ad+c*A]
def efuel(z):
 t,w=chart(z[0]);return -(w*p**3)@(V@z[1:5])/C
E=-(w0*p**3)@(V@hc0)/C;eq=np.r_[0,hc0/E,A0/E]
def boundary(t,z):return min(30-abs(z[0]),100-max(abs(z[1:])))
boundary.terminal=True;boundary.direction=-1
rng=np.random.default_rng(355);bestcross=-1;longest=0
for j in range(100):
 zz=eq.copy();amp=10**rng.uniform(-5,-1);zz[0]+=amp*rng.normal();zz[1:]+=amp*rng.normal(size=6)*np.maximum(abs(eq[1:]),.01)
 if min(zz[5:])<=0:continue
 E=efuel(zz);zz[1:]/=E
 sol=solve_ivp(flow,[0,300],zz,rtol=1e-8,atol=1e-10,max_step=.1,events=boundary);u=sol.y[0];cross=np.sum(u[1:]*u[:-1]<0)
 if cross>bestcross or sol.t[-1]>longest:
  bestcross=max(bestcross,cross);longest=max(longest,sol.t[-1]);print('BEST',j,'amp',amp,'cross',cross,'T',sol.t[-1],'u',min(u),max(u),'endnorm',np.linalg.norm(sol.y[:,-1]-eq),'fuel',efuel(sol.y[:,-1]),flush=True);np.savez('workspace/agent4_focus_flow_best.npz',eq=eq,z0=zz,t=sol.t,y=sol.y)
