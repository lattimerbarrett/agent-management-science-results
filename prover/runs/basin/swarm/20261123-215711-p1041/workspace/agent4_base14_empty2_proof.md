# Unconditional empty codimension-two flat for the base14 target words

Uses: firm KT<2d; universal2d-span theorem checked by agents2,3,4; codim5 gaps66/70 (agent4_codim5_no66_70.md); weight68 proper support in ambient>=11 (agent4_weight68_proper_support.md); the short-annihilator lemma for three second-weight branches (agent3#343, independently checked agent4#346).

LEMMA1. Every codimension6 word U of weight<=156 in ambient13 or14 has an empty affine codim2 flat.
Indeed Parseval, even hyperplane sections, and Fourier residue mod4 give a hyperplane section of weight<=70. In the codim5 code it cannot have weight66/70. If below64, firm KT provides a factor (orders>=7>5), if64 universal2d-span bound gives affine span<=11 (strictly less than ambient section12 or13), if68 the proper-support theorem gives a factor. A zero section is trivial. Thus that hyperplane section has an empty hyperplane inside it, proving the lemma.

LEMMA2. Every codimension6 word U in ambient13 of weight<=156 either has proper affine support or has a hyperplane section of weight32.
By lemma1 use branches0,a,b,h in11 variables, degree<=6, sum degree<=5. Sorting, smallest<=52, hence32 or48. If32, it and the zero branch together give the desired32-point hyperplane section. If48, the only permitted <64 triples summing<=156 are (48,48,48),(48,48,56),(48,48,60). Let their top6 forms be alpha=F4 q4, beta=G4 q4', gamma=alpha+beta. All KT possibilities for gamma have nonzero wedge annihilator. The agent3 short-annihilator lemma says if F intersection G=0 then D(alpha+beta)=0 (p6); contradiction. Hence a common linear factor exists. Each branch weight<64 forces actual support in a level of that factor, and the three levels fit an affine equation using the two control bits. Thus U is properly supported.

LEMMA3. In ambient13, no full-affine-span codim6 word has weight<128; and among weights128..142, only128 is possible.
The first assertion is firm KT. For the second use lemma1 and sorted branches. Smallest32, second32or48. If second32, third has weight u-64. For u>128 but<=142, that weight lies strictly between64 and80; since both minimum32-flat top6 forms share a factor (6+6>11), the third top also has it. If both factor-levels were nonzero, their weights (min32,next48) would total>=80 unless exactly64; impossible. Thus all branches have actual factor levels and U is properly supported.
If second48, third is one of48,56,60,62 by firm KT. Let alpha be the minword top6 (rank20), beta=F4 q4 (middle rank32). If alpha has no factor in F, the shear argument makes the middle contraction images disjoint, so rankgamma>=52. But the third branch's KT possibilities have middle ranks32,44,38,40,40, all<52. (TypeI ranks beyond6 cannot fit because n11 minus4 factors leaves7 variables.) Thus a common factor exists and all branch weights<64 force proper support.

THEOREM. Every f in RM(7,14) with weight322,326,330 or334 has an empty affine codim2 flat.
If not, every hyperplane section has full affine span13. Parseval supplies one U of weight<=156. Lemma2 gives a hyperplane section inside U of weight32 (U cannot be properly supported). This is a codim2 flat in the original ambient. Let the other three coset weights be a,b,c. The three hyperplane weights32+a,32+b,32+c must have full span13, hence are>=128 by lemma3; a,b,c>=96. Their total with32 is<=334, so each a,b,c<=110, and all three hyperplane weights are<=142. Lemma3 then forces each128, so a=b=c=96 and total320, contradiction.

All uses of Parseval need only the upper bound156, not earlier erroneous sharper per-target bounds.
