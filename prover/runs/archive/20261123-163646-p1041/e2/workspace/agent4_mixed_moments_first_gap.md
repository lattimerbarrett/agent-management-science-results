# Mixed moments and the first gap (agent 4)

## 1. Elementary punctured minimum distance

If nonempty A is a subset of F_2^n minus {0} and every nonconstant
squarefree monomial of degree at most e sums to zero on A, then
|A| >= 2^(e+1)-1. Indeed adjoin 0 if |A| is odd. The resulting nonempty
set has every moment of degree at most e (including the constant moment)
zero, and hence is a nonzero word of RM(n-e-1,n). Its minimum distance
is 2^(e+1). If e>=n there is no such nonempty A, since the nonconstant
monomials span all functions on the punctured cube. For e=0 the assertion
is simply |A|>=1.

The minimum-distance assertion used here follows inductively by writing
f=g+x_n h. If h=0, wt(f)=2wt(g). Otherwise wt(f)>=wt(h), and deg(h)
is one smaller than the allowed degree of f. This proves the standard
minimum distance 2^(n-r) without a classification theorem.

## 2. Mixed-moment lemma

Let X=F_2^a minus {0}, Y=F_2^b minus {0}, d>=1. Suppose nonempty
P subset X times Y satisfies

    sum_(x,y in P) x_I y_J = 0

for all nonempty I,J with |I|+|J|<=d. Then |P|>=2^d-1.

Proof. Regard P as a binary matrix M with row index x and column index y.
Choose the least degree j>=1 of a Y-monomial y_J for which v=M eval(y_J)
is nonzero. If no such monomial of degree <=d exists, each nonzero row
has all nonconstant Y-moments through degree d zero, and therefore has
weight >=2^(d+1)-1; this is already enough.

Otherwise 1<=j<=d. Every nonzero row annihilates the nonconstant
Y-monomials through degree j-1, and so has weight >=2^j-1. The nonzero
vector v has all nonconstant X-moments through degree d-j zero, and so
has weight >=2^(d-j+1)-1. Each row indexed by support(v) is nonzero.
Consequently

    |P| >= (2^j-1)(2^(d-j+1)-1) >= 2^d-1.

The last inequality holds because, among 1<=j<=d, the product is
minimized at j=1 or j=d. This proves the lemma.

## 3. An extra radical coordinate

Now let P subset X times Y times F_2 satisfy all mixed-moment identities
of total degree <=d, where the radical coordinate r may occur or not.
Write P_0,P_1 for the two r-slices. Their symmetric difference is a
mixed-moment set of order d, and each slice is a mixed-moment set of
order d-1. If P_0 differs from P_1, the preceding lemma gives
|P|>=|P_0 symmetric_difference P_1|>=2^d-1. If they are equal and
nonempty, |P|>=2(2^(d-1)-1)=2^d-2. Thus always

    P nonempty ==> |P| >= 2^d-2.                 (1)

For d>=2 equality is attained by r free, x fixed nonzero, and y ranging
through the nonzero vectors of a (d-1)-dimensional linear subspace.

## 4. Canonical two-flat quotient

For c>=5 put d=c-2, and use coordinates (r,x,y) with r in F_2 and x,y
in F_2^(c-1). Let

    T={(r,x,0):x!=0} union {(r,0,y):y!=0}.

This is the symmetric difference of two c-flats meeting in a line, and
|T|=2^(c+1)-4. Every mixed monomial x_I y_J r^e of degree <=d vanishes
on T. Hence if P is outside T and

    sum_(p in P) nu_d(p) belongs to span {nu_d(t):t in T},

its cross part C=P intersect {x!=0,y!=0} satisfies the conditions of (1).
Thus either P consists only of the two common-line points, or

    |C| >= 2^(c-2)-2.                            (2)

In particular no P of size 3 exists. More strongly there is no P with
3<=|P|<=2^(c-2)-3. Notice that only the inclusion of mixed monomials
in the vanishing ideal is needed, not an equality of ideals.

## 5. Consequence conditional on the classical below-2d KT theorem

Use the classical Kasami--Tokura classification strictly below twice
minimum distance (NO above-2d theorem is used). Its consequences needed
here are:

(A) For coorder c the weights strictly between 0 and 2^(c+1) are
    2^(c+1)-2^t, 1<=t<=c, when realizable.
(B) In dimension 2c-1, a word of weight 2^(c+1)-4, for c>=5,
    is affine equivalent to T from section 4.
(C) In dimension 2c, every strictly-below-2d word of weight divisible
    by 4 is supported in a proper affine hyperplane. This follows
    from the two KT forms: a quadratic times r-2 linear factors
    spans at most c+2 dimensions, and the two-flat form with an
    intersection of dimension at least 1 spans at most 2c-1.

Let w=2^(c+1)+2. In dimension 2c the unordered pair-parity function
Q(v)=#{unordered pairs of distinct support points summing to v} mod2,
with Q(0)=w/2 mod2, is constant 1. (The elementary pair-parity identity
is documented independently by agent 1.) Thus every nonzero k_v is
odd, and quotient weight w-2k_v is divisible by 4 and <=2^(c+1).
By (A), the only possible k_v are 1 and 1+2^j for 1<=j<=c; the last
option j=c corresponds to zero quotient. Since

    sum_(v!=0)(k_v-1)
      = C(w,2)-(2^(2c)-1)
      = 2^(2c)+3*2^c+2 = 2 mod4,

some k_v=3. Its quotient is T by (B), and its three double fibers give
an outside P of size 3 whose degree-(c-2) syndrome belongs to span(T).
This contradicts (2).

For ambient dimensions below 2c, zero-extend the support into 2c; this preserves coorder c and weight. For larger dimensions, pair counting compresses injectively down to
2c+1: C(w,2)<2^(2c+2)-1. Suppose no injective quotient exists there,
so all directions occur as differences. Q is affine with Q(0)=1.
If nonconstant, on the 2^(2c) directions in its zero AFFINE hyperplane (the coset L=1) all
k_v are even and >=2. These directions contribute cross-pairs for the
associated affine partition, forcing at least 2^(2c+1) cross-pairs.
But there are at most w^2/4=(2^c+1)^2<2^(2c+1). Hence Q=1.

Again k_v is in {1} union {1+2^j:1<=j<=c}. If 1<=j<=c-3,
(C) puts the quotient in a proper hyperplane. The original support
outside its preimage has size at most 2k_v=2+2^(j+1)<2^(c-1).
Restriction to that affine halfspace has minimum nonzero weight
2^(c-1). Therefore it is empty, contradicting full affine span
(which is forced by occurrence of every difference direction).

All remaining k_v-1 are divisible by 2^(c-2), but

    sum_(v!=0)(k_v-1)
       =C(w,2)-(2^(2c+1)-1)=3*2^c+2
       =2 mod 2^(c-2),

a contradiction. Thus an injective quotient to 2c exists, where absence
was already proved. This proves, for every c>=5 and every ambient
dimension, absence of weight 2^(c+1)+2. In particular 66,130,258 are
universally absent at coorders 5,6,7 respectively.

## 6. Independent executable checks

workspace/agent4_first_gap_3sum.py constructs all degree-(c-2) Veronese
columns, reduces modulo span(T), and tests EVERY unordered pair of
outside points against the syndrome dictionary for a distinct third.
Actual executed results:

 c=5: T60,  rank50,  452 outside,   101926 pairs: no relation.
 c=6: T124, rank112, 1924 outside, 1849926 pairs: no relation.
 c=7: T252, rank238, 7940 outside,31517830 pairs: no relation.

These checks are redundant with sections 1--4, but independently verify
the particular collision obstruction used in section 5. The remaining
inputs (KT and Q) are mathematical, not purportedly proved by these
finite checks. This note does NOT prove the user's main nonexistence
claim; a genuine 14->15 spectral change remains missing.
