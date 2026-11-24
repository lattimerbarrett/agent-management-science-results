# Critical audit and exact conditional classification

No hidden distinction was found in the definitions supplied in the question. In particular, for every d>=1 and every k>=d-1, the pure k-decomposable complexes are precisely the pure shellable complexes.

## Full-boundary closure (audited induction)
Suppose C is pure d and k-decomposable, and F is a missing (d+1)-set with every proper subset in C. Then C union 2^F is k-decomposable. Use lexicographic induction on (d, number of facets of C). Dimension zero is immediate; in positive dimension the simplex case cannot occur, since the vertices of F would all belong to its sole facet, forcing equality. Let sigma be a shedding face, D=del_sigma C and L=lk_sigma C.
* If sigma is not contained in F, deletion becomes D union 2^F and link is L. All proper subsets of F lie in D. D has fewer facets than C, so induction applies.
* If sigma is contained in F, deletion remains D, since every proper face of F avoiding sigma already belongs to D. Link becomes L union 2^(F\sigma), with full boundary already in L. Link dimension is smaller, so induction applies.
The deletion is still pure of dimension d in either case, and |sigma| does not change. There is no empty-face deletion: all chosen sigma are the nonempty faces from the original decomposition. Ghost vertices never enter.

## Equivalence with shellability
A shedding decomposition gives a shelling: shell D, then append sigma*H in a shelling order of L. For every such facet, its intersection with D contains exactly all its faces avoiding sigma, namely (boundary sigma)*H, a pure codimension-one subcomplex. Contributions from earlier link facets also have codimension one.
Conversely, induct a shelling of C. For the last facet F, let R be its unique restriction face. If |R|<=d, then R is an allowed shedding face for (d-1)-decomposability, deletion is the preceding shelling prefix, and link is the simplex on F\R. If R=F, its full boundary lies in the preceding prefix, so full-boundary closure applies. The first facet is a simplex. Thus shellable implies (d-1)-decomposable. Monotonicity in k completes the assertion.

## The append lemma
If C and C union 2^F are shellable pure d-complexes, then every shelling of C can append F. If not, the intersection C intersect 2^F has an inclusion-maximal face T with |T|<=d-1. The link of T in the union is the union of lk_T C and the simplex on F\T. These have disjoint vertex sets: a common vertex would extend T inside the intersection, contradicting maximality. Both are nonempty and have dimension d-|T|>=1. Thus this link is disconnected. But links of shellable pure complexes are shellable, hence connected in positive dimension. Contradiction. The argument includes T=empty if it can arise; in the question's r=0 setting all vertices of F are old, so T cannot actually be empty and maximal.

## Simon equivalence including ambient vertices
Let Simon_d mean: every partial shelling of the full d-skeleton of a simplex extends to a complete shelling.
For k>=d-1, Simon_d implies b(d,k)=0 immediately from shellable=(d-1)-decomposable.
Conversely, suppose b(d,k)=0. Start with any partial shelling on ambient W, whose current vertex set is U. Its underlying complex is k-decomposable. Apply b=0 on U. The append lemma shows that each facet addition appends the GIVEN shelling, not merely some reordered shelling. This reaches the full d-skeleton on U. If U is not W, introduce each remaining vertex w by adding w*R for all d-subsets R of the current vertex set, in a shelling order of the full (d-1)-skeleton. The old full skeleton contains every R, so this is a shelling extension. Repeat. Thus the exact-vertex-set clause creates no loophole.

## Dimension three
The independently proved and implemented universal upper bound is b(d,k)<=d-2 for d>=3,k>=1. Consequently for every k>=2,

    b(3,k) = 0 if Simon_3 holds,
             1 if Simon_3 fails.

Equivalently b(3,k)=1-1_{Simon_3}. This is an exact conditional classification, not a decision of Simon_3. Neither direction requires Cohen-Macaulay algebra, characteristic choices, or an unverified computation.
