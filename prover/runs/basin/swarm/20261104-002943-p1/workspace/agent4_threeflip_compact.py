import numpy as np,itertools
from scipy.integrate import solve_ivp
from pathlib import Path
DEL=4*np.sqrt(2);C=32.;allmu=np.r_[-np.sqrt(5+2*np.sqrt(2)),-np.sqrt(5-2*np.sqrt(2)),np.sqrt(5-2*np.sqrt(2)),np.sqrt(5+2*np.sqrt(2))]


def raw(z,mus):
 u,k0,k1,k2,E=z[:5];A=z[5:];t=np.tanh(u);tt=t*t;P0=tt*tt-10*tt+17;R=P0*P0-DEL*DEL;D=(tt-1)*(tt-5)*(tt-9);Kt=k0+k1*t+k2*tt;v=2*D*Kt/C;ud=-2*(tt-5)*(tt-9)*Kt/C
 dk=np.array([v*((8*t*(tt+5)/C+20*t*P0/R)*Kt-k1-t*k2),v*(8*(tt-5)*Kt/C-k2),-4*t*v*(4/C+P0/R)*Kt]);dF=-v*P0*Kt;ad=[]
 for j,mu in enumerate(mus):
  pm=-DEL;Dm=(mu*mu-1)*(mu*mu-5)*(mu*mu-9);J=8*DEL*(mu+t)*(mu*mu+tt-10)*pm/R;B1=8*DEL*(mu*mu-5)*pm/C;B2=-8*DEL*(mu+t)*pm*((mu*mu-5)*D-C)/(C*R);B0=J-t*B1-tt*B2
  dk+=A[j]**2*np.array([B0,B1,B2]);dF+=A[j]**2*(-8*DEL*pm)
  Km=k0+k1*mu+k2*mu*mu;ad.append(A[j]*(-(Dm*Km-D*Kt)/(C*(mu-t))+2*E))
 return np.r_[ud,dk,-dF/C,ad]
def normode(t,z,mus):
 dz=raw(z,mus);r=z[1:]@dz[1:]/(z[1:]@z[1:]);dz[1:]-=r*z[1:];return dz

def ef(t,z):return z[4]
ef.terminal=True;ef.direction=-1
def eu(t,z):return 30-abs(z[0])
eu.terminal=True;eu.direction=-1
if __name__=='__main__':
 rng=np.random.default_rng(993);best=(-1,None);longest=0
 for missing in range(4):
  mus=np.delete(allmu,missing)
  for j in range(250):
   K0=1.;K2=10**rng.uniform(-2,2);K1=2*np.sqrt(K2)*rng.uniform(-.99,.99);E=10**rng.uniform(-1,2);A=10**rng.uniform(-5,0,size=3);z0=np.r_[0,K0,K1,K2,E,A];z0[1:]/=np.linalg.norm(z0[1:])
   sol=solve_ivp(lambda t,z:normode(t,z,mus),[0,200],z0,rtol=2e-7,atol=2e-9,max_step=.25,events=[ef,eu]);u=sol.y[0];cross=np.sum(u[1:]*u[:-1]<0)
   if cross>best[0] or sol.t[-1]>longest:
    best=(max(best[0],cross),None);longest=max(longest,sol.t[-1]);print('BEST','missing',missing,'j',j,'cross',cross,'T',sol.t[-1],'u',min(u),max(u),'E',sol.y[4,-1],flush=True)
    np.savez('workspace/agent4_threeflip_best.npz',mus=mus,z0=z0,t=sol.t,y=sol.y,missing=missing)
