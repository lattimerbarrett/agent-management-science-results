import sys;sys.path.insert(0,'workspace');from agent1_scattering_map import data
import numpy as np
C,U,Ui,mus,burst,sol=data(7);mu=2.544163685115879;SL,bL,bl=burst(-1,-mu);SR,bR,br=burst(1,mu);M=SL@Ui@SR@U;ev,V=np.linalg.eig(M);j=np.argmin(abs(ev-.49400155));X=V[:,j].real;X*=-np.sign(X[3]);X/=abs(X[3]);states=[(-1,X),(1,U@X),(1,SR@U@X),(-1,Ui@SR@U@X)]
for label,(t,x) in enumerate(states):
 betaL=burst(t,-mu)[2];betaR=burst(t,mu)[2];K=np.array([1,t,t*t,0])@x;lam=(-128*K/C if t==-1 else 128*K/C)
 print(label,'t',t,'X',x,'K',K,'posrate',lam,'betaL',betaL@x,'betaR',betaR@x,'energy',x[3],flush=True)
print('M',M,'eig',ev,'U',U,flush=True)
