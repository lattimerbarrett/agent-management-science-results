# Independent audit of agent1_single_patch_audit.md (agent4)

This is an audit, not a claimed proof of the original requested compactness theorem.
No fatal flaw was found in the candidate NONcompactness reduction after the
normalization clarifications below.

## Step 1: geometry
For f_e=e^9 F(x/e)chi(x/rho), deg F<=8, each kth derivative is bounded
by C_k sum_d e^(9-d)rho^(d-k). With rho=1/log(1/e), this tends to zero
for each fixed k. Pullback metrics converge smoothly. A fresh exact spherical
boundary patch can be flattened by a fixed local conformal map before insertion.

## Step 2: source
At n19, d8, the first graph source is O(r^-11) on R18. Its critical
trace-dual exponent is36/19, so it is integrable and its norm tail isR^-3/2.
The exact boundary residual is odd in graph amplitude mu. Nonlinear/linear
pointwise ratio is bounded by delta^2, delta=mu R7=e rho7 ->0.
The cutoff bubble residual at fixed chart radius is O(e^8.5)=o(mu=e8).

## Step 3: inverse
The stated contradiction proof is valid: the background weak limit solves
an invertible positive Robin conformal Laplacian; the rescaled weak limit is
in the half-space bubble Jacobi kernel. Conformal compactification and even
reflection identify this kernel with the n first Neumann spherical harmonics.
Orthogonality removes it. Strong local L2 plus the small L^(n/2) tail of
U^(p-1) gives the contradiction by testing against the normalized sequence.

## Step 4: contraction
For n19, p=21/17 and q=38/17. The positive-part remainder is O(||phi||^p)
in the dual energy norm; its local Lipschitz constant tends to0. Thus phi=O(mu),
and nonlinear energy remainder O(mu^q)=o(mu^2). Transplanting the finite-energy
first correction and using the uniform inverse identifies phi/mu strongly.

## Step 5: fixed bubble energy
A bubble centered on the OLD plane remains even in its normal coordinate,
including for tangential center and scale parameters. For every compactly
supported graph G, pure graph energy is odd in mu. The first variation cancels
by D=(b/2)Delta'(U^2), without assuming G homogeneous. Thus no quadratic pure
shape term occurs. Translated/dilated cutoff degree8 bounds are uniform on a
fixed compact parameter packet. Worst cubic terms have radial density exponent
3, so O(mu^3 R4)=O(e20 rho4)=o(e16). Normal displacement of the actual boundary
center is handled by the nonkernel constant-graph shape correction.

## Step 6: exact profile and constants
For bubble center xi and scale lambda in Euclidean rescaled coordinates, the
unit-sphere conformal factor is Omega=2lambda/(lambda^2+|x-xi|^2). Setting
y=(x-xi)/lambda gives normal shape

eta(y)=mu [2/(1+|y|^2)] lambda^(-1) F(xi+lambda y).

This is exactly the profile entering the spectral shape quadratic. THERE IS
NO angular-degree-dependent 2 factor: Omega=1+z and r=sin(theta)/(1+z).
An earlier suggestion by agent4 of factor2^(1-l) was wrong and was retracted.
The original target-normalized U compactifies to a radius1/2 hemisphere; using
a unit hemisphere changes all energies/shape quadratics by a common positive
constant only. It does not alter critical parameters or Hessian signs.

Our translation certificate uses zeta=xi/lambda, differentiating
lambda^(-1)F(lambda(y+zeta)). At the even centered critical point, converting
to xi multiplies translation Hessian by positive lambda^(-2). Mixed
scale/translation entries vanish by parity. Thus strict full maximality is
unchanged.

## Exact certificate
workspace/agent4_exact_full_hessian.py computes all cross-angular Gram entries
by exact polynomial telescoping and verifies Hessian signs with Fraction+Machin
pi intervals. Root lambda lies in [.951902323,.951902324]. In its zeta parameter,
Hscale in[-.17629396840,-.17629369241],
Hparallel in[-.28156987935,-.28156977858],
Hperp in[-.18010947169,-.18010945685] (multiplicity17).
Independent spectral sums through100000 agree with all exact angular Gram
matrices at relative errors below9e-12. Hence this is not numerical-only.

## Steps 7-8
A strict full Q maximum gives a reduced-action interior minimum from uniform
C0 asymptotics; no higher derivative expansion or PDE nondegeneracy is required.
Parameter derivative matrix is the bubble Gram pluso(1), so reduced criticality
annihilates residual kernel coefficients. Coercivity and positive-part testing
give positivity. Critical trace mass on an e-cap gives boundary maximum
at least c e^-8.5. The resulting robust energy-gap packet is compatible with
agent2's conditional disjoint-support diagonal persistence construction.

## Conclusion of audit
The assembled arguments support the candidate n19 noncompactness mechanism,
not the demanded empty-set conclusion. A fully polished proof would have to
state the function spaces, pullbacks, projections, and uniform parameter
estimates explicitly; but no missing positive term, center constraint, or
normalization obstruction was found. A verified source for the purported
all-dimensional arbitrary-boundary compactness theorem is urgently needed.
