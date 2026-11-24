# Bounded-defect color-profile realization for r>=3

## Power-coloring fact (complete proof)
The categorical power P=K_r^{times m} has vertex set [r]^m; two tuples are adjacent iff they differ in every coordinate. For r>=3 every proper r-coloring is pi(x_j), a coordinate projection followed by a permutation.

Indeed P has N=r^m vertices, degree d=(r-1)^m, and adjacency eigenvalues (-1)^s(r-1)^{m-s}. Its least eigenvalue is uniquely the s=1 level, tau=-(r-1)^{m-1}. The Hoffman independent-set bound gives alpha<=N/r. To recall the equality argument, for an independent set S of density a use f=1_S-a and 0=<1_S,A1_S>=a^2 dN+<f,Af>>=a^2 dN+tau a(1-a)N. Hence a<=1/r. Equality forces f into the tau-eigenspace, so 1_S=1/r+sum_j g_j(x_j). A {0,1}-valued sum of independent one-coordinate functions has at most one nonconstant summand: two nonzero coordinate differences would give four numbers t,t+A,t+B,t+A+B all in {0,1}, impossible. Its mean then makes S exactly a slice {x_j=c}. Every color class of a proper r-coloring has size N/r, so is a slice. Disjoint slices must use the SAME coordinate. This proves the fact.

## Exact relation gadget
For any finite relation R={t^1,...,t^m} subset [r]^d whose d column vectors are distinct, take P above and distinguish vertex x_i=(t_i^1,...,t_i^m). Distinguished diagonal vertices p_c=(c,...,c) form an r-clique. Proper r-colorings with p_c colored c give precisely the tuples in R. Without pinning the palette, the profiles are the global color-permutation closure of R. This is completely explicit (possibly enormous).

## Robust inequality gadget
Fix a desired maximum monochromatic degree Q, and choose M>rQ. For each edge uv of the relation gadget, REPLACE its proper-color requirement by the following graph, using private new vertices. Add r-1 pairwise completely joined independent sets A_1,...,A_{r-1}, each of size M, and M independent clones z_1,...,z_M. Join every A_i to u and to every z_j, and join every z_j to v. (No uv edge is needed.)

In ANY assignment of vertices to r classes with monochromatic degree at most Q, each A_i has at least Q+1 vertices in one class, so all vertices joined to A_i avoid that class. Different A_i reserve different classes. Consequently u and every z_j are in the single remaining class. Since v has M>Q neighbors z_j there, v is in a different class from u. Thus every protected uv inequality holds exactly. Conversely any proper r-coloring with u!=v extends properly over this gadget: put all z_j in u's color and put the r-1 independent anchor sets in the other colors.

## Application to prescribed finite monochromatic patterns
Let W be the disjoint union of finitely many graphs F_i, together with a star of D leaves centered at a new vertex v. Each F_i is a disjoint union of trees and chordless unicyclic graphs (in particular chi(F_i)<=3). Specify finitely many profile types: in type i the required vertices/edges of F_i occupy prescribed color classes, and all other F_j and the root star are properly colored. Add a special star type in which the whole root star has one color and every F_j is properly colored. Allow all global color permutations and all proper color choices in the inactive components. Assume every type has at least one monochromatic edge. Let R be the finite set of these profiles.

The columns of R can be chosen distinct: trees and chordless unicyclic graphs admit proper 3-colorings separating any specified pair of distinct vertices, and inactive components can be recolored independently; leaves of the root star can be separated in any nonstar profile, since r-1>=2. Global permutations ensure no column is a constant palette column. (If more general F_i are wanted, distinct-column separability must be checked separately.)

Take the exact relation gadget, robustify every edge with M>rQ, and add the UNPROTECTED actual edges of W. Call the resulting simple graph H. Then:
* H is not r-colorable: a proper coloring induces a relation profile, each of which has a prescribed bad edge of W.
* H-v IS r-colorable: use the special star profile; the only bad edges of W were incident with v, and all robust gadgets extend properly. Thus chi(H)=r+1 and v is critical.
* In any r-partitioned host with monochromatic degree <=Q, every H-copy induces one of the prescribed profiles on W. Therefore its prescribed monochromatic pattern occurs in the host.
* Conversely, in a complete r-partite host with bounded internal modifications, whenever a prescribed monochromatic pattern occurs, H embeds for sufficiently large part sizes: map that pattern first and embed every other vertex of H into distinct fresh bulk vertices according to the selected proper extension. All required cross edges exist. The same holds with finitely many cross holes provided each used pattern vertex is fully adjacent to the opposite bulk.

Choose D=Q+1. The special star profile is impossible in hosts of internal maximum degree Q, so precisely the prescribed F_i patterns determine H-containment there. The special profile simultaneously makes H critical and supplies a star decomposition. Including a one-color linear-forest profile supplies the genuine classical Simonovits hypothesis.

## Status
This lemma gives a route to arbitrary finite component-pattern realization for r>=3, overcoming the failed attempt to derive all such patterns from chi3 apex bases. It is NOT by itself a solution of the original problem: one must still specify sharp phase/residue classes, prove their edge and cycle extrema, handle the r4 equality case, and finish the global cycle-template reduction/lower bound. The construction proof above is explicit and not an appeal to unspecified CSP universality.
