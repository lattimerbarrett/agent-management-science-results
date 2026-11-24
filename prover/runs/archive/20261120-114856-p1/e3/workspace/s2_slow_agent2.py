import numpy as np
from scipy.integrate import solve_ivp
D=np.longdouble
u=D(1);v=D(4);t=D(9)/8;H=D(1863)/4096

def trans(m,h,z,w,u,v):
 M=[D(1),m,u*m+h,u*u*m+u*h+z]
 for j in range(4,8): M.append((u+v)*M[j-1]-u*v*M[j-2]+H*M[j-4]-2*H*w*t**(j-4))
 a=(m*M[2]-M[3])/(M[2]-m*m);b=-M[2]-a*m
 qq=[b*b,2*a*b,a*a+2*b,2*a,D(1)]
 E=[sum(qq[k]*M[k+j] for k in range(5)) for j in range(4)]
 mm,mm2,mm3=[E[j]/E[0] for j in [1,2,3]]
 return mm,mm2-v*mm,mm3-v*mm2,w*(t*t+a*t+b)**2/E[0]
def Fslow(time,state):
 m,p,q=map(D,state);r=D('.003')
 outs=[]
 for sign in [1,-1]:
  h=r*sign;z=p*h*h;w=q*h**4
  vals=trans(*trans(m,h,z,w,u,v),v,u)
  outs.append([(vals[0]-m)/h**2,(vals[1]-h)/h**3,(vals[2]-z)/h**4,(vals[3]/w-1)/h**2])
 fm,fh,fz,gw=(np.array(outs[0])+np.array(outs[1]))/2
 return np.array([fm,fz-2*p*fh,q*(gw-4*fh)],float)
for ini in [[.3,0,1],[.3,1,1],[.4,0,1],[.35,-1,.01],[.35,1,.01],[.35,0,.001]]:
 print('start',ini,'F',Fslow(0,ini),flush=True)
 def event(t,x):return min(x[0]-.2472,.4751-x[0],10-abs(x[1]),100-x[2],x[2])
 event.terminal=True
 sol=solve_ivp(Fslow,[0,100],ini,rtol=1e-6,atol=1e-8,events=event,max_step=.02)
 print('end',sol.t[-1],sol.y[:,-1], 'mrange',sol.y[0].min(),sol.y[0].max(),flush=True)
np.savez('workspace/s2_slow_agent2.npz',t=sol.t,y=sol.y)
from pathlib import Path
Path('workspace/s2_slow_agent2.py').write_text(Path(__file__).read_text())
