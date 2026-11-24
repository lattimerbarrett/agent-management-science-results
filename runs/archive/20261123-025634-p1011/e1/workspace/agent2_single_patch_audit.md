# Independent audit of agent1_single_patch_audit.md

All eight steps were checked. No fatal flaw identified. This is an audit of
a proposed noncompactness construction, NOT a proof of the user's demanded
empty-set conclusion.

1. Highest-degree physical graph derivative bound epsilon*rho^(8-k) tends
   to zero for every fixed k when rho=1/log(1/epsilon). Disjoint patches can
   preserve exact spherical boundary regions at all future chosen centers.
2. Exact graph Robin formula agrees with directly computed normal/mean
   curvature formula. Its linear part and cubic error are valid; n19 tail
   norm exponent is -3/2. I independently derived the exact residual in Slack.
3. Uniform inverse is obtained by coercivity outside concentration, hemisphere
   Jacobi kernel classification inside concentration, and potential-tail
   integrability. A negative bubble eigenvalue does not obstruct an inverse;
   only zero modes are projected out. Graph slope and curvature form norms
   are O(delta), sufficient for perturbation.
4. Positive-part nonlinearity is C1 from H1 to dual for p=21/17>1 and has
   remainder O(||phi||^p); contraction and C1 parameter dependence follow.
5. Direct SymPy check in agent2_shape_energy_cancellation.py verifies the
   all-dimensional exact first-energy-variation identity. Fixed U is even
   in normal coordinate, including tangential translations and positive
   dilations; pure graph energy therefore has no quadratic term. Degree8
   cubic integrand grows as r^3, yielding mu^3 R^4=o(mu^2).
6. Exact normalized graph profile is Omega(t)*F(xi+lambda*t)/lambda,
   Omega=2/(1+|t|^2), up to common radius1/2 factor. Hence homogeneous degree
   d terms have lambda^(d-1), agreeing with certified shape Q. Translation
   coordinates used in certificate differ by positive scaling xi=lambda*zeta,
   preserving Hessian definiteness at centered critical point. L0 shape
   contribution is zero because its Jacobi correction is normal coordinate,
   which has zero boundary trace. L1 forcing vanishes. Higher modes have
   positive inverse DN, as independently ODE-checked by me.
7. Strict local maximum of Q gives an interior minimum of J_red using only
   uniform C0 expansion; J_red is C1 and thus stationary at that minimum.
   Corrected parameter Gram remains nonsingular. Positive-part equation
   implies u>=0 by testing u_-; Hopf and strong principles imply u>0. Trace
   critical norm on a cap gives exact boundary blowup lower bound without
   requiring weighted pointwise estimates.
8. Packet energy gap and projected inverse persist under sufficiently small
   later C^(4,alpha) graph changes, for each fixed epsilon. The diagonal
   persistence argument in agent2_diagonal_persistence.md proves a fixed
   smooth limit domain retaining all high-peak packets. Euclidean flatness,
   positive type from H>0, connected ball topology, and nonhemisphere from
   nonzero tracefree II all persist.

Checks I executed independently:
- radial PDE / Green Pohozaev / halfspace ADM constants;
- n19 hemisphere DN ODE for six modes;
- exact rational interval/tail negativity of auxiliary weighted form;
- genuine leading Green angular correction, plus slow-decay mass ambiguity;
- first shape-energy cancellation in arbitrary symbolic n.

An exact finite-dimensional maximum alone is not a theorem counterexample.
The above audit also checks the analytic links needed to realize it; these
must be stated with their function spaces and estimates in any final proof.
No verified citation for the asserted empty-set theorem has been supplied.
