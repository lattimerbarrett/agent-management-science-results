# Conditional fixed-domain construction via Baire category

This note proves an abstract topological step. It does not assert the required
one-bubble PDE insertion lemma, and in particular does not prove the requested
dimension threshold.

Let q be a point on the round sphere S^(n-1), and let A be a closed neighborhood
of another point, disjoint from q. Let X consist of C-infinity real functions f
on S^(n-1) whose entire jet vanishes at q and whose restriction to A is a fixed,
small, nonumbilic graph f_*. With its usual C-infinity topology X is a closed
affine Frechet subspace of C-infinity(S^(n-1)), hence completely metrizable.
Choose f_* small enough that X contains a strictly convex graph. Let U be a
nonempty C^2-open subset of X consisting of strictly convex embedded graphs.
It is a Baire space. Euclidean metrics on the corresponding domains are LCF,
positive Yamabe type, and not conformal to a hemisphere (the fixed nonumbilic
patch excludes that).

For N a positive integer, define P_N as the subset of U admitting a positive
solution with boundary maximum>N, obtained by a reduced finite-dimensional
strict interior minimum with an energy barrier. Assume:

(I) P_N is open in U. It is enough that the projected inverse and reduced
    energy depend continuously on the smooth domain, since a strict barrier
    persists under uniform perturbation. No nondegeneracy of the exact solution
    is required.
(II) If a domain has a round boundary patch, then a degree-eight local graph
     insertion can produce a member of P_N by an arbitrarily small perturbation
     in any prescribed finite collection of C^k seminorms.

Then each P_N is dense in U. Indeed, every f in X is flat at q. For centers
q_j tending to q, choose balls B_j centered at q_j, of radius comparable to
its distance from q, and disjoint from q and A. Replacing f by zero on a smaller
concentric ball with a standard cutoff changes any prescribed finite C^k norm
by o(1): flatness gives |D^a f|=O(dist(q_j,q)^L) for arbitrarily large L,
while cutoff derivatives cost only inverse powers of the ball radius. The
modified domain has an exactly round patch. Apply (II), still within the
prescribed neighborhood. The perturbation is supported away from q and A,
so it remains in X, and sufficiently small C^2 changes preserve U.

By Baire's theorem, intersection_N P_N is nonempty. Fix one element f in it.
For each N choose its positive solution u_N. Then max_boundary u_N>N on one
fixed smooth domain with all required geometric properties.

# Local insertion scaling bookkeeping

Let h be a degree-eight polynomial of the form H_2(z)p(|z|^2), where H_2 is
harmonic quadratic and p has degree three. Insert

  b_(mu,lambda,rho)(x) = mu*lambda^8*chi(x/rho)*h(x/lambda),  lambda<=rho.

For each fixed K, product differentiation gives

  ||b||_(C^K) <= C_K mu rho^(8-K).

Indeed its four homogeneous components have coefficients
mu*lambda^(6-2j), degrees 2+2j, j=0,1,2,3. After cutoff differentiation each
is bounded by C_K mu lambda^(6-2j)rho^(2+2j-K), at most
C_K mu rho^(8-K). Thus mu can first be made arbitrarily small to meet every
prescribed finite C^K budget, independently of the later lambda choice.
The shape amplitude seen at bubble scale is t=mu*lambda^7. A background
cutoff/mass energy O(lambda^(n-2)) is o(t^2) precisely when

  lambda^(n-16)/mu^2 -> 0.

For any fixed mu>0 this can be enforced by lambda->0 whenever n>16.

Important: this topological/scaling argument has no cutoff at dimension20.
Together with the currently certified n19 formal strict minimum, it highlights
why the genuine PDE insertion lemma or the claimed compactness premise still
needs careful resolution.
