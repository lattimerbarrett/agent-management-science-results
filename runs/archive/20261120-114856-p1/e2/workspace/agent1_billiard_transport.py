import sys,numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0,'workspace')
from agent2_edge_ode import *

def mat(th):
 w,wt,H,*_=data(th,np.zeros(3))
 Vrow=np.array([data(th,np.eye(3)[j])[-1] for j in range(3)])
 g=-np.linalg.solve(H,Lc.T@((wt*wt/(4*w))*p(CORE)))
 return np.outer(g,Vrow)
def ode(th,Y):return (mat(th)@Y.reshape(3,3)).ravel()
eta=1e-7
sol=solve_ivp(ode,(1+eta,2-eta),np.eye(3).ravel(),rtol=2e-11,atol=1e-12,dense_output=True,max_step=.01)
P=sol.y[:,-1].reshape(3,3);print('transport',P, 'eig',np.linalg.eigvals(P))

def endpoint(th):
 H=data(th,np.zeros(3))[2]
 rows=np.array([[(4*data(th,np.eye(3)[j])[4]-2*data(th,np.eye(3)[j])[7][i])/h for j in range(3)] for i in range(2)])
 vs=np.array([np.linalg.solve(H,p(xi)*Le[i]) for i,xi in enumerate(EXTRA)]).T
 print('theta',th,'coupling',rows@vs)
 Ss=[np.eye(3)-2*np.outer(vs[:,i],rows[i])/(rows[i]@vs[:,i]) for i in range(2)]
 Ss.append(Ss[0]@Ss[1]);return rows,vs,Ss
lrow,lvs,LS=endpoint(1.);rrow,rvs,RS=endpoint(2.)
Lvec=lambda th:2*d*np.array([1,2-th,7-2*th])
for jl in range(3):
 for jr in range(3):
  C=LS[jl]@np.linalg.solve(P,RS[jr]@P)
  val,vec=np.linalg.eig(C)
  print('combo',jl,jr,'eig',val)
  for ii,ev in enumerate(val):
   if abs(ev.imag)>1e-8 or ev.real<=0 or ev.real>=.999999:continue
   aa=vec[:,ii].real;aa*=np.sign(Lvec(1)@aa);aa/=Lvec(1)@aa
   ar=P@aa;arb=RS[jr]@ar;al=np.linalg.solve(P,arb)
   print(' candidate',ev,'aL',aa,'right u',rrow@ar,'left u',lrow@al,'E R before/after,Lbefore',Lvec(2)@ar,Lvec(2)@arb,Lvec(1)@al)
   print(' V signs inL,inR,outR,outL',data(1.01,aa)[-1],data(1.99,ar)[-1],data(1.99,arb)[-1],data(1.01,LS[jl]@al)[-1])
