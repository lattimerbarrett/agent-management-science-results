# Conditional nonlinear Lyapunov--Schmidt completion (agent 1)

SCOPE: This is a complete abstract implication once the residual, inverse, and
reduced-energy hypotheses below hold. It does NOT provide the dimension-18
seed or its reduced-energy expansion.

Let n>=6, p=(n+2)/(n-2), kappa=n(n-2), and let H=H1(M) have the coercive inner
product E determined by the positive-Yamabe Robin quadratic form. Write S for
the E-Riesz solution operator, so E(Sf,w)=int f w. Sobolev gives boundedness
S:L^(2n/(n+2))->H. Let W_i(theta)>=0 be smooth ordinary cutoff boundary bubbles,
theta in a fixed compact ball D in R^n, with scales delta_i comparable uniformly
to some delta_i^0->0. Assume uniformly on D:

(A) ||W_i||_H<=C and eta_i=sup ||W_i-kappa S(W_i^p)||_H ->0.
(B) K_i(theta) has a C1 E-orthonormal frame z_1,...,z_n, with uniformly bounded
    parameter derivatives. The matrix M_ba=E(partial_theta_b W_i,z_a) has
    uniformly bounded inverse. The partial derivatives of W_i lie in K_i.
(C) P_i^perp A_i restricted to K_i^perp has uniformly bounded inverse, where
    A_i v=v-kappa p S(W_i^(p-1)v).

Parameters are taken in bubble-scaled coordinates. For ordinary cutoff bubbles
(B) follows from rescaled Jacobi Gram convergence; (C) is proved in
workspace/agent4_projected_inverse_lemma.md. We keep (A)-(C) explicit rather
than silently asserting them for arbitrary moving-domain seeds.

## Nonlinear correction
Because 1<p<=2, the pointwise inequalities
 |(a+b)_+^p-a^p-p a^(p-1)b| <= C_p |b|^p,
 |N(a,b)-N(a,c)| <= C_p (|b|+|c|)^(p-1)|b-c|
hold for a>=0. The second follows by integrating the derivative and using
Holder continuity of x->p(x_+)^(p-1). Holder and Sobolev, with
p*[2n/(n+2)]=2n/(n-2), imply
 ||S N(W,v)||_H<=C||v||_H^p,
 ||S(N(W,v)-N(W,w))||_H
   <=C (||v||_H+||w||_H)^(p-1)||v-w||_H.

On K_i^perp the projected equation for u=W_i+v is equivalent to
 v=-(P_i^perp A_i)^(-1) P_i^perp[W_i-kappa S(W_i^p)]
   +kappa (P_i^perp A_i)^(-1) P_i^perp S N(W_i,v).
For fixed sufficiently large C0, the ball ||v||<=C0 eta_i is invariant and the
right-hand side has Lipschitz constant O(eta_i^(p-1))<1/2. The contraction
mapping theorem gives a unique v_i(theta) in this ball. After trivializing the
C1 family of orthogonal complements, the C1 implicit-function theorem applies:
the derivative in v differs from P_i^perp A_i in norm by O(eta_i^(p-1)). Thus
v_i is C1 in theta.

## Reduced minimum gives an exact solution
Define
 J(u)=E(u,u)/2-kappa/(p+1) int_M(u_+)^(p+1),
 j_i(theta)=J(W_i(theta)+v_i(theta)).
The projected equation says the E-gradient of J is sum_a c_a z_a. Differentiating
E(v_i,z_a)=0 gives E(partial_b v_i,z_a)=-E(v_i,partial_b z_a)=O(eta_i), so

 partial_b j_i=sum_a c_a[M_ba+O(eta_i)].

The bracketed matrix is invertible for large i. Consequently an interior
critical point of j_i gives c_a=0 for every a, hence the full weak equation
 -L_g u=kappa(u_+)^p, B_g u=0.

Suppose additionally that, uniformly on D,
 j_i(theta)=C_i+A_i F(theta)+o(A_i), A_i>0,
and F(theta0)+gamma<=inf_boundaryD F for some theta0 in interior D and gamma>0.
For large i the uniform remainder is less than gamma A_i/3. A minimum of j_i
on compact D is therefore attained in its interior and is a critical point.
Only this C0 expansion is needed; no derivative expansion is assumed.

## Positivity and smoothness
Testing the exact weak equation with u_-=max(-u,0) gives -E(u_-,u_-)=0, because
the right-hand side vanishes there. Coercivity gives u_-=0. Since ||v_i||_H->0
and W_i has a fixed positive critical Lp mass, u_i is not identically zero.
Brezis--Kato iteration applies to -Delta u=(kappa u^(p-1)-cR)u, whose
coefficient belongs to L^(n/2); the Robin coefficient is smooth. It gives
u in every finite Lq, then elliptic boundary regularity gives C1 and bootstrap.
The strong maximum principle gives u>0 in the interior. If u vanished at a
boundary point, the Hopf lemma would give a strictly negative outward normal
derivative, contradicting B_g u=0 there. Hence u>0 on the compact closure.
Its positive minimum makes u^p smooth, and full bootstrap gives C-infinity.
(The regularity invoked here is the standard elliptic Brezis--Kato/Robin
regularity theorem, not a dimensional blow-up compactness assertion.)

## Boundary blow-up requires no pointwise correction estimate
Let q_b=2(n-1)/(n-2), the critical boundary trace exponent. The trace theorem
and ||v_i||_H->0 imply ||v_i||_L^q_b(boundary)->0. On a boundary cap C_i of
radius R delta_i centered at the bubble, the exact bubble scaling gives
 ||W_i||_L^q_b(C_i)>=c_R>0 for fixed R>0, while |C_i|<=C delta_i^(n-1).
The triangle inequality therefore gives ||u_i||_L^q_b(C_i)>=c_R/2. Hence

 max_boundary u_i >=(c_R/2)|C_i|^(-1/q_b)
                  >=c delta_i^(-(n-2)/2)->infinity.

Thus an actual strict-minimum reduced-energy expansion, together with (A)-(C),
produces exactly the positive smooth boundary-blowing-up solutions requested.
The unproved central input is the seed/expansion at ambient dimension18.


## Ordinary cutoff bubbles satisfy the small-residual hypothesis
For a fixed smooth metric choose boundary flattening coordinates orthonormal at
the bubble center, a fixed chart cutoff chi, and W_delta=chi U_delta. The weak
residual is a functional on H1. Split its support into |x|<=R delta and its
complement. On the first set, rescaling makes metric coefficients and volume
and boundary Jacobians converge uniformly to Euclidean ones. The Euclidean
bubble weak identity cancels the leading terms. Their differences are bounded
by o_delta(1) times ||v||_H, for fixed R, using the bubble's uniformly bounded
D1,2 and critical Lp norms. On the complement, Holder bounds all gradient and
nonlinear contributions by the corresponding Euclidean bubble tails, which
tend to zero as R->infinity. Derivatives of chi are supported in a fixed annulus,
where U_delta and its derivatives tend to zero uniformly. The R term tends to
zero in H^{-1}, since W_delta converges strongly to zero in L^(2n/(n+2)); this
follows from bounded critical norm, pointwise convergence off the center, and
uniform integrability in every strictly lower exponent. The Robin H term is
handled the same way using the boundary trace exponent and its conjugate.
Therefore ||W_delta-kappa S(W_delta^p)||_H->0. All estimates are uniform over
bubble-scaled parameters in a fixed compact set. The same argument with Jacobi
fields and the linearized Euclidean identity gives ||A_delta Z_delta,a||_H->0.

This establishes only a qualitative residual o(1), sufficient for the abstract
correction but NOT the much finer energy remainder relative to the tiny
multi-scale gain. Those refined estimates remain part of the missing seed
expansion theorem.
