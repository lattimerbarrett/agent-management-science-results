# Conditional coarse-KTA geometric consequences

WARNING: The coarse structural KTA cover below has NOT been verified against an actual complete published normal-form statement by the team. This file records valid deductions IF that cover is supplied; it is not a proof of that cover.

Assumed coarse cover (for r>=6 and weight<2.5d): a word either (i) has an affine-linear factor, (ii) is XOR of at most3 minimum affine flats, or (iii) is a minimum flat plus a prefactored quadratic KT word. Rank2/rank4 quadratics in (iii) are respectively one/two minimum flats and may be absorbed into(ii); every remaining quadratic piece has weight at least112 for codimension6 and is supported in an affine8-flat.

1. In RM(7,13), a full-affine-span13 word of weight<=156 must satisfy(ii). Factor case impossible. In case(iii), let L8 support the non-twoflat quadratic and M6 be the minimum flat. If disjoint, total weight>=176. If their union spans13, their intersection has dimension1, so overlap<=2 and total weight>=112+64-4=172. Thus case(iii) impossible. All needed full-span-threeflat facts were exhaustively independently verified in agent3_fullspan_threeflat_checker.py: weights<=156 with full span13 are only128/156 and each has a32-point hyperplane section; weights<=142 only128.

2. Empty2-flat for bad m14 words. Suppose S hits every affine codim2 flat. Then every hyperplane section of S has full affine span13, else an empty codim2 flat exists. Parseval and divisibility supply a hyperplane section U with |U|<=156. By1, U has a codimension-one section inside that hyperplane of size32. Let a,b,c be the other three coset weights of this codim2 flat. Each32+a is a full-span13 hyperplane-section weight, hence >=128. So a,b,c>=96; with total<=334 each<=110. Consequently every32+a<=142, and by1 each must be128. Thus a=b=c=96 and total=320, a contradiction for the four target weights.

3. In RM(8,14), every word of weight<=156 has affine span<=13. Factor case obvious. Threeflat case follows the same finite D4 enumeration (largest ambient span is13). In mixed case, full span14 would require L8 and M6 to intersect in at most a point, giving weight>=112+64-2=174; disjoint gives>=176. Hence impossible.

4. Empty2-flat for bad m15 words. Parseval supplies a hyperplane section of size<=156. By3, its support is in a hyperplane inside the14-hyperplane, so there is an empty affine codim2 flat in the original15-space. Combine with agent4_m15_qzero_empty2_proof.md and the Q!=0 reduction.

5. In RM(6,12), weight136/144 top6 has nonzero linear wedge annihilator. Factor case obvious; threeflat case exhaustively checked in agent2_c6_threeflat_invariants.py. In mixed case, overlap of minimum64 flat with quadratic112 piece is20/16; hence the containing6/8 flats intersect in dimension>=5/4 and their union has affine span<=9/10, so proper support. For quadratic120 or larger the required overlap is even greater, giving the same conclusion.

6. In RM(6,12), odd-half weights154/158 must be threeflat. Factor case impossible by Ax4-divisibility after restricting proper support. For mixed case, overlap is odd. Restriction of a quadratic to the intersection flat has odd weight only if that flat has dimension<=2, hence overlap<=3, giving total >=112+64-6=170. Contradiction. Thus by agent2_c6_threeflat_invariants.py the middle3-flattening rank is exactly52.
