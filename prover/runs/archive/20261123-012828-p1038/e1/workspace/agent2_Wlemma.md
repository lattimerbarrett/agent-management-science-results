# Strictly positive substochastic circulant W

Let r<R, d>0 and x,y>0 satisfy
r(x-x^{-1})-R(y-y^{-1})=2d.
Set K=d²+r²+R² and t=2Rr/(K+sqrt(K²-4R²r²)); thus 0<t<r/R<1.
On the annulus t<|z|<1/t take
s(z)=sqrt(K-Rr(z+z^{-1})), positive on the unit circle,
c(z)=(R/z-r)/(d+s(z)), b(z)=z c(z), and
W(z)=sqrt(ry/(Rx)) (1+x c(z))/(1+y b(z)).

**Claim.** Every Laurent coefficient of W on that annulus is strictly positive.
Consequently, sampling W on m-th roots of unity produces a circulant matrix with
strictly positive entries and row sum W(1)<1, for every m>=1.

## Proof
Put u=x/y. Substitution x=uy in the Joukowski equation gives
(ru-R)y²-2dy+(R-r/u)=0. Its discriminant is
4[K-Rr(u+u^{-1})]>=0, so t<=u<=1/t.

Write W=κ(s+A)/(s+B), κ=sqrt(ry/(Rx)),
A=d-rx+Rx/z, B=d+Ry-ryz. Then
A-B=(x-yz)(R/z-r), and direct algebra gives
z(s²-B²)=(r/x)(rz-R)(x-yz)(xyz+1).

All possible zeros of s+B away from cuts are removable in W.
Indeed 1+yb=0 and the quadratic spectral identity imply either c=x or c=-1/x.
The first would give z=-1/(xy)<0, impossible because c(z)<0 on the negative axis.
The second gives z=u and 1+xc=0. If u is in the open annulus, a zero of s+B
there is simple: the preceding cubic identity shows this unless u=R/r;
but at R/r we have s=d,B=d, so s+B=2d>0. Hence numerator cancels.
At a cut endpoint u=t or1/t, numerator and denominator have the same leading
square-root term, so their ratio remains bounded. These are harmless endpoint
singularities, not poles.

On the upper lip of the outer cut z>1/t, s=-iv, v>0, and
Im W=κ v(A-B)/(B²+v²)>0.
Here z>u and z>R/r, so both factors in A-B are negative.
On the upper lip of the inner cut 0<z<t, s=+iv and
Im W=-κ v(A-B)/(B²+v²)<0,
since now z<u and z<R/r.
At infinity W=O(z^{-1/2}); at zero W=O(z^{-1/2}).
Cauchy-contour deformation therefore gives, for Laurent coefficient w_j,

w_j=(1/π)∫_{1/t}^∞ Im W(v+i0) v^{-j-1}dv >0       (j>=0),
w_{-n}=-(1/π)∫_0^t Im W(v+i0) v^{n-1}dv >0       (n>=1).

The annular series converges absolutely on the unit circle. Discrete Fourier
coefficients are its periodizations, hence strictly positive. Their sum is W(1).
Finally the triangle-defect identity
(R/y)|1+yb_k|²-(r/x)|1+xc_k|²
=(1+|c_k|²)(s_B-s_A+s_k)>0
shows |W(ζ^k)|<1. Strictness holds because equality would put B_k on the segment
from the axis point to A_0, impossible since all points of that segment have
radial distance at most r<R. In particular 0<W(1)<1. ∎

Checks: `agent2_W_substochastic.py` verifies the rational polynomial identities
exactly and100 random sampled circulants at100 decimal digits. The analytic
argument, not those finite tests, establishes the all-m claim.

This lemma does NOT yet identify the full Atiyah determinant with a
substochastic-network determinant. That is still the essential missing step.
