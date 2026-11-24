# Conditional reverse Lyapunov--Schmidt lemma in every dimension n>=3

This is a complete abstract implication under an explicit strong one-bubble
approximation hypothesis; it is NOT unrestricted blow-up extraction.

Let H=H1(M) have the coercive positive-Yamabe inner product E, with norm ||.||.
Set p=(n+2)/(n-2), q=p+1=2n/(n-2), kappa=n(n-2). Let S be the E-Riesz inverse
from L^(q/p) to H. Define
 T(u)=u-kappa S((u_+)^p), J'(u)[w]=E(T(u),w).

For each i let W_i(theta)>=0 be a C2 H-valued family on a fixed parameter
neighborhood D in R^n. Assume uniformly there:
 (i) ||W_i||+||d_theta W_i||+||d_theta^2 W_i||<=C;
 (ii) Z_ia=d_a W_i have Gram matrix G_iab=E(Z_ia,Z_ib) with eigenvalues in
      [g0,g1], 0<g0<=g1<infinity;
 (iii) for K_i=span{Z_ia}, the compressed operator
      P_i^perp A_i:K_i^perp->K_i^perp,
      A_iv=v-kappa p S(W_i^(p-1)v), has inverse norm <=C;
 (iv) eta_i=sup_D ||T(W_i)||->0.

Suppose exact solutions T(u_i)=0 satisfy
 d_i=||u_i-W_i(theta_i0)||->0,
where theta_i0 remain in a compact subset of D. Then for all large i there
are unique nearby theta_i and v_i such that
 u_i=W_i(theta_i)+v_i,  v_i perpendicular_E K_i(theta_i),
 |theta_i-theta_i0|<=C d_i,  ||v_i||<=C d_i.
In fact ||v_i||<=C||T(W_i(theta_i))||<=C eta_i, and v_i is exactly the unique
small projected LS correction at theta_i. Therefore u_i belongs to the
forward LS branch and its reduced energy has zero gradient at theta_i.

## Quantitative modulation
For fixed u_i define
 F_ia(theta)=E(u_i-W_i(theta),Z_ia(theta)).
At theta_i0, |F_i|<=C d_i, and
 d_b F_ia=-G_iab(theta)+E(u_i-W_i(theta),d_ab^2 W_i(theta)).
On a parameter ball of radius r about theta_i0, bounded first and second
derivatives imply
 ||dF_i(theta)+G_i(theta_i0)||<=C(d_i+r).
No modulus of continuity of a third derivative is used here: the Gram matrix
is Lipschitz by the bounded first/second derivatives, and the last displayed
error is bounded directly by ||u_i-W_i(theta)||<=d_i+Cr.

The map theta -> theta+G_i(theta_i0)^(-1)F_i(theta) is a contraction on a ball
of radius C0 d_i about theta_i0 for fixed large C0 and large i. Its displacement
at the center is O(d_i), and its Lipschitz constant is O(d_i). The contraction
principle gives the unique zero there and the parameter estimate. The H norm
of v_i is bounded by d_i+C|theta_i-theta_i0|. A fixed sufficiently small
parameter neighborhood has uniformly invertible derivative dF_i as well,
so local uniqueness is uniform.

## Nonlinear estimate in all dimensions
Write N(W,v)=(W+v)_+^p-W^p-pW^(p-1)v. For 1<p<=2,
 |N(W,v)|<=C|v|^p.
For p>=2,
 |N(W,v)|<=C(W^(p-2)|v|^2+|v|^p).
Holder, Sobolev and ||W||_q<=C give in either case
 ||S N(W,v)||<=C(||v||^2+||v||^p).
The Holder exponents are exact: 1/(q/p)=(p-2)/q+2/q in the p>=2 case.

There is likewise the all-p local Lipschitz bound
 ||S[N(W,v)-N(W,w)]||
 <=C[||v||+||w||+(||v||+||w||)^(p-1)]||v-w||.
For 1<p<=2 retain only the last term; for p>=2 use the bounded W^(p-2)
factor with Holder. Constants depend only on the uniform W bound and n.

## Reverse estimate and uniqueness
At the modulated parameter exactness and projection give
 P^perp A_i v_i=-P^perp T(W_i)+kappa P^perp S N(W_i,v_i).
By (iii),
 ||v_i||<=C||T(W_i)||+C(||v_i||^2+||v_i||^p).
Since ||v_i||->0, absorb the last terms to obtain ||v_i||<=2C||T(W_i)||.
The standard forward fixed-point map is a contraction on a ball C1 eta_i
for fixed large C1; the all-p Lipschitz estimate above proves this also for
3<=n<=5, where p>2. Thus v_i lies in that uniqueness ball for large i.
Alternatively two projected solutions of uniformly small norm have difference
bounded by a factor <1 times itself, proving local uniqueness directly.

The projected correction depends C1 on theta by the Banach-space IFT: the
critical Nemytskii map u -> (u_+)^p is C1:H->H*, and the derivative of the
projected equation at the small correction is an o(1) perturbation of the
uniformly invertible compressed A_i. Hence the reduced energy is C1.
For the actual u_i, J'(u_i)=0, so differentiating its branch parameterization
immediately yields zero reduced gradient.

Scope: proving d_i->0 for arbitrary blowing-up positive solutions is NOT done
here. Nor does this lemma supply the C1/Pohozaev expansion needed to exclude
critical points of the reduced energy at low-dimensional boundary jets.
