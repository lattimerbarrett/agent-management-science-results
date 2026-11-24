# Checked proof: the zero-second-moment orientation in the (64,64) coset

Let X=Y=F2^6. Let h have degree at most6 and homogeneous degree6 part
prod X + prod Y. Translate X,Y separately so every row and column has
centroid0. This is possible since all mixed degree6 coefficients vanish,
so each centroid is constant. Each row and column has odd cardinality.
Assume wt(h) in {194,198,202,206}.

For a row T, let P(T)=sum_{v in T} vv^t over F2; its diagonal is0.
Assume P(T)=0 for EVERY row. We use the independently proved global lemma:
the affine image of column moment Q(y) contains0 and has vector-space
dimension at most2 (agent1 Slack228). All its matrices have rank at most2;
this was proved without KTA by the Plucker/48-outside argument (Slack223).

Set K=h+delta_0(Y). Each K-row has parity, first, second moments0,
hence degree at most3. The total degree6 homogeneous part of K is prod X.
For j=maximal Y-degree of K, suppose j>=1. Each nonzero row has weight
at least 2^(6-j), hence contributes >=2^(6-j)-2 excess over the baseline
one point per h-row. Since wt(h)-64<=142, the number of nonzero K-rows
is <=23,10,4 for j=3,2,1 respectively. A coefficient of a Y-monomial of
degree j has X-degree <=5-j, since mixed top degree6 terms vanish.
Its nonzero weight is at least 16,8,4 respectively, with next weight
at least24,12,6. Thus every nonzero leading coefficient is a MINIMUM
RM word, all with the SAME affine support A: two different minimum
supports have union size at least1.5 times their size.
So A is an affine (j+1)-flat.

K has NO support outside A. Otherwise choose maximal Y-degree r among
rows outside A. If r>=1, a relevant coefficient has X-degree <=5-r;
its support outside A has size >=2^r: separate any outside point by a
hyperplane containing A, restrict to its complementary half-space,
and apply the RM minimum-distance bound there. On these outside rows,
K has degree <=r and weight at least2^(6-r), hence h-row excess >=
2^(6-r)-2. The outside excess is at least64-2^(r+1)>=64-2^j.
If r=0, one nonzero constant row gives excess62, which also exceeds
64-2^j. The rows inside A already give excess at least
2^(j+1)*(2^(6-j)-2)=128-2^(j+2). The total would be at least
192-5*2^j, equal152,172,182 for j3,2,1, all >142.

Every K-column is odd with centroid0; since supported in A, its odd
centroid belongs to A. Thus0 in A, so A is LINEAR. Put d=j+1 in{2,3,4}.
Factor K=1_A(X) k(X_A,Y). Then k has degree <=d and its homogeneous
degree d part is prod X_A. It has NO mixed degree-d coefficients.
Its columns are odd and centroid0. Let gamma=wt(k), t=wt(k(.,0)).
Then wt(h)=64+gamma-2t, t<=2^d-1, so gamma<=142+2*(2^d-1).
The column second moments Q of k are the same Q as h, embedded in A;
in particular their affine image contains0 and has dimension r<=2.

If r=1, or r=2, the planes in Q share a common vector u: for r2 the
three nonzero decomposable bivectors form a linear plane, and the two
generating 2-spaces must intersect. Write Q(y)=u wedge L(y), L affine.
Define M(x,y)=delta_u(x)+delta_{L(y)}(x)+delta_{u+L(y)}(x).
This is the unique minimum odd centroid0 column for its moment:
weight1 at Q0, weight3 otherwise. M has degree<=d and top part prod X_A;
indeed its last two affine graphs are parallel so their top parts cancel.
Its weight B is128 if r1,160 if r2. In each nonminimum column, with
excess e over the minimum1 or3, the symmetric difference from M has
weight <=4e. Hence wt(k+M)<=4*(gamma-B). Also degree(k+M)<=d-1 on
d+6 variables, so its minimum nonzero weight is128 and second weight192.

* d=4: gamma<=172. If r2, wt(k+M)<=48<128, hence k=M; then
  wt(h)=64+160-2t is218 or222, impossible. If r1, wt(k+M)<=176<192,
  hence k=M or k+M is a minimum128 word, i.e. affine7-flat R.
* d=3: gamma<=156. r2 is impossible already by gamma>=160. If r1,
  wt(k+M)<=112<128, hence k=M and wt(h)=186 or190.
* d=2: gamma<=148. r2 cannot occur since exterior-square A has dimension1.
  For r1, wt(k+M)<=80<128, hence again wt(h)=186 or190.

In the d4,r1 case, after embedding in the original12-space, M is one
6-flat parallel to delta_X plus a 7-flat D (the last two parallel graph
6-flats unite into D). Thus h is delta_Y + a parallel translate of
 delta_X + D + R, with D,R affine7-flats (R possibly absent).
For original f with four selector branches (0,delta_X,delta_Y,h), pair
parallel6-flat branches into two7-flats; D,R each lift unchanged to the
last selector quadrant. Therefore f is XOR of at most4 affine7-flats,
which the independently verified four-affine-flat theorem excludes
at weights322,326,330,334.

It remains r=0, where all column second moments vanish. Thus
k+delta_{X_A} has X_A-degree <=d-3.

* d2: k=delta_X_A, giving h126.
* d3: k=delta_X_A+u(Y), deg u<=2. Then
  wt(h)=126+6*(wt(u)-2u(0)); a nonzero nonconstant quadratic u has
  weight>=16, so this is >=210. The constants give126 orlarger.
* d4: k=delta_X_A+u(Y)+x dot v(Y), deg u<=3, deg v<=2.
  A column with v0 has weight1 or15; with v!=0 it has weight7 or9.
  Since gamma<=172, at most18 y have v(y)!=0. If v nonzero, every
  nonzero component is a minimum weight16 quadratic on Y; two distinct
  such supports unite in >=24 points. Thus v=beta*1_B for a common
  affine4-flat B. These16 columns already contribute at least112,
  and the remaining48 at least48, total160. Any u1 outside B adds14,
  impossible; so u is supported in B. Factor u=1_B*ell, deg ell<=1.
  If ell is not identically1 on B, at least8 B-columns have weight9
  rather than7, giving gamma>=176. Thus ell1, gamma160, and t1 or7,
  so wt(h)=222 or210. If v0, wt(h)=126+14*(wt(u)-2u(0)), which cannot
  equal194,198,202,206 (their differences from126 are68,72,76,80,
  none divisible14).

Finally j0 gives K=p(X), so wt(h)=64+62wt(p); since wt(p) odd, this
cannot be194,198,202,206.

CONCLUSION: provided the independently proved global moment-image
lemma, P_row=0 or symmetrically P_col=0 excludes all four target h,
using only standard minimum/second weights and minimum-word flat form.
The proof is for the (64,64) zero2-flat branch, NOT arbitrary f yet.
