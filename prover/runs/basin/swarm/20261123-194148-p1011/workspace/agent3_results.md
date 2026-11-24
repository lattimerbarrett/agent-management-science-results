# Agent 3: exact local shape analysis and explicit background

## Local source
In dimension n, m=n-1, on Omega_e={t>=eF(y)},
U=(1+|y|²+t²)^(-(n-2)/2) and outward normal (e grad F,-1)+O(e²).
The first Robin residual is
r_F=(n-2)U^(n/(n-2))[F-y.grad F+(1+|y|²)Delta F/(2(n-1))].
For F=H_l(y)|y|^(2q), Delta H_l=0, degree H_l=l, this is
(n-2)U^(n/(n-2)) H_l[A_q |y|^(2q-2)+B_q |y|^(2q)],
A_q=q(2q+n+2l-3)/(n-1), B_q=A_q+1-l-2q.

## Spectral diagonalization
Conformal transfer to a unit hemisphere gives Jacobi operator -Delta-n.
For equatorial spherical degree k, its Dirichlet-to-Neumann eigenvalue is
beta_k=2 Gamma((k+n+1)/2) Gamma(k/2)/(Gamma((k+n)/2) Gamma((k-1)/2)).
k=0 has inverse DN=0; k=1 is kernel, source orthogonal to it.
For k>=2 beta_k>0. The optimized shape Hessian is -1/2 times the
inverse-DN quadratic energy, since fixed ambient U energy has zero
first and second shape derivatives (first cancels, second vanishes by parity).

Set a=(n+2l-3)/2, alpha=a+1/2. After separating angular H_l and using
s=(1-r²)/(1+r²), source profiles are finite linear combinations of
(1+s)^(-p), p=l,...,l+q. Their Gegenbauer coefficients are beta integrals:
I_j(p)=(-1)^j 2^(2a-p+1) B(a+1,a-p+1)
        (p)_j (2a+1)_j / [j! (2a-p+2)_j].
h_j=pi 2^(1-2alpha) Gamma(j+2alpha)/[j!(j+alpha)Gamma(alpha)^2].
Thus C_pq=sum_j g_p(j)g_q(j) I_j(l)^2/(h_j beta_(j+l)).
All normalizations in the scripts follow these explicit formulas.

## All n>=33
For l=2, q=0,1, put C00,C01,C11 for inverse-DN shape coefficients.
Normalized source ratio S_j=2(j+2)(n+j)/(n-1)-3.
Writing w_j=I_j(2)^2/(h_j beta_(j+2)), normalized w0=1, gives
w_(j+2)/w_j=((j+3)/(j+n+1))² (2j+n+6)/(2j+n+2).
If z_j=w_j/(2j+n+2), polynomial telescoping computes all moments:
(j+n-1)^2 Q(j)-(j+3)^2 Q(j+2)=(2j+n+2)P(j),
sum w_jP(j)=(n-1)^2 Q(0)/(n+2)+r n²Q(1)/(n+4), r=w1/w0.
Here r<8(n+4)/(pi(n+1)^2)<400(n+4)/(157(n+1)^2).
The exact symbolic certificate agent3_all_n33.py proves
12 C00 C11-16 C01²<0 for all n>=33, using negative Bernstein
coefficients after n=x+33. Thus a=C01/C00,b=C11/C00 satisfy 4a²>3b.
For F=H2(1-r²), the scale minimum is at
z=lambda²=1/[2a+sqrt(4a²-3b)], so az<1/2.

## Translation stability all n>=33
Let H2=y^T A y, tr A=0, and rho=(A²)_aa/tr(A²) in [0,1].
For the absolute (not independently normalized) angular C matrices,
C^(1)_11=2(C01+C00)/(n-1),
C^(3)_00=((n-1)C01-(n+3)C00)/2.
These follow exactly from cross-angular weights, using K=k(k+n-2):
W1/W2=1/[K-(n-1)], W3/W2=(K-2n)/4.
The translation Hessian H(rho) is affine. Its endpoints obey
H(0)/(2zC00)=1+z-2(n+1)/(n+3) az > z+2/(n+3)>0,
H(1)/(2zC00)=5+z(1-16/(n-1))
 -2(5n²+8n+19)/((n-1)(n+3)) az
 >(n-17)[z/(n-1)+2/((n-1)(n+3))]>0.
All gamma and polynomial identities are checked in agent3_transall.py.
Scale Hessian is positive at the smaller simple root; mixed derivatives
vanish by parity. Thus a strict local shape minimum exists for every n>=33.

## Dimensions 19,...,32
Use radial polynomial P(s)=1-.46284 s+.05655 s²-.001408 s³.
agent3_finite_n.py uses exact rational moments and a Machin-certified
50-digit pi enclosure to prove negative dilation direction in all these n.
agent3_transcert.py finds the first scale root z in an interval of width
1e-7, checks the derivative signs and root nondegeneracy, and certifies
the entire translation Hessian positive, using outward interval arithmetic
and analytic infinite-tail bounds for the l=1,3 quadratic forms.
It runs in 10 seconds. Output is agent3_transcert_results.txt.

## Explicit flat-patch positive-type background
Let h(s)=0 for s<=1 and h(s)=(s-1)^2 exp(-1/(s-1)) for s>1.
Take Omega0={h(|y|²)+(t-1)²<=1}. It is smooth, compact, connected,
convex, with flat bottom/top boundary disks and curved boundary elsewhere.
Indeed h'>=0,h''>0 off the flat interval, Hess defining function>=0,
and gradient cannot vanish on level1. Mean curvature is nonnegative and
not identically zero, so Q(v)=int|grad v|²+2c_n int_boundary H v²
is coercive. Yamabe positivity persists under sufficiently small C² graph
perturbations. Put all bubble patches inside the exactly flat bottom disk.
This avoids background sphere-jet cancellation issues. The formula and
flat junction checks are in agent3_flat_base.py.

## Status
These are rigorous local algebra / geometric contributions, not a full
compactness theorem. The analytic reduction from arbitrary boundary
blowup (including clusters) to the jet dilation form is not proved here.
Do not claim the original problem solved solely from these calculations.

## Tail enclosure proof for agent3_transcert.py
For l=1,3 and j>=N, the weight excluding beta and the constant K is exactly
B(j)=(j+alpha) product_{r=1}^{l-1}(j+r)
 product_{r=n+l-1}^{n+2l-3}(j+r) / product_{r=l}^{n+l-2}(j+r).
Consequently B(j)<=j^(2l-n)(1+(n+2l)/N)^(2l-1).
Gamma logconvexity gives Gamma(x+1/2)/Gamma(x)>=x/sqrt(x+1/2)
>=sqrt(x/2) for x>=1/2. Applying this twice in beta_k gives
beta_k>=(k-1)/2, hence 1/beta_(j+l)<=2/j.
The code's exponent 3l-2 is at least 2l-1, so its Kw is safe.
Each source ratio is a product of explicit positive quadratic factors;
replacing (j+c) by j(1+c/N) gives the code's Kgs bounds.
Finally sum_{j>=N}j^(-E-1)<=(N-1)^(-E)/E for E>0.
Thus every entrywise interval really includes the complete infinite tail.
