# (64,96) zero2 branch: zero-row-moment case proved

Assume selectors have branches (0,a,b,h), on X6 x Y6, with a min64,
b second96, h weight in {162,166,170,174}, and h+a+b degree<=5.
Odd <a,b> implies a-support and affine hull L8 of b meet in a 2-flat,
on which b's quadratic is nondegenerate. Decompose b=B1+B2 with min64
flats intersecting in4-flat; a and B1 meet in a point. Coordinates give
 a=delta_Y, B1=delta_X, B2=1_{U4(X)=0}1_{W2(Y)=w}.
Their intersections with a have sizes1 and0/4 respectively.
We can align a with the constant row centroid of h by translating Y
only on selector t=1; this changes b,h but not a and leaves B1 fixed.
We can align B1 with the constant column centroid of h by translating X
only on selector s=1; this changes h but not a or b. Global translations
then put a=delta_Y, B1=delta_X, both h-centroids0. These are affine
transformations on the full14-space, not ad hoc polynomial changes.
The leading6-form is
 H6=prod X6 + prod Y6 + prod U4(X) prod W2(Y).
Every row/column has odd cardinality; first moments are constant because
mixed X1Y5/X5Y1 coefficients vanish. Row second moment P(X) is AFFINE,
as the mixed X2Y4 coefficient vanishes. Assume P identically0.

K=h+delta_Y has row parity, centroid and second moments0, so its Y-degree
is <=3. Its top6-form is prod X6+prod U4 prod W2. In particular its maximal
Y-degree j is2 or3. A nonzero K-row of degree <=j has weight>=2^(6-j),
so its h-row contributes excess >=2^(6-j)-2 over the baseline1. The total
excess is wt(h)-64 <=110.

j=3: Each Y3 coefficient has X-degree<=2, so its nonzero weight is16 or
>=24 by minimum/second distance. There are at most floor(110/6)=18
nonzero K-rows. Thus every nonzero Y3 coefficient is a minimum quadratic
with affine4-flat support. All these supports coincide, since the union
of distinct such supports has size>=24. Call this16-point affine flat A.
K is supported in A. Otherwise pick maximal Y-degree r outside A.
For r2, a coefficient has X-degree<=4. Its support outside A has >=2
points: choose any outside point, separate it from A by an affine
hyperplane, then restrict the coefficient to that5-space and use minimum
distance2. These outside rows cost >=2*14=28 excess, while the16 A-rows
cost >=16*6=96. Total124>110, impossible. For r1 the X-degree<=4 again,
so >=2 outside rows cost >=60, even worse. For r0 one row costs62.

All K-columns are odd and centroid0. An odd subset of A has centroid
in A, so0 in A and A is linear. Factor K=1_A k, on X_A4 x Y6. Then
k degree<=4 and its top4-form has only types X4 and X2Y2; in particular
there is no mixed X3Y1. (The X-only factor top(1_A) divides U4, since
it divides the Y2 part of top K.) Every one of16 rows has the SAME
nonzero cubic top in Y, so is at least8. Set gamma=wt k and
q=wt k(.,0). The latter is odd, hence q<=15, and
 gamma=wt h-64+2q <=140.
Thus at most3 rows can be non-minimum (second RM(3,6) weight12).
At least13 minimum rows are affine3-flat indicators with the SAME
leading cubic, hence with a COMMON direction V3. Choose Y coordinates
(z3,w3) with w3 the free V3 coordinates. Each coefficient of a Y-monomial
involving any w has X-degree<=2 (including Y1, since X3Y1 is absent).
It vanishes on at least13 X-points, so must vanish identically: a nonzero
quadratic in4 variables has weight>=4, not<=3. Thus k is independent of w.
Its weight gamma is8 times the weight of k' on X4 x Z3. All8 columns
of k' have odd cardinality, so wt k' is even; gamma is a multiple16.
Since128<=gamma<=140, gamma128. All16 rows are minimum and k' is the
indicator of a graph from X4 to Z3. Every one of its8 fibers is odd with
centroid0 in X4. At most one fiber is a singleton (that singleton must
be0); all others have at least3 points. This needs >=1+7*3=22 graph
points, contradicting16.

j=2: Each nonzero K-row costs >=14 excess, hence there are <=7 such
rows. The unique canonical Y2 coefficient can have X-degree4 and has
decomposable leading4-form U4; every other Y2 coefficient has degree<=3
and minimum weight8, hence is0. The canonical coefficient has weight<8,
so is a minimum4 word: weight6 is the second RM(4,6) type whose top form
is F2 times a rank4 quadratic, not decomposable (firm KT below2d).
Its support is an affine2-flat A. The same outside argument gives
4*14+2*30=116>110 for r1 and4*14+62=118>110 for r0. Thus K is supported
in A, and A is linear by the column centroid. Its annihilator is U4,
so A=T2, complementary to U4. Factoring K=1_A k gives k of degree2
with top2 equal prod T2+prod W2, a rank4 quadratic on8 variables.
Also gamma=wt K=wt h-64+2q <=174-64+6=116 since q<=3.
An unbalanced rank4 quadratic on8 variables has weights96/160;
a linear radical term gives balanced128. Thus gamma96, forcing
wt h=64+96-2q<=160, contradiction.

Conclusion: P=0 excludes all four (64,96) target branches. No KTA above
2d is used. The remaining orientation is wt h174 and P affine rank1.
The general moment argument forces all32 P0 rows minimal delta_Y and
P(0) nonzero; the degree5 difference g=h+a+b is supported on the P1
linear half A5 containing T2. This last orientation is not yet excluded.
