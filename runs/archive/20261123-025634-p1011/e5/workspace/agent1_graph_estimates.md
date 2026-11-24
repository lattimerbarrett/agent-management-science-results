# Exact graph source and direct-energy estimates (agent 1)

Let n>2D, D>=2, let h be a polynomial of degree at most D, and assume
|D^j h(x)|<=C(1+|x|)^{D-j} for j=0,1,2. Set h_R=chi(x/R)h,
where chi is fixed, smooth, equals one on the unit ball and vanishes outside
the ball of radius two. Constants below are independent of R>=1. Put
U(x,z)=(1+|x|^2+z^2)^(-(n-2)/2), Omega_t={z>t h_R(x)}.
Let s=C|t|R^{D-1} and assume s<=1/10. The physical bubble is U restricted
to Omega_t (not U composed with a graph straightener).

## 1. Boundary residual
With upward graph and outward normal (t Dh_R,-1)/sqrt(1+t^2|Dh_R|^2),

(B_{Omega_t} U)dS = [t Dh_R.grad_x U(x,th_R)-U_z(x,th_R)
 +2c_n {t Delta h_R-t^3 Hess h_R(Dh_R,Dh_R)/(1+t^2|Dh_R|^2)}
 U(x,th_R)] dx.

Hence its first coefficient is

A_h=(n-2)U(x,0)[(h-x.grad h)/(1+|x|^2)+Delta h/(2(n-1))].

The remainder after subtracting t A_{h_R} is pointwise at most
C s^2 |t| (1+r)^{D-n}. Indeed |th_R|/(1+r)<=Cs, |tDh_R|<=Cs,
and evaluating U or its tangential first derivative at z=th_R changes it
by relative O(s^2); the odd normal derivative has the same relative bound
after division by th_R. The cubic graph-curvature term is bounded using
|tDh_R|^2<=Cs^2.

Let q=2(n-1)/n, the dual critical trace exponent. Then
integral_1^infinity r^{q(D-n)+n-2} dr<infinity iff n>2D.
Consequently ||residual-t A_{h_R}||_{L^q}<=Cs^2 |t|, and
||A_{h_R}-A_h||_{L^q} tends to zero as R tends to infinity.
These also hold in the dual homogeneous H^1 norm by the trace inequality.

## 2. Exact cancellation of the first two direct energy terms
Use
J_Omega(v)=1/2 integral_Omega |grad v|^2
 +c_n integral_boundary H v^2
 -(n-2)^2/2 integral_Omega v^{2n/(n-2)}.
At z=0, with e=|grad U|^2/2-(n-2)^2 U^{2n/(n-2)}/2,

e(x,0)=(n-2)^2/2 (r^2-1)(1+r^2)^(-n)
       =c_n Delta_x(U(x,0)^2).

Thus integration by parts cancels the linear coefficient exactly:
-integral h_R e(x,0)+c_n integral Delta h_R U(x,0)^2=0.
The full difference J_{Omega_t}(U)-J_{Omega_0}(U) is odd in t:
the volume layer integrates an even density in z, and H dS is odd while
U(x,th_R)^2 is even. Therefore its quadratic coefficient is zero.

More quantitatively the exact difference is

-integral_x integral_0^{th_R} e(x,z) dz dx
+c_n t integral_x [Delta h_R-
 t^2 Hess h_R(Dh_R,Dh_R)/(1+t^2|Dh_R|^2)] U(x,th_R)^2 dx.

After the linear cancellation every remaining term is bounded by
C |t|^3 (1+r)^{3D-2n}. For example the volume term uses
|partial_z^2 e(x,z)|<=C(1+r)^(-2n), and the boundary terms use
|partial_z^2(U^2)(x,z)|<=C(1+r)^{2-2n}. Since
|t|(1+r)^{D-1}<=Cs on the support, this is at most
Cs t^2 (1+r)^{2D+1-2n}. Integrating over R^{n-1} gives

|J_{Omega_t}(U)-J_{Omega_0}(U)|
 <=Cs t^2 integral_0^infinity (1+r)^{2D-n-1}dr <=C' s t^2.

The displayed radial integral converges exactly for n>2D.

## 3. Straightener and quadratic forms
F_t(x,z)=(x,z+t h_R(x)) has determinant one. Its pullback metric has
inverse entries g^{ij}=delta_ij, g^{in}=-t h_i, g^{nn}=1+t^2|Dh_R|^2.
Thus the pulled-back gradient quadratic form is explicitly

integral [|grad_x v|^2-2t Dh_R.grad_x v v_z
 +(1+t^2|Dh_R|^2)v_z^2].

The boundary form has H dS as above. Its perturbation norm is O(s), since
||t D^2h_R||_{L^{n-1}(R^{n-1})}<=C|t|R^{D-1}=O(s)
and the critical trace inequality controls boundary v^2.
The physical bubble pulls back to U composed with F_t, and
(U composed with F_t-U)/t tends to h U_z in homogeneous H^1 as
R tends to infinity and s tends to zero. A dominated bound is
|grad(h U_z)|<=C(1+|(x,z)|)^{D-n}, square-integrable for n>2D.

## Scope
These are local graph estimates, NOT by themselves an existence theorem.
They apply equally to D=6,n=21 and D=8,n=19. Thus they do not resolve the
team's discrepancy with the asserted sharp dimension 21.
