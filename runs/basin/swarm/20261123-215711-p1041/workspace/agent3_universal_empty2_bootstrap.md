# Universal empty affine codimension2 lemma for the four target weights

Assumptions already proved elsewhere using only KT below2d:
(1) codim5 words cannot have weights66/70 (agent4_codim5_no66_70.md).
(2) codim5 words of weight68 in ambient12/13 have proper affine support.
(3) codim c>=3 words of weight2^(c+1) have affine span<=2c+1.
(4) KT below2d, minimum words and Parseval.
No KTA above2d is assumed.

LEMMA A (two factored rank4 forms). Let alpha=vol_F q4 and beta=vol_G q4',
where F,G have dimension p-2, q4/q4' are nondegenerate rank4 quadratics,
and p>=6. If F intersect G=0 then D(alpha+beta)=0, where D is the linear
wedge-annihilator space. Indeed v(alpha+beta)=0 implies v alpha=v beta.
Nonzero v cannot belong to F or G, since that would kill exactly one side.
If v lies outside U_alpha=F+support(q4), then v alpha is nondecomposable
with wedge annihilator F+<v>, dimension p-1. Equality requires v outside
U_beta too, since inside U_beta its wedge is decomposable. The equal
annihilators would contain F+G of dimension2p-4>p-1. Contradiction.
Otherwise v lies in both U's. Then v alpha is a nonzero decomposable
(p+1)-form: on the4-dimensional quadratic support, v wedge q4 is a
nonzero decomposable3-form. Its supporting(p+1)-space contains F+G,
but2p-4>p+1 for p>=6. Contradiction.

LEMMA B (bootstrap small codim6 words). Let u be codim6 in ambient n13/14,
with nonzero wt u<=156. Parseval gives a hyperplane section of weight<=70:
max Fourier magnitude>=sqrt(w(2^n-w)/(2^n-1)), rounded using even weights.
The section has codim5 in ambient12/13. If weight<64, KT gives affine
span<=10; weight64 gives span<=11 by(3); weights66/70 impossible by(1),
and weight68 proper by(2). Thus the section is proper in its hyperplane,
and u has an EMPTY affine codimension2 flat.
Normalize branches(0,a,b,h) on n-2 variables, all degree<=p=n-7,
with a+b+h degree<=p-1. The minimum branch weight is32; after sorting,
a has weight32 or48. If a32, u has a hyperplane section of weight32.
If a48, sorting gives b<=(156-48)/2=54, so b48 by KT; h has
weight48,56 or60. The tops alpha,beta of a/b are factored rank4 quadratics; gamma=alpha+beta
is a KT below2d form and has a nonzero wedge annihilator (all types at
48,56,60 have at least p-4>=2 support factors). Lemma A therefore forces
F_alpha intersect F_beta nonzero. Any common ell divides all3 tops.
Since all3 branch weights<64, the top factor becomes an actual affine
support factor: both ell-slices nonzero would each weigh>=32. The three
possibly distinct support offsets fit an affine equation in the two
selector variables (the zero00 branch imposes no constraint). Thus u
has proper affine support. CONCLUSION: every FULL-SPAN codim6 word of
weight<=156 in ambient13/14 has a hyperplane section of weight32.

LEMMA C (small proper-support range). Every codim6 word u of weight
130,132,134,136,138,140,142 in ambient n13/14 has proper affine support.
Parseval gives a hyperplane section<=64. KT below64 and(3)at64 make this
section proper, so u has an empty2-flat. Sorted branches have weights
(32,32,h66..78) or (32,48,h50..62), on N=n-2 variables of degree p=n-7.
First case: the minword top p-spaces have intersection dimension>=
2p-N=n-12>=1. Choose ell common. If top h0, h has degree<=p-1, whose
minimum64/second96 exclude66..78. Otherwise ell divides top h; its slices
have minimum32 and next48, so both nonzero total64 or>=80, not66..78.
Thus all3 branches have actual ell factors, making u proper as above.
Second case: KT excludes h50/52/54/58, leaving56/60/62. Write alpha top
minword, beta=F_(p-2)q4. If support(alpha) meets F, again all3 branches
have actual common support factor, hence u proper. If not, use3/(p-3)
flattenings. Both the column and row images of beta have an F factor
(p>=6), whereas alpha images lie in exterior powers of its disjoint
p-space. Thus both image intersections are0, and rank gamma equals the
sum of the two ranks. For p6 the ranks are20+32=52; for p7,35+55=90.
But any KT h56/60/62 has flatten rank at most44/75 respectively. TypeI
sum-of-two-product forms have rank<=2 binom(p,3)=40/70. The only possible
non-two-flat quadratic here is h56: rank44/75. Higher-rank quadratics
for h60/62 would need support dimension p+6 or p+8, exceeding N=p+5.
Contradiction. This proves Lemma C.

MAIN EMPTY2 LEMMA. Let f in RM(m-7,m), m14/15, have weight322/326/330/334.
Suppose it has no empty codimension2 flat. Then every hyperplane section
has FULL affine span in its hyperplane. Parseval guarantees a section
u of weight<=156; this numerical bound is independently checked in
agent4's Parseval arithmetic. Its codimension is6. Lemma B says u has
a hyperplane section of weight32. The four cosets of the resulting
codimension2 flat in the original space have weights32,A,B,C.
Each union32+A (and likewise B,C) is a full-span codim6 hyperplane
section, so its weight is>=128: KT below128 has span<=12, less than
13/14. Hence A,B,C>=96. Since their total is at most334-32=302, each
is<=110 (the other two cost at least192). Thus each32+A lies in
[128,142]_2. Lemma C excludes all these full-span possibilities except
128. Therefore A=B=C=96, giving total320, not a target. Contradiction.
So every target f in ambient14 OR15 has an empty affine codimension2 flat.
