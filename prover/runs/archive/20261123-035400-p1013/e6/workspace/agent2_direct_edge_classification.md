# Direct edge-extremizer classification for the projective renderer

This avoids BOTH Simonovits's D theorem and the cycle-max structure theorem.
It applies to the proposed r=3 renderer H with the following exact projection
payloads: K_{1,11}, the fork5, P12 disjoint-union P11, C3,...,C22, and one
edge in each of two different color classes. The renderer has a color-critical
vertex and has the stated exact projection characterization whenever all
monochromatic degrees are at most 10.

Let G be ANY edge-extremal H-free n-vertex graph, n tending to infinity.
All uses of O(1), o(n), and sufficiently large n depend only on fixed H.

## A. Ordinary stability and coarse normalization
Classical Erdos--Stone plus H-stability gives a partition into three parts
of size n/3+o(n), with o(n^2) internal/missing-cross edges. Delete an o(n)
set of bad vertices to obtain a good core whose vertices have o(n) missing
cross-neighbors and o(n) own-part neighbors uniformly.

Since H has a color-critical vertex, ANY vertex v having at least epsilon*n
good neighbors in EACH part would give H: properly 3-color H minus its
critical vertex, place all its vertices in the appropriate good-neighbor
sets of v, greedily avoiding the o(n) cross-nonneighbors. This works even
if not every H vertex is adjacent to the critical vertex; extra edges do
not hurt. Thus every v has o(n) good neighbors in at least one part,
uniformly. Assign each bad vertex to such a part. Good vertices keep their
original part. The new partition has maximum internal degree eta_n*n=o(n)
and total missing cross edges M_n=o(n^2).

Choose tau_n->0 with tau_n>>eta_n and tau_n^2>>M_n/n^2. Let B consist of
vertices with at least tau_n*n missing cross neighbors. Then
 b=|B| <=2M_n/(tau_n*n)=o(tau_n*n).
Replace ALL B vertices by internally isolated, cross-complete vertices in
their assigned classes, including making all appropriate B--B cross edges.
This new graph G* is H-free. Indeed any new H copy replaces its newly
inserted vertices by fresh old vertices from the good core in the same
classes. At most |H|*tau_n*n=o(n) nonneighbors are forbidden per class, so
greedy replacement gives H already in G.

If b>0, at least (tau_n*n-b)b cross edges to the unchanged good set are
added, while at most eta_n*n*b internal edges are deleted. Hence e(G*)>e(G),
contradiction. Thus max missing cross degree is o(n).

## B. Payloads directly bound EVERY internal component
For any one-part payload F, H embeds in complete cross parts with F inside
one part, with all other vertices in that part internally isolated. In G,
if F occurs internally, map those H vertices there and fill all others
greedily using o(n) missing cross degree. Therefore G[V_i] avoids EVERY
one-part payload.

Consequently each internal graph avoids K1,11, fork5, C3,...,C22, and
P12 disjoint-union P11. It is a forest with components stars <=11 or paths
<=22 (the elementary argument is in agent2_counterphase_audit.md). In
particular EVERY internal component has order <=22 and <=21 edges.

## C. Fresh-copy saturation and bounded exceptional set
There are finitely many internal component types. A type with linearly many
copies in a part is cross-complete to ALL other parts. Otherwise add a
missing cross edge incident to a copy. Edge-extremality creates H, but move
that whole component's used H vertices to a fresh isomorphic copy avoiding
the o(n) cross-nonneighbors of the at most h outside H vertices. This gives
H already in G, contradiction.

Each part has such a linear reservoir. For ANY internal component C, isolate
its vertices and complete all their cross edges. The resulting graph is
H-free: any new H vertices formerly in C are now internally isolated and
can be replaced by fresh vertices in distinct cross-complete reservoir
components of that part. At most e(C)<=21 edges were deleted. Thus edge
extremality implies at most 21 missing cross edges incident to C.

Now repeat the fresh-copy saturation argument. Any type with more than
22h copies is cross-complete: at most 21h copies are forbidden by outside
H vertices and at most h are occupied. Let R be the union of all rarer
components. Then |R|=O_H(1). Every vertex in R is adjacent to ALL normal
vertices in OTHER parts, and to NONE in its own part (components are
disjoint). Thus all R vertices are ordinary, with no separate exceptional
neighborhood argument required.

## D. Exactly one active class; complete cross edges
The two-active-edge payload forbids normal nontrivial components in two
parts. If no part has normal nontrivial components, internal edges are O(1),
contradicting the explicit H-free lower-bound construction with linear
surplus. Therefore exactly one part is active.

An internal edge in ANY other part also embeds that payload, using a normal
active edge and normal vertices for everything else. All relevant cross
edges are normal--normal or normal--rare and are present. Thus all internal
edges occur in the active part.

Complete every missing R--R cross edge. Internal degrees stay <=10. The
renderer rigidity says any H copy must use a projection payload. None can
occur: all one-part patterns are already absent and the two-active-edge
pattern is impossible. The root's extra projection is excluded by its >10
neighbors in every color. The completed graph is H-free, so extremality
forces there were NO missing cross edges.

Thus EVERY edge-extremizer is a complete tripartite join with all internal
edges in one part, and those internal components obey exactly the phase
rules proved in agent2_counterphase_audit.md.

## E. Exact edge bounds
For active size s>=12, f(s)=s-ceil(s/11)+1. Writing s=n/3+delta and using
sum of squared deviations >=3delta^2/2, while balanced-rounding contributes
at most 1/3, gives
 e(G)-t3(n)-10n/33
 <= 1+1/3+10delta/11-3delta^2/4
 <= 1+1/3+100/363 <2.
Hence ex(n,H)<=t3(n)+10n/33+2 eventually.

At n=33q, the exact integer optimization forces balanced parts of size 11q,
and the internal graph is uniquely P22 disjoint-union (q-2)K1,10. This is a
GLOBAL classification of ALL edge-extremizers, not merely a D-template
classification. No uniqueness-lifting theorem is involved.
