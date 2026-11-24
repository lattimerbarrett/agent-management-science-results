# Complete exclusion of the zero-2-flat branch (96,112,126)

Suppose a,b,h are in RM(6,12), have weights 96,112,126, and a+b+h has degree
at most 5. Their degree-6 leading forms alpha,beta,gamma satisfy gamma=alpha+beta.
Treat degree-6 leading forms as elements of Lambda^6(V), dim V=12 over F2.
This is covariant under affine changes: translations do not affect the top form,
and repeated variables under linear substitutions lower the squarefree degree.

The standard <2d Kasami--Tokura forms give:
* alpha = (u1 wedge ... wedge u4) wedge q, where q is a rank4 2-form.
  Its exterior support U has dimension8.
* beta is either common4 wedge rank6 2-form (support10), or
  common3 wedge (p1p2p3+q1q2q3), with the two triples independent (support9).
* gamma is the sum of two decomposable 6-forms on complementary6-spaces,
  so its exterior support is all of V.

Let T_omega:Lambda^3 V* -> Lambda^3 V be contraction by omega. In matching
monomial bases it is a symmetric matrix over F2. Direct exterior-degree counting
(or the supplied 0.01-second Python checker) gives
rank(T_alpha)=32, rank(T_betaI)=44, rank(T_betaII)=38, rank(T_gamma)=40.

Rank inequality: if A,B are symmetric matrices and their images meet in a
t-space, rank(A+B) >= rank(A)+rank(B)-2t. Indeed the stacked map x->(Ax,Bx)
has rank rank(A)+rank(B)-t since the row spaces equal the column spaces;
projection (u,v)->u+v loses at most t further dimensions.

For betaII: support U_beta has dimension9. Since gamma has full support,
U+U_beta=V, so W=U intersect U_beta has dimension5. The two contraction images
meet in Lambda^3 W, whose dimension is C(5,3)=10. Thus rank(T_gamma)>=
32+38-20=50, contradicting rank40.

For betaI: W=U intersect U_beta has dimension6. We need a sharper image bound.
Write U=F directsum Q, dim F=dim Q=4, alpha=vol_F wedge q with q rank4 on Q.
Then the contraction image S is the direct sum
Lambda^3 F (dimension4), Lambda^2 F wedge Q (dimension24), F wedge <q> (dimension4).
The stabilizer of alpha includes every shear Q->Q+F. Therefore any6-space
W in U can be put in the form F_a directsum P_b, where a=dim(W intersect F),
b=6-a, and (a,b) is (2,4),(3,3), or (4,2). These shears preserve S.
Exterior-degree counting now gives
 dim(S intersect Lambda^3 W)=C(a,3)+C(a,2)b + (a if b=4 else0),
which is respectively6,10,16. (The q component contributes only when all Q
is in W, because q has full support Q.) Hence the two contraction images
meet in dimension at most16. Consequently rank(T_gamma)>=32+44-32=44,
again contradicting rank40.

Both possible KT types for beta are excluded. Thus the branch (96,112,126)
cannot occur. Every finite rank and canonical intersection computation above
is independently checked by agent2_96112126_exterior.py.
