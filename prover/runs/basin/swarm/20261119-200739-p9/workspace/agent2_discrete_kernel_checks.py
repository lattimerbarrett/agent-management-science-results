from pathlib import Path
import numpy as np
from scipy.integrate import quad

def cell_kernel(k):
 if k==0:return 0.
 def f(t):return 0. if t==0 else t*np.log(abs(t))
 return (f(k+1)+f(k-1)-2*f(k))/np.pi
err=0.
for k in list(range(-20,0))+list(range(1,21)):
 numerical=quad(lambda t:np.log(abs(k+t))-np.log(abs(k+t-1)),0,1,epsabs=1e-12)[0]/np.pi
 err=max(err,abs(numerical-cell_kernel(k)))
 assert abs(numerical-cell_kernel(k))<1e-11
 assert abs(cell_kernel(k)+cell_kernel(-k))<1e-14
print('Exact cell-kernel formula checked against40actual numerical integrals; maxerror=',err)
Path('workspace/agent2_discrete_embedding.md').write_text(r'''# Rigorous embedding of uniform-cell discrete models

Let W be constant on each unit cell and let its arbitrary invertible roots be M_i. For vector step functions h(x)=h_i on celli, averaging Hh on cellj gives exactly sum_i K_{j-i}h_i, where
K_k=((k+1)log|k+1|+(k-1)log|k-1|-2klog|k|)/pi, k!=0,
K_0=0, and 0log0=0.
This follows by integrating first in y, then in x; the diagonal double principal-value integral vanishes by antisymmetry. Conditional averaging on cells is an Lp contraction after multiplying by constant M_j. Consequently the weighted finite-matrix operator norm of (M_j K_{j-i} M_i^-1) is a LOWER bound for the continuum weighted Hilbert norm (restricting input/output to the chosen finite cells only). Step inputs can be smoothed with convergence of input norm and truncated-output pairings; for finite-valued positive weights this also follows immediately from ordinary unweighted Lp convergence and global bounded ellipticity.

The full real-interval matrixAp characteristic of a unit-cell-constant weight is at most 3^p times the supremum over grid-aligned intervals. If |I|>=1, its smallest grid coverJ has |J|<=3|I|; positivity of the two integrals gives A_I<=(|J|/|I|)^p A_J. If |I|<1 it meets at most two neighboring cells. Its probability distribution on those two values is pointwise dominated by twice their equal-mixture distribution, so A_I<=2^p A_union. Thus grid-aligned evaluation is quantitatively sufficient, not merely a heuristic, for uniform cells. If the weight is constant outside N cells, intervals with farther-out endpoints may also be reduced up to a factor2^p to intervals padded by at most N additional constant cells (compare their inside/outside mixture to the equal mixture). This allows a finite rigorous search, subject to certified optimization and control of all matrix powers.

This supplies exact computational infrastructure; it does not by itself prove a sharp asymptotic lower bound.
''')
Path('workspace/agent2_discrete_kernel_checks.py').write_text(Path(__file__).read_text())