# High-dimensional analytic bridge (agent_1, independently audited by agents 2 and 4)

This proves the high-dimensional existence half, using standard Sobolev-trace,
Banach implicit-function, spectral, and elliptic regularity results. It is NOT a
claim that the original two-sided theorem is complete: no low-dimensional
blow-up theorem is supplied here.
The finite-model strict maxima are proved separately by the team's exact algebra.

Let q=2n/(n-2), a=n(n-2), c=(n-2)/(4(n-1)), n>16. Let H=D^{1,2}(R^n_+),
with inner product integral grad v.grad w. For a compactly supported smooth graph
h:R^{n-1}->R, pull its epigraph back by T(y)=(y',y_n+h(y')). Write
b_h=Delta h - h_a h_b h_ab/(1+|grad h|^2). The exact pulled-back functional is

 I_h(v)=1/2 int[|grad v|^2-2h_a v_a v_n+|grad h|^2 v_n^2]
          +c int_boundary b_h v^2 - a/q int(v_+)^q.

The volume Jacobian is one. The boundary identity is H_h dS=b_h dy'.
The Sobolev trace inequality bounds the difference of quadratic forms by
 C(||grad h||_infty+||grad h||_infty^2+||b_h||_{n-1}) ||v||_H||w||_H.
Choose this quantity sufficiently small. Then Q_h is coercive on H.

For a Euclidean bubble U=U_{xi,lambda}, let K be the span of its n parameter
derivatives (n-1 tangential translations and one dilation). The linearization
 A_0=I_0''(U) on K^perp is a bounded invertible operator to its dual. Indeed
conformal transformation to a round hemisphere reduces its kernel to Neumann
solutions of (Delta+n)w=0: the tangential coordinate functions, exactly K;
the remaining discrete spectrum is separated from zero. The inverse norm is
uniform on compact parameter sets, or globally after conjugating by bubble
symmetries. Small quadratic-form perturbations preserve invertibility of the
projected A_h uniformly.

The critical power integral is C^2 on H because q>2. Its Hessian is uniformly
continuous near the compact family of normalized bubbles. Thus the quantitative
implicit function theorem solves
 Pi_{K^perp} I_h'(U+w)=0, w in K^perp,
with ||w||_H <= C ||I_h'(U)||_{H*} whenever the right-hand side is small.
The solution depends C^1 on the bubble parameters. A critical point of the
reduced function is a full critical point: since w is orthogonal to K,
<partial_i w,Z_j>=-<w,partial_i Z_j>. The reduced-gradient/kernel-residual
matrix is therefore the baseline Gram matrix plus O(||w||_H), hence invertible.
No quantitative estimate on parameter derivatives of w is needed.

## Local profile and exact expansion

Let f be a polynomial of degree <=8, and let f_R=f chi(y'/R), chi=1 near zero.
For bubbles in a fixed compact parameter set,

 ||grad(f_R-f) grad U||_2 + ||Delta(f_R-f) U||_{2(n-1)/n} ->0.

Indeed grad f=O(r^7), Delta f=O(r^6), grad U=O(r^{1-n}), U=O(r^{2-n}).
The squared bulk tail is bounded by C int_R^infty r^{15-n}dr; the trace-dual
integrability gives the same condition n>16. Cutoff derivatives obey the same
bounds. This also applies to first parameter derivatives if needed.

The linear graph residual is the bounded functional
 R_f(v)=-int f_a(U_a v_n+U_n v_a)+2c int_boundary Delta f Uv.
Every compact graph has zero first direct energy variation:

 L_f(U)=-int f_a U_a U_n+c int_boundary Delta f U^2=0.

To verify this, integration in y_n and then y' gives
 L_f(U)=int_boundary f[a/q U^q - |grad' U|^2/2 + c Delta'(U^2)]=0;
the last bracket vanishes pointwise for every Neumann bubble. Differentiating
this identity in parameters gives R_f(Z)=0 for all Z in K. It extends to the
polynomial f by the weighted convergence above.

The exact direct energy difference is
 I_h(U)-I_0(U)=1/2 int |grad h|^2 U_n^2
 -c int_boundary h_a h_b h_ab/(1+|grad h|^2) U^2.

Take a rescaled local graph h_local=delta f_R, with R=r/eps,
delta=mu eps^7 and ||grad h_local||_infty=O(mu r^7)->0. The residual satisfies
 I_h'(U)=delta R_f+o(delta)
provided all other graph patches have residual o(delta). Quadratic bulk
residuals are bounded by sup|grad h_local| times delta times the finite
weighted norm; cubic boundary residuals similarly by sup|grad h_local|^2.
The direct bulk energy is delta^2 B_f+o(delta^2),
 B_f=1/2 int |grad f|^2 U_n^2.
The absolute cubic boundary energy is bounded by
 C delta^3[1+R^{max(23-n,0)}+log R (when n=23)].
For 17<=n<23 its ratio to delta^2 is bounded by
 C mu eps^{n-16} r^{23-n}; at n=23 by C mu eps^7 log(r/eps), and for n>23
by C delta. These tend to zero for the explicit scales below.

The global linearized operators need not converge in operator norm, but converge
strongly on each fixed vector: local coefficients tend to zero and fixed-vector
Sobolev/trace tails are small, with uniformly bounded global form norms.
Uniform inverses and the residual convergence therefore imply
 w/delta -> V_f=-A_0^{-1}R_f strongly in H. The power remainder in energy is
O(||w||_H^q)=o(delta^2), and hence uniformly on compact parameter sets

 I_h(U+w)=I_0(U)+delta^2[B_f-1/2<R_f,A_0^{-1}R_f>]+o(delta^2).

For compact f the bracket is a negative constant times the spherical spectral
shape form Q(f;xi,lambda). One proof uses conformal transformation of the
physical bubble to a constant on the round hemisphere. For a boundary normal
graph t rho, the direct second variation of the UNNORMALIZED functional at the
constant is zero: volume and integrated mean curvature have odd expansions.
The first correction has (Delta+n)v=0 and Neumann data proportional to
(Delta_equator+n-1)rho. Elimination of v gives minus one half of its boundary
pairing. In boundary degree L>=2 this is a positive multiple of
 (L-1)^2(L+n-1)^2 / mu_L,
 mu_L=2 Gamma((L+n+1)/2)Gamma(L/2)/
          [Gamma((L-1)/2)Gamma((L+n)/2)].
The L=1 source vanishes; the L=0 solution has zero boundary value (Dirichlet
resonance), hence contributes zero to the pairing. The exact negative coefficient on the unit sphere is -2c^2 u0^2, where
u0=2^{-(n-2)/2}. This is precisely the spectral form used in the team's model
certificates. For clarity about changing coordinates, the flattened base U(y)
differs from the physical bubble pullback U(T_t y) by t W, W=f U_n. A base shift
by W changes R to R+A0 W and B to B+R(W)+A0(W,W)/2; direct expansion shows that
B-<R,A0^{-1}R>/2 is unchanged. Kernel components are harmless since R(K)=0 and
A0(K)=0. For compact f this is ordinary differentiation in H. For degree8,
W=O(r^{9-n}) and grad W=O(r^{8-n}), so W belongs to H exactly under n>16.
Approximation by f_R and weighted convergence identify the polynomial bracket.

## Countably many patches in ONE fixed graph

Fix one certified polynomial profile f=P_2(y')F(|y'|^2), degree <=8, for the
chosen n>=19. Let p_k=2^{-k}e_1, r_k=2^{-k-3}, mu_k=tau 2^{-k^2},
eps_k=2^{-k^4} (discard finitely many initial k if necessary). Set
 h_k(x')=mu_k eps_k^8 f((x'-p_k)/eps_k) chi((x'-p_k)/r_k), h=sum h_k.
The supports are disjoint. For every m,
 ||D^m h_k||_infty <= C_m mu_k r_k^{8-m},
so h is C-infinity, flat at the accumulation point zero, and compactly supported.
Its global slope and ||b_h||_{n-1} can be made as small as required by tau.
At p_k its Hessian has nonzero tracefree part mu_k eps_k^6 Hess P_2.

After centering and scaling at p_k, the local graph is delta_k f_{R_k}, with
 delta_k=mu_k eps_k^7, R_k=r_k/eps_k. Every other support has distance >=c2^{-k}
from p_k. Using bubble decay, all other patches together have residual norm
 <=C 2^{Ck} eps_k^{(n-2)/2}
and absolute direct energy difference <=C 2^{Ck} eps_k^{n-2}.
For example integration in the normal variable gives bulk weight
 int_0^infty |grad U(y',t)|^2 dt <=C |y'|^{3-2n} at large |y'|;
the boundary term follows from trace-dual Holder. All unweighted graph norms
are bounded independently of eps_j; distance >=c2^{-k} therefore gives the
stated exponential constants. The ratios to delta_k and delta_k^2 tend to zero
because n>16 and eps_k^{n-16}/mu_k^2 decays like 2^{-(n-16)k^4+2k^2}.

The preceding expansion is thus uniform on a fixed small parameter ball around
the certified strict maximum of Q. The reduced energy has a minimum in its
interior for every sufficiently large k, since uniform C0 o(delta_k^2) errors
are smaller than the strict boundary energy gap. Its C1 regularity gives a
critical point, hence an exact nonzero weak solution of the full equation.

Testing against its negative part, coercivity and the positive-part nonlinearity
force the solution to be nonnegative. Regularity and the strong maximum/boundary
point principles give smooth strict positivity. Under rescaling, correction
norm tends to zero. The trace Sobolev inequality gives boundary trace convergence
to the positive bubble on a fixed boundary ball. Therefore some boundary value
is >=c eps_k^{-(n-2)/2}, and the boundary maxima diverge.

Finally compactify infinity by the round spherical factor. Since h=0 outside a
compact set, the resulting compact manifold has smooth boundary near infinity.
The finite-energy solution transforms to H1 and extends weakly across the
boundary point at infinity, which has H1 capacity zero. Local Brezis-Kato
iteration (the critical potential is L^{n/2} and has arbitrarily small norm on
small balls), followed by Robin elliptic regularity, gives smooth extension.
The solution remains strictly positive. Coercivity and the critical Sobolev
inequality imply positive first eigenvalue on the compactified manifold. The
metric is round restricted to the perturbed domain, hence LCF. Nonzero tracefree
II at each p_k excludes conformal equivalence to a hemisphere.

INDEPENDENT AUDIT: agents 2 and 4 checked the weighted exponents, exact sphere
source/coefficient, strong-operator argument, coordinate-invariant Schur
complement, implicit-function kernel Gram step, infinite-patch scales and
compactification. Their audits found no remaining dimension-specific theorem
missing on the high-dimensional side. The low-dimensional compactness half is
entirely separate and remains unproved. All claims of the original full
classification must retain this essential limitation.
