# Exact W7 extremal classification from standard stability

Write W=K_1 join C_6 and f(n)=floor((n+1)^2/4)+1. We use only the standard Erdős--Simonovits stability theorem: a W-free graph with e(G)>=t_2(n)-o(n^2) has a bipartition with o(n^2) internal edges and o(n^2) missing cross edges. All asymptotic statements below are uniform over the indicated class of graphs.

## High-minimum-degree lemma
Fix C=10. For all sufficiently large n, every W-free n-vertex graph satisfying e(G)>=f(n) and delta(G)>=n/2-C is exactly an extremal construction described below.

Choose a maximum-cross-edge bipartition A,B. Stability implies |A|,|B|=n/2+o(n) and o(n^2) missing cross edges. For every fixed eta>0, no vertex can have eta n neighbors in BOTH A and B, for the cross graph between these two neighborhood sets has density 1-o(1), and hence contains K_{3,3}, thus C6, in its neighborhood. (Use the standard elementary fixed-complete-bipartite density lemma, or Kővári--Sós--Turán.) Therefore min(d_A(v),d_B(v))=o(n) uniformly. The maximum-cross property gives internal degree <= cross degree at each vertex, so every internal degree is o(n).

Minimum degree now implies every vertex has n/2-o(n) cross neighbors; since part sizes are n/2+o(n), every vertex misses only o(n) cross neighbors. If v has three internal neighbors x,y,z, the opposite part contains linearly many common neighbors of v,x,y,z. Choose three distinct such neighbors; together with x,y,z they form an alternating C6 in N(v). This is forbidden. Thus both internal graphs have maximum degree at most 2.

Set K=2C+4. Minimum degree and internal degree<=2 imply each part has size between n/2-C-2 and n/2+C+2, and every vertex misses at most K opposite-part vertices.

Both internal graphs cannot have maximum degree<=1, since then e(G)<=t_2(n)+floor(n/2)<f(n). Relabel so a vertex v in A has two internal neighbors x,y. If e(G[B])>6K+3, remove from B the at most 3K vertices not adjacent to every vertex of {v,x,y}. At most 6K internal edges disappear, leaving at least four edges in a graph of maximum degree 2, hence two vertex-disjoint edges b1b2,b3b4. Now x,b1,b2,y,b3,b4 is a C6 in N(v), contradiction. Consequently
 e_B<=M:=6K+3.

Let a=|A|,b=|B| and let D be the total number of missing cross edges. Since e_A<=a and ab+a<=floor((n+1)^2/4)=f(n)-1,
 D=ab+e_A+e_B-e(G)<=M-1.
Furthermore e_A>=f(n)-ab-M>=n/2-M, so A contains linearly many edges and linearly many vertices of internal degree 2 (the latter follows from 2e_A-a <= #degree-2 vertices).

If B has a vertex w with two internal neighbors y,z, discard from A all vertices not adjacent to every vertex of {w,y,z}. This discards only O(M) vertices and hence O(M) internal edges. Since e_A is linear, two disjoint A-edges remain. As above these edges and y,z give a C6 in N(w), impossible. Thus G[B] is a matching.

If this matching has two edges b1b2,b3b4, let S be the A-vertices missing an adjacency to one of these four endpoints. Since D<=M-1, |S|<=M-1. At most 3|S| vertices of A lie in S or have an internal neighbor in S. Choose an internal-degree-2 vertex v outside this set; its two internal neighbors x,y and v are adjacent to all four endpoints. Again x,b1,b2,y,b3,b4 is a C6 in N(v). Thus e_B<=1.

We conclude
 e(G)=ab+e_A+e_B-D<=ab+a+1<=f(n).
All hypotheses imply equality. Therefore D=0, e_A=a, e_B=1, and a maximizes a(n+1-a). In particular G[A] is 2-regular. It contains no P5: if a1...a5 is such a path and uv is the B-edge, then v,a1,...,a5 is a C6 in N(u). Hence every component of G[A] is C3 or C4.

Conversely, every complete-cross graph with A a union of triangles and quadrilaterals and B containing exactly one edge is W-free. For a center in A, its neighborhood contains at most two A-vertices and only one B-edge, insufficient for a C6. A center in B not incident to the edge sees only A, which has no C6. A center incident to the B-edge sees A plus one B-vertex; a C6 through that vertex would require a P5 in A, which does not exist.

## Progressive induction removes the minimum-degree hypothesis
Let N be a threshold for the lemma. Suppose a W-free G of order n has e(G)>f(n). While the current order m>N and there is a vertex of degree <m/2-C, delete one such vertex. Since
 f(m)-f(m-1)=ceil(m/2),
the positive defect e(G)-f(m) increases by at least C on every deletion. If the process stops above N, the high-minimum-degree lemma is contradicted. If it reaches N, its defect is at least 1+C(n-N), whereas it is at most binom(N,2)-f(N), impossible for all sufficiently large initial n. Thus ex(n,W)<=f(n) for all sufficiently large n.

For every sufficiently large n, f(n) is attained: choose a nearest integer to (n+1)/2 for a and partition a into 3's and 4's (possible for all a>=6), use corresponding C3/C4 components in A, and put one edge in B. The preceding paragraph checks W-freeness. Hence ex(n,W)=f(n).

Finally for an extremal graph G of sufficiently large order n, deleting any vertex gives an (n-1)-vertex W-free graph with at most f(n-1) edges, so delta(G)>=f(n)-f(n-1)=ceil(n/2). The high-minimum-degree lemma applies and gives the full exact classification.

For n=2m, the active part A has size m or m+1. Thus the exact classification required by the cycle proof is proved without invoking a specialized odd-wheel theorem.
