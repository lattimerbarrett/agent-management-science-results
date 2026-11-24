# Complete universal upper bound b(d,k)<=d-2 (k>=1)

All complexes are represented by faces; joins and skeletons have their usual meanings.

## Lemma 1: elementary consequences of k-decomposition
(a) Every pure skeleton and every link of a k-decomposable complex is k-decomposable.
(b) Its facets admit an order all of whose prefixes are k-decomposable.
For (b), recursively order the deletion facets, followed by sigma joined to the link facets. During the latter stage sigma remains shedding, with fixed deletion and link a prefix. For (a), recurse on a shedding face sigma. For links, separate whether sigma is contained in the linked face; alternatively commute link with deletion on sigma minus the linked face. For rank-q skeletons: when |sigma|>q, every q-face avoiding sigma lies in the deletion, so skeleton equals deletion skeleton; when |sigma|<=q, recurse on deletion skeleton and rank-(q-|sigma|) link skeleton. Borderline rank zero is the simplex {empty}.
(c) If X is pure d-dimensional and k-decomposable, and a is fresh, one can add all facets a*G for G a d-element face of X, in an order preserving k-decomposability. Use (b) on the pure (d-1)-skeleton of X: after any nonempty prefix a is shedding, deletion X, link that prefix.

## Lemma 2: apex plus filled boundaries
Let L be pure (d-1)-dimensional and k-decomposable, a fresh vertex, and E any family of (d+1)-sets with boundary contained in L. Then
T=(a*L) union union_{F in E} 2^F
is pure d-dimensional and k-decomposable.
Proof by the recursive decomposition of L. If L={empty}, T is a nonempty zero-dimensional complex, hence vertex-decomposable. If L is a nonempty-vertex simplex, E must be empty (every vertex of F would lie in L but |F|>|vertices L|), so T is a simplex. Otherwise choose a shedding face sigma of L. Then
 del_sigma T = a*del_sigma L union union_{F in E,sigma not subset F}2^F,
 lk_sigma T = a*lk_sigma L union union_{F in E,sigma subset F}2^(F minus sigma).
For the deletion formula, any piece of an F containing sigma but avoiding sigma is in a proper face of F, hence belongs to del_sigma L. The boundaries required on both right-hand sides follow from boundary(F) subset L. Induction supplies both decompositions and purity.
The same proof with k=0 shows T vertex-decomposable if L is.

## Lemma 3: dimension-two base
Every pure two-dimensional k-decomposable complex X (k>=1) completes on its existing vertices with every prefix k-decomposable.
Its graph is connected: recurse on decomposition, since each facet in a shedding star meets the pure connected deletion along an edge.
While a graph edge uw is missing, connectedness supplies a path u-v-w of length two with uw missing (take the first three vertices of a shortest path between nonneighbors). Add triangle uvw. Edge uw is shedding in the new complex: deletion is X; link is the simplex {v}. This is allowed for k>=1. Repeat until graph complete.
For k>=2, add remaining triangles arbitrarily: each new triangle is itself a shedding face because its boundary already lies in X.
For k=1 use the following closure property: adjoining any missing triangle F whose boundary already lies in a pure two-dimensional 1-decomposable X preserves 1-decomposability. Induct on a decomposition of X, choosing shedding sigma of size one or two. If sigma is not contained in F, the boundary of F lies in del_sigma X; apply induction there, leaving the link unchanged. If sigma is contained in F, deletion is unchanged. For |sigma|=2 the link merely gains a vertex, still a zero-dimensional vertex-decomposable complex. For |sigma|=1 the link is a connected graph and gains an edge between existing vertices, still connected, hence vertex-decomposable. A simplex has no eligible missing F. This proves closure.
For completeness every connected graph is vertex-decomposable: remove a leaf of a spanning tree, so the remaining graph is connected; its pure link is a nonempty zero-dimensional complex. Recurse, with the single-edge simplex as base.

## Main induction
For d=2 use Lemma 3. For d>=3 choose fresh apex a. Apply Lemma 1(c) to obtain X union a*L with L=X^(d-1). By dimension induction, L completes on V union B for |B|=d-3, through k-decomposable complexes L_j, adding one d-set H at a time. Lift every such addition by adding a union H to the d-complex. At every stage the d-complex is X union a*L_j and is k-decomposable by Lemma 2: the boundary of every old facet of X lies in the original L. Now L_j is the complete (d-1)-skeleton on V union B. Add all remaining (d+1)-subsets of V union B in any order. Lemma 2 applies with L_j vertex-decomposable (uniform skeletons are vertex-decomposable), so every such final-stage complex is even vertex-decomposable. The added vertices are A={a} union B, exactly d-2 vertices. All added facets are distinct missing facets, and the three stages exhaust them.

The universal UPPER bound is proved. No LOWER bound obstruction is supplied here.
