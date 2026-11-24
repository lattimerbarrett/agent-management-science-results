# Direct exclusion of both (64,112,154/158) branches, without KTA above2d

Let a,b,h in RM(6,12), a+b+h degree<=5, wt a64, wt b112,
wt h154 or158. Their leading6-forms satisfy H=A+B. Odd total half-weight
implies <a,b>odd. We use only the firm KT below2d classification of b,
and the already-proved general affine row-moment lemmas:
For an h with odd centroid-zero6-variable rows AND columns, affine row
second-moment P, and wt h<=158, P must0. Indeed nondecomposable moments
force weight>=192, all decomposable values give either image avoiding0
(baseline192), or linear image rank>=2 (baseline160), or rank1 with
baseline128 and excess>=44, requiring weight>=172. Hence P0.

TYPE Q: b is the rank6 quadratic with4 support factors, affine span8.
Its intersection with the min6-flat a has dimension exactly2 with a
nondegenerate quadratic restriction: dimension>=2 by spans and <=2 by
odd intersection. Choose this symplectic plane as one quadratic pair.
Coordinates X6=T2+U4,Y6 put the leading form into
 H=X6+Y6+U4*q4(Z), where q4 is rank4 quadratic in4 Y coordinates.
All row and column first moments are constant (no X1Y5/X5Y1 top terms),
so translate X,Y to make them0. The row second moment P is affine
(no X2Y4 term), hence0 by the general moment lemmas. Put K=h+delta_Y.
Then its Y-degree<=3, its top is X6+U4*q4(Z), and wt h-64<=94.
If maxYdegree3, a leading coefficient has X-degree<=2, minimum16;
each such row costs at least6 h-excess, giving >=96>94, impossible.
If maxYdegree2, there are <=floor(94/14)=6 nonzero rows. Any Y2
coefficient with nonzero leading4-part has decomposable top U4, and
weight<8, hence is a minimum4 word by firm KT (the second weight6
has nondecomposable top). All remaining Y2 coefficients have degree<=3,
minimum8, and are0. The nonzero leading coefficients are minimum words
with the SAME top U4, hence are parallel affine2-flats; distinct supports
are disjoint and have union8>6. Thus all supports are the same A2.
An outside row of degree1 yields >=2 outside points by punctured
minimum distance (coefficient degree<=4), costing >=60 excess, while
inside A2 costs >=56; constant outside costs62+56. Both exceed94.
Thus K supported in A2. Odd centroid-zero columns force A linear.
Factoring K=1_A k leaves a rank6 quadratic top X_A2+q4(Z) on8 variables.
Such a quadratic has weight>=112. But wt K=wt h-64+2q<=158-64+6=100,
where q=wt K(.,0)<=3 is odd. Contradiction.

TYPE P: b=B1+B2, two min6-flats meeting in a3-flat.
Odd <a,b> lets us choose B1 with odd a-intersection, hence meeting it
in a point. Their directions are complementary. In X=a,Y=B1 coordinates,
B2's leading form is U3(X) wedge eta3, with
 eta3=product_{i=1}^3 (z_i(Y)+M_i(X_T3)),
where z1,z2,z3 are independent Y forms, X_T3 is complementary to U3,
and rank M<=2. The last fact follows because a and B2 have even
intersection: if their directions were complementary they'd meet in
one point; thus their direction intersection has dimension>=1.
By independent basis changes put M in diagonal rank d=0,1,2 form.
The top H=X6+Y6+U3 eta has constant row centroid, but its column centroid
may have a linear part if d2. In that case write X_T=(x1,x2,x3) and
 eta=(z1+x1)(z2+x2)z3. The linear column centroid is x3_direction*z3.
The rank-one shear x3 -> x3+z3 cancels it: B2 is unchanged since eta
is independent of x3, while X6 adds exactly U3*x1*x2*z3. Consequently,
in all cases (after this shear if needed),
 H=Y6+U3*(x1*x2*x3+z1*z2*z3+e1*x1*z2*z3+e2*x2*z1*z3),
with e1,e2 in{0,1}. Both centroids are now constant; translate to0.
The row moment P is still affine (top maxYdegree3), hence0 as before.
Set K=h+delta_Y. MaxYdegree3. There are <=floor(94/6)=15 nonzero rows.
The sole potentially degree3 leading Y3 coefficient has decomposable
top U3 and weight<16, hence is a minimum8 word by firm KT; the other
Y3 coefficients degree<=2 and minimum16 must vanish. Let A3 be this
common affine3-flat support, parallel to T3.

K has no support outside A. For a maximal outside Y-degree r2, the
coefficient has degree<=4 and its TOP4 is divisible by U3 (from the
displayed top H). Separate an outside point from A by a hyperplane
lambda in U3. Restriction kills the degree4 part, so on5 variables it
has degree<=3 and at least4 outside points. Thus excess is at least
8*6+4*14=104>94. For r1, the same argument gives degree<=4 on5 variables,
at least2 outside points, and excess>=48+60=108>94. For r0, excess>=110.
Thus K supported in A3, linear by the column centroid condition.
Factor K=1_A k. Then k has degree<=3 on9 variables, and its top3-form
in the6-dimensional X_A3+Z3 space is
 omega=x1*x2*x3+z1*z2*z3+e1*x1*z2*z3+e2*x2*z1*z3.
Its middle exterior quadratic invariant is1: the X3/Z3 complementary
pair contributes1 and the other monomials have no complements. Each
of the8 slices of the remaining3 unused variables therefore has weight
2 mod4. Its minimum weight is at least14 by firm KT in RM(3,6): below16
the only weights are8,12,14, of which only14 is2 mod4.
Thus wt K>=8*14=112. But wt K=wt h-64+2q<=158-64+14=108 (q<=7odd).
Contradiction. Both types excluded without KTA above2d.
