import sympy as s
from pathlib import Path
results=[]
for n in range(2,11):
 for q in range(1,n+1):
  # Full complex-negative core dimension q-1; remaining real-negative axes.
  ell=q-1
  rr=n-q+1
  H=s.diag(*([-2]*(2*ell)+[-2,4]*rr))
  # Interlaced real coordinates (x1,y1,...).
  lev=s.diag(*([s.Rational(-1)]*ell+[s.Rational(1,2)]*rr))
  for j in range(n):
   assert (H[2*j,2*j]+H[2*j+1,2*j+1])/4==lev[j,j]
  index=sum(int(bool(v<0)) for v in H.diagonal())
  assert index==n+q-1
  assert sum(int(bool(v>0)) for v in lev.diagonal())==n-q+1
  results.append((n,q,index))
text='''q-convex Morse index bound and sharp model. Let H be the real Hessian at a nondegenerate critical point in complex dimension n, and suppose its complex Levi form has at least p=n-q+1 positive eigenvalues. If E is H-negative of real dimension k, E intersect JE has real dimension at least 2k-2n and is J-invariant. The Levi form is negative on this complex subspace, since L(v)=1/4[H(v,v)+H(Jv,Jv)]. Thus its negative index is at least k-n whenever k>=n. Since positive index is at least p, negative index is at most n-p=q-1. Therefore k<=n+q-1. This bound is sharp for the quadratic model Q=-sum_{j<=q-1}|z_j|^2+sum_{j>=q}(-x_j^2+2y_j^2). Its full real Morse index is 2(q-1)+(n-q+1)=n+q-1; Levi has q-1 negative eigenvalues -1 and n-q+1 positive eigenvalues 1/2. The descending real core is C^(q-1) x R^(n-q+1). Its complement factors as C^(q-1) x (C^(n-q+1) minus R^(n-q+1)). For q<n the latter complex dimension is at least two. This identifies a plausible threshold for a relative Oka handle theorem; it DOES NOT establish such a theorem or assert model complements Oka without a verified source.\n'''
Path('workspace/agent3_qconvex_morse_models.txt').write_text(text)
print('PASS exact real/complex Hessian index checks for',len(results),'models')
print(text)
