# A bounded-excess odd-order witness: 0 belongs to S_2

This proof is complete modulo the genuine classical Erdos--Simonovits
stability theorem. It does not use any cycle-extremizer structure theorem,
Simonovits D-classification, or conjectural normality.

## The graph

For i=1,2 take disjoint double-stars D_i: centers a_i,b_i joined by an
edge, with three pendant neighbors U_i at a_i and three pendant neighbors
W_i at b_i. Add v adjacent to all twelve pendant vertices and to none of
the four centers. Call the resulting seventeen-vertex graph H.

H-v is bipartite. Each D_i+v contains a C5, so H is 3-chromatic and v is
its UNIQUE critical vertex: deleting any other vertex leaves the C5 in
the other copy. In every proper bipartition of H-v each D_i contributes
exactly three neighbors of v to each color. Thus both color classes
contain SIX neighbors of v.

H embeds in a complete bipartite graph with TWO disjoint internal edges
in one part: put v and all four centers in that part, and all leaves in
the other. It also embeds with ONE internal six-edge star: put v and six
of its neighbors in one part according to a proper bipartition of H-v.

## Two H-free graphs

E_n is balanced complete bipartite with ONE triangle in EACH part.
A_n, for odd n=2m+1, is K_{m,m+1} with ONE five-edge star in the larger part.

To see A_n is H-free, deleting its star center makes the host bipartite.
An H-copy must therefore use that center as its UNIQUE critical vertex v.
After deleting v, the image respects a proper bipartition of H-v, so v
would need SIX neighbors in its own host part; it has only five.

To see E_n is H-free, suppose v maps into part A. If it is internally
pure, all twelve leaves map into B. Any center mapped into B would need
three B-neighbors, impossible since the B-triangle has maximum degree two.
Thus all four centers map into A, requiring two disjoint A-edges.
If v maps to an A-triangle vertex, at most two leaves map to A. If the
centers of one D_i both map to A, they occupy the other two A-triangle
vertices, so NO leaf can map to A; then all remaining centers must map
to A too, again requiring a second disjoint edge. Otherwise each copy
has at least one center in B. Two B-centers in one copy would each need
two A-leaves (their mutual B-edge already uses one of their two internal
neighbors), exceeding the total allowance two. Thus each copy has
exactly one B-center and exactly one A-leaf. Each B-center must have
its other two leaves in B. This requires TWO vertex-disjoint P3's inside
the single B-triangle, impossible.

## Exact edge extremizers, without a normality theorem

We prove for all sufficiently large n:

ex(n,H)=t_2(n)+6,

and EVERY edge extremizer is E_n.

Since E_n is H-free, an edge extremizer G has e(G)>=t_2(n)+6. Classical
Erdos--Simonovits stability gives a partition into parts of size n/2+o(n)
with o(n^2) cross-holes and o(n^2) internal edges. Fix constants
0<epsilon<<eta<<delta<<1/|H|. All but o(n) vertices form a core A0,B0,
and every core vertex has at most epsilon*n cross nonneighbors in the
other core part.

A useful greedy observation: if a vertex x has at least eta*n neighbors
in A0 and at least six in B0, then H embeds with v=x; likewise with A0,B0
interchanged. Choose the six neighbors on the sparse side first, then
choose the six opposite neighbors in N(x) intersect their common core
neighborhoods; epsilon<<eta guarantees choices. Map the four centers
greedily to unused core vertices. Equivalently use the six-star
bipartition of H-v. All constraints involve only a fixed number of
cross-regular vertices. Consequently no vertex has eta*n neighbors in
BOTH core parts.

Assign every noncore vertex to the part in which it has at most five
core neighbors, if its opposite core neighborhood has size at least
eta*n. Vertices sparse to BOTH core parts can be assigned arbitrarily.
The original core assignments remain unchanged. Part sizes are still
n/2+o(n). Call a noncore vertex truly bad if it misses delta*n vertices
in its opposite CORE part. Simultaneously replace all truly bad vertices
by pure vertices of their assigned parts.

This replacement gains at least delta*n good-core cross edges per
one-dense-part bad vertex, while deleting at most five good-core
internal edges. A two-sparse-part bad vertex gains (1/2-eta-o(1))*n
such cross edges and loses at most eta*n internal core edges. Edges
among the o(n) noncore vertices cost only o(n) per replaced vertex.
Thus if any truly bad vertex exists, the total edge count strictly rises.

The final graph is H-free: in any new H-copy, remap ALL replaced pure
vertices to unused OLD core vertices of the same assigned parts. Every
unreplaced noncore vertex misses at most delta*n of the relevant core
part, and every old core vertex misses at most epsilon*n. Each greedy
common neighborhood therefore has size at least n/2-|H|*delta*n-o(n)>0.
All required edges at replaced pure vertices are cross edges. This would
give an old H-copy, a contradiction. Hence no truly bad vertex exists.

All vertices are now cross-regular, with at most 2delta*n cross-holes.
The same greedy six-star embedding shows GLOBAL internal maximum degree
at most five. The two-matching embedding similarly shows internal
matching number at most one in EACH part: fix the two disjoint internal
edges as the four centers, put v at an unused core vertex in the same
part, and all twelve leaves at unused opposite core vertices.

A graph of matching number at most one is a star or a triangle (plus
isolates). Therefore the two internal graphs have at most five edges
each, on at most twelve nonisolated vertices in total.

Fill every cross-hole with at least one internally pure endpoint.
This is H-safe. In a new H-copy call a vertex active if it has an internal
neighbor IN THE COPY. Active images belong to the bounded internal
support, and all edges between active images were unchanged. Remap all
nonactive vertices to unused OLD internally pure core vertices in their
respective parts. Their required edges are cross, and cross-regularity
gives positive common neighborhoods. This yields an old H-copy. Edge
maximality therefore says these holes were already absent: all holes
are between the bounded internal supports.

Finally, an internal claw in A and ANY internal edge in B force H, with
no cross-edge requirement between support vertices: put v at a pure
B-vertex. Use the B-edge as the two centers of D_1, its six leaves pure A.
Use the A-claw as one center and its three leaves in D_2; its other center
is pure B, and its other three leaves pure A. All necessary cross edges
meet pure vertices and are present.

Thus if both internal parts are nonempty, BOTH internal maximum degrees
are at most two. Matching number at most one then permits at most three
edges per part, equality only for a triangle. If just one part is
nonempty, its internal edge count is at most five. Hence

e(G)<=|A||B|+6<=t_2(n)+6.

Equality forces balanced part sizes, no cross-holes, and a triangle in
each part. This proves the asserted exact classification.

## Odd-order cycle comparison

Put B_m=c(K_{m,m+1}) and L_m=m!(m+1)!/(2m). Define
I_j(2)=sum_{s>=0}1/(s!(s+j)!). Direct alternating-cycle counts give

B_m/L_m = sum_{s=0}^{m-2} [m/(m-s)]/[s!(s+1)!] -> I_1(2).

For a specified internal edge in the smaller part, its new cycles are

(m-2)!(m+1)! sum_{s=0}^{m-2}1/[s!(s+2)!].

For one in the larger part, they are

(m-1)!m! sum_{s=0}^{m-1}1/(s!)^2.

Consequently the first-order normalized weights, with scale 1/m, are

beta_A=2I_2(2)/I_1(2),   beta_B=2I_0(2)/I_1(2).

Any cycles using two or more edges from a fixed finite internal graph
contribute only O(B_m/m^2). This follows either by contracting the
selected internal path forests, or from the exact finite-forest formula
in agent2_H17_odd_cycles.py. For total selected internal edges j>=2,
the falling-factorial ratios contribute O(m^-j); the omitted-vertex
series is factorially summable. Wholly internal cycles are negligible.
Thus

c(E_{2m+1})/B_m = 1+3(beta_A+beta_B)/m+O(m^-2),
c(A_{2m+1})/B_m = 1+5 beta_B/m+O(m^-2).

The elementary series recurrence I_0(2)-I_2(2)=I_1(2) gives
beta_B-beta_A=2. Also
I_1(2)-2I_2(2)=sum_{s>=0}s/[s!(s+2)!]>0,
so beta_A<1. Therefore

5 beta_B-3(beta_A+beta_B)=4-beta_A>3.

It follows that c(A_{2m+1})>c(E_{2m+1}) for all sufficiently large m.
EVERY edge extremizer is E_{2m+1}, so no graph simultaneously maximizes
edges and cycles at these infinitely many odd orders.

Since ex(n,H)=t_2(n)+6 for all sufficiently large n, H witnesses 0 in S_2.
Upward closure and the definition a>=0 therefore give

S_2=[0,infinity).

## Executed code

agent2_H17_odd_a0_checks.py/json checks the exact graph, unique critical
vertex, two-matching coloring, and exhaustively all possible finite
internal type pairs/hole budgets with signed bonus at least six.
agent2_H17_odd_cycles.py/json gives the exact cycle formula, independently
brute-checks two small hosts, and computes actual separating values.
The human edge proof above renders the SAT audit supplementary rather
than a black box.
