# Audit of agent1_single_patch_audit.md (agent3)

I checked steps 2--7 against the explicit Euclidean and spherical formulas.
No fatal flaw was identified. Specific checks:

- Exact graph Robin defect is odd in the graph amplitude. For degree8,
  the cubic error is bounded by delta^2 times the linear majorant r^-11,
  delta=mu R^7. This majorant is in L^(36/19)(R18), with tail R^-3/2.
- Pure fixed-bubble shape action is odd in graph amplitude. Its linear
  coefficient cancels after integration by parts using D=(alpha/2)Delta U².
  Cubic density at infinity is at worst mu³ r^(3d-n-2)=mu³r³,
  hence integral O(mu³R4). Higher terms have extra factors <=delta².
- Uniform complement inverse and nonlinear contraction are justified in
  agent3_uniform_inverse.md. No positivity/coercivity of the linearized
  bubble Hessian is required; the one negative direction is invertible.
- Residual profile is compatible with Jacobi kernel: after compactification
  it is (Delta_Sigma+m)eta, orthogonal to first boundary harmonics.
- Euclidean standard U compactifies to radius1/2; switching to unit sphere
  adds only a constant positive multiplier to the action/shape quadratic.
- At center eps*xi and scale eps*lambda, the boundary profile in standard
  bubble coordinates is lambda^-1 F(xi+lambda*y). Hence radial coefficients
  c_j lambda^(2j+1) exactly match the certificate. Our center Hessian uses
  zeta=xi/lambda and must be congruence-rescaled by lambda^-2; signs persist.
- Subtracting graph constant/linear terms when recentering on actual
  boundary changes Q by zero: these are the exact plane-motion kernel.
- Strict full maximum of Q gives robust reduced-action local minimum by
  uniform C0 expansion; differentiability suffices for an interior critical
  point. Natural constraint parameter Gram matrix is nonsingular.
- Positive-part nonlinearity and lambda1>0 force actual solution nonnegative;
  strong maximum principle/Robin Hopf force positivity up to boundary.
- Trace Sobolev norm of correction=o1 prevents cancellation of the bubble's
  fixed trace mass on an eps-cap; boundary height >=c eps^-17/2 follows.

Together with independently checked diagonal persistence, these calculations
support a noncompactness construction in n19 rather than the requested
empty-set assertion. No external literature citation has been identified.
One should not claim the asserted empty-set theorem on the basis of a false
local quadratic sign lemma.
