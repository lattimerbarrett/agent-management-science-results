# Finite bounded-tree structure after coarse normalization

Fix H with h vertices and chi(H)=r+1, and assume
ex(N,H)<=t_r(N)+aN+C eventually, with a<1/r. Suppose a sequence of H-free
n-vertex graphs G has partitions V_1,...,V_r with |V_i|=n/r+o(n) and every
vertex has o(n) nonneighbors in each OTHER part (uniformly). All constants
below depend only on H,r,a.

## 1. Critical vertex and bounded internal degree
The graph U_N=K_1 join T_{N-1,r} has
 e(U_N)-t_r(N)=ceil(N/r)-1.
If H had no color-critical vertex, U_N would be H-free: deleting its universal
vertex leaves an r-colorable graph. The extremal bound contradicts its
surplus. Thus H has a vertex z such that H-z is r-colorable. Choose such an
r-coloring; putting z in any one color class shows H embeds a complete
r-partite graph with one internal star on at most h vertices.

If some G[V_i] contained K_{1,h}, map the internal vertices of this fixed H
embedding into that star. Map all remaining H vertices greedily in the other
parts. Each of at most h previously chosen vertices forbids o(n) choices in
a prescribed part, so there are always linearly many choices. This embeds
H, contradiction. Therefore every internal degree is at most Delta=h-1.

## 2. Factor tests and bounded tree components
Choose k>=2 such that (k-1)/(kr)>a. For every fixed k-vertex tree F, balanced
T_{n,r} with an F-factor inserted into one part has surplus
 ((k-1)/(kr))n+O(1), and hence contains H for large n. Fix one such embedding.
It uses at most h factor copies. Consequently G[V_i] cannot contain h
vertex-disjoint copies of F: map the fixed internal H pattern into those
copies and fill the remaining parts greedily, as above.

There are at most tau=k^(k-2) unlabeled k-vertex tree types. A maximal packing
of k-vertex trees in G[V_i] therefore contains at most (h-1)tau copies. Its
vertex union S has size at most B=k(h-1)tau. Every component of G[V_i]-S has
order less than k. At most Delta*B such components touch S, so the union of
all original components of order at least k has at most
 B*(1+Delta*(k-1)) vertices.

For any connected cyclic F of order j<k, an F-factor insertion has surplus
 e(F)n/(jr)+O(1)>=n/r+O(1)>an+C. The same argument forbids h disjoint copies
of F internally. There are at most 2^(j choose 2) such unlabeled types.
Thus all cyclic components of order less than k together contain at most
 (h-1)*sum_{j<k} j*2^(j choose 2)
vertices. Combining the two bounds: all internal components have uniformly
bounded order, and all but O(1) vertices lie in tree components of order <k.

## 3. Cross completion using repeated components
Assume now G maximizes the number of cycles among H-free n-vertex graphs.
By the dense-Dirac edge-addition lemma, adding any missing cross edge
strictly increases c(G), so G is H-saturated with respect to cross edges.

Suppose a component type T occurs linearly many times in part i. If a
missing cross edge xy has x in one such copy, adding xy creates H. Shift
ALL vertices of the internal component containing x that are used by this
copy of H into a fresh isomorphic T-copy. At most h outside H vertices must
be adjacent to the fresh images. They jointly forbid o(n) vertices, hence
o(n) T-copies, so a fresh valid copy exists. This gives H already in G,
contradiction. Therefore every vertex in every linearly repeated type is
cross-complete to ALL other parts. Each part has at least one such type,
because all internal components have bounded order.

Take any internal component C (its order is uniformly bounded by K). Form
G* by deleting all internal edges of C and adding all its missing cross
edges. G* is H-free: any newly created H copy can replace its vertices in C
by fresh vertices from DISTINCT cross-complete reservoir components of the
same part. Since C is now internally independent, no same-part adjacency
needs preserving; all cross adjacencies are present in the reservoir.

Both G and G* and their union are dense-Dirac graphs. If M cross edges were
added and L<=K^2 internal edges deleted, the uniform edge-addition estimate
 c(F+e)/c(F)=1+Theta_r(1/n)
shows c(G*)>c(G) whenever M exceeds a fixed constant times L. Thus M=O(1)
for EVERY component, and each vertex has O(1) missing cross edges.

Repeat the fresh-copy saturation argument. Now a type with more than a
fixed constant number of copies is cross-complete, because h outside H
vertices forbid only O(1) copies. There are finitely many component types;
all less frequent components together form a bounded set R. Hence G-R is
a complete join of r classes, each a disjoint union of bounded trees, and
all missing cross edges of G are in R x R.

## 4. At most one normal active part
If two normal parts each contain linearly many nontrivial tree components,
each contains arbitrarily many vertex-disjoint edges in distinct
cross-complete components. If H embedded into balanced T_{N,r} with perfect
matchings inserted in those TWO parts, its fixed embedding would use only
at most h matching edges and h isolated vertices per part. These can be
mapped into the available distinct normal components, with all cross edges
present, producing H in G. Consequently the two-matching augmented Turan
host must be H-free. Its surplus is N/r+O(1), contradicting a<1/r.
Thus at most ONE normal part has nontrivial tree components.

## What this does NOT prove
This structural reduction does NOT establish that an edge-extremizer and a
cycle-extremizer coincide. Different rare templates R can allow different
common tree shapes of the same maximal order. Their O(1/n) cycle corrections
can compete with a single-edge difference. Explicit exact graph pairs show
that generic bounded-forest edge-priority is FALSE. The needed H-specific
exchange/charging inequality remains a separate unproved step.
