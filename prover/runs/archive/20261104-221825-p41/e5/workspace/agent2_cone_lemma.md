# Cone saturation lemma
Let G be pure with facets of size m, and let X be any set of (m+1)-subsets, each of whose m-subsets belongs to G. For a fresh vertex a set E=(union_{F in X} 2^F) union (2^{a}*G). If G is k-decomposable, so is E.

Proof by induction on the number of faces of G. If G is a simplex on m>0 vertices, X is empty and E is a simplex. If G={empty}, E is an arbitrary nonempty zero-dimensional complex and is vertex-decomposable by successive vertex deletions. Otherwise choose a shedding face s of G. Every face of a facet F in X not containing s is supported in a facet aH with H in del_s G, unless it is F itself (and F avoids s). Indeed all proper faces of F lie in G, and pure deletion extends those avoiding s to a facet of del_s G. Hence
 del_s E = (union_{F in X, s not subset F} 2^F) union (a*del_s G).
Every ridge of those surviving F belongs to del_s G, so induction applies. Likewise
 lk_s E = (union_{F in X, s subset F} 2^{F\s}) union (a*lk_s G),
and every ridge of F\s belongs to lk_s G; induction applies. Both expressions are pure with the required dimensions since the cone terms are pure, and |s|<=k+1. This proves the lemma.

In particular Delta union a*skel_{d-1}(Delta) is k-decomposable whenever its ridge skeleton is k-decomposable, independently of Delta. It is vertex-decomposable if and only if its ridge skeleton is vertex-decomposable (necessity follows by taking link_a).
