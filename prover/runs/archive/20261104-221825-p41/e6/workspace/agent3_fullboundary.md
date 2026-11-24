# Full-boundary closure
Let X be pure of facet size q and k-decomposable. Let F be a q-set absent from X, with every proper subset of F in X. Then X'=X union 2^F is k-decomposable, for every k>=0.
Proof by induction lexicographically on (q, number of facets of X). For q=1, every pure zero-dimensional complex is vertex-decomposable. If X is a simplex and q>=2, no such F exists: two different q-sets differ in a vertex and F has a proper singleton absent from X. Otherwise choose a shedding face sigma.
If sigma is not contained in F, all proper subsets of F lie in del_sigma X. Thus deletion in X' is (del_sigma X) union 2^F, k-decomposable by induction on facet count, and link is unchanged.
If sigma is contained in F, deletion is unchanged because every new face avoiding sigma is a proper subset of F and hence already old. Link becomes (lk_sigma X) union 2^(F minus sigma). The residual facet is missing and has full boundary in the old link, so use the lower-rank induction. Purity and required dimension follow directly in each case.

# Consequence: shellability equals (d-1)-decomposability for d>=1
In a pure shelling, adjoining a facet F whose intersection with prior facets is not the full boundary has a unique restriction face sigma of cardinality at most d. It sheds to the prior complex, with simplex link. When the intersection is the full boundary, use full-boundary closure. Induction along the shelling gives (d-1)-decomposability. The converse follows from the usual recursive concatenation of deletion and face-joined-link shellings.

# Two-dimensional completion
For k>=1, the graph of any pure k-decomposable two-complex X is connected. While this graph is not complete, choose nonadjacent u,w at graph distance two, with common neighbor v. Add triangle uvw. Its unique new minimal face is edge uw, which sheds to the old X with simplex link {v}; thus the addition preserves k-decomposability. Each step increases the number of graph edges, so eventually the graph is complete. All remaining triangles now have full boundary and can be added using the closure lemma. No new vertex is needed.

# k=0 completion in all dimensions
For a vertex-decomposable complex choose shedding vertex v. Complete its pure deletion on the other vertices by induction, retaining v as shedding throughout. Then complete its link by dimension induction, keeping the now-full deletion fixed; every new link facet lifts to a facet containing v. If some ambient old vertices are initially absent from the link, after completing the link on its own vertices introduce these one by one through the truncated-cone prefix lemma. This completes the whole complex without new vertices.
