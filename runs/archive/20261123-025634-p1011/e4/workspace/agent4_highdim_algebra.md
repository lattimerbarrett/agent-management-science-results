# Exact algebraic strict-minimum certificate (not a nonlinear PDE theorem)

Let d=n-1 and let H_2(z)=z^T Tz, tr(T)=0. Set
p(s)=1-2s/5+9s^2/200-9s^3/8000 and h(z)=H_2(z)p(|z|^2).
Consider the quadratic shape response Q(h)=<D f,DN^{-1} D f>, where
f=2h/(1+|z|^2), D=Delta_{S^{n-1}}+n-1, and DN is for Delta_{S^n}+n.
The constant/linear graph modes lie in the response kernel.

For boundary spherical harmonic degree L>=2,
mu_L=2 Gamma((L+n+1)/2) Gamma(L/2) /
       (Gamma((L-1)/2) Gamma((L+n)/2)).
This follows by separation with sin(theta)^L times the Gauss hypergeometric function
with parameters ((L-1)/2,(L+n)/2;L+n/2;sin(theta)^2), and continuation at 1.

For angular degree2 write L=j+2, a=(n+1)/2, alpha=(n+2)/2,
and D_L=(L-1)(L+n-1). Its radial coefficient polynomial for r^(2k) is
R2_k(D)=sum_{m=0}^k (-1)^(k-m) binom(k,m)
 prod_{r=0}^{m-1}(D+r(n-r))/(m! prod_{r=1}^m(a-r)).
Up to a common positive constant, its Gram matrix is the moment matrix
G2_kl=sum_{j>=0} W_j R2_k(D_L)R2_l(D_L), where
W_j=(j+alpha)[Gamma((j+3)/2)/Gamma((j+n+1)/2)]^2.
For angular degree3 the corresponding R3_k replaces m! by (m+1)!, and the
weight is (D_L-(n+1))W_j. For angular degree1 (constant graph mode killed),
R1_k(D)=2 sum_{m=1}^k (-1)^(k-m)binom(k,m)
 prod_{r=0}^{m-2}(D+(r+1)(n-1-r)) /
 ((m-1)! prod_{r=1}^{m-1}((n-1)/2-r)),
and the weight is D_L W_j/(n-1)^2.
These equalities follow from Jacobi Rodrigues integration by parts. The
cross-angular constants are included, not discarded.

The moments M_k=sum W_j D_L^k, k<=6, are evaluated by exact telescopers
Q_k(j,n) in agent3_telescopers.json:
(j+n-1)^2 Q_k(j)-(j+3)^2 Q_k(j+2)=(j+alpha)D_L^k.
Thus M_k=(n-1)^2 Q_k(0) Gamma(3/2)^2/Gamma((n+1)/2)^2
+n^2 Q_k(1)/Gamma((n+2)/2)^2. The tail vanishes for n>4+2k.
Consequently all required matrices are exact for n>16. After a common positive
factor is removed, entries are affine in
y=4 Gamma((n+1)/2)^2/(pi Gamma((n+2)/2)^2).
Gamma log-convexity gives 8/[pi(n+1)]<y<8/[pi n].

For x=lambda^2 let a(x)=(1,-2x/5,9x^2/200,-9x^3/8000).
The scale shape response is q(x)=x a(x)^T G2 a(x).
Agent3_alln_scale_check.py and agent3_alln_scale_strict_check.py prove exactly,
for every real n>=20, q'(.95)>0, q'(1.1)<0, and q''<0 on this interval.
Hence a unique strict scale maximum exists there.

For a T eigenvalue tau define rho=tau^2/tr(T^2). The translation Hessian
bracket is a(x)^T B_rho a(x), with d=n-1, c_k=1+2k/(d+2), and
B_kl=2(d+2)rho c_k c_l G1_kl
 +4[1/(d+4)+2d rho/((d+2)(d+4))]kl G3_(k-1,l-1)
 +l[2+8rho+4(1+4rho)(l-1)/(d+4)]G2_(k,l-1),
where absent negative indices give zero and B is symmetrized.
Agent4_alln_translation_checks.py proves this bracket strictly negative on
x in [.95,1.1], n>=20, and
rho in [(n-2)/(n(n-1)), n/((n-2)(n-1))].
It checks the two rho endpoints and two gamma-ratio endpoints. Each of the
seven Bernstein coefficients has, after sign reversal, a numerator and
denominator with strictly positive coefficients in n-20. This is an exact
finite polynomial certificate for all real n>=20, not a dimension scan.

Choose T diagonal: q repeated p times, -p repeated q times, where
p=floor(d/2), q=d-p. The two rho values belong to the certified interval.
Coordinate reflection symmetries force the translation gradient and all
mixed Hessians to vanish. Thus -Q has a strict full scale/translation
minimum in this quadratic model for every integer n>=20.

IMPORTANT LIMITATION: this proves only the quadratic finite-dimensional
algebra. A separate uniform Lyapunov-Schmidt construction and fixed-domain
iteration are needed to produce solutions. Moreover the same model admits
a rigorously certified strict minimum in dimension19 (agent3 certificate),
so it cannot be used as a proof of the requested dimension19 compactness.
