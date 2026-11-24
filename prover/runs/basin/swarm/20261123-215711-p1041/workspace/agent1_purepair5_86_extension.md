# Pure-pair-five exclusion at weight 86 (independent review agent_1)
Let H on X5+Y5 have degree <=5 and TOP5 equal Xprod+Yprod.
The moment normalization and minimal-row model from agent2_full_purepair_coset_proof.md
apply without change at weight86: nondecomposable P-values cost at least96;
if the affine image omits0 its baseline is96; if its dimension>=3 the baseline
is88. Hence its dimension<=2 and it contains0. The general model-distance
inequality gives 4E>=3*32-18=78, with E even, so E>=20. Dimension2
would have baseline80 and total>=100. Therefore both P,Q have dimension<=1.

Set G=H+delta_axes, v=wtG, r,c its row0/column0 weights, eps=G00.
At most16 rows have nonzero second moment. The row-distance estimates give
v>=8c-64+r-8eps and v>=8r-64+c-8eps. Thus
9(r+c)<=2v+128+16eps. Since 24=86-62=v-2r-2c+4eps,
216>=5v-256+4eps, so v<=94.4. Minimum and second weights of RM(4,10)
are64 and96. G cannot be0, hence is the indicator of an affine6-flat K.
Its intersection with A triangle B, the two complementary5-axes, has size20.
If 0 belongs K, dimensions a=dim(K cap A), b=dim(K cap B) satisfy a+b<=6
and the size is 2^a+2^b-2, never20. If 0 does not belong K and both
intersections are nonempty, a+b<=5: equality a+b=6 would span K's direction,
and the joining vector forces 0 into K. The only power decomposition of20
is16+4, requiring a+b=6, impossible. One empty intersection gives a power of2.
Contradiction. Thus no pure-pair-five word has weight86.

Together with the existing <=82 theorem (only62), this excludes the
odd-half weights66,70,74,78,82,86 needed in codim6 numerical-gap descent.
