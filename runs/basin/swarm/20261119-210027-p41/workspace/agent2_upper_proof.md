# Constructive upper bound
For every d>=3,k>=1, b(d,k)<=d-2.

## Full-boundary closure
If C is k-decomposable and F is a missing facet of its dimension with full boundary contained in C, then C+F is k-decomposable. Induct along any shedding face sigma of C. If sigma is not contained in F, only the deletion gains F, whose boundary lies in the old deletion. If sigma is contained in F, deletion is unchanged and link gains F\sigma with its full boundary already present. Induct on vertices/dimension. A simplex cannot satisfy the hypothesis for a new F in positive dimension; dimension zero is immediate.

Consequently shellable d-complexes are (d-1)-decomposable for d>=1: induct a shelling; its last restriction face either has size<=d and is permitted, or is the full facet and full-boundary closure applies.

## Base dimension two
A connected graph underlying a shellable pure 2-complex can have every missing edge inserted by adding a triangle on a length-two path with the opposite edge missing. The attachment is along precisely two edges, hence is a shelling extension. Once the graph is complete, insert all remaining triangles along their complete boundaries. All intermediates are shellable, thus 1-decomposable and k-decomposable for k>=1.

## Initial cone lemma
For a new vertex a, C can be enlarged to C union a*skel_{d-1}C by facet additions preserving k-decomposability. Induct original shedding sigma, with deletion D and link L. First perform initial cone construction for D, keeping sigma as shedding and L unchanged. Then lift initial cone construction for L by joining sigma. Faces avoiding sigma needed for purity are present in the completed cone over D. Base simplex: adding any subset of its apex-coned ridges gives a partial simplex boundary, which is vertex-decomposable.

## Filling lemma
Let Lambda be pure (d-1)-dimensional and k-decomposable, and let S be any collection of (d+1)-sets whose boundaries lie in Lambda. Then a*Lambda union the simplices on S is k-decomposable. Induct a shedding sigma of Lambda. Deletion and link have the same form with del_sigma Lambda and lk_sigma Lambda. Any proper remnant of an old F containing sigma and avoiding sigma is already in del_sigma Lambda. The boundaries of the link old facets lie in lk_sigma Lambda. Base simplex permits no old F, except dimension-minus-one case, which gives a pure zero-dimensional complex.

## Induction
Choose apex a and d-3 further auxiliary vertices B. First apply initial cone lemma. Complete Lambda=skel_{d-1}C by dimensional induction on V union B, lifting each new link facet R to aR. The filling lemma verifies every intermediate. At the end all d-facets through a are present. The resulting complex remains vertex-decomposable after adding any subset of the remaining facets: delete any non-apex vertex; deletion and link have the same full-apex-star form. Thus insert all remaining facets in arbitrary order.

Implementation: workspace/agent2_upper_construction.py computes the actual ordering and uses an exact recursive shedding oracle to check each intermediate and final skeleton equality. Executed for 26 admissible random inputs in (d,n,k)=(3,6,1),(3,7,1),(4,6,1), all successful.

This is only an upper bound. It does not decide whether any auxiliary vertices are necessary. For k>=d-1, zero auxiliaries is equivalent to Simon's dimension-d conjecture.
