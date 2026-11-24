# Trapping lemma at a non-neutral minimal-support cycle

Let F be the normalized monic degree-s residual map, and G=F^2. Suppose y_k is a nonterminating orbit and u is an omega-limit point of the even subsequence. Suppose S=supp(u) has s+1 distinct eigenvalues and, for each j outside S, the two-step multiplier L_j(u) is not 1. Then the full even subsequence converges.

Proof. All constructions are restricted to the finite set of eigenspace directions present initially. At u, H>0. Thus q_y, H(y), F(y), and the diagonal multipliers L_i(y) in G(y)_i=L_i(y)y_i are analytic in a neighborhood U of u. On the face supported by S, G is exactly the identity, by the barycentric reciprocal formula. Write w_i=y_i^2. The weight map G_w is analytic in w there and its restriction to that face is the identity. Shrinking U, there exist constants c,C>0 such that

(1) |L_j(y)-1|>=c for j outside S;
(2) sum_{i in S}|G(y)_i^2-y_i^2| <= C sum_{j outside S} y_j^2;
(3) L_i(y)>0 for i in S.

Combining (1) with G(y)-y yields sum_{j outside S} y_j^2 <= c^{-2} ||G(y)-y||^2, for y in U. Hence, while successive even iterates remain in U, their active weights have total variation bounded by C c^{-2} times the sum of squared even steps.

The general Lyapunov identity gives sum_k ||y_{2k+2}-y_{2k}||^2<infinity. Thus its tail tends to zero, and individual even steps tend uniformly to zero. On late visits to U, (1) also shows all inactive coordinates are uniformly small. Choose a closed active-weight box B about u, with signs of active coordinates fixed, whose corresponding small inactive-coordinate neighborhood lies in U, and a strictly smaller concentric box B0. Since u is an omega point, there are arbitrarily late visits to B0. After such a visit, the tail squared-step sum is smaller than the active-weight distance from B0 to the boundary of B, divided by C c^{-2}. Consequently no first exit through an active-weight face of B is possible. No first exit through an inactive-coordinate face is possible either, since within U the inactive coordinates are bounded by c^{-1} times the next even step, which is uniformly arbitrarily small at late times. Active signs cannot change, by (3). Therefore the orbit stays in U thereafter.

Now sum of inactive weights is finite and active weights have finite total variation. Inactive coordinates tend to zero, active weights converge, and active signs are eventually fixed. The even vectors therefore converge. QED.

Corollary. If the even sequence fails to converge, every minimal-support omega point has at least one inactive eigenvalue with multiplier +1. This is a global trapping conclusion, not merely a conditional statement assuming the omega set is already local.
