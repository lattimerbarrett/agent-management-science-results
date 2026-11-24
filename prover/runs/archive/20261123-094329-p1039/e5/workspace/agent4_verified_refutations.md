# Verified Hénon-basin counterexamples to speculative lemmas

Let a=1/4 and n>=2. Define the polynomial automorphism
H(z1,...,zn)=(z1^2+a zn,z2^2+a z1,...,z_{n-1}^2+a z_{n-2},a z_{n-1}).
Its inverse is obtained recursively from the last coordinate backwards.
The linear part A is a times a cyclic unitary permutation, so ||A||=a.
The quadratic remainder N satisfies ||N(z)||<=||z||^2.

On B(0,1/16), ||H(z)||<=q||z||, q=5/16. Therefore
h_k=A^{-k}H^k converges locally uniformly, since
||h_{k+1}-h_k|| <= a^{-1}(q^2/a)^k ||z||^2
and q^2/a=25/64<1. Its limit h has Dh(0)=I and hH=Ah.
The local conjugacy extends injectively to the full attracting basin
Omega = {z : H^k(z)->0}. It is onto C^n: for any y, take k large
so A^k y is in the local image of h, then apply H^{-k}.
Consequently Omega is a Fatou-Bieberbach domain.

Put r=max_{j<n}|zj|. If r>=max(2,|zn|), a coordinate attaining r
has next first-(n-1)-coordinate modulus at least r^2-r/4>=7r/4,
whereas the next last coordinate has modulus at most r/4.
This cone is invariant and escaping. Hence
Omega subset { max_{j<n}|zj| < max(2,|zn|) }.

Scale the first n-1 coordinates by epsilon=1/(4 sqrt(n-1)), leaving
zn unchanged, obtaining another Fatou-Bieberbach domain Omega'.
Then Omega' subset D={||z'||^2 < 1+|w|^2} and
Omega' intersection {w=0} subset {||z'||<1/2,w=0}.

For n>=3, Omega' contains NO ambient-closed analytic hypersurface
through 0: intersection of such a hypersurface with {w=0} would be a
nonempty closed analytic set of dimension >=n-2>=1, bounded by the
last displayed bound. Positive-dimensional compact analytic sets in
a Euclidean space do not exist (maximum principle).

Likewise, for K0={||z'||=1,w=0}, 0 belongs to the rational hull of K0.
Indeed, any polynomial vanishing at 0 either vanishes identically on
{w=0}, or has a positive-dimensional zero set there through 0.
That zero set has an unbounded connected component through 0 and thus
meets the unit sphere. Yet K0 is disjoint from Omega'.

Thus, in n>=3, complements of Fatou-Bieberbach domains need NOT avoid
rational hulls of their compact subsets. A proof for Oka complements
cannot replace the Oka hypothesis by individual full-rank domination.

The symbolic inverse/determinant/contraction identities have been checked
in agent4_indefinite_ball_refutation.py. Analytic convergence and dimension
arguments above are mathematical proofs, not claims of numerical checks.
