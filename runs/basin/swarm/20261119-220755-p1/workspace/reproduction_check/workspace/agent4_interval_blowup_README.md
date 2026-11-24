# Interval blowup field: formulas and guarantees

Implementation: `agent4_interval_blowup.py`.
Checks: `agent4_interval_blowup_checks.py` (RAN, all passed).

**Convention:** state is `(theta,w0,w1,w2,w3,Z0,Z1)` with theta POSITIVE;
the earlier shared `BlowupODE` instead uses h=-theta.

Parameters q1,q2,N are exact rationals passed as strings. Form
P6=prod(x-lambda), lambda=(-3,-1,0,1,2,3), Q2=(x-q1)(x-q2).
The exact eight real roots of P6 Q2+N are isolated by SymPy's exact rational
Sturm intervals, each of width <=10^(-floor(.302*bits)-20). The factor f uses
ordered indices 0,3,5,6; g uses 1,2,4,7. The negative outside eigenvalues are
ordered roots 1,6 of P6 Q2+2N. All roots are simple; the constructor asserts
these facts by exact isolation. Interval/ball coercions and every subsequent
arithmetic operation round outward. The construction works at both candidate
q1=-289/400 and the newer q1=-143/200; N=3/50,q2=17/10 by default.

Write d_i=P6'(lambda_i), H_i=lambda_i-theta and V_ij=lambda_i^j, j=0..3.
Then p_i=N H_i/(d_i f_i), p'_i=H_i f_i/d_i, and
M=V^T diag(p)V, Mp=V^T diag(p')V. Both M,Mp are affine in theta.
The first-order partner polynomial perturbation is dg=-Mp^(-1)M w and
D=deltaN=N sum_i p_i w_i/f_i. For the limiting two-cycle, f_i*g_i=N exactly;
for the negative nodes, f_mu*g_mu=-N exactly. The code uses these exact
identities to remove avoidable interval dependence.

The rational coefficient form is

 theta' = b(theta) w =: v,
 w' = w-K(theta) v^2 + Force(theta) Z,
 Z_mu' = Z_mu [2+L_mu(theta) w].

Here

 K= -N/(4P6(theta)) M^(-1) (1,theta,theta^2,theta^3)^T,
 Force_mu=-4 f_mu M^(-1) (1,mu,mu^2,mu^3)^T,
 L_mu w=2[w(mu)/f_mu+dg(mu)/g_mu]-2D/N,
 b_j=2theta/N [g(0)*1_(j=0)+f(0)*DG_(0,j)-D_j], DG=-Mp^(-1)M.

The b formula evaluates theta'=-2H_i*ratio_i at the base node lambda_i=0,
where ratio_i=(g_i*w_i+f_i*dg_i-D)/N. All six nodal values agree exactly
(the first-order dual polynomial is monic linear). For K, use
sum_i lambda_i^j/[d_i(lambda_i-theta)]=-theta^j/P6(theta), j<=4;
this follows from partial fractions of z^j/P6(z).

## No interval matrix inversions at runtime

The Christoffel determinant identities are

 det M(theta)=c*f(theta), det Mp(theta)=cp*g(theta),

where c,cp are the degree-four leading determinant coefficients. They follow
by applying the Christoffel determinant formula to the signed base weights
1/(d_i f_i) and f_i/d_i. The associated degree-four monic orthogonal polynomials
are f and g, as checked directly by Lagrange interpolation. Both are polynomial
identities and remain valid without any positivity assumption on those signed
auxiliary weights. The code also computes all determinant coefficients by
permutation expansion and asserts every coefficient difference encloses zero.

Adjugate entries are polynomials of degree <=3. All numerators for b,K,Force,L
are precomputed and combined algebraically BEFORE interval/PS evaluation:

 b=nb/g(theta), K=nK/[f(theta)P6(theta)],
 Force=nForce/f(theta), L=nL/g(theta).

`coefficient_formulas(theta)` accepts a generic ring scalar, including power
series over RBF/RIF. `field_generic(y)` never coerces the input scalars.
`field_jac_hess(y)` computes first and second derivatives by univariate Jet2
coefficient differentiation, followed by the explicit polynomial-in-(w,Z)
chain rule. It works for interval/ball boxes and for PS scalars alike.

`transformed(W,Zscale)` returns the field with original w=W*wnew and
original Z=Zscale*Znew; theta is unchanged. The rational polynomial numerators
are combined with W and W^(-1) ONCE, before evaluating any uncertain theta.
This is important for interval Taylor conditioning. The same transformed object
provides full interval field/Jacobian/Hessian and generic PS evaluation.

## Independent checks performed

* Interval and ball arithmetic both tested at five phases, three independent
  integer directional Taylor seeds per phase: generic multivariate PS field
  coefficients agree with explicit analytic F, J*d, (d^T H d)/2, with every
  difference interval containing zero.
* Twenty random corners of a genuine box were enclosed componentwise by its
  field, Jacobian, and Hessian interval evaluations.
* Original field agrees with shared independently-coded double formulas to
  3.2e-11 at a sample phase.
* With agent2's exact-ball whitening W,Zscale, transformed field agrees with
  independently-coded WhiteGenericField to 5.7e-82 at 300 bits.
* Dynamical order16 Taylor jets in transformed coordinates took .029 seconds;
  coefficient radii were ~8e-73 at order1 and ~6e-46 at order16 (300 bits).

These are finite implementation checks, NOT the periodic-orbit interval
existence certificate, which is a separate computation owned by agent2.
