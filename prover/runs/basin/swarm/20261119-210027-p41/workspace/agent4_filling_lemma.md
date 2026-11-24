# Filling lemma (all k)
Let L be pure of dimension e and k-decomposable, and let S be any collection of (e+2)-element sets whose boundaries belong to L. Let a be a new vertex. Then C=(a*L) union the simplices on members of S is k-decomposable.

Proof by induction along a k-decomposition of L. If e=-1 then C is an arbitrary zero-dimensional complex, hence vertex-decomposable. If L is a simplex and e>=0, no (e+2)-set can have its entire boundary in L (the union of its proper faces has e+2 vertices, but L has only e+1 vertices). Thus S is empty and C is a simplex.

Otherwise choose shedding face sigma of L, put D=del_sigma L and K=lk_sigma L. For deletion retain those members F of S not containing sigma. Their boundaries are in D. Every remaining face of C not containing sigma is either in a*D, in a retained old simplex, or a proper face G of a removed F; in the latter case G belongs to D because G is in L and avoids sigma. Thus del_sigma C has precisely the same form a*D plus retained old facets. It is pure dimension e+1 and k-decomposable by induction.

The link has the same form a*K plus simplices F\sigma for old F containing sigma. Every proper subset H of F\sigma satisfies sigma union H proper in F, hence sigma union H in L, so H is in K. It is pure dimension e+1-|sigma| and k-decomposable by induction. Therefore sigma is a valid k-shedding face of C.

This works even when sigma is a facet of L: K={emptyset}, and the link is a zero-dimensional complex, covered by the base case.
