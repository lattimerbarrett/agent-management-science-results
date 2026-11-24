# Complete pure-pair-six coset gap

**Theorem.** Let H be a Boolean function on X+Y, dim X=dim Y=6, of degree at
most6, with degree6 part equal to the sum of the full X and full Y monomials.
Then wt H is not194,198,202,206.

Inputs: elementary binary RM minimum/second weights and minimum supports;
the standard Kasami--Tokura classification below twice minimum distance;
and the independently checked four-affine-flat exclusion in F2^14
(agent2_four_affine_checker.py and its geometric lemma file).
No above-2d KTA classification is used in this theorem.

## 1. Moment normalization and row costs
Each row and column has odd weight. Its XOR (centroid) is constant, independent
of the row/column parameter, since the mixed degree6 coefficients vanish.
Independent translations of X,Y therefore make every row/column centroid0.
For a row T subset Y define the alternating second-moment matrix
P=sum_(y in T) yy^t (its diagonal is0 since the centroid is0).
P=P(x) is affine in x: its entries are sums of monomial coefficients of Y-degree
at least4, and the degree4 coefficients have X-degree at most1 because all
mixed degree6 coefficients vanish. Define Q(y) symmetrically.

For any odd set with centroid0, rank(P)<=|T|-1. Thus P=0 has row minimum1,
uniquely {0}; rank2 has minimum3, uniquely the three nonzero vectors in its
2-dimensional support; rank4 has minimum5, and any minimum5 row lies in the
4-dimensional support of P. These claims follow by writing one point as the
sum of the others; in a minimum row, its span equals the moment-matrix image.
If two rows have the same parity, centroid and P, their XOR has zero moments
through degree2, hence belongs to RM(3,6), minimum distance8.

## 2. Every P-value is decomposable
A rank2 alternating matrix is called decomposable; zero is also allowed.
Suppose P has a nondecomposable value. If its affine image dimension d>=3,
at least56 rows have P nonzero. A nonzero4-by-4 Pfaffian composed with the
affine map P is a nonzero quadratic Boolean function, hence is nonzero on at
least16 x's. These rows have rank at least4. The row-cost lower bound is then
64+2*56+2*16=208, impossible.

If d<=2 and0 is not an image, the baseline192 plus at least16 nondecomposable
rows already gives224. If0 is an image, d=1 with rank>=6 gives256; rank4 gives
baseline192. For d=2, two or more nondecomposable nonzero values give baseline
at least16*(1+3+5+5)=224. The only remaining case has values0,alpha,beta,gamma,
where alpha,beta are rank2 and gamma=alpha+beta has rank4. All their supports
lie in W=im gamma, dimension4. The d=1 remaining case also has such W.
Both cases have baseline192, and every minimum row lies in W.

Projection to Y/W, dimension2, has parity pattern delta0: parity, centroid,
and second moments determine this four-value pattern. Thus every actual row
has an odd number of points in W, in particular at least1. A nonminimal row
of minimum m in {1,3,5} and excess e>=2 has at most m+e-1<=3e points outside W.
Every outside column is odd and nonempty, so at least48 outside points are
needed. But total excess E<=206-192=14 gives at most42. Contradiction.
Thus all P-values are zero or rank2. The same holds for Q.

## 3. Pairwise intersection and minimal-row model
The supporting2-planes of nonzero P-values pairwise intersect. Otherwise take
two disjoint ones alpha,beta and gamma=alpha+beta of rank4. For every value eta,
eta+gamma is also in the affine image. Both eta and eta+gamma are decomposable,
so their supports are contained in im gamma=W4. Zero is not in the affine image.
The baseline is192; minimum rows lie in W. Nonminimum rows have at most2e
outside points (m=3, e>=2), so total outside is at most28, less than48.

A pairwise-intersecting family of2-planes either has a common1-space, or all
planes lie in a common3-space. Elementary proof: choose two distinct planes
U,V with common line L; if a third misses L it lies in U+V, and any plane not
contained in U+V would have to contain L and hence miss that third plane.
Consequently the affine P-image lies in a star u wedge Y (dimension5) or
Lambda^2 W3 (dimension3), and has affine dimension d<=5.

Let M(x) be the unique minimum row for P(x). Every M-column has even parity
and a constant centroid c. If d<=4, each P-fiber has dimension at least2,
so both its parity and its XOR are0; hence c=0. If d=5, the image is the full
5-dimensional star, and the kernel fibers are pairs with difference k.
For y=0, its M-column is the zero-P fiber; for y=u it is the union of31
nonzero fibers; for every other y it is one fiber. Each has even parity and
centroid k, so c=k in this last case.

Let B=wt M=64+2*#{x:P(x) nonzero}, E=wt H-B, and D=H+M.
Every nonzero row difference has weight Delta<=4e, where e is its row excess:
for a rank2 row, e>=2 and Delta<=e+6<=4e; for P=0, e>=6 and Delta<=e+2<=4e.
Every D-column is odd with centroid c. Put r=wt(D row c), and let e_c be that
row's excess. A column containing c costs at least1; a column missing c costs
at least3. Thus wt D>=192-2r. On the other hand
 wt D<=r+4(E-e_c),     r<=e_c+6.
Therefore4E>=192-3r+4e_c>=174. Since E is even, E>=44.
If0 is not in the image, B=192, impossible. If d>=3, B>=176, also impossible.
Thus P and Q have affine dimension at most2, and their images contain0.

## 4. Excluding dimension2
Dimension2 has B=160, so E>=44 leaves only target206, E=46.
For P, let m0 be its minimum at row0, e0 that row's excess, r its D-row weight,
and z the number of other P-zero rows which are nonminimal.
For each such zero row,4e-Delta>=16. Since M-column centroids now equal0,
 192-2r <= wt D <= r+4(46-e0)-16z.
So4e0-3r+16z<=-8. Using r<=e0+2m0 gives
 e0+16z<=6m0-8.
For m0=1 this is impossible; hence m0=3, e0<=10,z=0. All16 zero-P rows are
{0}, and row0 of H has weight at most13.
If Q has dimension0 or1, it has64 or32 zero columns. At most13 can be the
minimum singleton {0}; the other zero columns have excess at least6.
This costs at least306 or114, exceeding their total excess142 or78.
If Q has dimension2, its same argument forces all16 zero-Q columns to be
{0}, giving row0 weight at least16, also impossible. Thus neither P nor Q
has dimension2. Both have dimension at most1 and images containing0.

## 5. Short reduction to the standard <2d theorem
Set g=H+delta_X+delta_Y, v=wt g, r=wt(g row0), c=wt(g col0), epsilon=g(0,0).
Then degree g<=5 and the exact identity is
 s=wt H-126 = v-2r-2c+4epsilon, with s<=80.
Every g-row has zero parity and centroid. Except in at most32 rows its second
moment is0, and then a nonzero row has weight at least8; in those at most32
rows it has weight at least4. Count the c rows containing column0, then add
the exact row0 weight separately. This gives
 v>=8c-128+r-8epsilon.
The transpose gives v>=8r-128+c-8epsilon. Hence
 9(r+c)<=2v+256+16epsilon,
 9s>=5v-512+4epsilon,
so v<=246.4.

The Kasami--Tokura theorem for RM(5,12), minimum128, now leaves only
v=0,128,192,224,240. Zero would give H=delta_X+delta_Y of weight126.
The128 case is one affine7-flat; the192 case is two such flats; each224/240
case is either two such flats, or a rank6/rank8 quadratic times three linear
factors. In the latter cases g is supported in an affine9-flat L.

Let A,B be the two complementary6-flats (the delta axes). In the exceptional
quadratic case I=|g intersect(A triangle B)|=(v+126-wt H)/2>=72. But I<=70:
if L contains0 and g(0)=1, putting p=dim(L intersect A),q=dim(L intersect B)
gives p+q<=9 and I<=2^p+2^q-2<=70. If g(0)=0, restrictions to A,B have even
weights and omit0, so the upper bound improves to68. If L avoids0, two
nonempty intersections have p+q<=8, giving I<=68; one empty gives at most64.
Contradiction.

In all other cases g is the XOR of at most two affine7-flats. Introduce two
new variables t,s and form
 F(t,s,x)=t*1_A(x)+s*1_B(x)+ts*g(x).
Its four branches are0,1_A,1_B,H, and its weight is128+wt H, one of the four
forbidden322,326,330,334. It is the XOR of at most four affine7-flats in14
variables, contradicting the independently checked four-flat theorem.
This proves the stated coset gap.

## Appendix: pure-pair-five gap (dimension10)
The identical normalization for dim X=dim Y=5 proves: if wt H<=82, then wt H=62.
Here P,Q are affine. A nondecomposable value with image dimension>=3 gives
baseline32+2*28+2*8=104; image dimension<=2 gives at least96. Thus all values
are decomposable. Zero must be an image (otherwise baseline96), and image
dimension is at most2 (otherwise baseline88). Consequently minimal-row model
M has even columns and centroid0 (fibers dimension>=3). The excess calculation
is4E>=3*32-18=78, so even E>=20. Image dimensions1,2 have baselines64,80,
which would give weight at least84,100. Thus P=Q=0 for EVERY weight at most82.
Now g=H+delta_axes lies in RM(4,10), minimum64, and each nonzero row/column has
zero moments through degree2, hence weight at least8. Therefore v>=8r,8c,
and wt H-62=v-2r-2c+4epsilon>=v/2. A nonzero g costs at least32, so wt H>=94. Zero g gives62. Consequently the ONLY pure-pair-five coset weight at most82 is62.
