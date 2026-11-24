import numpy as np
from scipy.integrate import solve_ivp
from pathlib import Path
DEL=4*np.sqrt(2);C=32.;mus=np.array([-np.sqrt(5+2*np.sqrt(2)),np.sqrt(5-2*np.sqrt(2))]);Dmu=(mus*mus-1)*(mus*mus-5)*(mus*mus-9)
def ode(tau,z):
 u,k0,k1,k2,F,a,b=z;t=np.tanh(u);tt=t*t;P0=tt*tt-10*tt+17;R=P0*P0-DEL*DEL;D=(tt-1)*(tt-5)*(tt-9);Kt=k0+k1*t+k2*tt;v=2*D*Kt/C;ud=-2*(tt-5)*(tt-9)*Kt/C
 d0=v*((8*t*(tt+5)/C+20*t*P0/R)*Kt-k1-t*k2)
 d1=v*(8*(tt-5)*Kt/C-k2);d2=-4*t*v*(4/C+P0/R)*Kt;dF=-v*P0*Kt
 A=np.array([a,b]);ad=np.empty(2)
 for j,mu in enumerate(mus):
  pm=-DEL;J=8*DEL*(mu+t)*(mu*mu+tt-10)*pm/R;B1=8*DEL*(mu*mu-5)*pm/C;B2=-8*DEL*(mu+t)*pm*((mu*mu-5)*D-C)/(C*R);B0=J-t*B1-tt*B2
  d0+=A[j]**2*B0;d1+=A[j]**2*B1;d2+=A[j]**2*B2;dF+=A[j]**2*(-8*DEL*pm)
  Km=k0+k1*mu+k2*mu*mu;ad[j]=A[j]*(-(Dmu[j]*Km-D*Kt)/(C*(mu-t))-2*F/C)
 return np.r_[ud,d0,d1,d2,dF,ad]
def ef(t,z):return -z[4]/C
ef.terminal=True;ef.direction=-1
if __name__=='__main__':
 rng=np.random.default_rng(722);bestturn=-1;besttime=0
 for j in range(1000):
  K2=10**rng.uniform(-2,2);K1=2*np.sqrt(K2)*rng.uniform(-.99,.99);E=10**rng.uniform(-1,2);At=10**rng.uniform(-5,0);rat=10**rng.uniform(-1,1)
  z0=np.array([0,1,K1,K2,-C*E,At*np.sqrt(rat),At/np.sqrt(rat)])
  sol=solve_ivp(ode,[0,100],z0,rtol=1e-7,atol=1e-9,max_step=.1,events=ef);pos=np.tanh(sol.y[0]);turns=np.sum(np.diff(np.sign(np.diff(pos)))!=0)
  if turns>bestturn or sol.t[-1]>besttime:
   bestturn=max(bestturn,turns);besttime=max(besttime,sol.t[-1]);print('BEST',j,'T',sol.t[-1],'turns',turns,'range',min(pos),max(pos),'Eend',-sol.y[4,-1]/C,'params',K2,K1,E,At,rat,flush=True)
   np.savez('workspace/agent4_mixedpair_best.npz',params=[K2,K1,E,At,rat],t=sol.t,y=sol.y,z0=z0)
