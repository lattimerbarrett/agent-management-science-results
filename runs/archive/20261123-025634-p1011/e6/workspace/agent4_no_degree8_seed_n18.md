# No degree-at-most8 polynomial graph seed in ambient dimension18

This is a theorem about the specific second-order one-bubble graph reduction,
not about all Yamabe solutions and not a refutation/proof of the requested
classification. It exhausts an otherwise tempting but unsuccessful seed class.

Let n=18, m=17. For a real polynomial P on R17 of degree<=8, define F_P(eps,xi)
as the quadratic corrected halfspace bubble energy for the graph perturbation
aP, divided by a^2. Its existence follows from n>2deg P and the flat-graph,
projected inverse, and reduced-energy lemmas already proved. The normalization
is F=-C_n B/2, with C_n>0 and B the hemisphere source/response pairing.
Let
 G=span{1,x1,...,x17,|x|^2}.
Then for every P outside G,
 partial_eps F_P(eps,xi)<0 for all eps>0, xi in R17.
For P in G the quadratic reduction vanishes identically.

## Proof

Translate the polynomial: P_xi(y)=P(xi+y). Fischer decomposition yields
 P_xi(y)=sum_(q,alpha) sum_i c_(q,alpha,i) |y|^(2i)H_(q,alpha)(y),
where H_(q,alpha) is a real orthonormal basis of homogeneous harmonic degree-q
polynomials restricted to S16. The index range is q+2i<=8. Rotational symmetry
of the halfspace linearized problem makes different (q,alpha) sectors
orthogonal in B. Within a sector let Q_q be the radial Gram matrix computed
from the exact Jacobi/hemisphere Dirichlet-to-Neumann series.

Under bubble scale eps, normalize x'=xi+eps y', t=eps y_n. The effective graph
is eps^-1P(xi+eps y'), so the coefficient of its degree-(q+2i) term becomes
 v_i=eps^(q+2i-1)c_(q,alpha,i).
Consequently
 F_P(eps,xi)=-C_n/2 sum_(q,alpha) v^T Q_q v,
 eps partial_eps F_P=-C_n sum_(q,alpha) v^T K_q v,
 (K_q)_ij=(q+i+j-1)(Q_q)_ij.
The q0 indices i0,i1 and q1 index i0 are gauge null directions, including all
cross-pairings. In the hemisphere picture these graph variations have only
spherical degrees0,1: degree1 has zero mean-curvature forcing; degree0 has
linear response with zero boundary value. Thus they contribute nothing to B.
They are precisely the polynomial subspace G.

For every remaining index block q=0,...,8 the matrix K_q is strictly positive
definite. This is established by the exact executable certificate
`agent4_exact18_blocks.py`, which analytically sums the rational-in-k series
by partial fractions and checks all Sylvester principal minors as exact
positive rational numbers. It uses the independently audited generic formula
from agent2's even-dimensional checker, not a floating eigensolver or a
truncated series. Full rational minors are saved in agent4_exact18_results.txt.

Hence the displayed scale derivative is strictly negative whenever P_xi is
not in G. Since G is invariant under translations, P outside G implies P_xi
outside G for every xi. Scaling eps>0 never kills a nonzero coefficient, so
at least one strictly positive quadratic contribution remains. This proves
the theorem. If P in G, all contributions are gauge and F=0.

On a compact parameter set the strictly negative derivative is bounded away
from0. The C1 reduced-energy expansion then shows that sufficiently small
polynomial-core perturbations in this class have no associated one-bubble
critical point with parameters in that compact set. This does NOT rule out
other geometric regimes or supply the missing unrestricted compactness
analysis; it only identifies a fully exhausted construction ansatz.
