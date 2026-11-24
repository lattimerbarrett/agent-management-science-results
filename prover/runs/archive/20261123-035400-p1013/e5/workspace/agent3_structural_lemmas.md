# Structural lemmas for constant Turan excess

Let H have chromatic number r+1 and h vertices. Suppose ex(n,H)<=t_r(n)+C for all sufficiently large n. Put p=1-1/r.

## Forced templates
For arbitrarily large M, add a star of M-1 edges inside one part of T_{rM,r}. Its edge excess exceeds C, so it contains H. Consequently H has an r-coloring except for edges lying in one internal star; in particular deleting the image of the star center makes H r-colorable. The same argument adding an internal matching of floor(M/2) edges shows H has an r-coloring except for edges lying in one internal matching. In each embedding at most h vertices occur, so the required star and matching templates have at most h vertices per class and at most h prescribed internal edges.

## High minimum degree structural lemma
There exist epsilon>0 and n0 depending on H such that every H-free graph G on n>=n0 vertices with delta(G)>=(p-epsilon)n admits an r-partition with at most 2r(h-1)^2 internal edges. Moreover every vertex misses at most (h+7)eta*n cross edges in this partition, where eta=1/(1000*r*h*h).

Proof. Erdos--Simonovits stability, applied after choosing epsilon sufficiently small, gives an initial partition with every class size n/r +- eta*n and at most eta^2*n^2 missing cross edges. This follows since the minimum-degree assumption gives e(G)>=t_r(n)-epsilon*n^2/2-O(1). We may require epsilon<=eta. Let B consist of vertices missing at least eta*n cross neighbors in this initial partition. Then |B|<=2eta*n. Call the other vertices good.

For any vertex v, there is an initial part in which v has at most (h+1)eta*n good neighbors. Otherwise use v as the critical vertex in the forced star coloring of H. Embed the other vertices in their indicated initial parts, choosing neighbors of v when required. Each chosen good vertex forbids at most eta*n vertices in any other part, and there are at most h choices, so greedy embedding succeeds for n sufficiently large. This contradicts H-freeness.

Assign v to one such sparse part. Every good vertex remains in its initial part: in each other initial part it has at least n/r-2eta*n good neighbors, greater than (h+1)eta*n (with the additional removal of B, use n/r-4eta*n, still sufficient). Hence the new partition differs from the old only on B and its part sizes are n/r +-3eta*n. Every vertex has internal degree at most (h+3)eta*n. The minimum-degree hypothesis now implies that each vertex misses at most (h+7)eta*n cross neighbors.

If some vertex has h internal neighbors, start with that star and embed the forced star template for H. If some part contains a matching of h edges, start with those matching edges and embed the forced matching template. In either case all remaining vertices can be selected greedily: each class has at least n/r-3eta*n vertices and at most h(h+7)eta*n candidates are ruled out by adjacency constraints. The inequality
  3eta+h(h+7)eta < 1/(2r)
leaves a positive linear reservoir. Thus neither configuration can exist. Every internal graph has maximum degree at most h-1 and matching number at most h-1. Endpoints of a maximal matching form a vertex cover of size at most 2(h-1), so its number of edges is at most 2(h-1)^2. Sum over r parts.

## Structural gap lemma (requires only star and matching templates)
Suppose H has the two forced templates, without assuming a constant extremal bound in advance. Then ex(n,H)<=t_r(n)+M_H eventually. To prove this, start with an edge-extremal graph G, so e(G)>=t_r(n). Repeatedly remove a vertex whose degree is below (p-epsilon) times the current order. If D_m=t_r(m)-e(G_m), then each removal gives D_{m-1}<=D_m-epsilon*m+O(1). Since D_n<=0, reaching cn removals for any fixed c>0 (say c<1/2) would force D_{n-cn}<=-Omega(n^2), contradicting the Erdos--Stone bound ex(m,H)=t_r(m)+o(m^2). Consequently the procedure stops after k=o(n) removals at a high-minimum-degree core. The preceding lemma, which used only the two templates and ES stability, bounds the core edge count by t_r(n-k)+M_H. If k>=1, the deficit recurrence gives D_{n-k}<=-epsilon*k*(n-o(n))+O(k), contradicting D_{n-k}>=-M_H for large n. Therefore k=0 and e(G)<=t_r(n)+M_H.

## Completion lemma
In the preceding partition let S be the vertices incident with internal edges. Thus |S|<=4r(h-1)^2. Complete every cross edge unless both its endpoints belong to S; denote the resulting graph by K. Then K remains H-free.

Indeed, suppose K contains H. Keep fixed all images belonging to S. Re-embed the other vertices, one at a time in their original classes, into V(G)\S. Any edge of H inside a class already has both endpoints in S, since K has no internal edges incident with V(G)\S. Cross-adjacency constraints forbid at most h(h+7)eta*n candidates, in addition to O_H(1) used or exceptional vertices. The reservoir inequality above makes every greedy choice possible. This gives H in G, a contradiction.

All ordinary vertices in each class of K are now independent full twins. Missing cross edges and internal edges both have endpoints in S. Thus K is a bounded-edit complete r-partite graph.

## Cloning lemma
Any number of ordinary twins may be added to any class of K without creating H. For if the enlarged graph contains H, its at most h ordinary images in each class can all be remapped to old ordinary vertices in that class, preserving every edge (including adjacency to S). For large n there are at least h old ordinary vertices per class.

## Application to every edge-extremal graph
For edge-extremal G,
  delta(G)>=ex(n,H)-ex(n-1,H)>=t_r(n)-t_r(n-1)-C=pn-O_H(1).
Thus every sufficiently large edge-extremal G satisfies the structural lemma. Its completion K cannot add an edge, by edge extremality. Consequently every edge-extremal G is exactly a bounded-edit complete r-partite template. Since e(G)>=t_r(n), its part-size imbalance is O_H(1).

## Consequence conditional on high minimum degree of cycle optimizers
If a cycle-maximizing graph satisfies the high-minimum-degree hypothesis, its completion cannot add an edge either: adding a missing edge creates at least one new cycle because the graph has minimum degree above n/2 for r>=3. Thus it is also an exact bounded-edit template. The unresolved global step is establishing that hypothesis for cycle optimizers.
