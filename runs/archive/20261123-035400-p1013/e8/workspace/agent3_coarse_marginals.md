# Coarse local cycle marginals, r>=3

Fix r>=3. There are eps_r,c_r,C_r>0 with the following property.
Suppose a sequence G has r-partitions with n_i=n/r+o(n), every vertex has
at most eps_r*n missing cross-neighbours, and e_internal=o(n^2).
For a uniformly random simple cycle Z of G, every present edge e satisfies
 Pr(e in Z)<=C_r/n,
and every present CROSS edge satisfies Pr(e in Z)>=c_r/n.
The bounds are uniform under arbitrary internal-edge deletions and cross-edge
additions/deletions that preserve these hypotheses.

Proof of long-cycle dominance. Fix eta>0, then take eps_r sufficiently small
relative to eta (one fixed eta depending only on r suffices below). Put
q=floor(min_i n_i-delta*n), delta=eta/(4r), and use the cyclic part-word
(1,2,...,r)^q. Greedily select distinct vertices in that order. At every
ordinary step there are at least delta*n-eps_r*n choices, because a delta*n
reserve remains in the next part. At the final step insist on adjacency to
both the preceding and the first vertex; these lie in distinct parts from
the final part since r>=3, so at least delta*n-2eps_r*n choices remain.
Thus c(G)>=(delta*n/2)^(rq)/(2n). Since rq>=(1-eta/2)n for small eps_r,
cycles shorter than (1-eta)n comprise exp(-Omega(n log n)) of all cycles,
using the trivial upper bound n^((1-eta)n+1) on their count.

For eps_r small, minimum degree is at least (1/2+2eta)n, choosing eta>0
small in terms of r. On any cycle C of length at least (1-eta)n, a vertex
w outside C has at least eta*n insertion positions: the number of edges of
C whose two ends are neighbours of w is at least
 2|N(w) cap V(C)|-|C| >= 2delta(G)-2n+|C| >= eta*n.
Each resulting cycle has at most one predecessor after deleting w.
Consequently Pr(w not in Z)=O(1/n).

UPPER EDGE BOUND. Orient a long cycle containing uv as u->v. An oriented
edge x->y elsewhere on C can be switched by removing uv,xy and adding
ux,vy. At least
 |N(u)cap V(C)|+|N(v)cap V(C)|-|C|-O(1) >= eta*n
choices are valid; each produces one cycle not using uv. A resulting cycle
has at most four preimages, determined by the neighbours of u and v used
in the reverse switching. Thus Pr(uv in Z)<=4/(eta*n)+superpolynomially-small.
In particular E[e_internal(Z)]<=C_r e_internal(G)/n=o(n). Markov implies
that all but o(1) of all cycles have o(n) internal edges.

LOWER CROSS-EDGE BOUND. Fix cross-edge uv. All but o(1) of cycles contain
u,v, are long, and have o(n) internal edges. If already Pr(uv in Z)>=1/4
there is nothing to prove. Otherwise at least (1/2)c(G) cycles C satisfy
these conditions and omit uv. Orient one such C and write it as
  u-a- ... -v-b- ... -u.
For an oriented edge x->y on the first arc a...v, remove ua,vb,xy and add
uv,ay,bx. On the other arc b...u, add instead uv,ax,by. In BOTH cases the
result is a single cycle on the same vertex set.
Let A,B be the parts of a,b. If A=B, any cross-edge xy with both ends
outside A is admissible at the colour level. There are at least
 |C|-2n_A-o(n) >= (1-2/r-o(1))n
such edges. If A!=B, on the first arc a cross-edge is colour-bad precisely
when x is in B or y is in A. Three consecutive colour-bad CROSS edges are
impossible: a bad edge leaves B or enters A, so a bad run has at most
B->other->A. The same assertion with roles reversed holds on the second
arc. Removing the o(n) internal edges splits the word into o(n) runs;
therefore at least |C|/3-o(n) edges are colour-good across the two arcs.
At most 2eps_r*n candidates fail because ay/bx (or ax/by) is an absent
cross-edge, since the total cross-deficit at a,b is <=2eps_r*n.
For eps_r sufficiently small this leaves >=gamma_r*n switches per C.
Each resulting cycle using uv has at most O(n^2) preimages: select the two
other added edges and their orientations, then the deleted edges are
uniquely determined. Double counting yields Pr(uv in Z)>=c_r/n.
