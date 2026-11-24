# Post-entry finite-hole structure of cycle extremizers (r >= 3)

This lemma uses only the proved two-Posa-rotation endpoint-transfer bound in `agent3_rotation_transfer_lemma.md`, not an unproved normality assertion.

Fix H, chi(H)=r+1, r>=3. Suppose (a) H has a critical vertex, so it embeds into a complete r-partite graph with one fixed internal star K_{1,mu}; and (b) H has a linear-forest decomposition: it embeds into a complete r-partite graph with one fixed internal linear forest F. Let G be cycle-extremal and suppose the entry lemma has supplied a partition V_1,...,V_r, |V_i|=n/r+o(n), in which EVERY vertex misses at most delta*n opposite-part neighbors. Here delta>0 is sufficiently small in terms of H,r. Then:

1. Internal maximum degree is at most Q=mu-1.
2. Every internal connected component has bounded order K=K(H).
3. Every vertex misses at most M=M(H) opposite-part neighbors.
4. All crossholes have both endpoints in a bounded set R consisting of rare internal components. Thus G consists of bounded internal components and a bounded exceptional crosshole pattern.

No assertion that R has no crossholes is made.

## 1. Internal degree and component size
If an internal star K_{1,mu} occurs, use it for the monochromatic edges in the fixed star decomposition of H. All its vertices, including its leaves, have at most delta*n missing neighbors in every other part. Greedily place the other at most h=|H| vertices in their prescribed parts, intersecting at most h cross-neighborhoods each time. The available set has size at least n/r-o(n)-h*delta*n>h. This embeds H, contradiction. Hence Q=mu-1.

Let f=|V(F)|. If an internal component contains a path on f vertices, that path contains F as a noninduced subgraph (place its path components consecutively). The same greedy cross-embedding embeds H. A connected graph of maximum degree Q with no f-vertex path has bounded order, for example at most 1+Q+...+Q^{f}; BFS from any vertex suffices because every root-to-vertex shortest path has fewer than f vertices. This gives K.

## 2. Three uniform cycle-count estimates
The following estimates hold throughout any bounded sequence of crossedge additions and internal-edge deletions. Their constants depend only on r,Q. All vertices remain cross-delta-regular. Their cycle counts remain on the factorial lower scale, because we start with a cycle-extremizer, crossedge addition is monotone, and each internal-edge deletion loses only O(1/n) of all cycles as shown below.

Call cycles typical when they have length at least (1-gamma)n and at most tau*n internal steps, where gamma,tau,delta are sufficiently small fixed constants. The total atypical count E is at most n!*exp(-c*n*log n), by the exact elementary counting argument in the entry lemma (bounded internal degree Q). Thus E/c(G)=o(n^{-L}) for every fixed L. Every bounded number of rotations preserves the coarse typical conditions.

(A) A specified vertex w is omitted by at most C*c(G)/n cycles, up to E. Indeed any long cycle omitting w has at least length-2|part(w)|-2delta*n >= c*n edges whose endpoints both lie outside part(w) and are neighbors of w. Insert w into any such edge. The resulting cycle determines its unique predecessor by deleting w. This is a forward cn-to-one, inverse-one count.

(B) A specified internal edge xu belongs to at most C*c(G)/n cycles, up to E. Delete x from a typical cycle containing xu, orient the resulting path with endpoint u, and transfer u by two Posa rotations to any present opposite-part neighbor w of x. There are Omega(n) choices of w and Omega(n) pivots. Restore x. For a fixed output cycle the old endpoint u is FIXED, and the inverse two-rotation description has only O(n) choices (one intermediate endpoint); orientation costs a constant. Thus forward Omega(n^2), reverse O(n), giving the bound. The other endpoint is held fixed even if it too is an internal neighbor of x.

(C) Completing d>=1 missing crossedges incident with a fixed vertex x creates at least c*d*c(G)/n new cycles, up to o(c(G)/n^L), for every fixed L. Consider typical old cycles containing x with both its neighbors opposite-part. By (A),(B) these constitute (1-O(1/n))*c(G). For every target w among the d missing neighbors that is present in such a cycle, transfer one endpoint of the path G-x to w by two Posa rotations. There are Omega(n) pivot choices. By (A), summing over targets counts d*(1-O(1/n))*c(G) cycle-target pairs, even when d is CONSTANT; no incorrect assertion that every long cycle contains all d targets is needed. Restore x, giving a genuinely new cycle because xw was absent. A fixed output has at most two choices of the new endpoint w, at most n old endpoints, and at most n intermediate inverse pivots. Therefore forward Omega(d*n*c(G)), reverse O(n^2), proving the claim. The negligible errors are uniform also when d grows, since d<=n.

## 3. Bound maximum crosshole degree by purifying a whole component
Let J be the internal component containing a vertex x with d missing crossneighbors; |J|<=K. Complete all crossedges incident with J, then delete all internal edges of J. The final graph has all vertices of J pure in their original part. This final graph is H-free: if it had an H-copy, remap its newly pure vertices greedily into OLD vertices in the same part, preserving adjacencies to the remaining copy vertices. Each required neighbor is in another part and forbids at most delta*n candidates. At each step there are n/r-o(n)-h*delta*n>h unused choices. New pure vertices have no same-part requirements, so this remapping produces a copy in the original G, contradiction. The intermediate graphs need not be H-free.

By (C) cross-completion at x alone multiplies c by at least 1+c*d/n. Additional crossedges are harmless. At most KQ/2 internal edges are then deleted; (B), valid uniformly throughout, gives a factor at least (1-C/n)^{KQ/2} >= 1-C'/n. Thus the final cycle count is at least
 (1+c*d/n)*(1-C'/n)*c(G).
For d larger than a fixed constant M this is strictly greater than c(G) for large n, contradiction. Hence every vertex has crosshole degree <=M.

## 4. Fill holes incident with abundant components
Classify internal components by their host part and unlabelled graph type. There are finitely many types because their orders are <=K. Call a type abundant if it occurs at least L=h(M+1)+1 times; otherwise call it rare. The union R of all rare components has bounded order.

Complete every crosshole with at least one endpoint outside R. This operation preserves H-freeness. To prove this, suppose the completed graph has an H-copy. Keep all vertices of that copy lying in rare host components fixed. For every abundant host component used by the copy, remap ALL of its selected vertices simultaneously into an unused isomorphic old component of the same type. At most h already used components are forbidden by injectivity. For each fixed image vertex, at most M candidate components contain any of its missing crossneighbors, because distinct candidate components are disjoint. Thus at most hM additional components are forbidden. Since L>h(M+1), a candidate remains. Required internal edges are preserved by the component isomorphism. Required crossedges to all already fixed vertices exist by choice. There are no required same-part edges between distinct host components. Proceed until the entire H-copy lies in the ORIGINAL graph, contradiction.

Every added crossedge creates a triangle: choose a common neighbor in any third part, using |V_j|-2M>0 (or the weaker delta regularity). Therefore adding even one such edge strictly increases the cycle count. Since G was cycle-extremal, there were none. Hence all holes already have both endpoints in R, and their total number is bounded.

This finishes the post-entry finite-hole structure lemma. A separate imbalance/density argument is needed to deduce |V_i|-n/r=O_H(1) and the one-active-part/slopes classification. The r=2 entry and bounded-excess transfer are NOT supplied by this lemma.
