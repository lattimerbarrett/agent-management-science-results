# Spectral boundary-shape lemma and exact n=19 full-maximum certificate

This document supplies the complete analytic normalization and the finite exact
arithmetic certificate behind agent4's contribution. It does NOT by itself
assert compactness or noncompactness of the original PDE. The connection to
solutions on one fixed domain requires the separate analytic reduction and
diagonal lemmas.

## 1. Conventions and functional

Let D=S^n_+ have the UNIT round metric, Sigma=S^(n-1), R=n(n-1),
m=n-1, a=4(n-1)/(n-2), q=2n/(n-2). The normal points out of D.
Consider the unconstrained action

 J_D(w)=int_D [a|grad w|^2/2 + R w^2/2 - R(w_+)^q/q]
                  + int_Sigma H w^2.                    (1)

Its Euler equation is -a Delta w+Rw=R(w_+)^(q-1),
a partial_nu w+2Hw=0. Thus w=1 is critical on D. The interior Hessian
at1 is a(-Delta-n), and its quadratic form is

 A(v,z)=int_D (grad v.grad z-nvz).                       (2)

The Neumann kernel K is spanned by the restrictions of x_1,...,x_n,
the coordinate functions tangent to the equator in R^(n+1). Indeed the
Neumann spectrum is obtained by even reflection across the equator from the
round-sphere eigenvalues k(k+n-1). Constants have negative, but nonzero,
Hessian eigenvalue. On the L2-orthogonal complement of K, the Hessian has
a bounded inverse H1 -> (H1)*. This follows from its spectral decomposition,
or the coercivity of -Delta+1 plus a finite-rank spectral correction.

Let D_t be the normal graph t f over Sigma and pull functions back using any
smooth extension of the boundary deformation. Since1 is constant, the
first-order conformal variation is unambiguously w_t=1+t v+O(t^2).
The trace mean-curvature derivative is

 H'[f]=-(Delta_Sigma+m)f =: T f.                         (3)

For example the constant normal graph is a parallel latitude; its mean
curvature derivative is -m, verifying the sign with the stated outward normal.

## 2. Exact joint second variation

For w=1, equation(1) becomes

 J_Dt(1)=(R/n)Vol(D_t)+int_boundary(D_t) H_t.

The first variation is (R/n)int f + int Tf=0, since R/n=m.
Reflection in the equator maps D_t to the complement of D_-t. Thus both
Vol(D_t)-Vol(D) and int H_t are odd functions of t. Their second derivatives
are zero. In particular the pure-domain second variation is zero for EVERY
smooth f, not only volume-preserving f.

The first w-variation at1 on D_t is only the boundary term
2int H_t z: the interior Euler expression vanishes identically on every
round subdomain. Consequently the mixed derivative is 2int (Tf)z.
The w-w second derivative is a A(v,v). Combining the three Hessian blocks,

 d^2/dt^2 J_Dt(1+t v)|_0 = a A(v,v)+4int_Sigma (Tf)v.    (4)

This calculation does not impose a volume constraint, and therefore does
not discard or incorrectly minimize over the negative constant conformal mode.

The projected first-order correction v=v_f is characterized by

 A(v,z)=-(2/a)int_Sigma (Tf)z, z in K-perp.              (5)

The right side annihilates K because the boundary trace of K is exactly the
degree1 equatorial harmonics and T annihilates degree1. Thus(5) is also valid
for all z in H1 after fixing v perpendicular to K. Equivalently

 (Delta+n)v=0 in D, partial_nu v=-(2/a)Tf on Sigma.       (6)

Substituting(5) in(4) gives J''=-a A(v,v).

## 3. Boundary Dirichlet-to-Neumann eigenvalues

For a boundary spherical harmonic Y_L of degree L>=2, use theta in[0,pi/2]
for distance from the north pole. A regular solution of(Delta+n)v=0 with
this angular dependence is

 v(theta,omega)=(sin theta)^L
   2F1((L-1)/2,(L+n)/2;L+n/2;sin^2 theta) Y_L(omega).    (7)

Substitution in the polar-coordinate Laplacian verifies the hypergeometric
ODE. Set A=(L-1)/2, B=(L+n)/2, C=L+n/2. Then C-A-B=1/2.
Gauss's continuation formula at1 says that the scalar factor at the equator
has expansion A0+B0 cos theta+O(cos^2 theta), with

 A0=Gamma(C)Gamma(1/2)/(Gamma(C-A)Gamma(C-B)),
 B0=Gamma(C)Gamma(-1/2)/(Gamma(A)Gamma(B)).

The outward derivative is partial_theta, so the DN ratio is -B0/A0:

 mu_L=2 Gamma(L/2)Gamma((L+n+1)/2)
          /[Gamma((L-1)/2)Gamma((L+n)/2)] >0.            (8)

All gamma arguments in(8) are positive. For L=1 the Neumann solution is a
first harmonic and has zero normal derivative, as expected. For L=0 the
Dirichlet problem resonates, so one must NOT assign it a finite DN value.
Instead handle its Neumann problem directly: for f=f0 constant,
Tf=-m f0 and v=-(2m/a) f0 x_(n+1) solves(6). Its boundary value is0;
therefore A(v,v)=int_Sigma v partial_nu v=0. Degree1 f gives Tf=0.
These two modes have zero shape quadratic, without any missing radial term.

For general f, write f=sum f_L in boundary spherical harmonics and define

 Q(f)=sum_(L>=2) [(L-1)(L+n-1)]^2/mu_L * ||f_L||L2^2.    (9)

The L>=2 contribution to v's boundary value is
-(2/a)mu_L^-1 (L-1)(L+n-1) f_L. Green's identity and angular orthogonality,
including the L0 calculation, give

 A(v_f,v_f)=(4/a^2) Q(f).

Thus the projected shape action has exact Hessian and Taylor coefficient

 J''=-(4/a)Q(f),
 J_reduced(D_t)=J_D(1)-(2/a)t^2 Q(f)+o(t^2).             (10)

The principal growth mu_L~L follows from gamma-ratio asymptotics, so Q is a
continuous quadratic form on H^(3/2)(Sigma), zero exactly on degrees0,1.
This also extends(9)-(10)'s quadratic form by density to H^(3/2) shapes.
Only the quadratic form, not the nonlinear domain expansion, is asserted by
that density statement.

## 4. Stereographic shape normalization and polynomial cutoffs

On the equator under unit-sphere stereographic coordinates x in R^m,

 Omega=2/(1+r^2), z=(1-r^2)/(1+r^2),
 sin theta=2r/(1+r^2), r=sin theta/(1+z), Omega=1+z.

An OUTWARD Euclidean normal displacement t F changes spherical outward
normal height at first order by t eta, eta=Omega F. If instead the graph
is written vertically as x_n=t F with domain x_n>t F, its outward
normal height is -t eta. This harmless GLOBAL sign disappears in Q,
because Q(-eta)=Q(eta). There is NO angular-degree-dependent factor2.
For F=r^(2j)H_l(x), H_l homogeneous harmonic of degree l,

 eta=(sin theta)^l (1-z)^j(1+z)^(1-l-j)H_l(omega).       (11)

At z=0,r=1,Omega=1, both sides equal H_l(omega), a useful normalization check.
The target-normalized Euclidean bubble U=(1+r^2)^(-(n-2)/2) compactifies to a
radius1/2 hemisphere, not a unit hemisphere. Passing to the unit hemisphere
changes all actions/quadratics by an overall positive factor. There is no
l-dependent factor and none is used below.

At center xi and scale lambda, set y=(x-xi)/lambda. The unit-sphere conformal
factor becomes2/[lambda(1+|y|^2)], so the shape profile is exactly

 eta_(xi,lambda)(y)= [2/(1+|y|^2)] lambda^-1 F(xi+lambda y). (12)

For n19,m18, a degree d<=8 polynomial transforms near the omitted pole to
eta=O(s^(2-d)), with s distance from that pole. Cut it off at Euclidean
radius R. For the removed tail one has

 ||tail||H1=O(R^-2), ||tail||H2=O(R^-1)

in the worst case d8 (lower degrees decay faster). These follow by integrating
|D^k eta|^2=O(s^(4-2d-2k)) against s^17 ds, including the cutoff annulus.
Interpolation yields ||tail||H^(3/2)=O(R^-3/2). Therefore Q of cutoff profiles
converges to Q of the full polynomial, uniformly with any fixed finite number
of xi/lambda derivatives on compact parameter sets; those derivatives do not
increase the polynomial degree or its coefficient bounds.

### Exact transfer of the original Euclidean action

Here write A=4(n-1)/(n-2) to avoid confusion with the bubble exponent.
Let U=(1+|x|^2)^(-(n-2)/2), gbar=U^(4/(n-2))delta (radius1/2),
and gunit=4gbar. On ANY smooth deformed domain, integration by parts gives

 int A|grad(Uw)|^2+2int H_delta U^2w^2
 =int [A U^2|grad w|^2-A U Delta U w^2]
            +int_boundary [A U partial_nu U+2H_delta U^2]w^2
 =int_gbar [A|grad w|^2+R_gbar w^2]+2int_boundary_gbar H_gbar w^2.

Thus no additional boundary energy or flux is omitted by conformal transfer.
Also int (Uw)^q dx=int w^q dV_gbar, and A n(n-2)=4n(n-1)=R_gbar.
Consequently for the ORIGINAL target-normalized Euclidean action J_delta,

 J_delta(Uw)=J_gbar(w)/A=J_unit(w)/[A 2^(n-2)].

Here J_unit is exactly(1); scaling gunit=4gbar multiplies its action by
2^(n-2). Therefore(10) transfers with the explicit positive coefficient

 J_delta,reduced=J_delta,bubble-[2^(3-n)/A^2]t^2 Q(eta_unit)+o(t^2).

This is an identity on each deformed domain, not merely an asymptotic claim.
The outward-normal sign eta_unit=+/-2F/(1+r^2) disappears in Q.

## 5. Exact Jacobi-polynomial matrix representation

From now on n19,m18. For angular degree l, put alpha=l+8 and
P_k=P_k^(alpha,alpha), the standard Jacobi polynomial, not an orthonormal one.
The boundary harmonic with angular factor H_l(omega) is
(sin theta)^l P_k(z) H_l(omega), of total degree L=k+l. Its z-norm is

 h_k=2^(2alpha+1)/(2k+2alpha+1)
        *Gamma(k+alpha+1)^2/[Gamma(k+1)Gamma(k+2alpha+1)]. (13)

For g_j(z)=(1-z)^j(1+z)^(1-l-j), let
I_kj=int_-1^1 (1-z^2)^alpha g_j(z)P_k(z) dz.
Then, for a normalized angular factor, the raw shape Gram matrix is

 A_l,ij^raw=sum_k e_(k+l) I_ki I_kj/h_k,
 e_L=[(L-1)(L+18)]^2/mu_L for L>=2, e0=e1=0.            (14)

The physical angular norm must still multiply this raw matrix.
Formula(14) follows simply by expanding g_j in the orthogonal Jacobi basis
and then applying(9). No additional stereographic factors occur.

Useful moments, obtained from Rodrigues's formula by k integrations by parts,
are, for p positive integer,

 int (1-z^2)^alpha(1+z)^(-p)P_k(z) dz
 =(-1)^k 2^(2alpha-p+1)
 Gamma(k+alpha+1)Gamma(alpha-p+1)Gamma(k+p)
 /[Gamma(p)Gamma(k+1)Gamma(k+2alpha-p+2)].               (15)

Here alpha-p+1>0 in every moment used below. Expand(1-z)^j=[2-(1+z)]^j
and apply(15). The beta=0 term for l1 is supported at k0 only and is killed
by e1=0. Formula(15) can also be checked by the beta integral and the terminating
hypergeometric expression for P_k.

For l2, j0..3, divide these moments by the j0 moment. The resulting polynomials
are

 P0(k)=1,
 P1(k)=(k^2+21k+11)/9,
 P2(k)=(k^4+42k^3+467k^2+546k+264)/144,
 P3(k)=(k^6+63k^5+1372k^4+11319k^3+22855k^2
                             +26166k+10296)/3024.       (16)

Set C0=(9!)^2/4 and the strictly positive common weight

 w_k=(2k+21)(k+1)^2(k+20)^2
                [Gamma((k+1)/2)/Gamma((k+22)/2)]^2.     (17)

Duplication of Gamma shows A2,ij^raw=C0 sum w_k Pi(k)Pj(k).
All other radial matrices needed for translation Hessians reduce to this
same weight by shifting their index. Define

 R1(k)=(0, 2, (k^2+19k+2)/4,
             (k+1)(k+2)(k+17)(k+18)/56
                         -3(k+1)(k+18)/4+6),
 R3(k)=(1, (k+2)(k+21)/18-1,
             (k+2)(k+3)(k+20)(k+21)/432
                         -(k+2)(k+21)/9+1).

Then, with indices0..3 for A1 and0..2 for A3,

 A1,ij^raw/C0 = sum_(k>=0) w_k (k+1)(k+20)/324
                                      R1_i(k+1)R1_j(k+1),
 A2,ij^raw/C0 = sum_(k>=0) w_k Pi(k)Pj(k),
 A3,ij^raw/C0 = sum_(k>=0) w_k k(k+21)R3_i(k-1)R3_j(k-1). (18)

These identities follow directly from(13)-(15); equivalently compare equal
total degrees L for adjacent angular blocks. The k0 term of the last line
is0. The zero first row/column in A1 is the linear graph kernel.

## 6. Exact summation, with no unbounded numerical series

For every polynomial target p(k) in(18), its degree is at most12. The weight
satisfies exactly

 w_(k+2)/w_k = r(k)=(2k+25)(k+3)^2/[(2k+21)(k+20)^2],
 w0=8400*pi/(10!)^2,
 w1=23*4*441*(4^11*11!/22!)^2/pi.                       (19)

Find a polynomial B(k) such that

 (k+18)^2 B(k)-(k+3)^2 B(k+2)=(2k+21)p(k).              (20)

For every target used, B of degree at most12 exists. The exact executable
certificate constructs it by descending powers: the leading coefficient of
(20)'s left side applied to k^z is30-2z, at degree z+1. Therefore set
b_z=[current remainder]_(z+1)/(30-2z), subtract its contribution, and descend.
The final remainder is tested to be the zero polynomial, with rational
arithmetic, for every entry in all three matrices. This is a finite polynomial
identity certificate, not a numerical test.

Put q(k)=(k+18)^2 B(k)/(2k+21). Equations(19)-(20) say
q(k)-r(k)q(k+2)=p(k). Since w_k=O(k^-16) and q(k)=O(k^13), the telescoping tail
vanishes. Hence every infinite sum in(18) has the exact evaluation

 sum_(k>=0) w_k p(k)=w0 q(0)+w1 q(1).                 (21)

Thus all matrix entries belong to Q*pi+Q/pi and are computed exactly.
As an additional independent check, their numerical values agree with direct
spectral sums through100000 modes in relative error below9e-12. This numerical
agreement is not used in the certificate.

## 7. Translation algebra and angular norms

Let s=|y|^2,t=y1 and define solid spherical harmonics in R^m:
H1=t, H2=t^2-s/m, H3=t^3-3ts/(m+2).
Under normalized angular measure on S^(m-1), their squared norms are

 N1=1/m,
 N2=2(m-1)/[m^2(m+2)],
 N3=6(m-1)/[m(m+2)^2(m+4)].                            (22)

These follow from E[t^(2r)]=(2r-1)!!/[m(m+2)...(m+2r-2)].
For j>=0 write

 b_j=2(m-1)/m+4j(m-1)/[m(m+2)],
 k_j=2j b_j+6jm/(m+2)+12j(j-1)m/[(m+4)(m+2)].          (23)

Direct harmonic decomposition gives

 partial1(s^jH2)=b_j s^jH1+2j s^(j-1)H3,
 projection_l2 partial11(s^jH2)=k_j s^(j-1)H2,
 Delta(s^jH2)=2j(m+2j+2)s^(j-1)H2.                    (24)

For the sum over all coordinate first derivatives, use
partial_a(s^jH2)=(1+2j/(m+2))s^j partial_a H2
                       +2j s^(j-1)H3,a,
H3,a=y_aH2-s partial_aH2/(m+2). Orthogonality gives

 sum_a ||partial_aH2||^2=2(m+2)N2,
 sum_a ||H3,a||^2=mN2/(m+2).                           (25)

These identities can be checked from homogeneity and angular integration;
agent3_harmonic_translation_checks.py also verifies(22)-(24) symbolically.

## 8. Polynomial witness and full Hessian

Choose

 F(y)=H2(y)[1-461 s/1000+7 s^2/125-693 s^3/500000],
 c=(1,-461/1000,7/125,-693/500000).

Use center parameter zeta=xi/lambda and set
F_lambda(y)=lambda^-1 F(lambda y)=sum_(j=0)^3 v_j s^jH2,
v_j=c_j lambda^(2j+1). Define E(lambda)=Q(Omega F_lambda)/|S17|.
Let A1,A2,A3 denote the exact raw matrices(18), including C0. Then

 E=N2 v^T A2 v.

At center0, the first translation variation vanishes by evenness. Define
u1_j=b_jv_j (j0..3), u3=(2jv_j)_(j1..3),
sec=(k_jv_j)_(j1..3) followed by0,
u1sum_j=(1+2j/(m+2))v_j,
lap=(2j(m+2j+2)v_j)_(j1..3) followed by0.
The translation Hessian in the parallel direction and its trace, divided
by the same area |S17|, are

 Hparallel=2[N1 u1^T A1 u1+N3 u3^T A3 u3+N2 v^T A2 sec],
 Htrace=2N2[2(m+2)u1sum^T A1 u1sum
                    +m/(m+2)u3^T A3u3+v^T A2 lap],
 Hperp=(Htrace-Hparallel)/(m-1).                        (26)

This is the identity second_derivative Q(F)=2Q(F',F')+2Q(F,F''),
combined with(24)-(25). The scale Hessian is E''.
Since F is even in every coordinate and invariant under rotations of its
last17 coordinates, all scale-center mixed Hessian entries vanish at center0;
the center Hessian is diag(Hparallel,Hperp I17).

The exact script computes the matrices by(20)-(21), constructs(26), and then
uses rational interval arithmetic to certify

 lambda_* in[951902323/10^9,951902324/10^9],
 E'(left)>8.93061118e-11,
 E'(right)<-8.69877185e-11,
 E'' throughout interval in[-.17629396840,-.17629369241],
 Hparallel throughout interval in[-.28156987935,-.28156977858],
 Hperp throughout interval in[-.18010947169,-.18010945685]. (27)

The endpoints in(27) are outward rounded for display; the script's assertions
use exact Fractions, not these printed decimal approximations. To bound pi,
it uses Machin's identity pi=16atan(1/5)-4atan(1/239) and alternating arctangent
series with60 and20 terms. The interval evaluator treats each polynomial
coefficient as alpha*pi+beta/pi, bounds it using those rational pi bounds,
and bounds lambda powers on the positive rational interval. Each sign in(27)
is therefore a finite exact-arithmetic inequality.

By continuity and the sign change there is a root E'=0 in the displayed
interval. Strict negativity of E'' makes it unique there. Parity makes every
center derivative vanish at0, and(26)-(27) make the full Hessian negative
definite. Thus Q has a STRICT FULL LOCAL MAXIMUM at (zeta0,lambda_*).
Changing to the physical center xi=lambda zeta multiplies translation
Hessian by lambda_*^-2 and leaves strict maximality unchanged.

## 9. Reproducibility and scope

Run workspace/agent4_exact_full_hessian.py with SymPy available. It:
- constructs every required target polynomial and exact primitive;
- asserts zero remainder for every telescoping identity;
- builds exact matrices and full Hessian expressions;
- constructs rational pi bounds and asserts all signs in(27).
No floating-point operation contributes to any assertion. Decimal output is
for readability only. The associated txt file records the exact matrices
and Hessian polynomials.

The overall action coefficient from(10) is negative and nonzero. Passing
between unit and radius1/2 hemispheres changes it by a positive constant,
so it cannot change this strict maximum into a minimum or remove it.
The result here is a rigorously computer-certified analytic shape lemma.
Whether and how it implies a fixed-domain blow-up sequence is the separate
local-PDE reduction and diagonal-persistence question; no such implication
is smuggled into this algebraic lemma.
