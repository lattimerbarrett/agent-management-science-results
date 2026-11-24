# A rigorously checked restricted-family exclusion

This does NOT prove the requested nonexistence result.

No full-divided-square-syndrome word of weights 322,326,330,334 is a sum of
at most five axis-aligned affine seven-flat indicators in F2^15.

For an even point set S put Q(S)=sum_{unordered {s,t} subset S}[s+t]
 + (|S|/2 mod2)[0] in F2[F2^15]. Then Q(S triangle T)=Q(S)+Q(T)+S*T.
For a seven-flat Q=0. Two coordinate seven-flats contribute zero unless
their free-coordinate seven-subsets are disjoint, in which case their
convolution is an affine coordinate hyperplane indicator.

If two summands have the same free-coordinate subset, they either cancel,
or their sum is an affine eight-flat. The remaining mixed (8,7,7,7) case
is ruled out by agent4_mixed_flat_bounds.py: full Q=1 forces one seven-flat
complementary to the eight-flat; normalize this pair and apply its bounds.
Cases with fewer summands reduce to the same three-flat checks therein.

Otherwise all five free seven-subsets are distinct. Their disjointness
graph lies in KG(15,7). It has no triangles or quadrilaterals. It has no
five-cycle, since each coordinate belongs to at most two sets on such a
cycle, which would require 35 <= 30. Thus this graph is a forest.
Color each edge by the unique coordinate omitted by its two endpoint
sets. The coefficient of that coordinate in Q is the parity of the number
of edges of its color. Full Q=1 forces each color to occur evenly.
Edges of one color form a matching (the complement inside its 14-set is
unique). Four edges would therefore form a properly two-colored path on
five vertices. Three consecutive colors j,k,j are impossible: if A,B
are disjoint missing j and B,C disjoint missing k != j, then j belongs
to C, so C cannot have an edge colored j. Zero edges gives Q=0.
Therefore there are exactly two independent edges of the same color.

Full Q=1 means the two hyperplanes contributed by these edges have
opposite offsets. One pair of seven-flats intersects and the other pair
is disjoint. Translate the intersection point to zero, call the omitted
coordinate t, and normalize the first pair to A=F2^7 x0 and B=0xF2^7
inside t=0. The other pair has complementary free seven-subsets C,D
inside these 14 coordinates, with C in t=0 and D in t=1.
There is one remaining seven-flat E.

The code agent4_affine5_coordinate_check.py exhausts the residual cases.
Permutations inside A and B normalize C by k=|Cfree intersection Afree|.
Permutations preserving all three free sets normalize C's offset by its
Hamming weights in the two fixed coordinate cells. Since the final word
has weight <=334, the three-flat slice A triangle B triangle C has weight
<=334; with distinct free sets its possible weights are 254,314,318.
The script checks these possibilities directly.

If E crosses both t-slices, it is H6 x F2 for a coordinate affine six-flat.
To get final weight <=334, |H intersection D| >=32, so H shares five or
six free coordinates with D. Every such free-coordinate choice, every
offset of D and every consistent offset of H is enumerated exactly.
If E lies in slice t=0, the slice t=1 contributes 128, so the four-flat
slice must have weight 194,198,202,206. Every relevant affine E7 is checked;
a union-size upper bound prunes only cases unable to reach these weights.
If E lies in slice t=1, the first slice has weight >=254 and the second
slice, the difference of distinct seven-flats, has weight >=128, impossible.

Executed checker output:
Checked 10 canonical triple seeds; 770560 crossing cases;
49920 slice0 cases. All assertions passed.
