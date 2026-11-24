import sys,numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0,'workspace')
from agent2_edge_ode import data,CORE,EXTRA,h,d,Lc,Le,p,q

def rhs(t,y):
 th,a1,a2,M0,Mb=y;A=np.array([1/(2*d)-(2-th)*a1-(7-2*th)*a2,a1,a2]);M=np.array([M0,Mb])
 w,wt,H,dw,E,b,Rc,Re,V=data(th,A)
 Q=-np.linalg.solve(H,Lc.T@(w*Rc**2*p(CORE))/h**2+4*Le.T@(M*p(EXTRA)))
 L=2*d*np.array([1,2-th,7-2*th]);Lp=2*d*np.array([0,-1,-2]);DD=-(L@Q+(Lp@A)*V)
 Adot=Q+DD*A;Md=((4-2*Re)/h+2*DD)*M
 return np.r_[V,Adot[1:],Md]

def event(t,y):return 100-max(abs(y[1:3]).max(),y[3:].max())
event.terminal=True
