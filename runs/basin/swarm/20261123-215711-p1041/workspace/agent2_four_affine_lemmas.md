# Four-affine-flat exclusion (restricted family, NOT all RM words)

The self-contained checker `agent2_four_affine_checker.py` proves that the XOR
of four arbitrary affine 7-flats in F2^14 never has weight 322,326,330,334.
It does NOT assert that every low RM word is such an XOR.

## Rank model
Homogenize the four flats to linear 8-spaces L_A,...,L_D in a 15-space;
H is the 14-dimensional hyperplane at infinity. Let d_J be dimensions of all
intersections of these five subspaces (d_empty=15). Monotonicity,
supermodularity of intersection dimension, and Ingleton for the ranks
r(J)=15-d_J are necessary. For a nonempty J among A,B,C,D the affine
intersection size is 2^(d_J-1) if d_J>d_(J+H), otherwise zero.
Inclusion-exclusion for XOR gives 512-2*sum(pair sizes)+4*sum(triple sizes)
-8*quadruple size. The checker uses only necessary constraints, then adds the
following independently proved geometric exclusions. Z3 UNSAT therefore is
an exhaustive exclusion of this restricted family, not a realizability claim.

In the following 'point' means size 1, and an r-flat has dimension r.
All intersections not listed as positive in a profile are empty.

## Two general constraints
1. If B,D meet in a 6-flat, and C meets both but C intersect B intersect D
is empty, then |CB|=|CD|. Indeed inside the affine 8-space T=aff(B union D),
C intersect T meets B,D as two nonempty proper hyperplane sections.
2. Projection lemma. Suppose |BD|=64, AB empty, AD a point, |BC|=|CD|=2^r,
BCD and ACD empty. Then |AC| <= 2^(5-r) for r<=5, and AC is empty for r=6.
Put T=aff(B union D), dimension 8. E=C intersect T is an (r+1)-flat,
with E=CB union CD, and its direction modulo dir(BD) is the diagonal line
between dir B and dir D. F=A intersect T has dimension at most 1 because
FD=AD is a point. If F is a line, AB empty forces dir F subset dir B,
while AD point forces dir F not subset dir D. Thus dir F has zero
intersection with dir E. The projection of AC modulo dir T is consequently
injective. It avoids zero since AC intersect T subset ABC union ACD is
empty. But the projection of C is a linear (6-r)-space (C meets T).
An affine subspace avoiding zero has dimension at most 5-r, proving the claim.

## Six forbidden profiles
Write only pair sizes, then positive triples. All quadruple intersections
are empty. Permuting A,B,C,D gives the other excluded profiles.

P1: AB=AC=BD=CD=8, BC=64, AD=1; ABD=1.
B,C share the affine hyperplane BC. AB and AC are parallel 3-flats with
common direction U in dir(BC), since ABC is empty. Similarly BD and CD
have common direction V of dimension 3 in dir(BC). AD point implies
U intersect V=0. Thus AC and CD, both lying in the affine 6-space C minus B,
have complementary directions and intersect, contrary to ACD empty.

P2: AB=16, AC=64, BC=0, AD=CD=4, BD=1; no triples.
Put H=dir(AC), dimension 6. AB lies in A minus C, hence its direction U
is a 4-space in H. AD and CD have common 2-dimensional direction W in H
(by the argument of general constraint 1). BD point gives U intersect W=0.
The affine flats AB and AD lie in A minus C with complementary directions,
so meet, contrary to ABD empty.

P3: AB=AD=BC=CD=8, AC=1, BD=64; ABD=4.
T=aff(B union D) has dimension 8. Both A intersect T and C intersect T have
dimension 4: their displayed sections span 4-flats, and a larger intersection
would meet B in dimension at least 4. Also C intersect T=CB union CD.
Thus the AC point is outside T. The directions of A,C are complementary
7-spaces in the ambient 14-space. Their images modulo dir T are 3-spaces
whose sum must be the full 6-dimensional quotient. But the AC point outside
T supplies a nonzero common image, contradiction.

P4: AB=0, AC=BD=CD=8, AD=64, BC=1; no triples.
T=aff(A union D) has dimension 8, and C intersect T has dimension 4.
The BC point lies outside T because C intersect T=CA union CD.
E=B intersect T has dimension 3 or 4. If 4, the images of B,C modulo dir T
are 3-spaces sharing a nonzero image of BC, contradicting that their
directions are complementary 7-spaces. If 3, E=BD and CD are affine 3-flats
inside the affine 6-space D minus A; their directions are disjoint because
BC is a point, so they are complementary and must meet, contradiction.

P5: AB=1, AC=AD=4, BC=BD=8, CD=64; no triples.
T=aff(C union D) has dimension 8. The flats A intersect T and B intersect T
have dimensions 3 and 4. They both lie in the affine 7-space
K=(C minus D) union (D minus C). Their directions are disjoint because AB
is a point, hence complementary in dir K, so the flats meet in T.
But AB cannot lie in T because A intersect T is contained in C union D
and ABC,ABD are empty. Contradiction.

P6: AB=BC=4, AC=64, AD=CD=16, BD=1; ACD=8.
T=aff(A union C) has dimension 8. B intersect T has dimension 3, and
D intersect T dimension 5 (its two 4-sections intersect in dimension 3).
Their directions are disjoint because BD is a point, so they are
complementary in dir T and the flats meet in T. However B intersect T
is contained in A union C, while ABD and BCD are empty. Contradiction.

## Check
Running the self-contained checker, after excluding all permutations of
these six profiles and imposing the two general constraints, returns UNSAT
for each target. Independent final rerun: 322 13.19s, 326 12.87s,
330 12.88s, 334 13.54s. Results in agent2_four_affine_results.json.


## At most three flats (separate parity case)
At most two affine 7-flats have XOR weight at most 256. For three, writing p,q,r for the pair-intersection cardinalities and t for the triple cardinality gives w=384-2(p+q+r)+4t. All entries are zero or powers of two, and t<=min(p,q,r). Exhausting these nine possible powers yields only: w322 has pair sizes 1,16,16 and t1; w334 has pair sizes 1,8,16 and t0; no profiles occur for326 or330. The additional enumeration at the end of the checker verifies these finite statements. In the first profile, the two affine4-flats inside their common affine7-flat, containing the triple point, intersect in dimension at least4+4-7=1; their intersection cannot be a point. In the second, the affine4-flat and affine3-flat inside their common affine7-flat have disjoint direction spaces, because the remaining pair of7-flats intersects in a point. Their directions are therefore complementary within that7-flat, forcing a triple point, contrary to t0. Thus at most three flats are excluded as well.
