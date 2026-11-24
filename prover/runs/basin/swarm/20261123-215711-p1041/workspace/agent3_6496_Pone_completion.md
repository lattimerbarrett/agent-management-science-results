# Completion of (64,96) branch, remaining rank-one orientation

Uses the canonical setup and P=0 exclusion in agent3_6496_Pzero_proof.md,
and the general affine row-second-moment lemmas in
agent2_full_purepair_coset_proof.md. Let wt h174. Those general lemmas,
which only require P affine and odd centroid-zero columns, give:
P's image contains0 and has dimension<=1 (rank>=2 baseline160 plus
excess44 already exceeds174). If P=0 we are done. Suppose rank1.
The minimal-row model M has weight128, so excess E46. Its columns are
even and centroid0 (P fibers have dimension5). Let e0 be the row0 excess,
m0 its minimum1 or3, r=|h_row0+M_row0|, and z the number of other P0
nonminimum rows. As in the rank2 exclusion of the pure-pair proof,
 192-3r <= 4(46-e0)-16z,
 r<=e0+2m0,
whence e0+16z<=6m0-8. Therefore m0=3,z=0,e0<=10. So P(0)nonzero and
ALL32 zero-P rows of h are exactly delta_Y.

Write A=P^{-1}(nonzero), a LINEAR X5-flat through0. The degree5 function
g=h+a+b restricted to the P0 half is exactly b, supported on T_X2.
If the half meets T2, it meets it in exactly2 points (it cannot contain
T2 since0 in A). The coefficient of canonical Y2 in that restriction
is the2-point indicator, but has degree<=3 on the5 X variables and hence
minimum4, contradiction. Thus T2 subset A, and g vanishes outside A.
Consequently b and g both have the affine linear factor1_A(X).

In the original14-space f=s a+t b+st g. Subtract the original minimum
word G=s a (an affine7-flat). Put F=f+G=t(b+s g). It is supported on the
affine12-space L={t=1,X in A}, and has degree<=5 on L (two support factors
removed from the degree7 original). Its intersection with G lies in
the5-flat I=G intersect L. Every h-column is odd, while outside A its
Y0-column has32 points. Thus c=|h intersect{Y0}|=32+c_A where c_A is odd
between1 and31. It follows that
 v=wt F=334-2c is in [208,268]_4,
 i=|F intersect G|=|F intersect I|=(v+128-334)/2=(v-206)/2.

If v<256, firm Kasami-Tokura below2d classifies F. A sum of at most2
minimum7-flats gives f as at most3 such flats, excluded by the checked
four-affine-flat theorem. The other cases are factored rank6/8 quadratic
words of weight224/240, with affine support dimension9. Then i>=9,
so the affine supports of G and F intersect in dimension>=4. Their union
has affine span dimension<=7+9-4=12. But f, a degree7 word of weight334,
cannot have proper affine support in14-space: a support factor would
reduce to degree6 in13 variables, whose weights are divisible4 by the
standard divisibility theorem (or elementary degree<half parity-square).

It remains v in {256,260,264,268}; then i in {25,27,29,31}.

FAT-FLAT DESCENT LEMMA, applied within L=F2^12:
A degree5 function F meeting a5-flat I oddly meets EVERY parallel5-flat
oddly: the parity projection over the5 free coordinates is constant.
Its first-moment projection is affine in the7 quotient coordinates,
so the centroid graph C is an affine7-flat, of size128. Let J=|F intersect C|.
An odd row containing its centroid has at least1 point; an odd row missing
its centroid has at least3. The special i-point row contributes at least
i-3 beyond these baselines. Therefore
 v >= J+3(128-J)+(i-3)=381-2J+i,
 J >= (381+i-v)/2=(556-v)/4.
The degree5 word K=F+C therefore has weight
 k=v+128-2J <= (3v/2)-150 <=252 <256.
By firm KT below2d, either K is a sum of at most2 minimum7-flat words,
or it is a non-two-flat quadratic of weight224/240, affine support9.
In the former case f=G+C+K is XOR of at most4 affine7-flats and is
excluded by the independently verified four-flat theorem.
In the latter case
 |C intersect K|=(128+k-v)/2 >=(128+224-268)/2=42.
Thus their affine hulls intersect in dimension>=6, and F=C+K is supported
on an affine space of dimension<=7+9-6=10. Since G meets F in i>=25,
its intersection with this affine support has dimension>=5. Hence f has
affine support dimension<=7+10-5=12, again contradicting 334 mod4=2.

This completes ALL(64,96) target branches, using only firm KT below2d,
minimum-distance and divisibility, the general moment bounds already
proved, and the checked four-affine-flat exclusion. No above2d KTA
structural classification is used.
