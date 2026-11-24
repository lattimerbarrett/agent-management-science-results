# Weight136 has proper affine support (new unconditional proof)

THEOREM. A weight136 word in RM(6,12), or RM(7,13), has support in an affine hyperplane. Uses only the firm <2d Kasami--Tokura classification and the min/second-weight theorems.

Let ambient M=12 or13, degree r=M-6. Every hyperplane section is even. Parseval gives a nontrivial Walsh coefficient of magnitude at least12: mean nontrivial square=136(2^M-136)/(2^M-1)>100, while all coefficients are multiples4. Thus some section has weight<=62. It belongs to codim5 RM(r,M-1), min32, and by <2d KT classification has a linear factor (r>=6>5; TypeII has commonfactor r-mu>=r-5>=1, quadratic type has commonfactor r-2). Consequently the original support has an empty affine codimension-two flat.

Use that flat as branch00. The other three branches a,b,h on n=M-2 variables have degree R=r-1 and c=a+b+h degree<=R-1. Ordering branch weights, smallest<=45, hence32; next<=52, hence32 or48. Only tuples are (32,32,72) and (32,48,56).

A linear wedge factor ell of TOP_R(a),TOP_R(b) also divides TOP_R(h). If a,b,h each actually supported in one ell-level (not necessarily the same), the full original support is in an affine hyperplane: choose the affine function of the two outer control bits that takes the three required levels on10,01,11. Thus it suffices to find a common linear top factor. Any branch of weight<64 with such a factor is actually supported in an ell-level: restrict ell=0/1, each branch has degree<=R-1 on n-1 variables and min32, so both nonzero would have total>=64. For the72 branch the same conclusion holds because both nonzero would need32+40, and weight40 is excluded by the firm <2d spectrum (min32, next48).

CASE (32,32,72): a,b are affine5-flat indicators. If M=13 then their annihilator6-spaces intersect nontrivially automatically (6+6>11). If M=12, their annihilator5-spaces would be disjoint only if their direction5-spaces were complementary, in which case the affine5-flats meet in exactly one point. But for M=12, c belongs RM(4,10), doubly even and orthogonal to a,b in RM(5,10). The branch identity gives 136/2=|a intersection b| mod2, so that intersection must be even. Contradiction. Hence a common linear top factor exists.

CASE (32,48,56): write alpha=TOP_R(a), beta=TOP_R(b), gamma=TOP_R(h)=alpha+beta. Firm KT gives alpha decomposable, beta=vol(F) wedge q where dimF=R-2 and q is a rank4 quadratic on Q4. Gamma is either vol(F') wedge rank6 quadratic or vol(G) wedge (two complementary cubic monomials), the two KT possibilities for weight56.

Suppose alpha has no factor in F. Its support U_alpha meets F trivially. W=U_alpha intersection(F+Q) then projects injectively to Q. A shear Q->Q+F preserves beta and makes W a subspace of Q. For R=6, the middle3 contraction image of beta is Lambda3(F) + Lambda2(F) wedge Q + F wedge <q>, containing no pure Lambda3(Q). Thus the contraction images of alpha,beta have zero intersection. Both contraction matrices are symmetric, so rank(gamma)>=rank(alpha)+rank(beta)=20+32=52. But the two possible gamma ranks are44 and38, contradiction.

For R=5 use the rectangular2/3 flattening. The output Lambda3 image of beta has zero pure Lambda3(Q) part, while the transpose Lambda2 image intersects Lambda2(Q) in at most the line<q>. Hence image intersection dimensions are0 and at most1. The general matrix inequality rank(A+B)>=rankA+rankB-dim(ImA intersection ImB)-dim(RowA intersection RowB) gives rank(gamma)>=10+16-1=25. Its two KT ranks are22 and19. Contradiction.

Therefore alpha and beta share a factor in F; all branches are supported in an ell-level, proving the theorem.

All canonical ranks were independently computed over F2 in agent4_weight136_flattening_checks.json. The matrix inequality follows from the map ker(A+B)->ImA intersection ImB, x->Ax, whose kernel is kerA intersection kerB; dimensions of the latter are controlled by row-space intersection.
