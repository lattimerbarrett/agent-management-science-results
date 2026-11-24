# Conditional amplification of a three-dimensional shellable terminal core

## Core invariant
Suppose X is a pure d-dimensional k-decomposable complex, W is a subset of its vertices, all pairs from W are faces, and its triangle set K on W is noncomplete and tetrahedron-closed: on any four distinct W-vertices, the number of triangles in K is never three. Suppose all vertices outside W, including allowed new vertices, number at most d-3. Then X has no k-decomposable completion to the full d-skeleton.

Indeed, at the first added facet F that introduces a missing W-triangle abc, every already-present codimension-one face of F must omit a,b,or c. The intersection of F with the previous complex is pure codimension one, since both old and new complexes are shellable. To cover all three old edges ab,ac,bc, all three ridges F-a,F-b,F-c must be present. As |F intersect W|>=4, choose w in (F intersect W) minus {a,b,c}. The triangles abw,acw,bcw are present. These were present initially by firstness, while abc was missing, contradicting tetrahedron-closure.

Thus a d-dimensional core example without noncore vertices requires at least d-2 auxiliary vertices. Coning a q-dimensional core example by d-q vertices gives lower bound q-2 in dimension d.

## Conditional existence amplification
Assume one shellable pure three-dimensional complex D exists whose graph is complete, whose triangle set is tetrahedron-closed and noncomplete. Then such a shellable pure q-dimensional complex exists for every q>=3.

Remove from a shelling of D every homology facet (a facet attaching along its full boundary). Removing these facets does not change any proper face or any later shelling intersection. Thus we can assume every shelling step after the first attaches along a nonempty proper union of boundary triangles.

Choose m>=q+1, replace every vertex v by a disjoint m-element block B_v, and let Y be the pure (q)-skeleton of the union of simplices on unions of blocks corresponding to facets of D. The graph of Y is complete. Its triangles depend only on old supports: triples with at most two old vertex types are always present, and triples with three distinct types are present exactly when the old triple is in D. Tetrahedron-closure follows: on four new vertices with at most two types all four triples occur; with three types exactly two or four occur; with four types use old closure. Noncompleteness is retained.

To shell Y, process the old facets in their shelling order. On a cluster C of four blocks, the old intersection has form J=union_{i in R} 2^(C minus B_i), where R is nonempty and proper. Put P=C minus union_{i in R} B_i; then |P|>=m>=q+1. The new facets S are precisely the (q+1)-sets meeting each B_i, i in R. Order them by decreasing |S intersect P|, then group by S minus P, then use lexicographic order on S intersect P within each group.

Every intersection face lies in an old ridge: if it omits an outside-P vertex x and x is the unique S-vertex in its block, the ridge S-x lies in J. If that block has another S-vertex, replace x by an unused P-vertex; this supplies an earlier new facet containing S-x. If the intersection with a previous facet omits only P-vertices, the outside-P sets must coincide (by decreasing P cardinality), and ordinary lexicographic shellability of the uniform skeleton supplies the required ridge. Therefore this is a relative shelling.

Hence Y is shellable. It is (q-1)-decomposable, by the general equivalence in agent3_fullboundary.md. Cone it to dimension d, with q=min(d,k+1), to obtain the lower min(d,k+1)-2 for k>=2.

UPDATE: the missing base is now rigorously constructed from the explicitly certified shellable two-dimensional core in agent3_2core_order.json. The rank-four m=4 inflation has a literal shelling certificate checked by agent3_base_check.py and independently by agent1_lower_independent.py. The k=1 case is proved by the clone-transversal edge decomposition in agent2_k1_lower.md and agent2_base18_check.py. Thus no requested lower input remains missing.
