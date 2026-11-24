# Odd n, all even degrees d>=12
This proves the stronger universal bound
 d R_uv <= d(d+15)n/[2(d+1)^2] - d(d^2+4d+15)/[2(d+1)^2]
for every connected simple dregular Eulerian graph. For d>=12 this is strictly below n-278/45, and hence below every required odd-n normalized target.

## A two-connected block inequality
Let H be a simple two-connected graph of order B, maximum degree at most d, and degree deficit Delta=sum_x(d-deg_H(x)). Choose a shortest cycle C containing u,v, of length c. Orient both u-v arcs from u to v. There are no chords within either arc or incident to an endpoint, because any would shorten the cycle while retaining u,v. Chords between arc interiors satisfy: if A_iB_j and A_hB_k exist with i<h,j>k, then h=i+1,j=k+1. Indeed the two cross chords together with the outer pieces of the two arcs form a u,v cycle omitting h-i-1+j-k-1 vertices.

The chord graph on c-2 interior vertices has at most3(c-2)/2 edges. Here is a complete induction for any ordered bipartite graph with this spaced-inversion prohibition. A vertex of degree0 or1 can be deleted, losing at most1 edge. Otherwise every vertex has degree>=2. Its first A vertex and first B vertex must be adjacent: if not, both have two neighbors at positive indices, and the last of those A-neighbors and last B-neighbors give a spaced inversion. Given adjacency, their second neighbors must both have index1, by the same prohibition. Neither can have a third neighbor. Delete the first A and first B, removing exactly3 edges, and continue. Deletion preserves the prohibition.

Each outside vertex has at most3 neighbors on each arc (neighbors farther than2 arc steps apart shortcut through that outside vertex), hence at most6 on C. Summing degrees of C vertices, dc-Delta<=2c+2m_chord+6(B-c)<=6B-c-6. Therefore
 (d+1)c<=6B-6+Delta.

For every edge of H, R_e>=2/(d+1), by contracting all vertices except its endpoints and using their degrees<=d. Foster gives sum_e R_e=B-1. Resistance triangle on either arc and then averaging yield
2R_uv<=sum_{e in C}R_e<=B-1-(m_H-c)*2/(d+1).
Substituting m_H=(dB-Delta)/2 and the cycle bound gives
 R_uv<=A B+Q Delta-C0,
 A=(d+13)/[2(d+1)^2], Q=(d+3)/[2(d+1)^2], C0=1/2+6/(d+1)^2.

## Assemble the block path
Every connected Eulerian graph is bridgeless. For u!=v, let H_1,...,H_k be the two-connected blocks on their block-cut-tree path, orders B_i, deficits Delta_i. Electrical resistance adds along this chain, and components off it carry zero current.
Assign all off-path subtrees to the unique chain block where they attach, not recounting the root attachment vertex. Any such nonempty subtree has at least d+1 vertices other than its root: if it had at most d, each full-degree-d nonroot vertex would force exactly d other vertices in the rooted cap, and force the root to have degree d, impossible since it also belongs to a chain block. At an attachment root the total off-path incidence deficit is at most d-2. Since
 A(d+1)-Q(d-2)=(13d+19)/[2(d+1)^2]>0,
its assigned vertices more than pay for its deficit.

At each articulation between two chain blocks, the two deficits sum to d plus the number of off-path incidences there. Thus sum Delta_i=d(k-1)+Delta_off. Also sum B_i=n-M_side+k-1. Applying the local inequality and paying off-path deficits gives
R_uv<=A n+(A+dQ-C0)k-(A+dQ).
Here A+dQ-C0=d/(d+1)^2>0.
Each chain block with its assigned vertices has at least d+1 vertices: this is immediate if B_i>=d+1; otherwise every vertex of the block needs outside neighbors to reach degree d, and at least one of its>=3 vertices is not among its at most2 chain articulation ports, so it has an assigned off-path subtree of at least d+1 vertices. Since assigned orders sum n+k-1, it follows k(d+1)<=n+k-1, or k<=(n-1)/d.
Substitution gives the announced global bound.

## Compare with the claimed odd formula
For d>=12,
 1-d(d+15)/[2(d+1)^2]=(d^2-11d+2)/[2(d+1)^2]>=0.
The subtracted constant f(d)=d(d^2+4d+15)/[2(d+1)^2] is increasing for d>=12 (differentiate: derivative (d+5)(d^2-2d+3)/[2(d+1)^3], positive). Its value at12 is2484/338=1242/169>278/45. Thus dR_uv<n-278/45. Multiplying by n and using commute=ndR proves the exclusion of every even d>=12 for odd n in the domain.
