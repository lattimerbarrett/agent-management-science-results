# Fixed smooth-domain construction from a stable polynomial shape minimum

This note proves the construction implication; its only finite-dimensional input
is the stable shape minimum certified in the agent3 scripts. It does not invoke
the compactness/Pohozaev criterion needed for the opposite implication.

## 1. Statement, conventions, and Hilbert space

Fix n>=19, a=(n-2)/2, q=2n/(n-2), beta=(n-2)/(2(n-1)). Write
U_{t,xi}(y,s)=[t/(t^2+|y-xi|^2+s^2)]^a on the upper half-space.
Let F be a polynomial on R^{n-1}, of degree at most 8, vanishing to order 2
at zero. Suppose its shape functional Psi_F, defined below, has a strict
nondegenerate local minimum at (t_*,xi_*), with t_*>0. We will construct one
smooth compact connected bounded Euclidean domain Omega, of positive Yamabe
type and not conformal to a hemisphere, with smooth positive critical Robin
solutions whose boundary maxima diverge.

The energy on a smooth bounded Euclidean domain is

 E_Omega(v)=1/2 Q_Omega(v,v) -(n-2)^2/2 integral_Omega (v_+)^q,
 Q_Omega(v,w)=integral_Omega grad v.grad w + beta integral_boundary H v w.

For positive-type Omega, Q is an equivalent Hilbert norm on H^1(Omega).
The trace, critical Sobolev, and dual trace estimates used below are

 ||v||_{L^q(Omega)}+||v||_{L^{2(n-1)/(n-2)}(boundary)} <= C ||v||_Q,
 |integral_boundary f v| <= C ||f||_{L^{2(n-1)/n}} ||v||_Q.

These are valid, with uniform constants, for the bounded C^2-small domain
perturbations used here. Coercivity follows from the positive first Robin
eigenvalue. Conversely, for the explicit base below it follows directly from
Poincare with a nonzero nonnegative boundary term, and persists by pullback
under a sufficiently small C^2 perturbation.

## 2. Half-space source and shape functional

The Jacobi bilinear form is

 A_{t,xi}(v,w)=integral_half grad v.grad w
             -n(n+2) integral_half U_{t,xi}^{4/(n-2)} v w.

Its kernel in D^{1,2}(R^n_+) has dimension n and is spanned by the scale and
n-1 tangential-translation derivatives of U. This follows, for example, by
conjugating by U to the round hemisphere: the equation becomes
(-Delta_{S^n}-n)f=0 with Neumann boundary data; its kernel is exactly the
restrictions of the n coordinate functions tangent to the equator. This
conjugation is an isomorphism of the energy spaces. Since its potential is a
compact multiplication perturbation of the Dirichlet inner product, A has a
bounded inverse on the Dirichlet-orthogonal complement of this kernel.

For Omega_epsilon={s>epsilon F(y)}, evaluate the outward critical Robin
operator on the AMBIENT bubble U_{t,xi}, restricted to Omega_epsilon. Its
first-order boundary defect is epsilon S_{F,t,xi}, where

 S_{F,t,xi}=(n-2)U_{t,xi} [F-(y-xi).grad F]/[t^2+|y-xi|^2]
                        + beta (Delta F) U_{t,xi}             (s=0).

For t,xi in a fixed compact parameter set with t bounded away from zero,
S and its parameter derivatives are bounded by C(1+|y|)^{8-n}. Thus they
belong to L^{2(n-1)/n}(R^{n-1}) for n>16. In particular they define bounded
energy-space functionals ell_{F,t,xi}(v)=integral_boundary S v.

For every compactly supported graph, the first shape variation of E at every
ambient bubble is zero. Explicitly its coefficient after tangential
integration by parts is

 -1/2 |grad_y U|^2 +(n-2)^2/2 U^q + (beta/2) Delta_y(U^2)=0.

The identity is pointwise, with the bubble scale included. Differentiating it
with respect to each bubble parameter gives ell(Z_alpha)=0 for every kernel
function Z_alpha. Approximation by cutoffs proves the same assertion for our
polynomial F, because all the resulting pairings converge for n>16.

Let w_{F,t,xi} solve A(w,v)=-ell(v), orthogonally to the kernel. Define

 Psi_F(t,xi)= -1/2 A(w,w)
            =-1/2 ell(A^{-1}ell).

(The inverse here acts on the kernel complement.) This is precisely the
finite-dimensional function used in the spectral certificates. Multiplying
all coefficients by the same positive constant does not change its minima.

## 3. One fixed smooth positive-type domain

Use any smooth bounded convex domain Omega_0 with an open flat bottom disk
containing {|y|<1/2,s=0}; let H>=0 and H not identically zero. One fully
explicit choice is

 h(v)=0 (v<=1), h(v)=(v-1)^2 exp[-1/(v-1)] (v>1),
 Omega_0={h(|y|^2)+(s-1)^2<1}.

Its boundary is smooth, its defining function is convex, and its bottom
contains {|y|<1,s=0}. The positive Robin form is coercive: if coercivity
failed, normalized functions with energy tending to zero would converge to
a constant, and the nonzero H term would force that constant to vanish.

For i>=2 take p_i=2^{-i}e_1, rho_i=2^{-i-5}, lambda_i=2^{-(i+I)^2}, with I fixed
sufficiently large. A harmless increase of I ensures lambda_i<<rho_i.
Choose a smooth radial chi equal to 1 on B_{3/4} and 0 outside B_1, and set

 f_i(y)=lambda_i^9 F((y-p_i)/lambda_i) chi((y-p_i)/rho_i).

For F=H_2 P_3 this is the same as
lambda_i^7 H_2(y-p_i)P_3(|y-p_i|^2/lambda_i^2) chi.
The disks B_{rho_i}(p_i) are pairwise disjoint and lie in the flat disk.
For every k,

 sup |D^k f_i| <= C_k lambda_i rho_i^{8-k}.

For polynomial terms of degree below 8 the bound is smaller by a power of
lambda_i/rho_i. Therefore the sum f=sum_i f_i, extended by zero at the
accumulation point 0 and outside the disks, is C^infinity, with every jet
zero at 0. Replacing only the bottom flat patch by s=f(y) gives one fixed
smooth bounded connected domain Omega. It is obtained from Omega_0 by a
C^2-small diffeomorphism, and Q_Omega remains coercive. It is Euclidean,
hence locally conformally flat including at the boundary.

If F has a nonzero tracefree quadratic term (as all our certified profiles
do), the boundary is nonumbilic at p_i: its tracefree second fundamental form
there is a nonzero multiple of lambda_i^7 (D^2 F(0))^0. The tracefree second
fundamental form transforms under a conformal change ghat=e^{2h}g by
IIhat^0=e^h II^0. The round hemisphere is totally geodesic, so Omega cannot
be conformally equivalent to it.

## 4. The scale comparisons and elementary weighted estimates

Set epsilon_i=lambda_i^8, R_i=rho_i/lambda_i. Under x=p_i+lambda_i z the
chosen patch is exactly z_n=epsilon_i F(z') for |z'|<3R_i/4. The remaining
patches lie outside the selected chart. On this chart

 epsilon_i(1+R_i)^7 = O(lambda_i rho_i^7)=:delta_i ->0.

The polynomial and graph-cutoff derivatives obey
|D^k F_R(z')|<=C(1+|z'|)^{8-k}, k<=3. In the region in which an ambient
bubble or its cutoff is evaluated, both the graph slope and the relative
height displacement |epsilon F|/(1+|z'|) are bounded by C delta_i.
All radial quantities evaluated at height epsilon F are consequently
comparable to their values at height zero. To identify the energy spaces, use
the vertical map Phi(y,s)=(y,s+epsilon F_R(y) zeta(s/(1+|y|))), with a fixed
smooth zeta equal to 1 near zero and compactly supported. Its derivative
differs from the identity by O(delta_i). The pulled-back Dirichlet form differs
by O(delta_i) in operator norm. The Robin term has the same bound, since
|H|<=C delta_i/(1+|y|), and the trace Hardy inequality bounds
integral_boundary (1+|y|)^(-1) v^2 by C integral_half |grad v|^2.
The physical comparison bubble pulls back as U composed with Phi, not U;
we retain that distinction throughout.

Here are the estimates needed for Taylor expansion (also for first parameter
derivatives on compact sets):

 (i) integral_{|z|>R} [(1+|z|)^14 |grad U|^2
                       +(1+|z|)^16 |D^2 U|^2]
       <= C R^{16-n};

 (ii) ||(1+|y|)^{8-n}||_{L^{2(n-1)/n}(|y|>R)}
       <= C R^{(16-n)/2}.

Both follow by polar integration. All Taylor remainders of the graph normal,
its area element, and its mean curvature have the extra factor delta_i
relative to their quadratic energy, or to their linear Robin-source,
majorants. For clarity, the normal is (epsilon grad F,-1)/sqrt(1+epsilon^2
|grad F|^2), H=div(epsilon grad F/sqrt(1+epsilon^2|grad F|^2)), and its
nonlinear error is bounded by C delta_i^2 epsilon |D^2F|. Evaluating U at
height epsilon F uses the ordinary Taylor formula, with
|epsilon F|/(1+|y|)<=C delta_i. The same estimates bound all mixed terms.
Estimates (i),(ii), the trace inequality, and Holder therefore give:

 * Robin residual = epsilon_i ell_{F,t,xi}+o(epsilon_i) in dual energy norm;
 * its first parameter derivatives have the same expansion;
 * fixed-bubble energy = E_half(U)+o(epsilon_i^2), in C^1(parameters),

once the chart cutoff errors below are included. One can check the last
assertion directly without retaining spurious quadratic terms: with an
ambient bubble even in z_n, both the domain-volume difference and the
integrated H term are odd functions of epsilon. Their linear term vanishes
by the stress cancellation in section 2. Their cubic remainder is bounded
by C delta_i epsilon_i^2 times the finite integral in (i).

Choose the physical bubble cutoff eta_i equal to 1 on B_{rho_i/4}(p_i),
zero outside B_{rho_i/2}(p_i), radially symmetric about p_i. Its energy-norm
error is O(R_i^{-a}), its fixed-bubble energy error is O(R_i^{2-n}),
uniformly with one parameter derivative. The possible linear graph term
in this cutoff annulus is at most C delta_i R_i^{2-n}, hence is covered by
the same energy error. Crucially,

 R_i^{-a}/epsilon_i
 =lambda_i^{(n-18)/2} rho_i^{-(n-2)/2} ->0       (n>=19).

Thus all cutoff errors are little-o of the relevant residual/energy scales.
The explicit superexponential lambda_i makes these comparisons valid even
with any fixed power of rho_i^{-1} coming from cutoff derivatives.

## 5. Uniform projected inverse

Let W_i(t,xi)(x)=eta_i(x)lambda_i^{-a}
U_{t,xi}((x-p_i)/lambda_i), restricted to the fixed domain Omega.
Let K_i be the span of its n parameter derivatives, and Pi_i the
Q-orthogonal projection onto K_i. Their Gram matrices converge uniformly to
the nonsingular half-space Gram matrix.

Let T be the Q-Riesz inverse for interior data:
Q(Tf,v)=integral_Omega f v. The linearized projected map on K_i^perp is

 L_i phi=(1-Pi_i)[phi-T(n(n+2)W_i^{4/(n-2)}phi)].

There are constants c>0 and i_0 independent of the compact parameter set
such that ||L_i phi||_Q>=c||phi||_Q for i>=i_0. Here is the full usual
contradiction argument. If not, choose normalized phi_i with projected image
tending to zero. Test the unprojected equation against each cutoff kernel
function; its Jacobi defect tends to zero by the residual estimates, so all
kernel coefficients tend to zero. Thus the unprojected image tends to zero.
The weak limit away from the single accumulation point solves the homogeneous
coercive Robin problem, and hence is zero; test functions avoiding that point
are dense in H^1 because n>=3. Rescaling at p_i gives a bounded D^{1,2}
sequence. Its weak limit solves the half-space Jacobi equation and is
orthogonal to all n kernel functions, so is zero. Rellich compactness makes
the weighted potential integral vanish on each fixed rescaled ball. Outside
that ball use Holder and
||U^{4/(n-2)}||_{L^{n/2}(|z|>R)} ->0.
Consequently integral W_i^{4/(n-2)}phi_i^2 ->0. Pairing the unprojected
equation with phi_i now gives 1=o(1), the contradiction. Since L_i is
self-adjoint Fredholm of index zero on the complement, this lower bound
proves surjectivity and the asserted uniformly bounded inverse.

## 6. Solving the infinite-dimensional equation

The gradient of E is G(v)=v-T(n(n-2)(v_+)^{q-1}). Its residual at W_i is
O(epsilon_i), uniformly C^1 in the parameters. For n>=19, 2<q<3, and

 ||G(W+phi)-G(W)-DG(W)phi -
   [G(W+psi)-G(W)-DG(W)psi]||_Q
 <= C(||phi||_Q+||psi||_Q)^{q-2} ||phi-psi||_Q.

This is the pointwise Holder estimate for derivative of x_+^{q-1}, followed
by Sobolev and Holder. The contraction mapping theorem on a ball of radius
C epsilon_i, using the uniform inverse of section 5, gives a unique
phi_i(t,xi) in K_i^perp with

 (1-Pi_i)G(W_i+phi_i)=0,   ||phi_i||_Q<=C epsilon_i.

The contraction depends C^1 on parameters (x_+^{q-1} is C^1), hence phi_i
is C^1 and ||partial_parameter phi_i||_Q<=C epsilon_i. Here is the derivative estimate needed because p=q-1 lies in (1,2), so
a bare Holder operator bound is insufficient. Each parameter derivative obeys
|partial W|<=C W. For f(v)=v_+^p, pointwise splitting into |z|<=W/2 and its
complement gives

 |fprime(W+z)-fprime(W)| W <= C(W^(p-1)|z|+|z|^p),
 |fprime(W+z)-fprime(W)-fsecond(W)z| |partial W| <= C|z|^p.

The first inequality bounds the differentiated linear term by O(epsilon_i),
and the second bounds the parameter derivative of the nonlinear remainder by
O(epsilon_i^p), in the dual Sobolev norm. The term multiplying partial phi is
O(epsilon_i^(p-1)) in operator norm and is absorbed using the uniform inverse.
The differentiated source is O(epsilon_i), and the kernel projections have
uniformly bounded derivatives; these facts give the asserted O(epsilon_i)
bound. Values where W=0 cause no difficulty since partial W=0 there.
One may identify the varying complements with a fixed complement using
their smooth Gram projections.

## 7. Reduced energy, including its C^1 remainder

Define J_i(t,xi)=E(W_i+phi_i). In rescaled variables, on every fixed ball,
phi_i/epsilon_i converges strongly to w_{F,t,xi}. To see this without
any possible loss of energy at infinity, approximate w_F in D^{1,2} by a
fixed compactly supported smooth function, scale and transport it into the
selected patch by Phi, and project it onto K_i^perp. First let i tend to
infinity, then exhaust the half-space by these approximations. The source
converges strongly in the dual energy norm by section 4, the form perturbation
is O(delta_i), all kernel Gram matrices converge, and the uniform inverse
from section 5 bounds the difference from the actual correction. This proves
strong energy convergence globally, rather than merely local convergence. The potential tail
estimate used there gives global energy convergence, not just local weak
convergence. These statements are uniform on the compact parameter set;
otherwise a countersequence of parameters has a convergent subsequence.
Differentiating the equations proves the same conclusion for first parameter
derivatives: the coefficients and source converge with one parameter
derivative, the differentiated projected inverse is uniformly bounded, and
the refined weighted pointwise inequalities of section 6 make the
differentiated nonlinear remainder O(epsilon_i^{q-1})=o(epsilon_i). Thus no differentiation of an uncontrolled little-o is involved.

Taylor expansion of E, with the q-power remainder, gives

 J_i=E(W_i)+E'(W_i)[phi_i]+1/2 E''(W_i)[phi_i,phi_i]
                  +O(||phi_i||_Q^q).

Testing the projected equation against phi_i combines the middle two terms
as -1/2 E''(W_i)[phi_i,phi_i]+O(epsilon_i^q). The strong convergences and
section 4 consequently give the precise reduced expansion

 J_i(t,xi)=E_half(U)+epsilon_i^2 Psi_F(t,xi)
                          +o_{C^1}(epsilon_i^2).

All constants are uniform on the selected compact parameter neighborhood.
Since q>2, epsilon_i^q=o(epsilon_i^2). This derivation is made in ambient
coordinates. If the domain is flattened first, the transported bubble
U(y,z_n+epsilon F(y)) must also be differentiated; its F U_n term cancels
the apparent extra direct F^2 term.

## 8. From the minimum to positive smooth blowup solutions

Take a small closed parameter ball around the strict local minimum of Psi,
with strictly larger Psi on its boundary. Uniform C^0 convergence in
section 7 suffices to give an interior minimum of J_i for all large i.
At that point partial J_i=0. The full gradient G(W_i+phi_i) already lies in
K_i; the matrix pairing its kernel components with the parameter derivatives
of W_i+phi_i is the kernel Gram matrix plus O(epsilon_i), hence invertible.
It follows that G(W_i+phi_i)=0 in the full Hilbert space.

The resulting weak solution u_i solves the truncated critical equation.
Testing with its negative part gives Q(u_i^-,u_i^-)=0, so u_i>=0. It is
not zero because its rescaled bubble has nonzero trace norm. Brezis--Kato
iteration (split the L^{n/2} potential into bounded and small-norm parts),
followed by the interior and Robin boundary elliptic estimates, gives
smoothness; the strong maximum principle and boundary Hopf lemma give
u_i>0 on the closed domain. It then solves the untruncated equation.

Finally, on any fixed rescaled boundary disk the trace of the rescaled
correction tends to zero, whereas U_{t,xi} has a positive fixed trace norm.
Thus max_boundary u_i >= c lambda_i^{-a}->infinity. This trace argument
does not assume an a priori pointwise error bound.

This proves the construction implication from the certified strict minimum.
For n=19,...,32 that input is certified by agent3_transcert.py (with exact
moment arithmetic and outward interval tail bounds). For n>=33 it follows
from agent3_all_n33.py and the exact translation-Hessian identities in
agent3_transall.py. Thus the construction side holds for every n>=19.
