# Conditional sharp lower-bound mechanism

These lemmas reduce the asserted lower bound for every d>=3 and k>=1 to one explicit edge-decomposable 3-complex. **No such seed has yet been found by the team.**

## 1. Closed-triangle persistence

Call a triangle family S on V closed if no four-element subset has exactly three triangles in S. Suppose K is a pure d-complex with complete 1-skeleton on V and proper closed triangle family S. If all prefixes of a facet completion are shellable, every new facet attaches along a pure union of ridges: a lower-dimensional maximal intersection face would have disconnected positive-dimensional link in the resulting shellable complex.

Assume at most d-3 fresh vertices are used. Consider the first added facet F introducing any old missing triangle T. Write B={x in F : F\{x} was already present}. Pure ridge attachment says that the new faces of F are precisely the faces containing B. Hence B is contained in T. As every old vertex and edge was present initially, B cannot have cardinality <=2. Thus B=T. Consequently all three ridges F\{t}, t in T, were already present. There are at least d+1-(d-3)=4 old vertices in F. Choose u in (F intersect V)\T. The three triangles {u} union (T\{t}) were already present, so belong to S, whereas T does not. This contradicts closedness. Thus at least d-2 fresh vertices are necessary for this K.

## 2. Acyclicization preserving the codimension-one skeleton

Every nonempty-dimensional or zero-dimensional pure k-decomposable complex K contains an acyclic pure k-decomposable subcomplex K0 having the same codimension-one skeleton. Induct on a decomposition certificate. A simplex is already acyclic. If the shedding face sigma is itself a facet, discard that facet and recursively acyclicize the deletion; purity of deletion guarantees that its entire boundary remains. Otherwise acyclicize deletion D and link L recursively and set K0=D0 union (2^sigma * L0). Every sigma-avoiding face contributed by the second part is a proper face of an original facet and is therefore in the unchanged codimension-one skeleton of D0. Hence sigma still sheds, and both deletion and link are the desired recursively acyclic complexes. All original proper faces survive. Acyclicity follows from the usual top-Betti additivity for this shedding decomposition.

For completeness that additivity is beta_d(K)=beta_d(D)+beta_{d-|sigma|}(L), with reduced beta_{-1}({empty})=1. All lower reduced homology vanishes because k-decomposable complexes are shellable. The face enumerator identity f_K(x)=f_D(x)+x^{|sigma|}f_L(x), evaluated at -1, gives the equality. In particular every child in a decomposition certificate of an acyclic complex is acyclic, and a shedding face of an acyclic non-simplex cannot be a facet.

## 3. Acyclic clique expansion preserves the SAME k

Let K be acyclic and pure k-decomposable, let q>=1, and choose m>=q. Replace each vertex v by an ordered cluster X_v of m vertices. Define E_q(K) to have as facets all q-element sets whose projection to the old vertices is a face of K. It is pure because every original facet supplies at least m>=q available copies.

**Claim:** E_q(K) is k-decomposable. The q=0 convention is the empty simplex.

Induct on the decomposition of K. A simplex expands to a uniform simplex skeleton, which is vertex-decomposable. Let sigma shed K, put s=|sigma|, D=del_sigma K, L=lk_sigma K. By acyclicity and top-Betti additivity both D and L are acyclic. If s>q then E_q(K)=E_q(D), so induction applies. Otherwise begin with the inductively k-decomposable E_q(D).

Order all transversals sigma' (one copy from each cluster of sigma) in decreasing lexicographic order. At phase sigma', add exactly those q-facets whose coordinatewise-minimal sigma-transversal is sigma'. Put r=q-s. Let B consist of the copies in the sigma clusters strictly larger than their chosen copy in sigma'. The new link of sigma' is exactly the pure rank-r skeleton of

    2^B * E_r(L).

By induction E_r(L) is k-decomposable; joins with a simplex and pure skeleta preserve k-decomposability. Thus this link is k-decomposable.

The deletion of sigma' is the complex before this phase. Indeed, take a new facet G and remove any chosen copy in sigma'. If its projection no longer contains sigma, it is in D and extends to an old q-facet. Otherwise its minimal transversal is lexicographically larger and has already been processed. It extends to a q-facet in that earlier phase using copies of a vertex outside sigma in a containing original facet; such a vertex exists because sigma is not itself a facet. Its cluster contains m>=q copies, so extension is always possible. For r=0 the latter case cannot occur. This proves purity of deletion and shows sigma', whose cardinality is s<=k+1, is a valid shedding face. Every phase therefore remains k-decomposable. All facets of E_q(K) are eventually included.

## 4. Conditional family from one seed

Suppose an edge-decomposable 3-complex K has complete 1-skeleton and proper closed triangle family S. Acyclicize it by Lemma 2 without changing triangles. For any d>=3 put q=d+1 and m>=q, and form E_q(K0). Lemma 3 makes this complex edge-decomposable, hence k-decomposable for every k>=1.

Its triangle family S' consists of all triples whose projection has size <=2, together with the triples projecting to S. It has complete graph and is proper. It is closed: a four-set projected to four distinct old vertices uses closedness of S; a projection of type (2,1,1) contributes either two or four triangles; all other multiplicity types contribute four. Lemma 1 now demands at least d-2 fresh vertices.

**Remaining obligation: provide and certify the single 3-dimensional edge-decomposable seed.** No assertion that this seed exists has been proved here.

Computational check: workspace/agent3_acyclic_expansion.py constructs actual expanded decomposition certificates, verifies exact deletion/link at every phase, and independently verifies the final entire certificate using agent2_checker.verify. It passed examples with 39, 920, 1276 and 5399 facets, including a genuinely non-vertex-decomposable acyclic edge-decomposable base complex.
