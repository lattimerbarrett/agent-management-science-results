# Unconditional codimension5 exclusions 66 and70

THEOREM. Neither66 nor70 occurs in RM(m-5,m) for any m>=10.

Reduction: for w<=70, |S+S|<=1+C(70,2)=2416<2^12. A weight-preserving quotient derivative descends every example in m>=12 to m11. For m<=9, Ax/McEliece gives4-divisibility (or the trivial very-low-dimensional cases). Thus suffice m10,11.

For m10 or11, every hyperplane section is even and w=2mod4, so Fourier coefficients are2mod4. Parseval gives max|F|>=10, hence a hyperplane section of size<=28(w66) or30(w70). It belongs to codim4 code, min16; firm <2d KT says it has an affine-linear factor because its order m-5 is>4. Thus original support has an empty codim2 flat. Write branches0,a,b,h on n=m-2 variables, degree R=m-6, with a+b+h degree<=R-1. Sorted branch weights yield (16,16,34) for w66, or (16,16,38)/(16,24,30) for w70. The missing tuple (16,24,26) is excluded by firm <32 KT.

For (16,24,30), top forms alpha,beta,gamma satisfy alpha+beta=gamma. Alpha is decomposable R-form; beta=F_(R-2) wedge rank4 quadratic; gamma is KT TypeII mu4 (F_(R-4) wedge sum of complementary degree4 monomials). TypeI mu4 cannot fit: remaining quadratic variables number6<8. If alpha shares no linear factor with F, their support intersection can be sheared into Q4. For R4, middle2 images of alpha,beta intersect in at most the line<q>, giving rank(gamma)>=6+10-2=14. Its canonical rank is12. For R5 use2/3 flattening: image intersections are0 and at most1, giving rank>=10+16-1=25; gamma rank20. Contradiction. Hence a common top linear factor exists. All three branch weights<32 force actual support in a level of that factor (otherwise two branches of min16); choosing an affine function of the two outer bits gives a global support hyperplane. Thus the word descends m11->m10 or m10->m9, with the latter impossible by4-divisibility.

For (16,16,34/38), if the minimum flat annihilators share a linear factor, the same argument applies: the34/38 branch with that top factor cannot have both levels nonzero, since its split weights would need16+18 or16+22, each excluded by the firm <32 spectrum. At m11 the annihilators have dimension5 in9, hence share a factor automatically. At m10 the only remaining possibility is complementary annihilator4-spaces, so after translation h is an8-variable degree4 function with TOP=productX4+productY4, weight34 or38.

PUREPAIR4 COSET GAP: such a function H cannot have weight34/38. Normalize row and column centroids to0 (their first moments are constant because there are no mixed top terms). Every row/column is odd. Its row second moment P(X) is affine, because mixed X2Y2 top coefficients vanish. Nonzero second moment costs row weight at least3. If P's affine image avoids0, baseline48>38; if its image rank>=2, at least12 of16 values are nonzero, baseline>=40>38. Thus P=0, or P has rank1 through0. Rank1 with nondecomposable rank4 value has baseline48; rank1 decomposable has baseline32 and excess E<=6. The minimal-row-model argument from the purepair6 proof gives universally 4E>=3N-18 with N16: 4E>=30, forcing even E>=8. Contradiction. Therefore P=0, and by transpose Q=0.

G=H+delta_X+delta_Y has degree<=3 in8 variables, hence either0 or weight v>=32. P=Q=0 makes all its nonzero rows/columns have weight>=8 (fiber degree<=1). With r=wt(G row0),c=wt(G col0),eps=G00, we have v>=8r,8c and
wt(H)-30=v-2r-2c+4eps>=v/2.
If G=0, H30; otherwise H>=46. In particular no34/38.

This completes all cases using only firm <2d KT, the minword theorem, and already proved row-model E inequality. No KTA above2d normal-form coverage is assumed.
