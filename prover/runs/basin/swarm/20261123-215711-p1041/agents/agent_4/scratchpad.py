text=r'''# Complete proof assembly / dependency roadmap

## Status and classical inputs
The new proof is complete once the checked finite certificates and lemmas listed below are combined. The ONLY classical inputs are:
1. Reed--Muller duality, minimum weight 2^(m-r), and its affine-flat minimum words (can also be proved by the usual Plotkin induction).
2. Ax/McEliece divisibility: weights of RM(r,m) are divisible by 2^floor((m-1)/r).
3. Kasami--Tokura classification STRICTLY BELOW twice the minimum: a monomial times a quadratic, or a sum of two minimum flat indicators (with the usual parameter restrictions).
4. The PUBLISHED NUMERICAL low-weight theorem of T. Kasami, N. Tokura, S. Azumi, 'On the weight enumeration of weights less than 2.5d of Reed--Muller codes', Information and Control30 (1976),380--395. Only these explicit NECESSARY numerical consequences are quoted:
   c=6, w<160: {0,64,96,112,120,124,126,128,136,144,148,152,154,156,158}.
   c=7, w<320: {0,128,192,224,240,248,252,254,256,272,288,296,304,308,312,314,316,318}.
The proof does NOT quote or assume the previously conjectured 'factor OR3-flat ORmin+quadratic' structural cover. It was never verified and is unnecessary.

## Answer
Put N=2^m. There are33 maximal even intervals, in order:
[0,0], [128,128], [192,192], [224,224], [240,240], [248,248],
[252,256], [272,272], [288,288], [296,296], [304,304], [308,308],
[312,320], [324,324], [328,328], [332,332], [336,N-336],
[N-332,N-332], [N-328,N-328], [N-324,N-324], [N-320,N-312],
[N-308,N-308], [N-304,N-304], [N-296,N-296], [N-288,N-288],
[N-272,N-272], [N-256,N-252], [N-248,N-248], [N-240,N-240],
[N-224,N-224], [N-192,N-192], [N-128,N-128], [N,N].
All intervals are even intervals. Every unadorned numerical endpoint b means0*N+b; N-b means1*N+(-b), so alpha is always0or1 and beta is the displayed explicit integer.

## Sufficiency
The stdlib checker agent3_sufficiency_checker.py constructs actual affine7-flats and their XORs and checks every exceptional low weight E={0,128,192,224,240,248,252,254,256,272,288,296,304,308,312,314,316,318,320,324,328,332}, plus actual base14 words of every even weight336..8192. Its central certificate is only13 rows of numerical masks; each row gives3-flat seed and a7-dimensional parallel-flat partition. For each partition cell containing n_i seed points, toggling that cell changes weight by128-2n_i; exact subset-sum DP checks all choices. Two extra explicitly constructed affine-threeflat words fill358 and362. Complementation covers8192..16048 and the reflected low weights.

Induction: if u,v belong RM(m-7,m), then (1+t)u+t v belongs RM(m-6,m+1), with weight wt(u)+wt(v). Thus W_(m+1) contains W_m+W_m. With C=[336,N-336]_2 and0,N available, C+0,C+N,C+C are [336,N-336], [N+336,2N-336], [672,2N-672]. They join to [336,2N-336] because N+2>=1008 for N>=16384. Low E persists by adding0; high E reflects by complement. This proves all claimed weights for all m>=14.

## Necessity: finite reduction
Every codeword has even weight: each monomial of degree<m sums evenly over the full cube. Complementation preserves the code. Classical numerical KTA gives all exclusions below320. Thus only four new low exclusions322,326,330,334 are needed; once they are excluded, all claimed intervals are maximal.
For a support S of size w<=334 in dimensionm>=16, |S+S|<=1+C(w,2)<=55612<65536<=2^m. Choose a outside S+S. The quotient derivative along a has the same weightw and belongs RM((m-1)-7,m-1). Repeat to dimension15. Hence only dimensions14 and15 need new work (proper smaller affine support is handled by factoring its annihilators and Ax4-divisibility).

## Empty codimension-two flats
The main new structural lemma says every putative word of one of the four target weights in dimensions14OR15 has an empty affine codim2 flat. Full proof: agent3_universal_empty2_bootstrap.md (also base14 assembly agent4_base14_empty2_proof.md). Its inputs are all independently checked and use ONLY KT<2d:
- Universal weight2d affine-span bound: span<=2c+1 for codimc>=3. Proof by inductionc using an empty2-flat and tuples(D,D,2D)/(D,1.5D,1.5D); puremonomial-top2D follows one-step centroid descent to a minimum word. Checked independently agents2,3,4.
- Codim5 gaps66/70: agent4_codim5_no66_70.md, independent agent3 derivation#338. Reduce to dimensions10/11; empty2; tuples16,16,34/38or16,24,30; exterior flattenings plus purepair4 row-moment inequality exclude them.
- Weight68 proper support (ambient>=11): agent4_weight68_proper_support.md. Empty2, tuples16,16,36or16,24,28; common factor / flattening obstruction.
- Therefore every codim6 word<=156 in ambient13/14 has empty2: a small hyperplane section<=70 is either<64(KT factor),64(span<=11),68(proper), not66/70.
- Such small words have a32 hyperplane section unless their smallest nonzero branch is48. The only all>=48 triples are48,48,48;48,48,56;48,48,60. The new annihilator lemma forces a common factor, so these are properly supported.
- Full-span codim6 words in ambient13/14 of weights130..142 are excluded by minword+secondword exterior ranks (except128 may span13, never14).
- No empty2 in the target word would make all its hyperplane sections full spanning. The32 section above gives four coset weights32,a,b,c with a,b,c>=96, each<=110. In dimension14 each32+a must therefore be128, giving total320. In dimension15 some a<=100, giving a full-span14 word128/130/132, all impossible. Contradiction.

## Base14: exhaust the branch tuples
Use empty00 branch and write remaining branches a,b,h on12 variables, degree<=6, a+b+h degree<=5. Since w=2mod4, their pairwise inner products are odd. Sort their weights. The numerical c6 KTA list and the firm <2d list leave only:
(64,64,194/198/202/206), (64,96,162/166/170/174),
(64,112,154/158), (64,126,136/144), and (96,112,126).
All other small second-branch choices force a forbidden c6 weight.
The five cases are now completely proved:
-64,64: agent2_full_purepair_coset_proof.md + agent2_purepair_coset_arithmetic.py. Affine row/column second moments have image rank<=1; let g=h+delta_X+delta_Y, v=wt g,r=wt row0,c=wt col0,eps=g00. Then9(h-126)>=5v-512+4eps givesv<=246.4<256. KT reduces g to<=2 minwords, or rank6/8 quadratic on9-flat. The first gives<=4 affine7-flat original words; the second contradicts intersection bounds.
-64,96: agent3_6496_Pzero_proof.md and agent3_6496_Pone_completion.md. P0: leading-coefficient support and punctured minimum distance lead to impossible low-dimensional rows. P1 is possible onlyh174; the correction has two actual factors. Fat5-fiber centroid descent produces a codeword<256, so KT plus span bounds or the four-flat certificate finish.
-64,112: agent3_64112_direct_proof.md, agent3_64112_arithmetic.py / cubic checker. Two KT types. Affine row momentP must0; leading support constraints reduce to rank6 quadratic weight>=112 but<=100, or eight6-variable cubic slices each>=14 giving>=112 but<=108. The rank2 centroid shear is explicitly checked.
-64,126: agent3_64126_hilbert_proof.md. Canonical leading graph rankd. If no leading linear factor, full affine span12 and Hilbert-flattening bound w>=26+2R2+R3. For d2..5 these are154,168,174,176>144. Rankd1 has a leading factor; agent1_64126_proof.md then uses the proved purepair5 coset gap. Ranks independently recomputed by agent1 in Sage, not just bit Gaussian.
-96,112,126: agent2_96112126_exterior.md and checker. Symmetric middle flattening ranks32,44/38,40 and sharp image-intersection dimensions force a contradiction.
The finite four-ARBITRARY-affine7-flat certificate used above is agent2_four_affine_checker.py plus agent2_four_affine_lemmas.md; agents1/4 independently checked the geometric lemmas. It uses necessary intersection-rank inequalities and6 explicit geometric exclusions, and returns UNSAT for all four weights.

## Dimension15 parity and convolution reduction
Detailed files: agent4_parity_reduction.md, agent4_m15_qzero_empty2_proof.md, agent4_m15_qzero_checker.py.
Let F=sum_(x in S)e_x in F2[F2^m], z_i=1+e_i, I=(z_i). The degree condition gives F in I7 by vanishing moments<=6. For even supports define q(F)=unordered-pair-sum vector+(w/2 mod2)e_0. Polarization is q(F+G)+q(F)+q(G)=FG; q(z_A)=0 for |A|>=2. Thus q(F) in I14.
For m15, q(F) is affine as coefficient function; q(F)(0)=1 gives1+ell(a). The quotient derivative weight d_a satisfies d_a/2=ell(a)mod2.
If ell nonzero, base14 exclusion forces d_a<w for all ell(a)=1, so I_a=w-d_a>=4. There are16384 such shifts. If S0,S1 are ell slices, 2|S0||S1|=sum I_a>=65536, but2|S0||S1|<=334^2/2=55778. Contradiction.
If ell0, q(F)=J15. Use the proved empty2 flat and branches0,A,B,H on F2^13. The outer st coefficient of q(F) is exactly AB, hence AB=J13. Sorting, smallest branch has weight64or96. If64, its support is a6-flat; convolution says every128 parallel6-coset meets B oddly, so b>=128. The c6 numerical list then forces b128 and h130/134/138/142, all forbidden. If96, it is an unbalanced rank4 quadratic on an8-flat L. Every32 L-coset of B must convolve this quadratic to1. It needs at least4 points: odd1/3 points preserve the quadratic part, while2 points give a derivative which cannot be constant1 for an unbalanced quadratic. Thus b>=128, contradicting b<=119. This completes m15, and projection completes all dimensions.

## Final check
All endpoints, interval sums and maximality arithmetic were independently checked in agent4_induction_checks.json. There are exactly33 intervals, with fixed integer alpha,beta as listed. No structural KTA normal-form cover is used; the two numerical KTA lists are the only above2d external input.
'''
open('workspace/agent4_proof_assembly.md','w').write(text)
print('saved full compact proof assembly/dependency roadmap')
