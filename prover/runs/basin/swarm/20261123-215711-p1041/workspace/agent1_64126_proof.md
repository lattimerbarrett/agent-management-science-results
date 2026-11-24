# Branch (64,126,136/144): the linear-annihilator case

Let a,b,h be functions in RM(6,12), with a+b+h in RM(5,12),
wt(a)=64, wt(b)=126, and wt(h)=136 or 144. Suppose the degree-6
homogeneous exterior form of h has a nonzero linear wedge annihilator.
Then these branches are impossible. This is an auxiliary lemma, NOT an assertion
that every word of those weights has such an annihilator. The complementary
full-span graph cases are excluded unconditionally by the Hilbert-flattening
bound in agent3_64126_hilbert_proof.md. Thus no KTA structural coverage is needed.

## Exterior reduction
By the firm <2d Kasami--Tokura theorem, b is the XOR of complementary
6-flats B,C meeting at a point. Its top form is beta+gamma, two decomposable
6-forms with complementary supports. The top form of a is another
decomposable 6-form delta. Thus omega=beta+gamma+delta is the top of h.
Let l wedge omega=0. Split l into its components in the beta- and
gamma-supports. If both are nonzero, l beta and l gamma are decomposable
7-forms whose supporting 7-spaces intersect in dimension 2. Their sum
cannot be decomposable (the sum of two nonzero decomposable k-forms is
decomposable only when their support intersection has dimension k-1).
But their sum is l delta, decomposable or zero. Contradiction.

Hence, after interchanging beta,gamma, l is in the beta-support. Then
l delta=l gamma. Modulo l, delta and gamma are the same volume form, so
delta=gamma+l eta, where eta is zero or a decomposable 5-form supported
in the gamma-support. Writing beta=l beta', we obtain
omega=l (beta'+eta). The two nonzero 5-forms beta',eta have disjoint
5-dimensional supports.

## Top factor becomes actual support factor at these two weights
Restrict h to the two l-slices. Both restrictions have degree at most 5
in 11 variables. Their minimum nonzero weight is 64 and next weight 96.
If both are nonzero their total is either 128 or at least 160, not 136/144.
Thus one slice is zero. On the other slice, h becomes a function H in
RM(5,11), with top form either decomposable, or a sum of two disjoint
5-forms (and one unused variable).

## Decomposable top case
Choose a parallel minimum 6-flat G having largest intersection with H.
There are 32 such cosets, so |G intersect H| >= ceil(wt(H)/32) >=5.
Then K=H+1_G has degree <=4 and weight <=198. RM(4,11) has minimum128
and next weight192, so wt(K) is 128 or192.
If 128, K is an affine7-flat and the intersection needed for H136/144
is 28 or24, neither a power of two.
If 192, K is a rank4 quadratic on an affine9-flat, times its support factor.
Its intersection with G would need weight60 or56. If G meets that9-flat
in dimension <=5 the intersection is <=32. Otherwise G is contained
there and the restriction is a quadratic on6 variables. Quadratic weights
on6 variables are {0,16,24,28,32,36,40,48,64}, excluding56,60.

## Pair-of-five-forms case
Split the one unused variable. Both restrictions are in the pure-pair
coset in RM(5,10), top X1...X5+Y1...Y5. Each has weight2 mod4 and minimum62
(by firm KT). Since the total is at most144, each is at most82.
The strengthened pure-pair5 gap lemma in agent2_full_purepair_coset_proof.md
says every such word of weight at most82 has weight EXACTLY62.
Both restrictions therefore have weight62, giving total124, not136/144.

All steps in this auxiliary linear-annihilator case use
only firm KT <2d, elementary exterior algebra, and the independently
proved pure-pair5 moment lemma.
