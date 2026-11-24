# A full-rank critical word represented by five minimum flats has only six Q-graph types

This is a constructor obstruction, NOT a proof of the original spectrum claim.
The executable arithmetic/isomorphism audit is agent4_fiveflat_Q_degree_checks.py.

Assume S is a coorder-seven support in F2^15, of weight
w in {310,322,326,330,334}, with affine span15, and Q identically1.
The final condition is necessary for any genuinely new weight in dimension15,
as proved in the team's pair-parity lemma. Suppose S is a sum of five minimum
words, affine7-flats H_i=b_i+U_i. Take a representation minimal in number of
minimum words. No actual pair intersection has64 points (two such minimum
words sum to another minimum word), and no two flats coincide. Thus every
actual pair intersection has at most32 points.

Define Q-graph edges ij by U_i intersect U_j=0. Such pairs contribute the affine
hyperplane indicator 1+L_ij(v)+L_ij(b_i+b_j) to Q, where L_ij is the unique
nonzero annihilator of U_i+U_j. Other pairs contribute zero; individual minimum
words contribute zero. Consequently sum_edges L_ij=0.

## 1. At most four edges, at least two edges

Writing E for the number of edges, each edge pair intersects in at most1 point.
The elementary odd-multiplicity Bonferroni inequality gives

 (640-w)/2 <= sum_(i<j) |H_i intersect H_j| <= 32(10-E)+E.

For these weights (640-w)/2 >=153, so E<=5. If E=5, all five nonedge actual
intersections must have size32: replacing even one by at most16 drops the upper
bound165 to149. Thus the five nonedges are exactly direction intersections of
dimension5. This relation is transitive here: two5-subspaces of the same
7-space intersect in dimension at least3, forcing the opposite pair to be a
nonedge. Hence the nonedge graph is a union of cliques. No partition of five
vertices gives five clique edges (checked exhaustively); contradiction. So E<=4.
E=0 gives Q=0 and E=1 cannot have normal sum0. Therefore 2<=E<=4.

## 2. Boundary256 dichotomy needed below

The already proved boundary256 classification says: a coorder-seven weight256
support is either an iterated graph over a full8-flat, or the exceptional support
of intrinsic dimension10, whose graph labels are affine (hence do not increase
intrinsic dimension).

For a graph over F2^8, every graph label is quadratic: the K_5 moment conditions
against original base monomials of degree at most5 force base degree at most2.
Subtract affine parts of all labels. Intrinsic extra coordinates give independent
homogeneous2-forms q_1,...,q_k. Coorder seven forces q_i wedge q_j=0 for i!=j:
in the graph indicator product(1+y_i+q_i), the coefficient of all graph variables
except y_i,y_j is (1+q_i)(1+q_j), whose degree must be at most3.

If one q has rank>=6, the kernel of multiplication q wedge - on2-forms is <q>,
so k<=1. Proof in the canonical pairing basis: every coefficient on an off-pair
vanishes by choosing a third disjoint canonical pair; coefficients on the
canonical pairs must all agree.
If one q has rank4, all other forms are supported on its active4-space (mixed
and radical coefficients vanish by wedging). The wedge pairing on its6-dimensional
space of2-forms is nondegenerate alternating, so k<=3.
Finally if all nonzero forms have rank2, their2-dimensional supports intersect
pairwise. Either all share one line, or all are contained in one3-space: take two
planes meeting in L, then any plane not containing L lies in their3-dimensional
sum; it forces every other plane into that same3-space. In the latter case k<=3.
In the common-line case q_i=l*a_i, and splitting base by l=0/1 writes the support
as the disjoint union of TWO affine7-flats.

Thus every boundary256 support either is a union of two minimum7-flats, OR has
intrinsic affine dimension at most11. This argument uses the completed boundary
classification but no additional enumeration.

## 3. Q-degree four is impossible

Remove a degree-four flat H. Its intersection I with the XOR T of the other four
flats is at most4, so wt(T)=w-128+2I. For the five critical w, these ranges are
182..190,194..202,198..206,202..210,206..214. Every range consists of strict KT
gaps for coorder seven. Impossible.

## 4. Q-degree three is incompatible with full affine span15

Remove a degree-three flat H. Its intersection with the one nonneighbor flat has
size r in {0,1,2,4,8,16,32}; its intersections with the three neighbors have at
most one point each. Hence I=|H intersect T| satisfies |I-r|<=3 and I<=35.
Then wt(T)=w-128+2I<=276. The globally established spectrum through276 is
{0,128,192,224,240,248,252,254,256,272}; using it is essential here.
The exhaustive arithmetic in the checker leaves exactly:

 w310: (wtT,I)=(192,5),(240,29),(248,33),(252,35).
 w322: (224,15),(252,29),(254,30),(256,31).
 w326: (224,13),(256,29).
 w330: (224,11),(240,19),(272,35).
 w334: (224,9),(240,17),(272,33).

For weights192,224,240,248,252,254, strict KT bounds the intrinsic affine spans
by9,10,11,12,13,14, respectively. All weight272 supports have span<=11 by the
completed272 classification. If I points lie in H intersect T, its affine hull
has dimension at least ceil(log2 I). Thus

 dim aff(S) <= dim aff(T)+7-ceil(log2 I).

All listed cases give at most14, EXCEPT the weight252/254 cases in the w322 row
and the weight256 cases before using the dichotomy. The weight252/254 strict-KT
supports are sums of two minimum7-flats. In the boundary256 case, the dichotomy
gives the same statement OR span<=11, the latter making the join bound<=13.

It remains to exclude S as a sum of at most three minimum flats with Q=1 and
critical weight. This has a direct proof. With three flats, normal sum0 rules
out one-edge Q-graphs; a triangle also cannot work (its three normals would all
annihilate each pair sum, forcing their span to have dimension1, but then their
odd sum is nonzero). With two edges, their normals coincide L, and Q=1 forces
the two leaves into opposite affine ker(L) cosets. The center lies in exactly
one coset, meets that leaf in one point, and is disjoint from the other; leaves
are disjoint. The weight is therefore exactly3*128-2=382, not critical. Zero
edges give Q=0. This completes the degree-three exclusion.

## 5. The six possible graph types

The Q graph has2..4 edges and maximum degree<=2. For three edges, a triangle
or a four-vertex path is impossible. In each case normal sum0 forces the middle
complementary pair to annihilate a normal space of dimension at least2, a
contradiction (rank1 would make all three nonzero normals equal and their sum
nonzero). Exhausting simple graphs on five vertices leaves precisely:

 2 edges: P3 plus two isolated vertices; 2K2 plus one isolated vertex.
 3 edges: P3 plus K2.
 4 edges: P5; C4 plus one isolated vertex; C3 plus K2.

The checker enumerates all1024 labeled graphs and confirms exactly six
isomorphism classes. None of these classes has yet been globally realized or
excluded. Abstract rank SAT results alone would not realize affine flats.
