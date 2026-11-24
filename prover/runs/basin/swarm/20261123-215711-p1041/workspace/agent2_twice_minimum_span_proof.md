# Weight twice minimum: affine-span theorem

**Theorem.** If c>=3 and f belongs to RM(n-c,n) with weight 2^(c+1), its support has affine span at most 2c+1.

Only the classical Kasami--Tokura theorem for weights strictly below twice minimum, minimum-weight classification, and elementary linear algebra are used. Independent reviews: agents 3 and 4 (Slack 333--336).

## Conventions and two facts
The highest squarefree homogeneous part transforms as an exterior form under linear changes of variables. A proper affine support with normal ell implies ell divides the top form. For a decomposable p-form, its linear divisor space equals its p-dimensional factor space. If alpha,beta are distinct decomposable p-forms with common factor space F, then their sum either is decomposable (when dim F=p-1), or has divisor space exactly F. This follows by factoring F and taking the sum of two decomposable forms with disjoint factor spaces, each of degree >=2: wedging by a nonzero vector outside F cannot kill that sum, by its two disjoint multidegrees.

For a degree-p form omega, use its contraction matrix from exterior k-duals to exterior (p-k)-vectors. For two matrices A,B of the same shape,

rank(A+B) >= rank(A)+rank(B)-dim(im A intersect im B)-dim(row A intersect row B).

The contraction image and row spaces of a decomposable form with factor space U are the appropriate full exterior powers of U. For beta=F_(p-2) wedge q, where q is a nondegenerate bivector on a complementary 4-space Q, its degree-j contraction-output space is

Lambda^j F + (Lambda^(j-1) F wedge Q) + (Lambda^(j-2) F wedge span(q)),

with impossible terms omitted. Thus for output degree j>=3 every vector has a positive F-factor. If a subspace W has W intersect F=0, shears of Q by F (which preserve beta) put W inside Q; the intersection of that output space with Lambda^j W is zero for j>=3, and is at most 1-dimensional for j=2.

## Pure decomposable-top lemma
Let H on X_C times Y_p have degree p, only top term Y_1...Y_p, and weight 2D where D=2^C. Assume C>=3 and p>=C+2. Every Y-row is odd. The parity sum of its Y coordinates (its centroid) is constant: these centroids are degree-at-most-one polynomials in X, and the coefficients of their linear terms would be mixed degree-p terms of H, which vanish. Translate the common centroid to zero. Let M be the indicator of Y=0, and J=|supp(H) intersect supp(M)|. A row containing zero costs at least 1; an odd row missing zero but with centroid zero costs at least 3. Hence

2D >= J+3(D-J)=3D-2J,

so J>=D/2. The top terms of G=H+M cancel, whence deg G<=p-1. G is nonzero since H has weight 2D rather than D. Its minimum possible weight is 2D, while

wt(G)=3D-2J<=2D.

Thus G is minimum and is an affine (C+1)-flat, and J=D/2. The affine C-flat M and affine (C+1)-flat G meet in a (C-1)-flat; their affine union span has dimension C+(C+1)-(C-1)=C+2. H is supported in that span. (In fact no p>=C+2 hypothesis was needed for this argument once the centroid degree assertion holds.)

## Induction
The case c=3 follows directly from moments: on the support S of size 16, evaluate all affine linear functions. Their evaluation code has dimension dim(aff S)+1 and is self-orthogonal, since all moments of degrees <=2 vanish. Thus dim(aff S)+1<=8.

Suppose c>=4, and the theorem is known for c-1. It suffices to show proper support whenever n>=2c+2; repeated factoring then gives the claimed bound. Put d=2^c. Parseval gives a hyperplane section of weight <d. This section is in a codimension-(c-1) code, hence is below twice its minimum. The strict KT classification shows its affine span has dimension at most 2c-2 (the two-minimum-word case has intersecting (c-1)-flats; the quadratic case has span c+1). It is therefore supported properly inside its hyperplane. This gives an empty affine codimension-two flat of f.

Normalize that empty flat to selector position 00. The other branches a,b,h, on N=n-2 variables, have degree at most p=n-c-1. They satisfy deg(a+b+h)<=p-1. Their minimum weight is D=2^(c-1), and their total weight is 4D. Reorder the three branches. The strict second-weight bound forces exactly

(D,D,2D) or (D,3D/2,3D/2).

If any branch is zero, the original support already lies in a hyperplane. Below assume all three are nonzero.

### Branch weights D,3D/2,3D/2
Let alpha be the decomposable top form of a. The top forms beta,gamma of b,h both have shape F_(p-2) wedge q_rank4. If alpha's factor space A meets F nontrivially, choose ell in that intersection. Then ell divides alpha,beta,gamma.

If A intersect F=0, let W=A intersect supp(beta). By the shear observation above, put W inside Q. When p>=6, choose contraction k=3: both output degrees 3 and p-3 are >=3, so the alpha and beta image spaces and row spaces have zero intersections. Consequently rank(gamma)>=rank(alpha)+rank(beta)>rank(beta), impossible because beta and gamma have the same canonical shape. When p=5, choose contraction k=2. The two intersections have dimensions 0 and at most 1; ranks alpha,beta,gamma are 10,16,16. Thus rank(gamma)>=25>16, also impossible. Here p>=c+1>=5, covering every case.

Thus ell exists. Since each branch has weight <2D and ell divides its top form, its restrictions to ell=0 and ell=1 have degree <=p-1, on N-1 variables, and minimum weight D. At most one is nonzero. Thus each branch is actually supported in one ell-slice.

### Branch weights D,D,2D
Let alpha,beta be the decomposable p-tops of a,b, and F their common factor space. Its dimension is at least 2p-N=n-2c>=2. Let gamma=alpha+beta be h's p-top.

If gamma is nondecomposable, its divisor space is exactly F. Induction applies to h, of codimension c-1 on N=n-2>=2(c-1)+2 variables and weight 2D. It has proper support, whose nonzero affine normal ell divides gamma and hence belongs to F.

If gamma is nonzero decomposable, dim F=p-1. Apply the pure-top lemma with C=c-1; since p>=c+1=C+2, h has affine span <=c+1. Its actual normal space has dimension at least N-(c+1)=p-2 and is contained in D(gamma), which has dimension p. Since F is another subspace of D(gamma), their intersection has dimension at least (p-2)+(p-1)-p=p-3>0. Choose ell there.

If gamma=0, h has degree <=p-1 and minimum weight 2D in that lower-order code, hence is an affine c-flat. Its normal space has dimension N-c=p-1. The common factor space of alpha=beta has dimension p; these meet in dimension at least 2p-1-N=n-2c-1>=1. Choose ell there.

In every subcase h is actually supported in an ell-slice. The minimum branches a,b are also actually supported in ell-slices, since ell divides their top forms.

## Recover the affine factor of f
In either weight pattern each nonzero branch is contained in one ell-slice. The three slice values, at selector positions 10,01,11, can be interpolated by a single affine function of the two selector bits (three equations for three affine coefficients). The zero branch 00 imposes no condition. Consequently the original support is contained in an affine hyperplane, completing the induction and theorem.
