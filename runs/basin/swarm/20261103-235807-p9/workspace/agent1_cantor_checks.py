import numpy as np
from pathlib import Path
from math import pi, log

def build(p,Q,N):
 q=p/(p-1); ew=1/Q; es=Q**(-1/(p-1)); rho=1/8
 sw=(1-ew)/rho; ss=(1-es)/rho; dw=ew/(1-rho); ds=es/(1-rho); r=Q**(1/p)
 assert max(ew,es)<=.5
 cells=[]
 def rec(l,L,n,w,s,z):
  de=r/(w**(1/p)*s**(1/q))
  if n==N:
   cells.append((l,l+L,n,w,s,z)); return
  for a,b,dz in [(0,1/4,-2),(5/16,11/16,0),(3/4,1,2)]:
   cells.append((l+a*L,l+b*L,n,w*dw,s*ds,z+dz*de))
  rec(l+L/4,L/16,n+1,w*sw,s*ss,z-de)
  rec(l+11*L/16,L/16,n+1,w*sw,s*ss,z+de)
 rec(0,1,0,1,1,0)
 cells.sort(); ar=np.array(cells)
 assert np.all(np.diff(ar[:,5])>=-1e-10)
 assert abs(np.sum((ar[:,1]-ar[:,0])*ar[:,3])-1)<1e-9
 assert abs(np.sum((ar[:,1]-ar[:,0])*ar[:,4])-1)<1e-9
 return ar,ew,es,r

def F(t):
 if abs(t)<1e-30:return 0.
 return t*log(abs(t))-t

for p,Q,N in [(2,8,6),(3,16,6),(1.5,8,6),(4,32,6)]:
 ar,ew,es,r=build(p,Q,N); q=p/(p-1)
 # Independent exact double integrals for compressed commutator.
 C=np.zeros((N,N))
 for a,b,n,w,s,z in ar:
  n=int(n)
  if n==N:continue
  for c,d,m,v,t,u in ar:
   m=int(m)
   if m==N:continue
   integ=(F(b-c)-F(a-c)-F(b-d)+F(a-d))/pi
   val=(z-u)*integ
   assert val>=-1e-12
   C[n,m]+=val
 aw=1-ew; ass=1-es
 K=np.zeros_like(C); lower=np.zeros_like(C)
 for n in range(N):
  ln=(1-1/8)*(1/8)**n; wn=ew/(1-1/8)*(8*aw)**n
  for m in range(N):
   lm=(1-1/8)*(1/8)**m; sm=es/(1-1/8)*(8*ass)**m
   K[n,m]=(ln*wn)**(1/p)*sm/(lm*sm)**(1/p)*C[n,m]/ln
   lower[n,m]=r/(2*pi)*ew**(1/p)*es**(1/q)*sum(aw**((n-k)/p)*ass**((m-k)/q) for k in range(min(n,m)))
 assert np.all(K+1e-8>=lower)
 print('p=',p,'cells=',len(ar),'min positive-layer ratio=',np.min(K[lower>0]/lower[lower>0]))
print('Passed monotonicity, scalar mean preservation, positive exact H kernels, and all finite depth matrix lower bounds.')
for p in [1.5,2.,3.,4.]:
 q=p/(p-1)
 Q=max(100.,2**(p-1))
 ew=1/Q; es=Q**(-1/(p-1)); r=Q**(1/p)
 alpha=(1-ew)**(1/p); beta=(1-es)**(1/q)
 R=int(np.ceil(10*max(1/(1-alpha),1/(1-beta))))
 N=4*R
 inp=np.zeros(N); inp[R:3*R]=1
 upper=np.zeros(N)
 for k in range(N-2,-1,-1): upper[k]=beta*(inp[k+1]+upper[k+1])
 out=np.zeros(N)
 for n in range(1,N): out[n]=alpha*(upper[n-1]+out[n-1])
 out*=r/(2*pi)*ew**(1/p)*es**(1/q)
 ratio=np.linalg.norm(out,ord=p)/np.linalg.norm(inp,ord=p)
 target=Q**(1+1/(p*(p-1)))
 assert ratio/target>.1
 print('Toeplitz witness: p=',p,'N=',N,'norm / target=',ratio/target)
Path('workspace/agent1_cantor_checks.py').write_text(Path(__file__).read_text())
