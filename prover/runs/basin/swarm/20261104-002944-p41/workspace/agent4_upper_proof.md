# Complete upper bound proof: b(d,k) <= d-2 for k>=1

Write rank for common facet cardinality, and S_q(X) for the pure skeleton whose facets are the q-element faces of a pure complex X of rank at least q. The rank-zero complex is {emptyset}.

## Elementary lemmas

1. Uniform skeletons of a simplex are vertex-decomposable: delete a vertex and use induction on vertex number and rank; the link is the uniform skeleton of rank one less. Consequently pure skeletons of a k-decomposable complex are k-decomposable. For the latter induct on a decomposition. If its shedding face sigma has size bigger than q, S_q(X)=S_q(del_sigma X). Otherwise sigma sheds S_q(X); its deletion is S_q(del_sigma X), and its link is S_(q-|sigma|)(lk_sigma X). To check purity, every sigma-avoiding face of a removed facet extends to a facet of the original deletion, by the original shedding property.

2. A k-decomposable pure complex has a facet order with every nonempty prefix k-decomposable. Induct on a decomposition: first order all deletion facets recursively, then order the facets sigma union H with H in a recursive prefix order of the link. During the second block sigma sheds every prefix: the deletion is fixed, and the link is the relevant link prefix. All sigma-avoiding faces are already in the deletion by its purity.

3. Full-boundary filling: if X is pure rank p, k-decomposable, F is a missing p-set, and every proper subset of F is a face of X, then X union 2^F is k-decomposable, for any k>=0. Induct on dimension and number of facets. Rank one is immediate, since every nonempty zero-dimensional complex is vertex-decomposable. A positive-dimensional simplex cannot contain the full boundary of a missing facet of the same rank. For a shedding face sigma of a nonsimplex X, if sigma is not a subset of F, use induction on del_sigma X with F added; the link is unchanged. If sigma is a subset of F, the deletion is unchanged and use lower-dimensional induction on lk_sigma X with F\sigma added. The full-boundary assumption passes to the appropriate deletion or link. The same sigma is a shedding face: each newly introduced sigma-avoiding face lies in a ridge F\{v}, v in sigma, already covered by the original deletion.

4. Conical lifting: let G be pure rank p and k-decomposable, let a be a new vertex, and let D be ANY collection of (p+1)-element sets, all of whose proper subsets are faces of G. Then X=(a*G) union (union over F in D of 2^F) is k-decomposable. Induct on the decomposition of G. If rank p=0, X is a nonempty zero-dimensional complex, hence vertex-decomposable. If G is a positive-rank simplex, D is empty, so X is a simplex. Otherwise let sigma shed G. It also sheds X. The deletion is a*del_sigma G, with the D-facets avoiding sigma adjoined; the link is a*lk_sigma G, with the facets F\sigma for F in D containing sigma adjoined. Each residual facet has all proper faces in the indicated base complex. Apply induction to both; the deletion is pure of the required rank. In particular, if G is the complete rank-p skeleton on W, the conclusion holds for every selection D of (p+1)-sets on W.

## Dimension two

Let X be a pure two-dimensional k-decomposable complex, k>=1. Its graph is connected. Indeed this follows inductively from its decomposition: the deletion is connected, the nonempty shedding-face star is connected, and they meet, since a facet containing sigma has a nonempty sigma-avoiding ridge lying in the pure deletion.

As long as this graph is not complete, it has nonadjacent vertices u,v with a common neighbor w (take the first three vertices of a shortest path of length at least two). Add the triangle uvw. The edge uv is new; it sheds the new complex, with deletion X and link the simplex on w. This is allowed since k>=1. Repeat until the graph is complete. Now every missing triangle has its whole boundary present, so add all such triangles using Lemma 3. Thus no new vertices are required in dimension two.

## Induction in dimension

Let d>=3, and assume the claimed upper bound d-3 in dimension d-1. Let Delta be pure rank d+1 and k-decomposable on V. Take new vertex a and a further set B of d-3 new vertices. Put G=S_d(Delta), which is k-decomposable by Lemma 1.

First choose a facet order H_1,...,H_s of G with all prefixes k-decomposable by Lemma 2. Add the d-facets {a} union H_j to Delta in that order. Each intermediate complex is k-decomposable: a sheds it, its deletion is exactly Delta (all H_j already belong to Delta), and its link is the corresponding k-decomposable prefix of G.

Next apply the dimension-(d-1) induction construction to G using B. For each facet H that this construction adds, add {a} union H upstairs. At every stage the upstairs complex is a*G_i together with the original facets of Delta. Every proper face of every original Delta facet belongs to G, hence to G_i. Lemma 4 therefore certifies that every upstairs complex is k-decomposable, even though a need no longer be a shedding vertex.

At the end G_i is the complete rank-d skeleton on V union B. Now add all missing rank-(d+1) facets on V union B, in arbitrary order. At each step Lemma 4 applies again, with this complete G_i as base and with D equal to the current selection of facets not containing a.

All facets containing a were supplied in the first two phases, and all facets avoiding a in the last phase. No facet was repeated and all additions were missing facets. The number of new vertices is 1+(d-3)=d-2. This proves the universal upper bound.

Executable construction and recursive certificates: workspace/agent1_upper.py.
Independent boundary-filling/base-two exhaustive checks: workspace/agent4_boundary_checks.py.
