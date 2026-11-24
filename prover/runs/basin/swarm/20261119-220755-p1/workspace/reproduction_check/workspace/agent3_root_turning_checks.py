import numpy as np
from pathlib import Path
rng=np.random.default_rng(872)
def op(q,x,t):
 V=x[:,None]**np.arange(t);c=np.linalg.solve(V.T@(q[:,None]*V),-V.T@(q*x**t));return np.r_[1,c[::-1]]
checks=0
for n,t in [(6,2),(9,3),(12,4)]:
 x=np.linspace(-1,1,n)
 for trial in range(300):
  q=rng.uniform(.1,2,n);H=op(q,x,t);rr=np.sort(np.roots(H).real);alpha=rr[0];j=np.searchsorted(x,alpha);a=rng.uniform(x[j-1]+1e-7,alpha)
  roots=rr.copy();roots[0]=a;g=np.poly(roots);weights=q*(np.polyval(H,x)/np.polyval(g,x))**2;l=op(weights,x,t);new=np.sort(np.roots(l).real)[0]
  assert new<=a+1e-7
  S=np.sum(q*np.polyval(H,x)**2/(x-a));R=np.sum(q*x*np.polyval(H,x)**2/(x-a)**2)/np.sum(q*np.polyval(H,x)**2/(x-a)**2)
  assert S<1e-6 and new<=R+1e-7 and R<=a+1e-7
  checks+=1
print(checks,'exact-root-turning numerical tests passed')
