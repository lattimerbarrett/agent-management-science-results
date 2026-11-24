proof=r'''# Complete lower bound: b(d,k) >= d-2

All ingredients below use only the recursive definition. Code independently verifying the finite data and actual decomposition certificates is `agent3_lower_standalone.py`.

## Elementary necessary attachment condition

Links of a k-decomposable complex are k-decomposable. To see this inductively, let sigma shed K with deletion D and link L, and take a face tau. If sigma is contained in tau, its link is a link in L. Otherwise tau belongs to D. If tau union sigma is not a face, its link equals its link in D. Otherwise sigma\tau sheds lk_tau K: deletion is lk_tau D, pure of the required dimension, and link is lk_{tau\sigma} L. Induction gives the claim.

Every positive-dimensional k-decomposable complex is connected. Induct on its decomposition. Its deletion is connected. Every removed facet F meets that deletion in F\{v}, for any v in sigma; this is a nonempty face when dimension >=1, and deletion purity guarantees its vertices remain. Thus every facet connects to the deletion.

Consequently, if K is pure d-dimensional and K'=K union 2^F is k-decomposable, with |F|=d+1 and F not a face, the intersection I=K intersect 2^F must be a pure union of ridges of F. Indeed, a maximal G in I with |G|<=d-1 would give

    lk_G K' = lk_G K union 2^(F\G).

The two terms have disjoint nonempty vertex sets (maximality of G gives disjointness), and the link has positive dimension. This contradicts the preceding two facts.

## A finite triangle certificate

On vertices 0,...,7 take the ordered list T0:

    012,023,124,234,015,145,035,356,567,346,457,
    347,146,167,137,017,047,046,026,256,027.

The restrictions of these triangles relative to preceding triangles are respectively

    -,3,4,34,5,45,35,6,7,46,47,37,16,17,13,07,04,06,26,25,27.

Here a restriction R means that exactly the faces containing R are new. Thus each nonfirst triangle introduces a new vertex or a new edge, and these are valid faces of cardinality <=2. The listed triangles contain every one of the 28 edges.

Let S=T0 union {127}. This is a proper triangle family (013 is absent). For its 70 four-vertex subsets, the numbers having respectively 0,1,2,3,4 triangles of S are

    9,14,46,0,1.

Thus S is closed under the rule that three triangles on four vertices force the fourth. The restriction table, all 28 edges, and all 70 cases are checked exhaustively by the supplied code.

## The dimension-d input

Put q=d+1 and m=q. Replace each old vertex v by an ordered cluster X_v of m vertices, disjoint across vertices. Let K_d have as facets all q-element subsets of the union of the three clusters corresponding to any triangle in T0. It is pure of dimension d and has complete graph on its 8m vertices.

We prove it is 1-decomposable. Start with all q-subsets in the clusters of the first triangle, a uniform simplex skeleton, which is vertex-decomposable. Consider a subsequent triangle F with listed restriction R, s=|R| in {1,2}. Its new q-facets are exactly those whose projection contains R.

Process transversals sigma, one chosen copy in each cluster of R, in decreasing lexicographic order. At phase sigma add exactly the q-facets whose coordinatewise-minimal R-transversal is sigma. Let U contain every copy in the clusters F\R, and the copies larger than the chosen one in each R-cluster. The added facets are exactly

    sigma union H,  H in binomial(U,q-s).

The face sigma was not present earlier. Its link after this phase is the complete rank-(q-s) simplex skeleton on U, hence vertex-decomposable.

Its deletion is exactly the complex before this phase. To check purity, remove any chosen vertex from an added facet. If its projection no longer contains R, this face belongs to the previous triangle blocks. Otherwise its minimal transversal has increased lexicographically and belongs to an earlier phase. In either case it extends to an old q-facet: in the latter case use an additional copy in one of the nonempty clusters F\R, which has m>=q copies; in the former use a containing earlier triangle block. Thus every new sigma-avoiding ridge is already covered by an old facet. Since s<=2, sigma is a legal 1-shedding face. Induction through every phase proves K_d is 1-decomposable, hence k-decomposable for every k>=1.

## The barrier and its persistence with too few new vertices

On the old vertex set of K_d define S* to consist of all triples whose projection to 0,...,7 has at most two vertices or belongs to S. It contains all triangles of K_d and is proper: one copy from each of clusters 0,1,3 gives a missing triple.

S* is closed under the three-of-four rule. For a four-set projecting to four distinct vertices use the corresponding property of S. If its cluster multiplicities are (2,1,1), it has either two or four triangles in S*. Every other multiplicity type has four.

Suppose a completion with r<=d-3 new vertices has all prefixes k-decomposable. Since the final skeleton includes every old triangle, consider the first added facet F introducing an old triangle T outside S*. Let

    B={x in F : F\{x} was present immediately before F}.

By the necessary attachment condition, the old faces of F are exactly those not containing B. Since T is new, B is contained in T. Every old vertex and old edge was present initially, so B cannot have size <=2. Consequently B=T. All three ridges F\{t}, t in T, were therefore present earlier.

There are at least d+1-r>=4 old vertices in F. Choose an old u in F\T. Each of the three triangles {u} union (T\{t}) was present earlier, hence belongs to S* by choice of F. Closedness forces T into S*, a contradiction.

Therefore K_d admits no such completion with r<d-2. Since K_d is 1-decomposable, this proves b(d,k)>=d-2 simultaneously for every k>=1.

## Actual executed checks

The standalone code constructs the entire decomposition certificate by these phases and independently checks each deletion and link directly from its facets. Executed cases:

    d  vertices  facets   actual triangles  barrier triangles
    3     32       7960        2720               2784
    4     40      54258        5505               5630
    5     48     357519        9736               9952

Each has complete graph, proper closed barrier, and a fully verified recursive 1-decomposition certificate. These computations supplement, rather than replace, the all-d construction and proof above.
'''
open('workspace/agent3_lower_proof.md','w').write(proof)
print('wrote',len(proof))
