# Agent 3: verified reductions and discarded shortcuts

## Projection reduction
Let d_n=a_{n+1}-a_n, so 0<=d_n<=1 and finite sums are <=1.
For 0<eta<=1 put t=eta/2 and p_n=1_(t,1](d_n), using AW* spectral calculus.
The commuting scalar functional-calculus inequalities give
  d_n <= t*1+(1-t)*p_n,  p_n <= d_n/t.
Thus monotonicity and abelian linearity yield
  tau(p_n) >= (eta-t)/(1-t)=eta/(2-eta),
and every finite sum of p_n is <=(2/eta)*1.
The missing main theorem is that such a bounded projection Bessel family cannot
have uniformly positive dimension in a finite AW* factor. We did NOT prove it.

## Binary pinching preserves q on projection inputs
For projections e,P, with f=1-e,
  q(ePe)=q(PeP), q(fPf)=q(PfP)
by q(x*x)=q(xx*), applied to eP,fP. The two right-hand positive elements
commute because PeP+PfP=P. Therefore
  q(ePe)+q(fPf)=q(P).
This uses only the stated axioms, not nuclearity or an external trace theorem.
No analogous identity for arbitrary positive inputs was established.

## Maximal plateau with invertible common support is impossible
Assume 0<=a,b,h=a+b<=1 and q(a)=q(b)=q(h)>0. Order implies spectral-tail
dimension domination. Equality of the integrated tails then forces equal
spectral distributions. Their support projections are equal, say p.
If h>=delta*p, equal distributions force b>=delta*p. Thus
  q(h)>=q(a+delta*p)=q(a)+delta*q(p)>q(a),
contradiction. General h can have arbitrarily bad lower spectral tails, and
we have NOT justified passing from this invertible case to the general case.

## Obstruction to norm-disjointization
For vertices i of a complete graph, let P_i on l2(edges) project onto edges
incident to i. Then sum_i P_i=2I, but ||P_i P_j||=1 for every pair.
Finite exact models checked in agent3_projection_checks.py. Thus bounded
positive sums do not imply a norm-almost-orthogonal subsequence.

## Obstruction to spectral-tail envelopes
The rational matrices in agent3_spectral_tail_obstruction.py form a bounded
increasing sequence a_n converging in norm to diag(3/4,1/4). Each has one
eigenvalue above 1/2 and one below; adjacent matrices do not commute.
Their high spectral lines are distinct, so every tail's high-projection join
is I. Spectral suprema of tails followed by a spectral infimum therefore do
not recover the ordinary supremum, even in M2(C).

## State-space ccc is NOT available
An uncountable Clifford II1 factor contains anticommuting self-adjoint
unitaries s_i. For p_i=(1+s_i)/2,
  ||p_i+p_j||=1+1/sqrt(2)<1.8.
The nonempty weak*-open state slices {phi:phi(p_i)>.9} are pairwise disjoint.
Thus finite factors' projection-ccc does not imply their state spaces are ccc.

## Files
- agent3_projection_checks.py: exact integer graph-projection identities and
  symbolic spectral-cutoff bound, executed successfully.
- agent3_spectral_tail_obstruction.py: 30 exact rational ordered-pair and
  commutator checks, executed successfully.

No claim that these auxiliary results determine G or close the main proof.
