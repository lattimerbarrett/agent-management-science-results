import numpy as np,pickle
from scipy.integrate import solve_ivp
from pathlib import Path
with open('workspace/agent4_nonmax_normal_jet.pkl','rb') as f:d=pickle.load(f)
x=np.array(d['x'],float).ravel()/8;V=np.vander(x,4,increasing=True);q=np.array(d['q'],float).ravel()/4096;w0=np.array(d['w0'],float).ravel();n=8
# center of frozen quadratic normal field
rat=-106151644319733567607/1611735622721970835
O=580098.454520748;hc3=(O-12545)/(675713+12545*rat);hc1=1+rat*hc3
h=np.array([0,hc1*8,0,hc3*512]);h/=max(abs(q*(V@h)))
def step(w):
 M=[V.T@(wi[:,None]*V) for wi in w];cc=[V.T@(wi*x**4) for wi in w];aa=[]
 for k in range(3):aa.append(np.linalg.solve(M[0],cc[k]-sum((M[j]@aa[k-j] for j in range(1,k+1)),np.zeros(4))))
 p=[x**4-V@aa[0],-V@aa[1],-V@aa[2]]
 pp=[sum((p[j]*p[k-j] for j in range(k+1)),np.zeros(8)) for k in range(3)]
 num=[sum((w[j]*pp[k-j] for j in range(k+1)),np.zeros(8)) for k in range(3)];den=[sum(a) for a in num];out=[]
 for k in range(3):out.append((num[k]-sum((out[k-j]*den[j] for j in range(1,k+1)),np.zeros(8)))/den[0])
 return out
def fun(t,z):
 w=z[:8];hh=z[8:];u=w*q*(V@hh);ff=step(step([w,u,np.zeros(8)]));b1=ff[1]-u
 G=V.T@((w*q*q)[:,None]*V);Gb=V.T@((b1*q*q)[:,None]*V);hf=np.linalg.solve(G,V.T@(q*ff[2])-Gb@hh)
 return np.r_[b1,hf]
def boundary(t,z):return min(z[:8])-1e-7
boundary.terminal=True;boundary.direction=-1
z0=np.r_[w0,h];print('w0',w0,'h',h,'speed',np.linalg.norm(fun(0,z0)[:8]))
sol=solve_ivp(fun,[0,100],z0,rtol=1e-9,atol=1e-11,events=boundary,dense_output=True,max_step=.1)
print('end',sol.t[-1],sol.message,'w',sol.y[:8,-1],'distance',np.linalg.norm(sol.y[:8,-1]-w0))
for t in np.linspace(0,sol.t[-1],11):
 zz=sol.sol(t);print(t,'w',np.round(zz[:8],6),'distance',np.linalg.norm(zz[:8]-w0))
np.savez('workspace/agent4_full_slow_flow.npz',t=sol.t,y=sol.y)
