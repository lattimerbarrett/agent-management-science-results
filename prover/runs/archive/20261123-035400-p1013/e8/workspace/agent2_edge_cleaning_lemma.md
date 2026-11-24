# High-minimum-degree cleaning and edge-extremal reduction

This lemma closes the global EDGE extremal reduction for our constructed realizers.
It does NOT by itself handle cycle-maximizers for the universal half.

Fix r>=2, H of chromatic number r+1, h=|H|, L. Suppose H embeds in a complete
r-partite graph with an extra K_{1,L} in one part (all part sizes bounded
constants). Let G_n be H-free with minimum degree at least (1-1/r)n-B, B fixed.
Then G_n has an r-partition with:

* n_i=n/r+O(1);
* maximum internal degree <=L-1;
* each vertex has O(1) missing cross-neighbors.

Proof. Erdős--Simonovits stability gives a partition with o(n^2) internal edges
and parts n/r+o(n). Choose a maximum r-cut instead; it retains both properties,
and for every vertex its degree in every other part is at least its internal
degree (otherwise moving it increases the cut).

For any fixed eta>0 choose theta<eta/(10h). All but o(n) vertices have internal
degree <theta*n. Such good vertices miss at most theta*n+o(n) cross-neighbors:
missing_cross(v)=(n-n_i)-deg(v)+deg_internal(v).

If v had eta*n internal neighbors, choose L good internal neighbors. In every
other part v has at least eta*n neighbors. Embed the fixed star realization
of H with center v and selected good leaves, choosing remaining vertices from
good vertices and, whenever adjacent to v, from its neighborhoods. At each
step every previously chosen good vertex removes at most theta*n+o(n)
possibilities. Thus each required candidate set still has positive linear
size. Vertices in v's own part have no required internal edges except the
specified star. This embeds H, contradiction. Consequently maximum internal
degree is o(n).

The displayed formula now shows every vertex misses o(n) cross-neighbors.
Any internal K_{1,L} can therefore be extended to H by the same greedy
embedding, this time using candidate sets n/r-o(n). Hence internal maximum
degree <=L-1. Minimum degree then gives
n_i <= n/r+B+L-1;
summing the part sizes gives the matching lower bound. The displayed formula
finally bounds every missing cross-degree by a constant.

## Application to the tensor/odd-cycle profile realizer

Let D=L-1 and let P be the chosen finite family of colored profiles. Each
profile has edges ONLY within its prescribed parts, not between them. Our
realizer H has the following two properties:

(A) In every graph of internal maximum degree <=D, an embedding of H forces
an internal copy of one profile. This is the dominant-heavy-cluster coloring
argument; completeness of cross-edges is NOT needed.

(B) In any r-partition with part sizes n/r+O(1), internal maximum degree <=D,
and missing cross-degree O(1), an internal profile extends to H, for large n.
Indeed fix its actual vertices. There are no required cross-edges between
these fixed vertices, since profiles are disjoint unions of within-part
components. All other actual vertices and all constraint vertices can be
embedded greedily using fresh vertices; each fixed vertex excludes only O(1)
positions in other parts.

Suppose the profile constraints imply total internal edges <=rho*n/r+O(1),
and some profile-free complete-cross construction has
 e >= t_r(n)+rho*n/r-O(1).
Then ex(n,H)=t_r(n)+rho*n/r+O(1), and EVERY edge-extremal graph is complete-cross
with profile-free internal graphs, for all large n.

Upper bound: induction on n. If a low-degree vertex of degree at most
 t_r(n)-t_r(n-1)+rho/r
exists, delete it and apply induction. Otherwise minimum degree is at least
(1-1/r)n-O(1). Apply the cleaning lemma and (B), then the internal-edge bound.
The O(1) constant can be chosen uniformly and enlarged for the finitely many
small n.

Exact edge-extremal form: matching upper and lower bounds imply
 deg(v)>=ex(n,H)-ex(n-1,H)>=(1-1/r)n-O(1)
in every edge-extremal G. Apply cleaning and (B), so its internal graphs avoid
all profiles. Filling every missing cross-edge preserves internal degrees
and profile-freeness, hence by (A) the resulting graph is still H-free. Edge
extremality forces there to have been no missing cross-edge.
