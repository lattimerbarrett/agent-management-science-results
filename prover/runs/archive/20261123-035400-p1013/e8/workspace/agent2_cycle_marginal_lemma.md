# Coarse cycle edge-marginal lemma (r>=3)

Let r>=3. There are positive constants eps_0,c,C,delta depending only on r
such that the following holds for all sufficiently large n. G has an
r-partition with n_i=n/r+o(n), each vertex misses at most eps_0*n cross edges,
and maximum internal degree o(n). For uniform choice among all simple cycles,

* every present edge e has probability at most C/n of lying on the cycle;
* every present CROSS edge has probability at least c/n.

The o(n) hypotheses can be replaced by sufficiently small fixed multiples
for the upper bound and by total internal edges o(n^2) for the lower bound.

1. Long cycles dominate. Fix delta>0 small compared with 1-2/r, and
   eps_0 << delta/r. Build cycles greedily following the periodic class word
   1,2,...,r, of length ell=floor((1-delta/2)n/r)*r. At every step there
   remain at least delta*n/(4r) available vertices in the next part; for the
   last step enforce adjacency to the initial vertex too, losing only a
   second eps_0*n candidates. Thus there are at least
   (delta*n/(4r))^(ell-O(1))/(2n) cycles. The number of cycles of length at
   most (1-delta)n is at most n^(floor((1-delta)n)+1). Their fraction is
   superpolynomially small.

2. Upper edge probability. For a long cycle containing uv, orient it with
   u->v. Choose another oriented cycle edge x->y and replace uv,xy by ux,vy,
   reversing the intervening path. This is one simple cycle. If u,v have
   different parts i,j, at least ell-n_i-n_j-O(eps_0*n) choices have ux,vy
   present CROSS edges. If u,v lie in the same part i, at least
   ell-2*n_i-O(eps_0*n) edges have both endpoints outside i and give valid
   switches. Both counts are Omega(n). Conversely a resulting cycle has at
   most four preimages, determined by its neighbors of u and v. Hence
   c_uv <= C*c(G)/n, including the negligible short cycles.

3. A fixed vertex is omitted only O(1/n) of the time. If a long cycle omits
   u, the number of cycle edges with BOTH endpoints adjacent to u is at
   least 2|N(u) intersect V(C)|-ell >= (1-2/r-3delta-O(eps_0))*n.
   Inserting u at any such edge produces a cycle containing u. Removing u
   recovers the original cycle uniquely. Thus c_not_u <= O(c_u/n), apart
   from negligible short cycles.

4. Almost all cycles have o(n) internal edges: by (2), the expected number
   is <=C*e_internal/n=o(n). For any fixed small gamma>0, cycles with
   >gamma*n internal edges form an o(1) fraction.

5. Lower CROSS-edge probability. Fix a present cross edge uv. Start with a
   long cycle C which contains u,v, does not already use uv, and has at most
   gamma*n internal edges. These comprise 1-o(1) of all cycles unless the
   desired lower bound is already true. Orient C as
       u->a ... v->b ... u.
   Choose a third edge x->y. If it is in the arc a...v, replace
       ua,vb,xy by uv,ay,bx;
   if it is in the arc b...u, replace them by uv,ax,by.
   Direct inspection of the three path segments shows this is one cycle.

   Write A=part(a), B=part(b). If A=B, every xy with both endpoints outside A
   is color-compatible, and there are ell-2*n_A-O(1)=Omega(n) of them.
   If A!=B, consider the first arc. A CROSS edge x->y is bad only if
   x is in B or y is in A. Three consecutive CROSS edges cannot all be bad:
   bad edges can only descend B -> another class -> A, after which the next
   CROSS edge is good. Thus each run of t cross edges contains at least
   (t-2)/3 good edges. The second arc has the same property with A,B
   interchanged. Internal edges split runs, so the total number of good
   choices is at least ell/3-I(C)-O(1)=Omega(n). Missing edges incident with
   a or b exclude only O(eps_0*n) additional choices. Avoid the O(1) edges
   meeting u,v,a,b. We retain Omega(n) valid switches.

   Conversely from a cycle containing uv there are O(n^2) possible
   preimages: choose the other two new edges, orient them, and undo one of
   the two reconnections. Double counting gives c_uv>=c*c(G)/n.

All switch counts concern unoriented cycles; allowing orientations merely
changes absolute constants. The argument is uniform under adding/deleting
cross edges while their missing maximum degree stays <=eps_0*n, and under
deleting any internal edges.
