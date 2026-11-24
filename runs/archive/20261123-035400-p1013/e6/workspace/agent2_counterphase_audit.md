# Audit of the proposed projective-renderer counterphase (r=3,k=11)

This document audits, rather than presupposes, the proposed counterconstruction.
The issue is serious: the resulting example would contradict the supplied
universal third claim. No use of the disputed compatibility lemma occurs here.

## Exact one-part forest optimization
Let I be a graph avoiding K_{1,11}, the five-vertex fork (arms 2,1,1),
C_3,...,C_22, and P_12 disjoint-union P_11.
Then I is a forest whose components are stars of order <=11 or paths of
order <=22. Indeed triangle-free plus fork-free implies each component of
maximum degree >=3 is a star; components of maximum degree <=2 are paths or
cycles. Long cycles (order >=23) contain disjoint P_12 and P_11, and all
shorter cycles are explicitly forbidden. The same disjoint-path condition
bounds path order by 22. If there is a path of order >=12, every other path
has order <=10. Stars of order 11 are still allowed.

For every m>=12, the maximum edge number is
 f(m)=m-ceil(m/11)+1.
Upper bound: at most one component has order >11 and that component has
order <=22, so the number of components is at least ceil(m/11)-1. Each
component is a tree. The lower bound is a P_22, stars of order 11, and a
last smaller star when m>=22; for 12<=m<=22 simply take P_m.

For m=11q, equality f(m)=10q+1 is attained UNIQUELY by
 P_22 disjoint-union (q-2)K_{1,10}.
To have q-1 components on 11q vertices, the sole oversized component must
have order exactly 22 and every other component order exactly 11. Since
the oversized path forbids any other P_11, all remaining components are
stars K_{1,10}.

## Exact partition optimization
Take n=r*m0 with m0=11q. If the active class has size s=m0+d, its internal
edge gain relative to s=m0 is d-ceil(d/11). The cross-edge loss is
 D=(1/2)sum_i(delta_i)^2.
For integral deltas summing to zero, D>=|d| (indeed sum of squares of the
other deltas is at least their absolute sum, which is >=|d|).
If d>0, the internal gain is <=d-1<D. If d<0, the internal gain is <=0<D.
If d=0 but another class is unbalanced, D>0. Thus the edge-optimal partition
is uniquely balanced, irrespective of which class is active.

## Why a finite-template joint graph should be cross-complete
After the previously established cycle-max finite-template reduction, all
rare vertices are ordinary: each is adjacent to ALL normal vertices except
those in its assigned part. A positive-neighborhood vertex in every normal
class would embed the single-star payload and is impossible; a vertex
missing two classes loses linearly many edges and cannot be edge-extremal.

The two-active-edge payload forbids any internal edge outside the active
part: combine it with an internal edge in a fresh normal active component.
All cross edges required by the embedding are rare-normal or normal-normal,
so missing rare-rare cross edges do not obstruct this copy.

Every one-part payload present internally similarly embeds H using normal
vertices for all H vertices outside that payload. Therefore I avoids all
one-part patterns listed above. Completing all missing cross edges preserves
H-freeness if the projective rigidity equivalence is valid: internal degree
stays <=10, and the only permitted projection tests are precisely these
patterns and the impossible two-active-edge pattern. Thus a joint graph
must be cross-complete and has the unique edge-optimal phase above.

## Projection rigidity: self-contained proof
Let Q=K_r categorical-power d, r>=3. Its adjacency matrix is
 (J-I) tensor-power d.
The degree is (r-1)^d and the least eigenvalue is -(r-1)^(d-1), with
least-eigenspace consisting exactly of sums of one-coordinate zero-mean
functions. Hoffman's bound gives independence number at most r^(d-1).
At equality, an independent-set indicator has the form
 f(x)=1/r+sum_i g_i(x_i).
A Boolean additive-separable function has at most one nonconstant summand:
otherwise a 2x2 rectangle has values u,u+a,u+b,u+a+b in {0,1}, impossible
for nonzero a,b. Hence every maximum independent set is a coordinate fiber.
A proper r-coloring consists of r maximum independent sets. Fibers in
different coordinates intersect, so the coloring is one coordinate
projection, followed by a color permutation.

Blow every core cell up to h>rD vertices. If a coloring has monochromatic
maximum degree <=D, its dominant colors form a proper r-coloring of Q
(otherwise two adjacent dominant cells make monochromatic degree >D).
Thus dominants are a projection i. Any minority-colored vertex in cell w
has >D same-colored neighbors in a neighboring cell z with z_i equal to
its wrong color and all other coordinates different from w. Contradiction.
All cell vertices, and all additional vertices with prescribed coordinate
words and the same product adjacency to the core, therefore follow the
same projection i.
