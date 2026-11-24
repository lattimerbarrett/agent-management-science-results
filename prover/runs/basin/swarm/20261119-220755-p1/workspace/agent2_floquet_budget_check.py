from fractions import Fraction as Q
s=Q(70711,50000);assert s*s>2
alpha=Q(1677,10000);rho=Q(1,25000);delta=s*Q(22,10**7);e=s*Q(1,1000);H=s*1600;b=s*2400;an=s*Q(1,10000);astar=Q(9999,10000);dmax=Q(6)
import numpy as np
D=np.load('workspace/agent2_floquetframe_m072.npz')['D']
for i in range(1,5):
 assert abs(Q(float(D[i,i])))>=alpha and abs(Q(float(D[i,i])))<=dmax
u,v=Q(float(D[5,5])),Q(float(D[5,6]));assert Q(float(D[6,6]))==u and Q(float(D[6,5]))==-v
assert abs(u)>=alpha and u*u+v*v<dmax*dmax
for i in range(7):
 for j in range(7):
  if i!=j and (i,j) not in [(5,6),(6,5)]:assert D[i,j]==0
assert D[0,0]==0
r=delta+e*rho+H*rho*rho/2;q=r/(astar-b*rho);ql=(e+H*rho+b*q)/(astar-b*rho);N=r+(an+(b+dmax)*rho)*q;f=N/(1-q);LipN=e+H*rho+(b+dmax)*q+(an+(b+dmax)*rho)*ql;Lip=LipN/(1-q)+N*ql/(1-q)**2
assert b*rho<astar and q<1 and f<alpha*rho and Lip<alpha
print('EXACT rational certificate budget PASS: fbar',float(f),'alpha*rho',float(alpha*rho),'Lipf',float(Lip),'alpha',float(alpha))
