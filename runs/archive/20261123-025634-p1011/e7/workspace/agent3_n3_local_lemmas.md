# Two quantitative lemmas for dimension-three boundary blow-up

These are local results, not a proof of compactness. The missing global step is selection/exclusion of clusters and proof that arbitrary blow-up points are isolated simple.

## 1. A bounded first boundary correction

Let H={t>0} in R^3, U=(1+|x|^2)^(-1/2), and let f(z) be a tracefree quadratic polynomial in z=(x1,x2). There is a smooth function Phi on the closed halfspace satisfying

    (Delta+15 U^4)Phi=0,   Phi_t(z,0)=-f(z)/(1+|z|^2)^(3/2),

with

    |Phi(x)| <= C ||D^2 f||,
    |DPhi(x)| <= C ||D^2 f||/(1+|x|),
    Phi(0)=0, DPhi(0)=0.

More precisely Phi=q+O(|x|^-1), DPhi=Dq+O(|x|^-2) at infinity, where

    q=f(z)/(2(r+t)^2).

### Construction and proof

It suffices to treat f=(x1^2-x2^2)/2 or f=x1*x2 and then take linear combinations. These lie in the azimuthal Fourier mode m=2 for rotations of (x1,x2). The explicit q is harmonic, degree zero, has q_t=-f/|z|^3 on t=0, and obeys |D^k q|<=C r^-k for r>0. Let Q=chi(r)q, with chi=0 on r<1 and chi=1 on r>2. Put L=Delta+15U^4. Seek Phi=Q+eta with eta in D^{1,2}(H), still in mode m=2. Its weak equation is

    B(eta,psi)= int_H LQ psi + int_{t=0} (Q_t+f/(1+|z|^2)^(3/2)) psi,
    B(eta,psi)=int_H Deta.Dpsi -15 int_H U^4 eta psi.

The interior forcing is smooth and O(r^-4). The boundary forcing is smooth and O(r^-3), since

    (1+r^2)^(-3/2)-r^-3= -3/(2r^5)+O(r^-7).

Thus they belong to L^{6/5}(H) and L^{4/3}(partial H), respectively, giving a bounded linear functional on D^{1,2} by Sobolev and trace inequalities.

The form B is coercive on azimuthal mode m=2, with explicit constant 4/7 relative to the Dirichlet norm. Indeed, set eta=U w and use gS=U^4 delta, the hemisphere of radius 1/2. The conformal energy identity gives

    int |Deta|^2 = int_S (|D_S w|^2+3w^2),
    B(eta,eta)=int_S (|D_S w|^2-12w^2).

Even reflection across the equator and the azimuthal m=2 condition exclude spherical harmonics of degrees 0 and 1. The next eigenvalue is 4*2*(2+2)=32. Hence

    B(eta,eta) >= (4/7) int |Deta|^2.

Lax-Milgram therefore gives a unique eta in this mode, with Dirichlet norm bounded by C||D^2 f||. Ordinary local boundary elliptic regularity makes eta smooth.

For completeness, the pointwise bounds do not follow merely from its energy norm. On an annulus of radius R>=4, rescale to unit size. Interior and Neumann boundary L-infinity estimates give

    sup_{r~R}|eta| <= C R^(-1/2)||eta||_{L^6(r~R)} + C R^-2 <= C R^-1/2.

Here the rescaled potential is O(R^-2), the interior forcing is O(R^-4), and the Neumann forcing is O(R^-3). Consequently 15U^4 eta=O(R^-9/2). The Neumann Newton representation for eta has volume source O((1+r)^-4) and boundary source O((1+r)^-3), both integrable. Splitting each potential into |y|<R/2, |x-y|<R/2, and the remaining exterior gives |eta(x)|<=C/R. The difference between eta and this potential is a homogeneous Neumann harmonic function in D^{1,2}, and is zero by testing against itself. Rescaled boundary gradient estimates now give |Deta|<=C/R^2. These estimates, combined with Q, prove all assertions. Mode m=2 forces the value and all first derivatives of Phi at the origin to vanish.

## 2. Isolated-simple decay from a one-dimensional argument

Consider positive solutions of

    Delta_g u_i -c_3 R_g u_i+3u_i^5=0,   B_g u_i=0,

near boundary points p_i -> p, with M_i=u_i(p_i)->infinity and epsilon_i=M_i^-2. Assume p_i are local boundary maxima. Assume:

(a) isolated blow-up: u_i(x)<=C dist(x,p_i)^(-1/2) in a fixed neighborhood;

(b) local bubble convergence: M_i^-1 u_i(F_i(epsilon_i y)) -> U(y) locally in C^2 on the halfspace;

(c) simplicity: in boundary Fermi coordinates (after a smooth fixed conformal normalization H=0), r^(1/2) times the Euclidean spherical average of the even reflection of u_i has exactly one critical point on (0,delta), for fixed sufficiently small delta.

Then

    u_i(x)<=C_delta M_i^-1 dist(x,p_i)^-1,

for epsilon_i<=dist(x,p_i)<=delta. The same bound, with the usual bubble expression, holds down to distance zero.

### Proof

Conformal normalization to H=0 is available from the positive principal eigenfunction; this changes all distance and height constants by bounded factors. In Fermi coordinates even-reflect u_i across t=0. The reflected metric is uniformly Lipschitz, g^{jk}=delta^{jk}+O(r), and its first derivatives are bounded. Annular rescaling, (a), Moser Harnack, and boundary Schauder estimates imply

    sup_{r/2<|x|<2r} u_i <= C inf_{r/2<|x|<2r}u_i,
    |D^k u_i|<=C r^-k A_i(r),   k=1,2,

where A_i(r) is its Euclidean spherical average. All constants are uniform. In the original smooth halfspace these derivative estimates are ordinary Neumann boundary estimates; even reflection preserves the needed second derivative bounds.

Writing the equation with Euclidean principal part and averaging gives

    A_i''+2r^-1 A_i' = -a_i(r) A_i^5 + E_i(r),
    3<=a_i(r)<=C,   |E_i(r)|<=C A_i(r)/r.

Indeed a_i=3 average(u_i^5)/A_i^5, controlled above by annular Harnack and below by Jensen. The metric error is bounded by O(r)|D^2u_i|+O(1)|Du_i|+O(1)u_i, hence by C A_i/r.

Set t=log r and v_i(t)=r^(1/2)A_i(r). Then

    v_i''=(1/4-a_i(t)v_i^4+e_i(t))v_i,  |e_i(t)|<=C exp(t).

Fix R large. By (b), v_i(log(R epsilon_i)) is as small as desired, and its derivative is negative. By simplicity it remains strictly decreasing until T=log delta. Choose R large and delta small so that the coefficient in the last ODE is at least kappa^2, with kappa=1/4. Backward comparison, using v_i'>= -infinity and v_i'<=0, yields for t<=s<=T

    v_i(s)<=2v_i(t) exp(-kappa(s-t)).

(The comparison is v_i(t)>=v_i(s)cosh(kappa(s-t)) -v_i'(s)sinh(kappa(s-t))/kappa.)

Put z_i=v_i'+v_i/2. Its equation is

    z_i'-z_i/2=-a_i v_i^5+e_i v_i.

Integrating backwards from T and using z_i(T)<=v_i(T)/2 gives

    z_i(t)/v_i(t) <= C exp(-(1/2+kappa)(T-t))
                        +C v_i(t)^4
                        +C delta^(1/2-kappa) exp((1/2+kappa)t).

For the middle term use the backward exponential comparison under the integral. For the last term integrate exp(-(s-t)/2)*exp(s)*v_i(s)/v_i(t). Each term has a uniformly bounded integral in t from t0=log(R epsilon_i) to T: the middle one by the preliminary exponential decay, the last one by O(delta). Therefore

    log(v_i(t)/v_i(t0)) = -(t-t0)/2+int_{t0}^t z_i/v_i
                         <= -(t-t0)/2+C.

Since v_i(t0) is bounded independently of i, this gives A_i(r)<=C epsilon_i^(1/2)/r=C M_i^-1/r. Annular Harnack upgrades the averaged estimate to the pointwise estimate. Local bubble convergence handles r<=R epsilon_i.

This lemma does not establish assumptions (a) or (c) for an arbitrary blow-up sequence.
