# Every finite boundary is attained (conditional only on the classical EDGE decomposition theorem)

Let q_r=(r-1)/r. Simonovits's standard linear-forest decomposition theorem yields the following slope-spectrum consequence:

If chi(H)=r+1 and ex(n,H)<=t_r(n)+a n+O(1) for some a<1/r, then there is a number b in
  {0} union {(k-1)/(kr): k=2,3,...}
such that ex(n,H)=t_r(n)+b n+O_H(1).

Reason: H must embed the one-universal-vertex Turan construction, since that has surplus n/r-O(1), so H has a chromatic-critical vertex. H must also embed a Turan graph with disjoint sufficiently long cycles in one part; on at most |H| vertices the internal edges used form a linear forest. Thus the classical decomposition theorem applies. Its finitely many exceptional vertices can be assigned to a missed Turan part; a vertex missing a positive fraction of another part can be replaced, simultaneously with the other such exceptions, by an ordinary vertex, gaining a linear number of edges and losing only boundedly many. Absorb the bounded defect neighborhoods into the exceptional set. Every bulk part is then a union of bounded symmetric connected components, with complete cross edges. A repeated connected component containing a cycle has edge/vertex ratio at least one, and could be repeated by itself in a Turan part to create an H-free construction with surplus at least n/r-O(1), contradiction. Hence all repeated nontrivial components are trees. Two bulk parts with nontrivial repeated trees give surplus at least n/r-O(1), likewise impossible. In the sole possible active part, an extremizer repeats a largest-order admissible tree, of order k: a smaller tree type has strictly smaller edge/vertex ratio and can be replaced by the more efficient type because its multiplicity is already unbounded and H is fixed. Its density is (k-1)/k. The active part has n/r+O(1) vertices. Bounded exceptions affect O(1) edges. This proves the slope assertion.

Consequently, using the team's verified construction showing 1/r belongs to S_r for r>=3 and 1/4 belongs to S_2, each S_r is a nonempty upward-closed CLOSED ray [alpha_r,infinity). Indeed, if alpha_r<1/r, witnesses with a tending down to alpha_r have actual slopes b from the displayed discrete set, whose only accumulation point is 1/r. A locally finite set has its infimum attained. If alpha_r=1/r it is attained by the explicit construction. The case alpha_r=0 is also locally isolated, since the smallest positive displayed slope is 1/(2r).

In particular S_2 is either [0,infinity) or [1/4,infinity). For r>=3, the unknown threshold is either 0, one of (k-1)/(kr), or 1/r.

WARNING: This does NOT determine alpha_r. It is a rigorous structural reduction of the boundary question, not a complete solution.
