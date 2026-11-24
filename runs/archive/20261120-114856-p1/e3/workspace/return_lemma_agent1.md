# Return-map lift lemma (conditional; not yet applied)
Let F be a continuous iteration on an open physical state space. Suppose a
cross-section has coordinates Phi(r,u) for 0<r<r0 and u in a neighborhood
of u0 in R^d, all representing physical nonterminating states. Suppose its
first-return map P is defined there whenever the orbit remains in this
coordinate neighborhood. Assume:
1. P extends C^1 to a neighborhood of (0,u0), P(0,u0)=(0,u0).
2. DP(0,u0) is hyperbolic, has exactly one stable eigenvalue 0<a<1,
   and its stable eigenvector has nonzero r-component.
3. A neighborhood of the half stable eigenray r>0 lies in the physical
   coordinate domain. The reconstructed missing spectral weights are
   strictly positive for r>0; for example w_j=r^{alpha_j} c_j(u), c_j>0.
4. Every sufficiently small physical return segment visits two fixed
   disjoint closed sets U,V of normalized residual directions, with
   dist(U,V)>0.
Then F has a nonterminating orbit whose normalized residual directions do
not converge.

Proof. The local stable manifold theorem gives a C^1 curve W^s through
(0,u0), tangent to the stable eigenvector, with P(W^s) subset W^s locally.
The nonzero radial tangent gives a half-curve with r>0. Assumption 3 makes
all points on this half-curve physical; shrinking it gives 0<r(Pz)<r(z)
and keeps its entire forward return orbit in the chart. Thus its infinitely
many return segments exist. Their physical iterates are nonterminating,
by the definition of the chart and return map. Assumption 4 supplies
infinitely many iterates in each of U,V, so their normalized directions
cannot converge. No finite-time or floating-point trajectory is used.

Stable manifold theorem can here be replaced by a direct Banach argument.
After a linear coordinate change P(x,y)=(a x+f(x,y), B y+g(x,y)),
||B^{-1}||<1, Df(0)=Dg(0)=0. Prescribe small x_0>0, choose a<theta<1,
and solve on theta-weighted sequence space:
 x_k=a^k x_0+sum_{j<k} a^{k-1-j} f(x_j,y_j),
 y_k=-sum_{j>=k} B^{k-1-j} g(x_j,y_j).
On a sufficiently small ball the right side is a contraction (geometric
series bounds), producing a decaying orbit. Its initial points form the
stable curve. The physical half is selected by its nonzero radial tangent.

## What is still missing
This is a lemma, not a counterexample. A valid application must explicitly
supply Phi, the limiting seed/phase return map, a fixed point u0, spectral
bounds, physical positivity, and uniform existence of the entire return
itinerary. A contracting eigenvector of a 2x2 endpoint-scattering product
alone does NOT supply these seed/phase conditions.
