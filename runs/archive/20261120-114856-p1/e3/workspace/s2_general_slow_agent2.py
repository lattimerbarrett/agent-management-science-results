import numpy as np
from scipy.optimize import root
from scipy.integrate import solve_ivp
D=np.longdouble
# q coefficients, q' coefficients, H, extra nodes
AA=D(-2);BB=D(0);CC=-(D(1)+D(16267)/5340);DD=D(16267)/5340;HH=D(247)/890
xis=np.array([D(1)/20,D(3)],dtype=D)
poly=np.convolve([D(1),AA,BB],[D(1),CC,DD]);poly[-1]-=HH
import sympy as sp
xx=sp.symbols('x')
lam=np.array(sorted(float(sp.re(rr)) for rr in sp.nroots(sum(float(co)*xx**(4-j) for j,co in enumerate(poly)))),dtype=float)
LH=BB-DD;LZ=AA-CC;NN=LH*LH+LZ*LZ

def trans(m,h,z,ws,a,b,c,d):
 M=[D(1),m,-a*m-b+h]
 M.append(-a*M[2]-b*m+z)
 for j in range(4,8):M.append(-sum(poly[k]*M[j-k] for k in range(1,5))-2*HH*np.sum(ws*xis**(j-4)))
 qa=(m*M[2]-M[3])/(M[2]-m*m);qb=-M[2]-qa*m
 qq=[qb*qb,2*qa*qb,qa*qa+2*qb,2*qa,D(1)]
 E=[sum(qq[k]*M[k+j] for k in range(5)) for j in range(4)]
 mm,mm2,mm3=[E[j]/E[0] for j in [1,2,3]]
 return mm,mm2+c*mm+d,mm3+c*mm2+d*mm,ws*(xis*xis+qa*xis+qb)**2/E[0]
def slow(time,state):
 m,p,lq1,lq2=map(D,state); qs=np.exp(np.array([lq1,lq2],dtype=D));r=D('.0001')
 hout=(-LH-p*LZ)/NN;zout=(-LZ+p*LH)/NN
 vals=[]
 for sign in [1,-1]:
  rr=r*sign;h=hout*rr;z=zout*rr;ws=qs*rr*rr
  mm,hh,zz,ww=trans(*trans(m,h,z,ws,AA,BB,CC,DD),CC,DD,AA,BB)
  vals.append([(mm-m)/rr,(hh-h)/(rr*rr),(zz-z)/(rr*rr),*((ww/ws-1)/rr)])
 F=(np.array(vals[0])+np.array(vals[1]))/2
 fm,fh,fz=F[:3];g=LH*fh+LZ*fz
 fp=-LZ*fh+LH*fz+p*g
 return np.array([fm,fp,*(F[3:]+2*g)],float)
# exact stationarylineweightaffine in m
A=np.array([np.ones(4),lam,lam**2,lam**3]);vec0=np.linalg.solve(A,[1,0,-float(BB),float(AA*BB)]);vec1=np.linalg.solve(A,[0,1,-float(AA),float(AA*AA-BB)])
lo,hi=-1e100,1e100
for aa,bb in zip(vec0,vec1):
 if bb>0:lo=max(lo,-aa/bb)
 else:hi=min(hi,-aa/bb)
print('lineinterval',lo,hi,flush=True)
rng=np.random.default_rng(2)
for trial in range(200):
 ini=[rng.uniform(lo,hi),rng.normal(),rng.uniform(-4,1),rng.uniform(-4,1)]
 sol=root(lambda x:slow(0,x),ini,tol=1e-7)
 if sol.success and np.linalg.norm(slow(0,sol.x))<1e-4 and lo<sol.x[0]<hi and max(abs(sol.x[2:]))<30:
  print('FIX',sol.x,'F',slow(0,sol.x),flush=True);break
else:print('no fix',flush=True)
for trial in range(30):
 ini=[rng.uniform(lo+.05,hi-.05),rng.normal(),rng.uniform(-8,-1),rng.uniform(-8,-1)]
 def event(t,x):return min(x[0]-lo-1e-4,hi-x[0]-1e-4,20-max(np.abs(x[1:3])),x[2]+40,x[3]+40)
 event.terminal=True
 sol=solve_ivp(slow,[0,30],ini,rtol=1e-6,atol=1e-8,events=event,max_step=.05)
 dif=np.diff(sol.y[0]);turns=np.sum((dif[1:]*dif[:-1]<0)&(abs(dif[1:])>1e-6)&(abs(dif[:-1])>1e-6))
 print('FLOW',trial,'time',sol.t[-1],'turns',turns,'end',sol.y[:,-1],flush=True)
 if sol.t[-1]>29:np.savez('workspace/s2_flow_agent2.npz',t=sol.t,y=sol.y)
from pathlib import Path
Path('workspace/s2_general_slow_agent2.py').write_text(Path(__file__).read_text())
