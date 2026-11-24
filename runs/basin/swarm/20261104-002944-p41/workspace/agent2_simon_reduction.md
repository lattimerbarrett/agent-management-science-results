# Exact relation of the missing lower bound to extendable shellability

Fix d>=1 and k>=d. A pure d-complex is k-decomposable if and only if it is shellable.

For the forward implication, induct on its decomposition. Shell the deletion first, then append the facets sigma union H as H runs through a shelling of the link. All sigma-avoiding faces are already in the deletion. Inside sigma-containing faces the shelling intersection condition is exactly the link shelling condition. This yields a shelling.

Conversely let F_1,...,F_t be a shelling, t>1. The intersection of the last simplex 2^{F_t} with the prior complex is a nonempty union of codimension-one faces of that simplex (the full boundary is allowed). Let R be the set of vertices v of F_t for which F_t minus v belongs to this intersection. This set is nonempty. A face G of F_t lies in the intersection exactly when it omits at least one vertex of R. Consequently the faces introduced by F_t are precisely the interval [R,F_t]. Hence deletion at R is the prior complex, and link at R is the simplex 2^{F_t minus R}. Since |R|<=d+1<=k+1, induction proves k-decomposability. (For a shelling whose last intersection is empty in dimension zero, the same interval statement uses R=F_t.)

Now suppose Delta is pure d and shellable, F is a missing (d+1)-set, and Gamma=Delta union 2^F is shellable. The intersection I=Delta restricted to F must be pure of dimension d-1. To prove this, suppose I has a maximal face G with |G|<=d-1. In link_G Gamma the simplex on F minus G and link_G Delta have disjoint vertex sets and no mixed faces: an intersection vertex would contradict maximality of G in I. Both sides have vertices, since Delta is pure and |G|<=d-1. Therefore this link has disconnected one-skeleton and dimension at least one. But links of pure shellable complexes are pure shellable, and a shellable complex of positive dimension has connected one-skeleton. Contradiction. Since F is missing, every maximal face of I thus has size exactly d.

It follows that appending F to ANY shelling of Delta is a valid shelling. In particular, a facet ordering whose every prefix is shellable is automatically a shelling extending any chosen initial shelling. Conversely every extension shelling has shellable prefixes.

Therefore b(d,k)=0 for k>=d is equivalent to the statement that every shelling of every pure d-dimensional subcomplex of the complete d-skeleton on V extends to a shelling of that complete skeleton. That is the standard extendable-shellability question for uniform matroid complexes (often called Simon's conjecture).

Thus the requested lower bound at d=3,k>=3 needs, at minimum, an explicit nonextendable shelling of a tetrahedral simplex skeleton. It cannot follow merely from a failure of vertex- or edge-decomposability in an augmented complex, nor from an arbitrary noncollapsible contractible complex. No such witness has yet been established by the team.


## Sharpening using the proved boundary-filling lemma

In fact, for d>=1, shellable is equivalent to (d-1)-decomposable. Induct on shelling length. If the final restriction face R has cardinality at most d, it directly sheds the final complex: deletion is the preceding shelling prefix and link is a simplex. If R has cardinality d+1, the preceding prefix contains the full boundary of F_t, and the general boundary-filling lemma preserves (d-1)-decomposability. The initial simplex starts the induction. Consequently the exact Simon reduction above already applies for k>=d-1; the requested d=3,k=2 lower bound itself needs a nonextendable shelling.

Independent exhaustive computational check: all1023 nonempty subsets of the10triangles on5ambientvertices give821shellable=821edge-decomposable; all32767nonempty subsets of the15tetrahedra on6ambientvertices give18153shellable=18153 2-decomposable. There are zero mismatches in either test.
