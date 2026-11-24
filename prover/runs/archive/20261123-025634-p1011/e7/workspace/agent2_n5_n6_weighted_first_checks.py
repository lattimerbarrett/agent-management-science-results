import sympy as s
from pathlib import Path
n=s.symbols('n',integer=True,positive=True)
beta=s.symbols('beta')
# Laplace r^beta and t*r^beta in ambient dimension n.
assert s.expand((4-n)*((4-n)+n-2)+2*(n-4))==0
assert s.expand((3-n)*((3-n)+n)+3*(n-3))==0
for N in [5,6]:
    p=s.Rational(N+2,N-2)
    source=(2-N)*(p-2)+2*(3-N)
    assert source<=2-N
    # On outer sphere r=delta/epsilon, weighted boundary data scales as R^-2.
    assert (N-4)+(2-N)==-2
    # Kelvin transform growth is rho^-2, milder than fundamental rho^(2-n).
    assert -2>2-N
print('Weighted first-correction barrier identities and decay exponents verified n5,n6.')
Path('workspace/agent2_n5_n6_weighted_first_checks.py').write_text(Path(__file__).read_text())
Path('workspace/agent2_n5_n6_weighted_first_approximation.md').write_text(r'''# Weighted first-order approximation for isolated simple boundary bubbles, n=5,6

## Hypotheses and conclusion

Let n=5 or6. Work in uniformly smooth locally Euclidean charts at boundary maxima p_i, with origin p_i and tangent plane t=0. A local flat Mobius normalization can ensure H(p_i)=0 while preserving u's tangential criticality and value: take the normal component of the Mobius factor's gradient, and zero tangential gradient. The chart boundary is t=h_i(z), with
h_i(z)=f2_i(z)+O(|z|^3), tr D^2 f2_i=0,
and all graph derivatives uniformly bounded. Put M_i=u_i(p_i), epsilon_i=M_i^(-2/(n-2)), and v_i(y)=M_i^(-1)u_i(epsilon_i y). Assume
v_i -> U=(1+|y|^2)^(-(n-2)/2) locally in C2,
v_i(y)<=C(1+|y|)^(2-n) for |y|<=delta0/epsilon_i.
These are exactly the local bubble convergence and isolated-simple strong decay hypotheses, NOT conclusions of this lemma.

Let Phi2_i be the physical Jacobi correction for the tracefree quadratic f2_i,
(Delta+n(n+2)(1+r^2)^(-2))Phi2_i=0,
partial_t Phi2_i=-(n-2)f2_i(z)(1+|z|^2)^(-n/2),
chosen orthogonal to the bubble kernel. The tangential angular degree2 coercive construction gives
|D^k Phi2_i|<=C(1+r)^(3-n-k), k<=3,
Phi2_i(0)=0 and tangential gradient Phi2_i(0)=0.
For every sufficiently small fixed delta>0 there is C_delta such that, writing R_i=delta/epsilon_i,
|v_i-U-epsilon_i Phi2_i|<=C_delta epsilon_i^2(1+r)^(4-n),
|D(v_i-U-epsilon_i Phi2_i)|<=C_delta epsilon_i^2(1+r)^(3-n),
through the curved halfball r<R_i. The correction is evaluated using a fixed smooth extension across the tangent plane when needed.

## Correction decay and extension

The quadratic correction has leading harmonic degree3-n at infinity, determined by its homogeneous Neumann datum of degree2-n. Subtracting a cutoff version of that homogeneous solution leaves an energy-dual residual, solvable by angular degree2 coercivity. Kelvin comparison and annular estimates give the displayed derivative decay. This is the same explicit-parametrix method used in agent2_n5_n6_local_coefficients.md; here n>4, so the original correction already has finite energy.

Extend Phi2 smoothly across t=0 by a linear combination of reflected copies Phi2(z,-kt), choosing coefficients to match derivatives through order2. Weighted derivative bounds persist. Since its Jacobi equation holds exactly up to the plane and the extension is C2, its Jacobi residual in the lower strip is O(|t|(1+r)^(-n)). On the scaled curved domain's part below the tangent plane, |t|<=C epsilon_i r^2; multiplication by epsilon_i therefore gives a bulk error <=C epsilon_i^2(1+r)^(2-n).

## Error equation and source bounds

Let w0_i=U+epsilon_i Phi2_i and e_i=v_i-w0_i. Since |Phi2_i/U|<=C(1+r), choosing delta small ensures w0_i>=U/2 throughout r<R_i. The exact nonlinear difference can be written
(Delta+a_i(y))e_i=F_i,
where 0<=a_i<=C(1+r)^(-4), and a_i converges locally to n(n+2)(1+r^2)^(-2). Use the divided difference between v_i and w0_i to define a_i. This includes the nonlinear e_i terms in the operator, not in an unjustified perturbative remainder.

The purely first-correction nonlinear remainder is bounded by C epsilon_i^2 U^(p-2)Phi2_i^2 because p=(n+2)/(n-2)>=2 in dimensions5,6 and epsilon_i|Phi2_i|<=CU. Its decay exponent is (2-n)(p-2)+2(3-n)<=2-n. Together with the extension-strip estimate this proves
|F_i|<=C epsilon_i^2(1+r)^(2-n).
On the curved boundary, the first Robin defect of U is canceled by epsilon_i Phi2_i. The next graph jet gives epsilon_i^2(1+r)^(3-n). Evaluating Phi2 at t=O(epsilon_i r^2), changing the normal by O(epsilon_i r), and the mean-curvature contribution each have the same bound by the derivative estimates. Thus
(partial_nu+2c_n H_scaled)e_i=G_i,
|G_i|<=C epsilon_i^2(1+r)^(3-n).
The scaled slope is O(epsilon_i r)<=Cdelta; scaled H times r is O(delta), and even O(delta^2) under H(p_i)=0. All source bounds hold also near0 with1+r in place of r.

At the outer spherical boundary, strong decay and correction decay give |e_i|<=CR_i^(2-n). At the center e_i(0)=0 and its tangential gradient is zero, since v_i(0)=U(0)=1, the point is a boundary maximum, and the degree2 correction vanishes to second tangential order there.

## Weighted inverse by contradiction

Set E_i=sup_(r<R_i) (1+r)^(n-4)|e_i|. Suppose E_i/epsilon_i^2 tends to infinity. Normalize q_i=e_i/E_i. The normalized sources tend to zero in all fixed local norms. Boundary elliptic compactness yields a global regular Neumann Jacobi solution q on Rn_+, satisfying |q|<=C(1+r)^(4-n), q(0)=0, tangential gradient q(0)=0.

This mild-decay Jacobi solution is in fact a standard bubble kernel element. To see why energy nondegeneracy applies despite the initially weak decay, transfer to the hemisphere and reflect evenly across the equator near its north pole. The transformed function grows at most rho^(-2), strictly slower than the fundamental rho^(2-n) singularity for n>4. For (Delta_S+n)q=0 such a point singularity is removable: subtract a local Newton potential of its integrable bounded-potential source, remove the harmonic part by the sub-fundamental growth bound, then bootstrap the gained two powers to smoothness. Hence the hemisphere solution is smooth and belongs to its degree1 eigenspace. The center value kills the scale mode and the tangential gradients kill all translations. Therefore q=0 and q_i ->0 on compact sets.

It remains to exclude a weighted maximum escaping infinity. On an exterior curved halfannulus use
B(y)=C r^(4-n)-D t r^(3-n), C>D>0.
The exact identities are
-Delta r^(4-n)=2(n-4)r^(2-n),
Delta(t r^(3-n))=-3(n-3)t r^(1-n),
and partial_nu(-t r^(3-n))=r^(3-n) on the flat plane. Choose C large relative to D, then choose the inner radius large so a_i B is absorbed, and finally delta small so boundary-slope and Robin errors are absorbed. Thus B is a positive supersolution dominating bulk sources of weight r^(2-n) and boundary sources of weight r^(3-n). Its scaled multiples also dominate data on the inner and outer spheres.

After dividing by E_i, inner data vanish by local convergence. The outer weighted data are at most C R_i^(-2)/E_i=C_delta epsilon_i^2/E_i ->0. The source coefficients epsilon_i^2/E_i also tend to zero. The maximum principle on this exterior annulus is valid for the linearized operator despite its positive potential: the positive supersolution B gives the ground-state transform, including its nonnegative Robin boundary term. Comparison implies sup weighted |q_i| ->0 outside the fixed inner radius, contradicting the normalization E_i. This proves the weighted C0 estimate. Run the C0 argument first with outer radius2delta/epsilon_i, taking2delta<delta0; annular interior/boundary estimates on its interior half then yield the stated gradient bound all the way throughdelta/epsilon_i. This avoids assuming any derivative control on the artificial outer Dirichlet sphere.

## Scope

This proves a genuine annular first-order estimate conditional on isolated-simple decay. It does not establish selection or simplicity. In dimension5 it is the main error-control input for the quadratic Pohozaev expansion. In dimension6 one still must extract the cubic logarithmic contribution, absorb even second-order quadratic interactions, and explicitly match the nonlinear Pohozaev identity. Those final sign calculations are not claimed here.
''')
