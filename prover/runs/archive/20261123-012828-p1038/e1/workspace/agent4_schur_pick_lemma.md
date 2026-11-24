# A proved RHP Schur/Pick lemma for the physical m=1 cocycle

This does **not** identify the Atiyah determinant with the Pick kernel.

Fix r>0, 0<c<1, tau>0. For 0<=t<=tau put R_t=r exp(t),
d_t=(R_t-r)(1-c^2)/(2c), and
x(z)=r/(z+sqrt(z^2+r^2)), y_t(z)=R_t/(z+d_t+sqrt((z+d_t)^2+R_t^2)).
Square roots have positive real part for Re z>0. The map x sends the RHP
conformally to Omega={Re u>0, |u|<1}; the inverse is z=r(1/u-u)/2.

Writing J(u)=u-u^{-1}, we have
J(y_t)=exp(-t)J(x)+(1-exp(-t))J(c), so y_t stays in Omega.
Define phi(u)=(u-c)/(1+cu). Its logarithmic derivative along this flow is

    d_t log phi(y_t)=-(1+c^2)y_t/[c(1+y_t^2)].

The physical cocycle is the analytic nonzero function

    w_t(z)=sqrt(exp(-t)*y_t/x)*(1+cx)/(1+cy_t), w_0=1.

The quadratic identity gives w_t^2=phi(y_t)/phi(x), including the
removable case x=c. Thus w_t=exp(-integral_0^t h_v dv), where

    h_t(z)=(1+c^2)y_t/[2c(1+y_t^2)]
          =(1+c^2)R_t/[4c sqrt((z+d_t)^2+R_t^2)].

For Re z>0,

  1/sqrt((z+d)^2+R^2)
    = (1/pi) integral_{-R}^R du/[sqrt(R^2-u^2)*(z+d-iu)].

(The substitution u=R cos theta and the elementary Poisson integral prove
this; it also follows by analytic continuation from positive real z.)
Every integrand has positive real part, so Re h_t>0 and |w_t|<1.

More concretely, set C(z,w)=1/(z+conj(w)). For a=d-iu, d>=0,

 [(z+a)^(-1)+(conj(w)+conj(a))^(-1)]/(z+conj(w))
 = [1+2d*C(z,w)]/[(z+a)*(conj(w)+conj(a))].

This is a positive semidefinite kernel: the first summand is rank one,
and C is the Gram kernel integral_0^infinity exp(-v*z) exp(-v*conj(w))dv.
Integrating over u proves positivity of K_h=(h(z)+conj(h(w)))/(z+conj(w)).
Differentiating w_t(z)conj(w_t(w)) gives the exact identity

 K_{w_tau}(z,w) = [1-w_tau(z)conj(w_tau(w))]/[z+conj(w)]
                = integral_0^tau w_t(z)conj(w_t(w))*K_{h_t}(z,w)dt.

Thus the Pick kernel is PSD. It is strictly positive definite at any
finite set of distinct RHP points: a null quadratic form would force
sum_i a_i*w_t(z_i)/(z_i+d_t-iu)=0 for almost every u in an interval,
for almost every t, and hence identically as a rational function in u.
Distinct z_i give distinct poles; all residues, and hence all a_i, vanish.

Algebraic identities are checked in agent4_schur_semigroup.py.
