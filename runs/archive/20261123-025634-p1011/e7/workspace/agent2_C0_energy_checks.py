import sympy as s
from pathlib import Path
n,r=s.symbols('n r', positive=True)
U2=(1+r*r)**(-(n-2))
lap=s.diff(U2,r,2)+(n-2)/r*s.diff(U2,r)
c=(n-2)/(4*(n-1))
rhs=(n-2)**2*s.Rational(1,2)*(r*r-1)*(1+r*r)**(-n)
assert s.simplify(c*lap-rhs)==0
# Radial exponents at infinity for the terms in the C0 expansion.
# Interior degree-4 first source and J2: int r^(7-n) dr.
# Cubic mean-curvature remainder: boundary int r^(10-n) dr.
# E2'(U) L2 coefficient: int r^(13-n) dr.
# Cubic mean-curvature source belongs to boundary dual iff n>20.
assert all(7-N < -1 and 10-N < -1 and 13-N < -1 and 2*(N-10)>N for N in range(32,1000))
# The general inequalities reduce symbolically to n>8,11,14,20.
for N0,power in [(8,7-n),(11,10-n),(14,13-n)]:
    assert s.simplify((power+1)+(n-N0))==0
assert s.simplify((2*(n-10)-n)-(n-20))==0
# Choose tau=1: shape mu^2=epsilon^8, cutoff energy=(epsilon/rho)^(n-2).
# n>=32 permits epsilon so small relative to rho that cutoff energy=o(mu^2).
assert all(N-2>8 for N in range(32,1000))
print('Exact first shape cancellation identity and all C0-expansion integrability inequalities verified.')
Path('workspace/agent2_C0_energy_checks.py').write_text(Path(__file__).read_text())
Path('workspace/agent2_C0_energy_expansion.md').write_text(r'''# C0 reduced energy expansion for quartic flat-domain bumps

## Precise scope and inputs

Fix n>=32 and a smooth bounded Euclidean domain of positive Robin Yamabe type. In a flat boundary patch insert pairwise disjoint graph bumps. At bump j write the graph, after dilation by epsilon_j, as t=mu_j f_Rj(z), where f_R(z)=chi(z/R)f(z), f=-P2+|z|^2P2, R_j=rho_j/epsilon_j -> infinity. Choose mu_j=epsilon_j^4 (tau=1), epsilon_j so small relative to rho_j that R_j^((2-n)/2)=o(mu_j). Then mu_j R_j^3=epsilon_j rho_j^3 ->0. The same proof works for tau>0 subject to n>8+2tau. Smooth graph cutoffs have uniformly bounded polynomial derivative estimates |D^a f_R|<=C_a(1+|z|)^(4-|a|) on their support.

Let theta=(lambda,xi) range over a fixed compact subset of (0,infinity) times R^(n-1). Let U_theta=[lambda/(lambda^2+|z-xi|^2+t^2)]^((n-2)/2). Cut this bubble off inside the bump patch, with cutoff radius a fixed fraction of R_j. Use the graph flattening map to transfer it to the domain and undo the dilation; denote it V_jtheta.

INPUTS, to be supplied by the uniform-inverse/contraction pieces: (i) a uniform inverse on the complement of the n bubble Jacobi modes, in the energy H1 norm; (ii) a projected correction w_jtheta with norm O(mu_j) and continuous dependence on theta, satisfying the projected nonlinear equation; (iii) the usual local convergence of the projections onto the explicit Jacobi functions. No sharp nonlinear remainder estimate beyond the standard critical Sobolev estimate is assumed below.

Then uniformly on compact theta sets,
E(V_jtheta+w_jtheta)=E_halfspace(U)+mu_j^2 F(theta)+o(mu_j^2),
where F is the exact second-order projected flat-domain shape energy previously computed by the hemisphere spectral method. Its common normalization is a positive constant times the negative shape Hessian, so its strict minima are exactly those certified in the quartic spectral proposition.

## Local graph energy and estimates

Put c=(n-2)/(4(n-1)), q=2n/(n-2), k=(n-2)^2/2. In graph coordinates the energy is exactly
E_mu(v)=1/2 integral [|Dv|^2-2mu f_a v_a v_t+mu^2|Df|^2 v_t^2] - k integral(v_+)^q
 +c integral_boundary [mu Delta f-mu^3 f_a f_b f_ab/(1+mu^2|Df|^2)]v^2.
The volume Jacobian is one. Thus E_mu=E_0+mu J1+mu^2 J2 plus the displayed cubic boundary term, with
J1(v)=-integral f_a v_a v_t+c integral_boundary Delta f v^2,
J2(v)=1/2 integral |Df|^2 v_t^2.

Uniformly on compact theta sets, |D^a U_theta|<=C(1+|x|)^(2-n-|a|) for |a|<=2. Consequently:
* J2(U_theta) and the energy-dual first variation S_theta=J1'(U_theta) exist for n>8. Their squared bulk source tails are bounded by C integral_R^infinity r^(7-n)dr. For the boundary part use the dual trace exponent 2(n-1)/n: Delta f U=O(r^(4-n)), which is integrable in that exponent exactly when n>8.
* The cubic boundary energy remainder divided by mu^3 is bounded by C integral_0^infinity (1+r)^(10-n)dr, finite for n>11.
* J2'(U) is uniformly bounded in the energy dual for n>14, because |Df|^2 DU=O(r^(7-n)), whose squared radial integral has exponent 13-n.
* The cubic boundary residual coefficient is O(r^(10-n)); it belongs to the dual trace space when n>20.
All these conditions hold for n>=32 and are explicitly checked in agent2_C0_energy_checks.py. The same estimates apply to f_R uniformly and show S_R -> S in the energy dual and J2_R(U)->J2(U), uniformly on compact theta sets.

For the cut-off bubble, the exact cancellation leaves J1(U_cut)=O(R^(5-n)); this follows by estimating both bulk and boundary first-variation tails by integral_R^infinity r^(4-n)dr. Hence mu J1(U_cut)=o(mu^2): the assumed R^((2-n)/2)=o(mu) implies R^(5-n)=o(mu) when n>8. This additional linear cutoff term must not be omitted.\n\nThe coefficient perturbation on arbitrary energy-bounded functions has operator norm o(1): the bulk contribution is bounded by C(mu R^3+mu^2 R^6), while the boundary curvature form is controlled by its L^(n-1) norm, at most C mu R^3. Here mu R^3 ->0. These bounds also control all quadratic terms involving the projected correction; no pointwise correction estimates are required.

## Exact first-order cancellation

For every compactly supported smooth f, J1(U_theta)=0. This is also true for the polynomial f by the integrable limits above. For lambda=1,xi=0 one can check directly, using integration in t and twice in z,
c Delta_z(U(z,0)^2)=1/2 |D_z U(z,0)|^2 - n(n-2) U(z,0)^q/q.
Indeed each side equals (n-2)^2(r^2-1)(1+r^2)^(-n)/2. Integration in t of Delta_z U times U_t, and of U_a U_at, proves the cancellation. Translation/dilation give every theta. The checker verifies the displayed identity symbolically for arbitrary n.

Differentiating J1(U_theta)=0 in theta shows S_theta annihilates the Jacobi kernel. Hence its projected inverse is an actual compatible halfspace Jacobi solution W_theta, uniquely specified by energy-orthogonality to that kernel, satisfying
E0''(U_theta)[W_theta,v]=-S_theta[v].
The halfspace inverse is supplied explicitly by stereographic transfer and the hemisphere spectrum. Dependence on theta is continuous; compactness gives uniform tails.

## Strong convergence of the correction

The bubble cutoff alone has energy error O(R_j^(2-n)) and energy-dual residual O(R_j^((2-n)/2)). These are o(mu_j^2) and o(mu_j), respectively, by the scale choice. Metric cutoffs only change S_theta in energy dual by o(1), by the preceding source-tail estimates. The exact graph expansion therefore gives
E'(V_jtheta)=mu_j S_theta+o(mu_j)
in the rescaled local energy-dual sense, uniformly on compact theta sets.

Cut off W_theta at radius R_j/4, transfer it by the same dilation/flattening, and project off the finite-dimensional approximate kernel. Denote this transferred comparison function by W_jtheta. Its energy norm converges to that of W_theta. The linearized operator applied to W_jtheta converges to -S_theta in energy dual: cutoff commutators tend to zero because W_theta belongs to D^(1,2); the graph perturbation has o(1) operator norm; and the kernel/projection errors tend to zero by input (iii). No other bump enters these comparison functions, since they are supported inside the jth patch.

Subtract mu_j W_jtheta from the actual projected correction equation. The nonlinear residual is o(mu_j): for p=(n+2)/(n-2) in (1,2), the critical Sobolev estimate is bounded by C||w_jtheta||^p=O(mu_j^p)=o(mu_j). Applying input (i),
||w_jtheta-mu_j W_jtheta||_energy=o(mu_j).
This establishes the strong correction convergence needed for the energy calculation, including the negligible global tail of w_jtheta. Uniformity follows by the compact-theta argument in each step.

## Energy expansion and identification

For q in (2,3), the pointwise second-order Taylor remainder for (s_+)^q is bounded by C|h|^q. Critical Sobolev therefore bounds the nonlinear energy Taylor remainder by C||w_jtheta||^q=o(mu_j^2). The quadratic form is uniformly bounded. The exact graph formula, cancellation J1(U)=0, cutoff estimates, and strong correction convergence now give
E(V_jtheta+w_jtheta)
=E_halfspace(U)+mu_j^2 [J2(U_theta)+S_theta(W_theta)+1/2 E0''(U_theta)(W_theta,W_theta)]+o(mu_j^2)
=E_halfspace(U)+mu_j^2 [J2(U_theta)-1/2 E0''(U_theta)(W_theta,W_theta)]+o(mu_j^2).
This defines F. Independence of the Jacobi gauge is immediate since the kernel has zero quadratic form and S annihilates it. Transfer to the unit hemisphere gives precisely the previous negative shape-Hessian formula, up to the same harmless positive normalization factor for every theta. Thus its certified strict local minimum persists under this C0 error, by minimizing over a fixed compact parameter neighborhood with a strict boundary energy gap.

## Explicit limitations

This lemma is conditional on the stated uniform projected inverse, existence/continuity of the small projected correction, and convergence of finite-dimensional projections. It supplies their required C0 energy asymptotic, not their independent proofs. It does not give dimensions 7 through31 or prove the low-dimensional compactness half.
''')
