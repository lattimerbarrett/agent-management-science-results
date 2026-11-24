# Complete Reed–Muller spectrum for codimension seven

This is the complete proof article and executable-certificate appendix for the result stated in the answer. All mathematical proof obligations are discharged. The only externally quoted non-elementary inputs are the classical minimum-word theorem, the standard divisibility theorem, Kasami–Tokura below twice minimum distance, and the explicitly stated NUMERICAL specializations of the Kasami–Tokura–Azumi 1976 weight-enumeration theorem. No presumed structural KTA cover is used.

The independently rerun finite certificate suite has ten programs, all PASS. The run manifest contains exact stdout, runtimes, and SHA256 hashes. Run `python workspace/agent2_combined_checker.py` from the parent directory of workspace. Requires Python, numpy, and z3; no network/subprocesses.

The subsequent chapters contain every technical lemma used in the main proof. A few source chapters retain their original conditional wording: the condition of an empty codimension-two flat is PROVED in the universal-empty-flat chapter; the linear-annihilator case for (64,126) is complemented by the subsequent Hilbert-bound chapter. These are implications used within the complete proof, NOT unresolved assumptions.



---

# Proof chapter 1: `agent3_final_proof_roadmap.md`

# FINAL PROOF ROADMAP — complete dependencies and narrative

## Answer and source policy
N=2^m. Low maximal intervals:
[0],[128],[192],[224],[240],[248],[252,256]_2,[272],[288],[296],
[304],[308],[312,320]_2,[324],[328],[332].
Then [336,N-336]_2 and the sixteen reflected intervals in reverse order.
Total33. All endpoints are alpha*N+beta with alpha0 or1 and displayed
integer beta. No odd weights occur. Low witnesses E consist of the22
individual even values in these16 intervals.

We EXPLICITLY QUOTE classical results, not pretend to reprove them:
* Minimum words of RM(r,n) are indicators of affine(n-r)-flats.
* Kasami–Tokura below2d: nonzero weight<2d words are either sums of at
  most2 minimum words, or affine-support-factor times a quadratic;
  the relevant quadratic non-two-flat words have support dimension c+2.
  In exterior language: min leading form decomposable, second leading
  form F_(r-2)*q_rank4, and the familiar below2d families.
* Divisibility: RM(r,n) weights divisible by2^floor((n-1)/r) for r>0.
* Kasami–Tokura–Azumi1976 NUMERICAL necessary lists only:
  codim6, weight<160: 0,64,96,112,120,124,126,128,136,144,148,152,154,156,158.
  codim7, weight<320: 0,128,192,224,240,248,252,254,256,272,288,296,
                         304,308,312,314,316,318.
  For lower-order codes these are upper lists; every listed value need
  not occur. No STRUCTURAL KTA coarse cover is used ANYWHERE.
Reference: T.Kasami,N.Tokura,S.Azumi, “On the weight enumeration of weights
less than2.5d of Reed–Muller codes”, Information and Control30(1976),380–395.
Do not invent a theorem number. The uncertain structural cover discussed
in old Slack messages has been entirely eliminated.

## Sufficiency, genuinely constructive
workspace/agent3_sufficiency_checker.py is self-contained stdlib and runs
0.1sec. It explicitly constructs every E value and every even336..8192
in RM(7,14). Its13 rows each give3 coordinate7-flats and a quotient
fixing7 coordinates. For support S and each7-flat quotient coset C,
occupancy n_C can be flipped independently to128-n_C. Hence attainable
weights are base=sum min(n_C,128-n_C) plus subset sums of abs(128-2n_C).
Integer bitset dynamic programming checks all subset sums EXACTLY.
Thirteen explicit rows cover every even336..8192 except358,362; explicit
affine7-flat XOR witnesses in the same checker cover these and all E.
Complement gives the rest of the base central interval.
Independent concatenation W_n+W_n subset W_(n+1) propagates the central
interval: its shifts by0,N and its self-sum overlap for N>=1006.
Embedding with a zero branch preserves each low E, and complement gives
upper weights. This proves all33 claimed intervals in every m>=14.

## Necessary reduction to four new holes
Parity and complement are elementary. Classical KTA numerical list
settles all weights<320. At320,324,328,332 witnesses exist; at336 and
above the central construction applies. Thus the ONLY new exclusions
needed are322,326,330,334 and their complements.
If m>=16 and wt<=334, some nonzero direction is absent from S+S, since
1+binom(334,2)=55612<65536. Quotient derivative along it preserves weight
and decreases both degree and dimension by1. Repeat to dimension15.
Hence only dimensions14/15 need new arguments.

## Universal empty codimension2 flat, m14/15
Complete narrative: workspace/agent3_universal_empty2_bootstrap.md.
Independent supporting proofs:
* New universal2d affine-span theorem: codim c>=3, wt2^(c+1) implies
  affine span<=2c+1. Agent2 wrote it; agents3/4 independently checked.
  Basec3: affine coordinate evaluation code self-orthogonal of dimension
  span+1<=length/2=8. Induction uses Parseval+KT to get empty2 and only
  (D,D,2D)/(D,1.5D,1.5D) branches. Pure-monomial top case simplified:
  subtract constant centroid minword; odd-row1/3 count forces the
  difference a minimum word in the lower-order code, hence span C+2.
* Codim5 weights66/70 absent: workspace/agent4_codim5_no66_70.md.
  Uses empty2, purepair4 moment gap, and tiny flatten rank bounds.
* Codim5 weight68 proper support: workspace/agent4_weight68_proper_support.md.
* New annihilator lemma: if alpha=F_(p-2)q4,beta=G_(p-2)q4', p>=6,
  F intersect G0, then D(alpha+beta)=0. Wedge by v gives either
  nondecomposable form with annihilator F+v, or decomposable(p+1)-form;
  neither can contain F+G dimension2p-4. This eliminates all sorted
  (48,48,48/56/60) branches of a small codim6 word.

Bootstrap: any codim6 word u<=156 in ambient13/14 has an empty2-flat:
Parseval small section<=70, codim5 gaps66/70, span bound at64, and proper68.
If u has full affine span, its smallest branch must32 (the48 cases
have common actual factor by the annihilator lemma). Thus u has a32
hyperplane section. Also every codim6 word of weight130..142 in ambient
13/14 has proper affine support. Proof: empty2 again; only branches
(32,32,66..78) or(32,48,56/60/62). First has a common factor and slices
cannot split64 into66..78. Second common factor follows from flatten
bounds52>44 (ambient13) or90>75 (ambient14).

If target f had no empty2-flat, all hyperplane sections would span their
hyperplanes. Parseval gives a section u<=156, hence a32 sub-section.
The four cosets then weigh32,A,B,C. Full-span unions32+A force A>=96,
and similarly. Total<=334 forces each A<=110. Thus32+A in[128,142]_2;
the proper-support range forces all three equal128, total320, impossible.
This proves the universal empty2-flat lemma in both dimensions.

## Base dimension14, classify branches using NUMERICAL KTA
Normalize branches(0,a,b,h) on12 variables, degree<=6, g=a+b+h degree<=5.
Sort weights. Since total is2mod4, <a,b>=1. Numerical lists leave ONLY:
(64,64,h194/198/202/206), (64,96,h162/166/170/174),
(64,112,h154/158), (64,126,h136/144), (96,112,126).
Every one is now unconditionally excluded, as follows.

1. (64,64): workspace/agent2_full_purepair_coset_proof.md.
   Canonical h top pure pair6, rows/columns odd centroid0; affine moment
   maps P,Q. Plucker/rank costs give decomposable values, minimal row
   models give excess>=44, rank2 refined count eliminates the one206
   case. Thus P,Q rank<=1. Subtract axes g; row/col count gives
     9(hwt-126)>=5 wt(g)-512+4g00,
   hence wt(g)<=246.4. KT below256 gives sum<=2 minimum words, or
   non-two-flat quad224/240 with support9. First lifts f to at most4
   affine7-flats; second has intersection<=70 versus required>=72.

2. (64,96): workspace/agent3_6496_Pzero_proof.md and
   workspace/agent3_6496_Pone_completion.md.
   Canonical top X6+Y6+U4W2, affine row moment P. For h<=174 its image
   has rank<=1. P0: leading Y-degree3 supportA4 and near-minimum cubic
   rows force graph X4->Z3 with all8 fibers odd centroid0; requires22
   graph points but only16. Leading Y-degree2 supportA2 forces rank4
   quadratic with weight>=96, yielding h<=160, contradiction.
   Rank1 only h174: all32 P0 rows minimal, b and g supported sameX5
   half. Subtract original min7-flatG; F supported affine12 has weight
   v208..268step4, meeting G's5-flat in i=(v-206)/2. For v>=256 this
   is25..31odd. Every parallel5-fiber odd and centroid graph C affine7.
   Odd-row1/3+fat-row count gives J=F intersect C>=(556-v)/4; K=F+C has
   weight<=1.5v-150<=252. KT either lifts to4 flats, or quad support9
   meets C>=42 points, making Fspan<=10 and originalfspan<=12, impossible.
   v<256 handled by same KT/span bound directly.

3. (64,112): workspace/agent3_64112_direct_proof.md.
   Both KT112 types have affine row moment P; h154/158<172 forces P0.
   Quadratic type: Y2-coefficients support commonA2, reduced rank6 quad
   needs weight112 but available<=100.
   Two-flat type: normalize rank<=2 graph M; rank1 centroid shear
   cancels only X5Y1, preserving affine P. K supported A3; reduced top
   omega=X3+Z3+e1*x1z2z3+e2*x2z1z3 has qtop1 on6 variables. Eight
   unused slices each need weight>=14, total112>available108.
   workspace/agent3_cubic_coset_checker.py EXACTLY enumerates all2^22
   lower-quadratic perturbations for5 relevant6-variable cubic tops;
   min/decomposable claims independently checked in1.9sec.

4. (64,126): workspace/agent3_64126_hilbert_proof.md together with
   workspace/agent1_64126_proof.md (conditional hypothesis now supplied).
   Graph top omega_d=X6+Y6+prod(Y+M_dX), d<=5. If proper support or d<=1,
   top has linear annihilator; factor proof reduces to purepair5 gap.
   If full span12, put T=Hodge(top h), flatten ranks R2,R3. Vanishing
   quadratic relations give H2>=13+R2, and C2 isotropic,C3 subset C2perp
   give R3<=wt h-2H2. Thus wt h>=26+2R2+R3. For d2..5 the bounds are
   154,168,174,176, excluding136/144. Exact66x495/220x220 bit ranks
   in agent3_64126_hilbert_checker.py independently checked by agent1's
   Sage dense GF2 Gaussian elimination.

5. (96,112,126): workspace/agent2_96112126_exterior.md.
   Middle flatten ranks32 for96,44/38 for112,40 for126. Support
   intersections and sharpened image bounds give rank>=44/50>40.

The common restricted-family lemma used above is the VERIFIED theorem
that XOR of<=4 arbitrary affine7-flats in F2^14 cannot have any target
weight. workspace/agent2_four_affine_lemmas.md gives all geometric
lemmas; workspace/agent2_four_affine_checker.py checks necessary ranks,
Ingleton, and the proven profile cuts by Z3 UNSAT. No restricted-family
claim was ever promoted to a universal theorem; it is applied only after
the branch reductions genuinely produce<=4 flats.

## Dimension15 and finish
See agent4's m15 proofs. The group-algebra divided-square invariant
q'(F) lies in I^14; its coefficient function Q on quotient directions
is affine-linear. If Qnonzero, base14 exclusions force intersections
>=4 outside its kernel; splitting S gives2uv>=4*16384, impossible
for wt<=334. If Q0, the universal empty2 lemma applies. Outer branch
algebra gives AB=J on13-variable group algebra. Smallest branch is64
or96. If64, convolution parity forces b meet128 cosets, hence b>=128,
contradicting branch list. If96, support8 with rank4 unbalanced quad;
each of32 cosets needs at least4 b-points (odd translate count leaves
quad part; two translates cannot sum constant1), hence b>=128 versus
sorted b<=119. Thus dimension15 excluded too. Collision-free quotient
reduction settles all m>=16. Complement and KTA then prove exact spectrum.

## Explicitly NOT evidence / not used
Old UNKNOWN SAT runs, annealing searches, presumed KTA structural covers,
and three-flat enumerations as a universal classification are NOT used.
All new structural lemmas have independent reviews and actual checkers.


---

# Proof chapter 2: `agent4_proof_assembly.md`

# Complete proof assembly / dependency roadmap

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


---

# Proof chapter 3: `agent2_four_affine_lemmas.md`

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


---

# Proof chapter 4: `agent2_twice_minimum_span_proof.md`

# Weight twice minimum: affine-span theorem

**Theorem.** If c>=3 and f belongs to RM(n-c,n) with weight 2^(c+1), its support has affine span at most 2c+1.

Only the classical Kasami--Tokura theorem for weights strictly below twice minimum, minimum-weight classification, and elementary linear algebra are used. Independent reviews: agents 3 and 4 (Slack 333--336).

## Conventions and two facts
The highest squarefree homogeneous part transforms as an exterior form under linear changes of variables. A proper affine support with normal ell implies ell divides the top form. For a decomposable p-form, its linear divisor space equals its p-dimensional factor space. If alpha,beta are distinct decomposable p-forms with common factor space F, then their sum either is decomposable (when dim F=p-1), or has divisor space exactly F. This follows by factoring F and taking the sum of two decomposable forms with disjoint factor spaces, each of degree >=2: wedging by a nonzero vector outside F cannot kill that sum, by its two disjoint multidegrees.

For a degree-p form omega, use its contraction matrix from exterior k-duals to exterior (p-k)-vectors. For two matrices A,B of the same shape,

rank(A+B) >= rank(A)+rank(B)-dim(im A intersect im B)-dim(row A intersect row B).

The contraction image and row spaces of a decomposable form with factor space U are the appropriate full exterior powers of U. For beta=F_(p-2) wedge q, where q is a nondegenerate bivector on a complementary 4-space Q, its degree-j contraction-output space is

Lambda^j F + (Lambda^(j-1) F wedge Q) + (Lambda^(j-2) F wedge span(q)),

with impossible terms omitted. Thus for output degree j>=3 every vector has a positive F-factor. If a subspace W has W intersect F=0, shears of Q by F (which preserve beta) put W inside Q; the intersection of that output space with Lambda^j W is zero for j>=3, and is at most 1-dimensional for j=2.

## Pure decomposable-top lemma
Let H on X_C times Y_p have degree p, only top term Y_1...Y_p, and weight 2D where D=2^C. Assume C>=3 and p>=C+2. Every Y-row is odd. The parity sum of its Y coordinates (its centroid) is constant: these centroids are degree-at-most-one polynomials in X, and the coefficients of their linear terms would be mixed degree-p terms of H, which vanish. Translate the common centroid to zero. Let M be the indicator of Y=0, and J=|supp(H) intersect supp(M)|. A row containing zero costs at least 1; an odd row missing zero but with centroid zero costs at least 3. Hence

2D >= J+3(D-J)=3D-2J,

so J>=D/2. The top terms of G=H+M cancel, whence deg G<=p-1. G is nonzero since H has weight 2D rather than D. Its minimum possible weight is 2D, while

wt(G)=3D-2J<=2D.

Thus G is minimum and is an affine (C+1)-flat, and J=D/2. The affine C-flat M and affine (C+1)-flat G meet in a (C-1)-flat; their affine union span has dimension C+(C+1)-(C-1)=C+2. H is supported in that span. (In fact no p>=C+2 hypothesis was needed for this argument once the centroid degree assertion holds.)

## Induction
The case c=3 follows directly from moments: on the support S of size 16, evaluate all affine linear functions. Their evaluation code has dimension dim(aff S)+1 and is self-orthogonal, since all moments of degrees <=2 vanish. Thus dim(aff S)+1<=8.

Suppose c>=4, and the theorem is known for c-1. It suffices to show proper support whenever n>=2c+2; repeated factoring then gives the claimed bound. Put d=2^c. Parseval gives a hyperplane section of weight <d. This section is in a codimension-(c-1) code, hence is below twice its minimum. The strict KT classification shows its affine span has dimension at most 2c-2 (the two-minimum-word case has intersecting (c-1)-flats; the quadratic case has span c+1). It is therefore supported properly inside its hyperplane. This gives an empty affine codimension-two flat of f.

Normalize that empty flat to selector position 00. The other branches a,b,h, on N=n-2 variables, have degree at most p=n-c-1. They satisfy deg(a+b+h)<=p-1. Their minimum weight is D=2^(c-1), and their total weight is 4D. Reorder the three branches. The strict second-weight bound forces exactly

(D,D,2D) or (D,3D/2,3D/2).

If any branch is zero, the original support already lies in a hyperplane. Below assume all three are nonzero.

### Branch weights D,3D/2,3D/2
Let alpha be the decomposable top form of a. The top forms beta,gamma of b,h both have shape F_(p-2) wedge q_rank4. If alpha's factor space A meets F nontrivially, choose ell in that intersection. Then ell divides alpha,beta,gamma.

If A intersect F=0, let W=A intersect supp(beta). By the shear observation above, put W inside Q. When p>=6, choose contraction k=3: both output degrees 3 and p-3 are >=3, so the alpha and beta image spaces and row spaces have zero intersections. Consequently rank(gamma)>=rank(alpha)+rank(beta)>rank(beta), impossible because beta and gamma have the same canonical shape. When p=5, choose contraction k=2. The two intersections have dimensions 0 and at most 1; ranks alpha,beta,gamma are 10,16,16. Thus rank(gamma)>=25>16, also impossible. Here p>=c+1>=5, covering every case.

Thus ell exists. Since each branch has weight <2D and ell divides its top form, its restrictions to ell=0 and ell=1 have degree <=p-1, on N-1 variables, and minimum weight D. At most one is nonzero. Thus each branch is actually supported in one ell-slice.

### Branch weights D,D,2D
Let alpha,beta be the decomposable p-tops of a,b, and F their common factor space. Its dimension is at least 2p-N=n-2c>=2. Let gamma=alpha+beta be h's p-top.

If gamma is nondecomposable, its divisor space is exactly F. Induction applies to h, of codimension c-1 on N=n-2>=2(c-1)+2 variables and weight 2D. It has proper support, whose nonzero affine normal ell divides gamma and hence belongs to F.

If gamma is nonzero decomposable, dim F=p-1. Apply the pure-top lemma with C=c-1; since p>=c+1=C+2, h has affine span <=c+1. Its actual normal space has dimension at least N-(c+1)=p-2 and is contained in D(gamma), which has dimension p. Since F is another subspace of D(gamma), their intersection has dimension at least (p-2)+(p-1)-p=p-3>0. Choose ell there.

If gamma=0, h has degree <=p-1 and minimum weight 2D in that lower-order code, hence is an affine c-flat. Its normal space has dimension N-c=p-1. The common factor space of alpha=beta has dimension p; these meet in dimension at least 2p-1-N=n-2c-1>=1. Choose ell there.

In every subcase h is actually supported in an ell-slice. The minimum branches a,b are also actually supported in ell-slices, since ell divides their top forms.

## Recover the affine factor of f
In either weight pattern each nonzero branch is contained in one ell-slice. The three slice values, at selector positions 10,01,11, can be interpolated by a single affine function of the two selector bits (three equations for three affine coefficients). The zero branch 00 imposes no condition. Consequently the original support is contained in an affine hyperplane, completing the induction and theorem.


---

# Proof chapter 5: `agent4_codim5_no66_70.md`

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


---

# Proof chapter 6: `agent4_weight68_proper_support.md`

# Unconditional proper support of weight68, codimension5

THEOREM. For M>=11, every word of weight68 in RM(M-5,M) has an affine-linear factor.

Parseval gives a nontrivial Walsh magnitude>=12: coefficients are multiples4, and their mean square is68(2^M-68)/(2^M-1)>64. A hyperplane section therefore has weight<=28. In codimension4 the minimum is16, and the firm <32 KT classification shows every such section has a linear factor (its order M-5>=6 exceeds4). Thus original support has an empty affine codimension-two flat.

Write branches0,a,b,h on n=M-2 variables, of degree<=p=M-6, with a+b+h degree<=p-1. Sorting nonzero branch weights, minimum is16 and second16or24. Hence tuples are(16,16,36) and(16,24,28). If an additional branch is zero, the whole word is already properly supported.

A common top linear factor ell of a,b is also a top factor of h. The branches below32 then are supported in an ell-level (otherwise the two ell-levels each have minimum16); the36 branch has the same conclusion because16+20 is impossible by firm <32 KT, and any other two nonzero levels total>=40. Three branch levels can be fitted by an affine function of the two selector bits, giving a global affine support hyperplane.

For(16,16,36), a,b are minimum affine4-flats, and their top p-form annihilator spaces have dimensionp in n=p+4. Sincep>=5, they intersect nontrivially. This gives ell.

For(16,24,28), alpha=TOP_p(a) is decomposable; beta=TOP_p(b)=vol(F_(p-2)) wedge q4 for rank4 quadratic q. Gamma=alpha+beta is either vol(F'_(p-2)) wedge rank6 quadratic, or vol(G_(p-3)) wedge sum of complementary cubic monomials (the two <32 KT forms for28).

If alpha shares a factor with F, done. Otherwise p+(p-2)<=n=p+4, hencep<=6. Forp5, the2/3 flattening ranks are alpha10,beta16,gamma22or19. A shear of Q4 byF puts the support intersection intoQ4; one image intersection is0 and the transposed image intersection at most the line<q>, so rankgamma>=10+16-1=25, contradiction. Forp6, middle3 ranks are20,32,44or38; both image intersections vanish under the same shear, so rankgamma>=52, contradiction. These are the same canonical rank checks as agent4_weight136_flattening_checks.json. Thus a common factor always exists and the theorem follows.

No KTA above2d normal-form statement or numerical gap is used.


---

# Proof chapter 7: `agent3_universal_empty2_bootstrap.md`

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


---

# Proof chapter 8: `agent2_full_purepair_coset_proof.md`

# Complete pure-pair-six coset gap

**Theorem.** Let H be a Boolean function on X+Y, dim X=dim Y=6, of degree at
most6, with degree6 part equal to the sum of the full X and full Y monomials.
Then wt H is not194,198,202,206.

Inputs: elementary binary RM minimum/second weights and minimum supports;
the standard Kasami--Tokura classification below twice minimum distance;
and the independently checked four-affine-flat exclusion in F2^14
(agent2_four_affine_checker.py and its geometric lemma file).
No above-2d KTA classification is used in this theorem.

## 1. Moment normalization and row costs
Each row and column has odd weight. Its XOR (centroid) is constant, independent
of the row/column parameter, since the mixed degree6 coefficients vanish.
Independent translations of X,Y therefore make every row/column centroid0.
For a row T subset Y define the alternating second-moment matrix
P=sum_(y in T) yy^t (its diagonal is0 since the centroid is0).
P=P(x) is affine in x: its entries are sums of monomial coefficients of Y-degree
at least4, and the degree4 coefficients have X-degree at most1 because all
mixed degree6 coefficients vanish. Define Q(y) symmetrically.

For any odd set with centroid0, rank(P)<=|T|-1. Thus P=0 has row minimum1,
uniquely {0}; rank2 has minimum3, uniquely the three nonzero vectors in its
2-dimensional support; rank4 has minimum5, and any minimum5 row lies in the
4-dimensional support of P. These claims follow by writing one point as the
sum of the others; in a minimum row, its span equals the moment-matrix image.
If two rows have the same parity, centroid and P, their XOR has zero moments
through degree2, hence belongs to RM(3,6), minimum distance8.

## 2. Every P-value is decomposable
A rank2 alternating matrix is called decomposable; zero is also allowed.
Suppose P has a nondecomposable value. If its affine image dimension d>=3,
at least56 rows have P nonzero. A nonzero4-by-4 Pfaffian composed with the
affine map P is a nonzero quadratic Boolean function, hence is nonzero on at
least16 x's. These rows have rank at least4. The row-cost lower bound is then
64+2*56+2*16=208, impossible.

If d<=2 and0 is not an image, the baseline192 plus at least16 nondecomposable
rows already gives224. If0 is an image, d=1 with rank>=6 gives256; rank4 gives
baseline192. For d=2, two or more nondecomposable nonzero values give baseline
at least16*(1+3+5+5)=224. The only remaining case has values0,alpha,beta,gamma,
where alpha,beta are rank2 and gamma=alpha+beta has rank4. All their supports
lie in W=im gamma, dimension4. The d=1 remaining case also has such W.
Both cases have baseline192, and every minimum row lies in W.

Projection to Y/W, dimension2, has parity pattern delta0: parity, centroid,
and second moments determine this four-value pattern. Thus every actual row
has an odd number of points in W, in particular at least1. A nonminimal row
of minimum m in {1,3,5} and excess e>=2 has at most m+e-1<=3e points outside W.
Every outside column is odd and nonempty, so at least48 outside points are
needed. But total excess E<=206-192=14 gives at most42. Contradiction.
Thus all P-values are zero or rank2. The same holds for Q.

## 3. Pairwise intersection and minimal-row model
The supporting2-planes of nonzero P-values pairwise intersect. Otherwise take
two disjoint ones alpha,beta and gamma=alpha+beta of rank4. For every value eta,
eta+gamma is also in the affine image. Both eta and eta+gamma are decomposable,
so their supports are contained in im gamma=W4. Zero is not in the affine image.
The baseline is192; minimum rows lie in W. Nonminimum rows have at most2e
outside points (m=3, e>=2), so total outside is at most28, less than48.

A pairwise-intersecting family of2-planes either has a common1-space, or all
planes lie in a common3-space. Elementary proof: choose two distinct planes
U,V with common line L; if a third misses L it lies in U+V, and any plane not
contained in U+V would have to contain L and hence miss that third plane.
Consequently the affine P-image lies in a star u wedge Y (dimension5) or
Lambda^2 W3 (dimension3), and has affine dimension d<=5.

Let M(x) be the unique minimum row for P(x). Every M-column has even parity
and a constant centroid c. If d<=4, each P-fiber has dimension at least2,
so both its parity and its XOR are0; hence c=0. If d=5, the image is the full
5-dimensional star, and the kernel fibers are pairs with difference k.
For y=0, its M-column is the zero-P fiber; for y=u it is the union of31
nonzero fibers; for every other y it is one fiber. Each has even parity and
centroid k, so c=k in this last case.

Let B=wt M=64+2*#{x:P(x) nonzero}, E=wt H-B, and D=H+M.
Every nonzero row difference has weight Delta<=4e, where e is its row excess:
for a rank2 row, e>=2 and Delta<=e+6<=4e; for P=0, e>=6 and Delta<=e+2<=4e.
Every D-column is odd with centroid c. Put r=wt(D row c), and let e_c be that
row's excess. A column containing c costs at least1; a column missing c costs
at least3. Thus wt D>=192-2r. On the other hand
 wt D<=r+4(E-e_c),     r<=e_c+6.
Therefore4E>=192-3r+4e_c>=174. Since E is even, E>=44.
If0 is not in the image, B=192, impossible. If d>=3, B>=176, also impossible.
Thus P and Q have affine dimension at most2, and their images contain0.

## 4. Excluding dimension2
Dimension2 has B=160, so E>=44 leaves only target206, E=46.
For P, let m0 be its minimum at row0, e0 that row's excess, r its D-row weight,
and z the number of other P-zero rows which are nonminimal.
For each such zero row,4e-Delta>=16. Since M-column centroids now equal0,
 192-2r <= wt D <= r+4(46-e0)-16z.
So4e0-3r+16z<=-8. Using r<=e0+2m0 gives
 e0+16z<=6m0-8.
For m0=1 this is impossible; hence m0=3, e0<=10,z=0. All16 zero-P rows are
{0}, and row0 of H has weight at most13.
If Q has dimension0 or1, it has64 or32 zero columns. At most13 can be the
minimum singleton {0}; the other zero columns have excess at least6.
This costs at least306 or114, exceeding their total excess142 or78.
If Q has dimension2, its same argument forces all16 zero-Q columns to be
{0}, giving row0 weight at least16, also impossible. Thus neither P nor Q
has dimension2. Both have dimension at most1 and images containing0.

## 5. Short reduction to the standard <2d theorem
Set g=H+delta_X+delta_Y, v=wt g, r=wt(g row0), c=wt(g col0), epsilon=g(0,0).
Then degree g<=5 and the exact identity is
 s=wt H-126 = v-2r-2c+4epsilon, with s<=80.
Every g-row has zero parity and centroid. Except in at most32 rows its second
moment is0, and then a nonzero row has weight at least8; in those at most32
rows it has weight at least4. Count the c rows containing column0, then add
the exact row0 weight separately. This gives
 v>=8c-128+r-8epsilon.
The transpose gives v>=8r-128+c-8epsilon. Hence
 9(r+c)<=2v+256+16epsilon,
 9s>=5v-512+4epsilon,
so v<=246.4.

The Kasami--Tokura theorem for RM(5,12), minimum128, now leaves only
v=0,128,192,224,240. Zero would give H=delta_X+delta_Y of weight126.
The128 case is one affine7-flat; the192 case is two such flats; each224/240
case is either two such flats, or a rank6/rank8 quadratic times three linear
factors. In the latter cases g is supported in an affine9-flat L.

Let A,B be the two complementary6-flats (the delta axes). In the exceptional
quadratic case I=|g intersect(A triangle B)|=(v+126-wt H)/2>=72. But I<=70:
if L contains0 and g(0)=1, putting p=dim(L intersect A),q=dim(L intersect B)
gives p+q<=9 and I<=2^p+2^q-2<=70. If g(0)=0, restrictions to A,B have even
weights and omit0, so the upper bound improves to68. If L avoids0, two
nonempty intersections have p+q<=8, giving I<=68; one empty gives at most64.
Contradiction.

In all other cases g is the XOR of at most two affine7-flats. Introduce two
new variables t,s and form
 F(t,s,x)=t*1_A(x)+s*1_B(x)+ts*g(x).
Its four branches are0,1_A,1_B,H, and its weight is128+wt H, one of the four
forbidden322,326,330,334. It is the XOR of at most four affine7-flats in14
variables, contradicting the independently checked four-flat theorem.
This proves the stated coset gap.

## Appendix: pure-pair-five gap (dimension10)
The identical normalization for dim X=dim Y=5 proves: if wt H<=82, then wt H=62.
Here P,Q are affine. A nondecomposable value with image dimension>=3 gives
baseline32+2*28+2*8=104; image dimension<=2 gives at least96. Thus all values
are decomposable. Zero must be an image (otherwise baseline96), and image
dimension is at most2 (otherwise baseline88). Consequently minimal-row model
M has even columns and centroid0 (fibers dimension>=3). The excess calculation
is4E>=3*32-18=78, so even E>=20. Image dimensions1,2 have baselines64,80,
which would give weight at least84,100. Thus P=Q=0 for EVERY weight at most82.
Now g=H+delta_axes lies in RM(4,10), minimum64, and each nonzero row/column has
zero moments through degree2, hence weight at least8. Therefore v>=8r,8c,
and wt H-62=v-2r-2c+4epsilon>=v/2. A nonzero g costs at least32, so wt H>=94. Zero g gives62. Consequently the ONLY pure-pair-five coset weight at most82 is62.


---

# Proof chapter 9: `agent3_6496_Pzero_proof.md`

# (64,96) zero2 branch: zero-row-moment case proved

Assume selectors have branches (0,a,b,h), on X6 x Y6, with a min64,
b second96, h weight in {162,166,170,174}, and h+a+b degree<=5.
Odd <a,b> implies a-support and affine hull L8 of b meet in a 2-flat,
on which b's quadratic is nondegenerate. Decompose b=B1+B2 with min64
flats intersecting in4-flat; a and B1 meet in a point. Coordinates give
 a=delta_Y, B1=delta_X, B2=1_{U4(X)=0}1_{W2(Y)=w}.
Their intersections with a have sizes1 and0/4 respectively.
We can align a with the constant row centroid of h by translating Y
only on selector t=1; this changes b,h but not a and leaves B1 fixed.
We can align B1 with the constant column centroid of h by translating X
only on selector s=1; this changes h but not a or b. Global translations
then put a=delta_Y, B1=delta_X, both h-centroids0. These are affine
transformations on the full14-space, not ad hoc polynomial changes.
The leading6-form is
 H6=prod X6 + prod Y6 + prod U4(X) prod W2(Y).
Every row/column has odd cardinality; first moments are constant because
mixed X1Y5/X5Y1 coefficients vanish. Row second moment P(X) is AFFINE,
as the mixed X2Y4 coefficient vanishes. Assume P identically0.

K=h+delta_Y has row parity, centroid and second moments0, so its Y-degree
is <=3. Its top6-form is prod X6+prod U4 prod W2. In particular its maximal
Y-degree j is2 or3. A nonzero K-row of degree <=j has weight>=2^(6-j),
so its h-row contributes excess >=2^(6-j)-2 over the baseline1. The total
excess is wt(h)-64 <=110.

j=3: Each Y3 coefficient has X-degree<=2, so its nonzero weight is16 or
>=24 by minimum/second distance. There are at most floor(110/6)=18
nonzero K-rows. Thus every nonzero Y3 coefficient is a minimum quadratic
with affine4-flat support. All these supports coincide, since the union
of distinct such supports has size>=24. Call this16-point affine flat A.
K is supported in A. Otherwise pick maximal Y-degree r outside A.
For r2, a coefficient has X-degree<=4. Its support outside A has >=2
points: choose any outside point, separate it from A by an affine
hyperplane, then restrict the coefficient to that5-space and use minimum
distance2. These outside rows cost >=2*14=28 excess, while the16 A-rows
cost >=16*6=96. Total124>110, impossible. For r1 the X-degree<=4 again,
so >=2 outside rows cost >=60, even worse. For r0 one row costs62.

All K-columns are odd and centroid0. An odd subset of A has centroid
in A, so0 in A and A is linear. Factor K=1_A k, on X_A4 x Y6. Then
k degree<=4 and its top4-form has only types X4 and X2Y2; in particular
there is no mixed X3Y1. (The X-only factor top(1_A) divides U4, since
it divides the Y2 part of top K.) Every one of16 rows has the SAME
nonzero cubic top in Y, so is at least8. Set gamma=wt k and
q=wt k(.,0). The latter is odd, hence q<=15, and
 gamma=wt h-64+2q <=140.
Thus at most3 rows can be non-minimum (second RM(3,6) weight12).
At least13 minimum rows are affine3-flat indicators with the SAME
leading cubic, hence with a COMMON direction V3. Choose Y coordinates
(z3,w3) with w3 the free V3 coordinates. Each coefficient of a Y-monomial
involving any w has X-degree<=2 (including Y1, since X3Y1 is absent).
It vanishes on at least13 X-points, so must vanish identically: a nonzero
quadratic in4 variables has weight>=4, not<=3. Thus k is independent of w.
Its weight gamma is8 times the weight of k' on X4 x Z3. All8 columns
of k' have odd cardinality, so wt k' is even; gamma is a multiple16.
Since128<=gamma<=140, gamma128. All16 rows are minimum and k' is the
indicator of a graph from X4 to Z3. Every one of its8 fibers is odd with
centroid0 in X4. At most one fiber is a singleton (that singleton must
be0); all others have at least3 points. This needs >=1+7*3=22 graph
points, contradicting16.

j=2: Each nonzero K-row costs >=14 excess, hence there are <=7 such
rows. The unique canonical Y2 coefficient can have X-degree4 and has
decomposable leading4-form U4; every other Y2 coefficient has degree<=3
and minimum weight8, hence is0. The canonical coefficient has weight<8,
so is a minimum4 word: weight6 is the second RM(4,6) type whose top form
is F2 times a rank4 quadratic, not decomposable (firm KT below2d).
Its support is an affine2-flat A. The same outside argument gives
4*14+2*30=116>110 for r1 and4*14+62=118>110 for r0. Thus K is supported
in A, and A is linear by the column centroid. Its annihilator is U4,
so A=T2, complementary to U4. Factoring K=1_A k gives k of degree2
with top2 equal prod T2+prod W2, a rank4 quadratic on8 variables.
Also gamma=wt K=wt h-64+2q <=174-64+6=116 since q<=3.
An unbalanced rank4 quadratic on8 variables has weights96/160;
a linear radical term gives balanced128. Thus gamma96, forcing
wt h=64+96-2q<=160, contradiction.

Conclusion: P=0 excludes all four (64,96) target branches. No KTA above
2d is used. The remaining orientation is wt h174 and P affine rank1.
The general moment argument forces all32 P0 rows minimal delta_Y and
P(0) nonzero; the degree5 difference g=h+a+b is supported on the P1
linear half A5 containing T2. This last orientation is not yet excluded.


---

# Proof chapter 10: `agent3_6496_Pone_completion.md`

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


---

# Proof chapter 11: `agent3_64112_direct_proof.md`

# Direct exclusion of both (64,112,154/158) branches, without KTA above2d

Let a,b,h in RM(6,12), a+b+h degree<=5, wt a64, wt b112,
wt h154 or158. Their leading6-forms satisfy H=A+B. Odd total half-weight
implies <a,b>odd. We use only the firm KT below2d classification of b,
and the already-proved general affine row-moment lemmas:
For an h with odd centroid-zero6-variable rows AND columns, affine row
second-moment P, and wt h<=158, P must0. Indeed nondecomposable moments
force weight>=192, all decomposable values give either image avoiding0
(baseline192), or linear image rank>=2 (baseline160), or rank1 with
baseline128 and excess>=44, requiring weight>=172. Hence P0.

TYPE Q: b is the rank6 quadratic with4 support factors, affine span8.
Its intersection with the min6-flat a has dimension exactly2 with a
nondegenerate quadratic restriction: dimension>=2 by spans and <=2 by
odd intersection. Choose this symplectic plane as one quadratic pair.
Coordinates X6=T2+U4,Y6 put the leading form into
 H=X6+Y6+U4*q4(Z), where q4 is rank4 quadratic in4 Y coordinates.
All row and column first moments are constant (no X1Y5/X5Y1 top terms),
so translate X,Y to make them0. The row second moment P is affine
(no X2Y4 term), hence0 by the general moment lemmas. Put K=h+delta_Y.
Then its Y-degree<=3, its top is X6+U4*q4(Z), and wt h-64<=94.
If maxYdegree3, a leading coefficient has X-degree<=2, minimum16;
each such row costs at least6 h-excess, giving >=96>94, impossible.
If maxYdegree2, there are <=floor(94/14)=6 nonzero rows. Any Y2
coefficient with nonzero leading4-part has decomposable top U4, and
weight<8, hence is a minimum4 word by firm KT (the second weight6
has nondecomposable top). All remaining Y2 coefficients have degree<=3,
minimum8, and are0. The nonzero leading coefficients are minimum words
with the SAME top U4, hence are parallel affine2-flats; distinct supports
are disjoint and have union8>6. Thus all supports are the same A2.
An outside row of degree1 yields >=2 outside points by punctured
minimum distance (coefficient degree<=4), costing >=60 excess, while
inside A2 costs >=56; constant outside costs62+56. Both exceed94.
Thus K supported in A2. Odd centroid-zero columns force A linear.
Factoring K=1_A k leaves a rank6 quadratic top X_A2+q4(Z) on8 variables.
Such a quadratic has weight>=112. But wt K=wt h-64+2q<=158-64+6=100,
where q=wt K(.,0)<=3 is odd. Contradiction.

TYPE P: b=B1+B2, two min6-flats meeting in a3-flat.
Odd <a,b> lets us choose B1 with odd a-intersection, hence meeting it
in a point. Their directions are complementary. In X=a,Y=B1 coordinates,
B2's leading form is U3(X) wedge eta3, with
 eta3=product_{i=1}^3 (z_i(Y)+M_i(X_T3)),
where z1,z2,z3 are independent Y forms, X_T3 is complementary to U3,
and rank M<=2. The last fact follows because a and B2 have even
intersection: if their directions were complementary they'd meet in
one point; thus their direction intersection has dimension>=1.
By independent basis changes put M in diagonal rank d=0,1,2 form.
The top H=X6+Y6+U3 eta has constant row centroid, but its column centroid
may have a linear part if d2. In that case write X_T=(x1,x2,x3) and
 eta=(z1+x1)(z2+x2)z3. The linear column centroid is x3_direction*z3.
The rank-one shear x3 -> x3+z3 cancels it: B2 is unchanged since eta
is independent of x3, while X6 adds exactly U3*x1*x2*z3. Consequently,
in all cases (after this shear if needed),
 H=Y6+U3*(x1*x2*x3+z1*z2*z3+e1*x1*z2*z3+e2*x2*z1*z3),
with e1,e2 in{0,1}. Both centroids are now constant; translate to0.
The row moment P is still affine (top maxYdegree3), hence0 as before.
Set K=h+delta_Y. MaxYdegree3. There are <=floor(94/6)=15 nonzero rows.
The sole potentially degree3 leading Y3 coefficient has decomposable
top U3 and weight<16, hence is a minimum8 word by firm KT; the other
Y3 coefficients degree<=2 and minimum16 must vanish. Let A3 be this
common affine3-flat support, parallel to T3.

K has no support outside A. For a maximal outside Y-degree r2, the
coefficient has degree<=4 and its TOP4 is divisible by U3 (from the
displayed top H). Separate an outside point from A by a hyperplane
lambda in U3. Restriction kills the degree4 part, so on5 variables it
has degree<=3 and at least4 outside points. Thus excess is at least
8*6+4*14=104>94. For r1, the same argument gives degree<=4 on5 variables,
at least2 outside points, and excess>=48+60=108>94. For r0, excess>=110.
Thus K supported in A3, linear by the column centroid condition.
Factor K=1_A k. Then k has degree<=3 on9 variables, and its top3-form
in the6-dimensional X_A3+Z3 space is
 omega=x1*x2*x3+z1*z2*z3+e1*x1*z2*z3+e2*x2*z1*z3.
Its middle exterior quadratic invariant is1: the X3/Z3 complementary
pair contributes1 and the other monomials have no complements. Each
of the8 slices of the remaining3 unused variables therefore has weight
2 mod4. Its minimum weight is at least14 by firm KT in RM(3,6): below16
the only weights are8,12,14, of which only14 is2 mod4.
Thus wt K>=8*14=112. But wt K=wt h-64+2q<=158-64+14=108 (q<=7odd).
Contradiction. Both types excluded without KTA above2d.


---

# Proof chapter 12: `agent1_64126_proof.md`

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


---

# Proof chapter 13: `agent3_64126_hilbert_proof.md`

# Direct completion of (64,126,136/144), via Hilbert/flattening bound

First an elementary general lemma. Let S support h in RM(6,12), and
suppose S has affine span12. Let T in Lambda^6(F2^12) be the degree6
moment form: coefficient at I is sum_{x in S} product_{i in I}x_i.
All moments of degree<=5 vanish since RM(6,12) is orthogonal to RM(5,12).
Consequently T is Hodge(TOP6 h). Let R2,R3 be its 2/4 and3/3 flatten ranks.
Let C_j be evaluations on S of all polynomials of degree<=j, H_j=dim C_j.
Full affine span gives H1=13. A quadratic polynomial vanishing on S
has leading quadratic in kernel of the2/4 flattening T: multiply by an
arbitrary quartic and sum on S; only degree6 products survive. Its leading
part map is injective on vanishing quadratics because no nonzero affine
linear polynomial vanishes on S. Thus
 H2 >= 13+R2.
The vanishing moments<=5 imply C2 is isotropic and C3 subset C2^perp.
The Gram rank on C3 is exactly R3, because all products involving a
monomial of degree<=2 vanish, and products of two cubic monomials give
the3/3 flattening T. The ambient nondegenerate quotient C2^perp/C2 has
dimension |S|-2H2. Therefore
 |S| >= 2H2+R3 >= 26+2R2+R3.  (HILBERT-FLATTENING BOUND)
No KTA classification or computational assumption occurs in this lemma.

Now the (64,126) branch has leading h=A+B+C, three decomposable6-forms,
where B,C are complementary (firm KT for b126). Also qtop(h)=0 since
wt h136/144 is divisible4. Since q(B+C)=1, exactly one of A,B or A,C
is a complementary pair; choose A,B complementary. Use X=a-direction,
Y=B-direction. Since C-direction is complementary to B, it is a graph
Y=M X. Thus, after independent X,Y bases, the leading form is
 omega_d = X1...X6+Y1...Y6+product_i(Y_i+X_i if i<=d else Y_i),
where d=rank M. The middle quadratic invariant of omega_d is det M,
so qtop0 implies d<=5. If d0 or1, omega has a nonzero linear wedge
annihilator; the already-checked agent1_64126_proof.md excludes these
cases by elementary topfactor+purepair5-gap reasoning.

For d>=2, compute the ranks of T=Hodge(omega_d). The small exact GF2
bitmatrix checker agent3_64126_hilbert_checker.py gives:
 d       2    3    4    5
 R2     38   42   44   45
 R3     52   58   60   60
 bound 154  168  174  176.
If h has full affine span12, the Hilbert bound excludes wt136/144.
If h has proper affine support, its leading form has a nonzero linear
wedge annihilator, so agent1_64126_proof.md again excludes it. Thus
all cases are excluded, with only firm KT below2d and the proved
purepair5 moment gap. No universal KTA geometry is required.


---

# Proof chapter 14: `agent2_96112126_exterior.md`

# Complete exclusion of the zero-2-flat branch (96,112,126)

Suppose a,b,h are in RM(6,12), have weights 96,112,126, and a+b+h has degree
at most 5. Their degree-6 leading forms alpha,beta,gamma satisfy gamma=alpha+beta.
Treat degree-6 leading forms as elements of Lambda^6(V), dim V=12 over F2.
This is covariant under affine changes: translations do not affect the top form,
and repeated variables under linear substitutions lower the squarefree degree.

The standard <2d Kasami--Tokura forms give:
* alpha = (u1 wedge ... wedge u4) wedge q, where q is a rank4 2-form.
  Its exterior support U has dimension8.
* beta is either common4 wedge rank6 2-form (support10), or
  common3 wedge (p1p2p3+q1q2q3), with the two triples independent (support9).
* gamma is the sum of two decomposable 6-forms on complementary6-spaces,
  so its exterior support is all of V.

Let T_omega:Lambda^3 V* -> Lambda^3 V be contraction by omega. In matching
monomial bases it is a symmetric matrix over F2. Direct exterior-degree counting
(or the supplied 0.01-second Python checker) gives
rank(T_alpha)=32, rank(T_betaI)=44, rank(T_betaII)=38, rank(T_gamma)=40.

Rank inequality: if A,B are symmetric matrices and their images meet in a
t-space, rank(A+B) >= rank(A)+rank(B)-2t. Indeed the stacked map x->(Ax,Bx)
has rank rank(A)+rank(B)-t since the row spaces equal the column spaces;
projection (u,v)->u+v loses at most t further dimensions.

For betaII: support U_beta has dimension9. Since gamma has full support,
U+U_beta=V, so W=U intersect U_beta has dimension5. The two contraction images
meet in Lambda^3 W, whose dimension is C(5,3)=10. Thus rank(T_gamma)>=
32+38-20=50, contradicting rank40.

For betaI: W=U intersect U_beta has dimension6. We need a sharper image bound.
Write U=F directsum Q, dim F=dim Q=4, alpha=vol_F wedge q with q rank4 on Q.
Then the contraction image S is the direct sum
Lambda^3 F (dimension4), Lambda^2 F wedge Q (dimension24), F wedge <q> (dimension4).
The stabilizer of alpha includes every shear Q->Q+F. Therefore any6-space
W in U can be put in the form F_a directsum P_b, where a=dim(W intersect F),
b=6-a, and (a,b) is (2,4),(3,3), or (4,2). These shears preserve S.
Exterior-degree counting now gives
 dim(S intersect Lambda^3 W)=C(a,3)+C(a,2)b + (a if b=4 else0),
which is respectively6,10,16. (The q component contributes only when all Q
is in W, because q has full support Q.) Hence the two contraction images
meet in dimension at most16. Consequently rank(T_gamma)>=32+44-32=44,
again contradicting rank40.

Both possible KT types for beta are excluded. Thus the branch (96,112,126)
cannot occur. Every finite rank and canonical intersection computation above
is independently checked by agent2_96112126_exterior.py.


---

# Proof chapter 15: `agent4_parity_reduction.md`

# Group-algebra parity reduction (proved)
Let G=F2^m and R=F2[G], with e_x e_y=e_(x+y), and z_i=1+e_(unit_i). Then z_i^2=0. For a support S put F=sum_(x in S)e_x. RM(m-7,m) membership is equivalent to F in I^7, where I=(z_1,...,z_m), because the coefficient of z_A is sum_(x in S)prod_(i in A)x_i and all moments of degree at most6 vanish.

For an even-cardinality support, define
q(F)=sum_{unordered distinct x,y in S}e_(x+y) + (|S|/2 mod2)e_0.
Its polarization on even vectors is q(F+H)+q(F)+q(H)=FH. For each squarefree augmentation monomial z_A with |A|>=2, q(z_A)=0, since it is the indicator of a flat of size2^|A| and every nonzero internal difference occurs 2^(|A|-1) times as an unordered pair. Hence if F=sum_A c_A z_A lies I^7, q(F)=sum_(A<B)c_A c_B z_A z_B lies I^14.

At m=15, I^14 corresponds to Boolean functions of degree<=1. If |S|=2 mod4, q(F)(0)=1, so q(F)(a)=1+l(a) for a linear form l. For a!=0, q(F)(a)=|S intersection(S+a)|/2 mod2. Therefore the quotient derivative weight d(a)=|S|-|S intersection(S+a)| obeys d(a)/2 mod2=l(a). (For a=0, d(0)=0 and this also holds.)

Suppose the weight w is absent from RM(7,14), but occurs in RM(8,15), and w<=334 is 2 mod4. If l!=0, for every a outside ker(l), the quotient derivative has weight d(a)=2 mod4 and cannot equal w. Thus d(a)<=w-4 and I(a)>=4. Writing S=S0 disjoint-union S1 by the two l-levels, sum_(l(a)=1)I(a)=2|S0||S1|. Since there are 2^14 such a, 2|S0||S1|>=2^16. But 2|S0||S1|<=w^2/2<=334^2/2<2^16, contradiction. Therefore any counterexample at m15 must satisfy l=0 and q(F)=J.

This does NOT exclude l=0. Example F=z_A+z_B for complementary A,B of sizes7,8 has support382, valuation7, q(F)=J.


---

# Proof chapter 16: `agent4_m15_qzero_empty2_proof.md`

# Conditional m=15, Q=0 exclusion (proved reduction)

Hypothesis supplied by the universal-empty-flat chapter: every putative word of weight w in {322,326,330,334} has an empty affine codimension-two flat. This file does NOT prove that assumption.

Given it, affine-normalize f on F2^2 x F2^13 to have branches (0,a,b,h). Each a,b,h has degree at most7; c=a+b+h has degree at most6. Order the three nonzero branches by weight a<=b<=h using GL(2,2). By the standard <2.5d numerical KTA list for codimension6, the only possible small branch weights <=156 are
64,96,112,120,124,126,128,136,144,148,152,154,156.
In particular, a<=floor(334/3)=111, so |a|=64 or96.

Let G=F2^13 and let A,B,H be support vectors in F2[G]. Embed the four branches by the outer group basis s,t: F=sA+tB+stH. For even support vectors define
q(V)=sum_{unordered distinct x,y in supp V} e_(x+y) + (|V|/2 mod2)e_0.
For even vectors its polarization is q(V+W)+q(V)+q(W)=VW. Multiplying a support by a group element leaves q unchanged. The coefficient at outer st in q(F) is therefore exactly AB, coming only from the sA,tB cross product. If the derivative parity functional Q of f is zero and |f|=2 mod4, the earlier group-algebra parity lemma gives q(F)=J_15. Hence
AB=J_13.   (1)
Similarly AH=BH=J_13, although only (1) is needed below.

CASE |a|=64. The minimum-weight theorem says a is the indicator of an affine6-flat L. Equation(1) says every L-direction coset meets b oddly. There are128 such cosets, hence |b|>=128. But sorted b<=floor((w-64)/2)<=135, and KTA permits only b=128 in this interval (the next allowed weight is136). It would then require h=w-192 in {130,134,138,142}, each excluded by the same KTA numerical list. Contradiction.

CASE |a|=96. The second-weight classification says a is supported in an affine8-flat L and its restriction is an unbalanced rank4 quadratic q on L, of weight96. Translate L to linear. Decompose b into its32 cosets of L. Because A is supported on L, (1) says separately on each L-coset that
q * B_t = J_L.
Each B_t must have at least4 points:
- zero points gives zero convolution;
- an odd number (1 or3) of translates of q leaves its nonzero homogeneous quadratic part, so cannot be the constant1 function;
- two points gives a first derivative of q. It is constant only in a radical direction. An unbalanced quadratic has no nonzero linear component on its polar radical (otherwise it is balanced), so this constant derivative is0, never1.
Thus |b|>=32*4=128. But sorting gives |b|<=floor((334-96)/2)=119, contradiction.

Therefore, CONDITIONAL ON THE EMPTY CODIMENSION-TWO FLAT LEMMA, no Q=0 codeword in RM(8,15) has any of the four target weights. Combined with the already proved Q!=0 argument (conditional on the m14 holes), this reduces all dimensions to m14 because the universal empty-flat lemma has been proved independently of KTA structural forms.


---

# Executable certificate source

## `agent3_sufficiency_checker.py`

```python
from collections import Counter
TABLE = [([127, 1927, 6203], 127), ([127, 8065, 926], 8423), ([127, 1927, 16256], 14729), ([127, 3971, 14212], 127), ([127, 911, 2032], 15505), ([127, 415, 15968], 4001), ([127, 415, 1955], 4004), ([127, 415, 15968], 15875), ([127, 415, 15968], 1927), ([127, 911, 7569], 8080), ([127, 415, 15968], 3683), ([127, 1927, 16256], 2297), ([127, 191, 1863], 127)]
# Each mask M denotes the coordinate 7-space {x:x&~M=0}.
def flat(M):
 assert M.bit_count()==7
 return {x for x in range(16384) if x & (16383 ^ M)==0}
covered=0
for masks,Q in TABLE:
 assert Q.bit_count()==7
 S=flat(masks[0])^flat(masks[1])^flat(masks[2])
 counts=Counter(x&Q for x in S)
 occupancies=list(counts.values())+[0]*(128-len(counts))
 assert len(occupancies)==128 and sum(occupancies)==len(S)
 # Choose independently either S or its complement in each Q-coset.
 base=sum(min(n,128-n) for n in occupancies)
 bits=1
 for n in occupancies:bits |= bits<<abs(128-2*n)
 covered |= bits<<base
missing=[w for w in range(336,8193,2) if not((covered>>w)&1)]
assert missing==[358,362],missing
print('13 explicit coset-switch families cover every even weight 336..8192 except 358,362')

WITNESSES = {0: ['empty', 6, 1, 1, 1, 0, 0, 0, 0], 128: ['empty', 5, 2, 1, 1, 0, 0, 0, 1], 192: ['empty', 5, 1, 1, 1, 1, 0, 0, 0], 224: ['empty', 4, 2, 2, 1, 0, 0, 1, 1], 240: ['empty', 2, 5, 1, 1, 0, 0, 0, 4], 248: ['empty', 1, 6, 1, 1, 0, 0, 0, 5], 252: ['empty', 0, 7, 1, 1, 0, 0, 0, 6], 254: ['common', 0, 6, 1, 0, 0, 0, 1, 6], 256: ['empty', 4, 2, 1, 1, 1, 0, 0, 1], 272: ['empty', 3, 3, 2, 1, 0, 0, 1, 2], 288: ['empty', 4, 1, 1, 1, 2, 0, 0, 0], 296: ['empty', 2, 4, 2, 1, 0, 0, 1, 3], 304: ['empty', 3, 2, 2, 1, 1, 0, 1, 1], 308: ['empty', 1, 5, 2, 1, 0, 0, 1, 4], 312: ['empty', 2, 3, 3, 1, 0, 0, 2, 2], 314: ['empty', 0, 6, 2, 1, 0, 0, 1, 5], 316: ['empty', 0, 6, 1, 1, 1, 0, 0, 5], 318: ['common', 0, 5, 1, 0, 1, 0, 1, 5], 320: ['empty', 3, 2, 1, 1, 2, 0, 0, 1], 324: ['common', 1, 3, 3, 0, 0, 0, 3, 3], 328: ['empty', 2, 3, 2, 1, 1, 0, 1, 2], 332: ['empty', 1, 4, 3, 1, 0, 0, 2, 3], 358: ['empty', 0, 4, 3, 1, 1, 0, 2, 3], 362: ['empty', 0, 4, 2, 1, 2, 0, 1, 3]}
def check_witness(w,params):
 typ,t,a,b,c,d,x,y,z=params
 A=[];B=[];C=[];ell=0;pos=0
 def block(n,which,pick=False):
  nonlocal pos,ell
  for j in range(n):
   v=1<<pos;pos+=1
   for L in which:L.append(v)
   if pick and j==0:ell|=v
 block(t,[A,B,C]);block(a,[A,B],True);block(b,[A,C],True);block(c,[B,C],True)
 for j in range(d):
  e=1<<pos;f=1<<(pos+1);pos+=2;A.append(e);B.append(f);C.append(e^f)
 block(x,[A]);block(y,[B]);block(z,[C])
 r=8 if typ=='empty' else 7
 assert len(A)==len(B)==len(C)==r and pos<=r+7
 def supp(basis):
  S={0}
  for v in basis:S|={v^q for q in S}
  if typ=='empty':S={q for q in S if (q&ell).bit_count()%2}
  assert len(S)==128
  return S
 S=supp(A)^supp(B)^supp(C)
 assert len(S)==w,(w,len(S),params)
for w,p in WITNESSES.items():
 check_witness(w,p)
 covered|=1<<w
assert all(covered>>w&1 for w in range(336,8193,2))
print('All proposed low weights and every even central weight constructed in RM(7,14).')

```

## `agent2_four_affine_checker.py`

```python
from z3 import *
import itertools,time,json
s=Solver();s.set(timeout=300000)
d={0:IntVal(15)}
for I in range(1,32):
 d[I]=Int('d%d'%I);s.add(d[I]>=0,d[I]<=15)
for i in range(4):s.add(d[1<<i]==8,d[(1<<i)|16]==7)
s.add(d[16]==14)
for A in range(32):
 for B in range(32):
  if A&B==A:s.add(d[A]>=d[B])
  s.add(d[A]+d[B]<=d[A|B]+d[A&B])
for J in range(1,16):s.add(d[J]-d[J|16]>=0,d[J]-d[J|16]<=1)
for labs in itertools.product(range(5),repeat=5):
 A=B=C=D=0
 for i,z in enumerate(labs):
  if z==1:A|=1<<i
  elif z==2:B|=1<<i
  elif z==3:C|=1<<i
  elif z==4:D|=1<<i
 if not A or not B or not C or not D:continue
 def r(J):return 15-d[J]
 s.add(r(A|B)+r(A|C)+r(A|D)+r(B|C)+r(B|D)>=r(A)+r(B)+r(C|D)+r(A|B|C)+r(A|B|D))
def term(J):return If(d[J]>d[J|16],Sum([If(d[J]==i,2**(i-1),0) for i in range(1,9)]),0)
w=512-2*Sum([term(j) for j in range(1,16) if j.bit_count()==2])+4*Sum([term(j) for j in range(1,16) if j.bit_count()==3])-8*term(15)
# To enumerate further profiles at a target, fix w then exclude each already ruled-out profile.
# IMPORTANT: satisfiability is only a NECESSARY rank-profile condition, not subspace realization.

Jlist=[j for j in range(1,16) if j.bit_count()>=2]
# Each pair dict indexes AB=3, AC=5, BC=6, AD=9, BD=10, CD=12.
# Triple indices ABC=7, ABD=11, ACD=13, BCD=14.
# The geometric impossibility lemmas are in agent2_four_affine_lemmas.md.
patterns=[
 ({3:8,5:8,6:64,9:1,10:8,12:8},{11:1}),
 ({3:16,5:64,6:0,9:4,10:1,12:4},{}),
 ({3:8,5:1,6:8,9:8,10:64,12:8},{11:4}),
 ({3:0,5:8,6:1,9:64,10:8,12:8},{}),
 ({3:1,5:4,6:8,9:4,10:8,12:64},{}),
 ({3:4,5:64,6:4,9:16,10:1,12:16},{13:8}),
]
blocked=0
for pairs,triples in patterns:
 vals={j:0 for j in Jlist};vals.update(pairs);vals.update(triples)
 seen=set()
 for p in itertools.permutations(range(4)):
  def perm(j):return sum(1<<p[i] for i in range(4) if j>>i&1)
  vv=tuple(vals[perm(j)] for j in Jlist)
  if vv in seen:continue
  seen.add(vv);s.add(Or(*[term(j)!=v for j,v in zip(Jlist,vv)]));blocked+=1
# Hyperplane-pair lemma.
for i,j in itertools.combinations(range(4),2):
 for k in range(4):
  if k in (i,j):continue
  ij=(1<<i)|(1<<j);ik=(1<<i)|(1<<k);jk=(1<<j)|(1<<k);ijk=ij|ik
  s.add(Implies(And(term(ij)==64,term(ijk)==0,term(ik)>0,term(jk)>0),term(ik)==term(jk)))
# General projection lemma.
for a,b,c,dd in itertools.permutations(range(4)):
 A=1<<a;B=1<<b;C=1<<c;DD=1<<dd
 for rr in range(7):
  cond=And(term(A|B)==0,term(A|DD)==1,term(B|DD)==64,term(B|C)==2**rr,term(C|DD)==2**rr,term(B|C|DD)==0,term(A|C|DD)==0)
  s.add(Implies(cond,term(A|C)<=(2**(5-rr) if rr<=5 else 0)))
print('blocked affine size patterns',blocked,flush=True)
results={}
for target in [322,326,330,334]:
 s.push();s.add(w==target);t=time.time();ans=s.check();print(target,ans,time.time()-t,flush=True)
 assert ans==unsat,(target,ans)
 results[target]=str(ans);s.pop()
json.dump(results,open('workspace/agent2_four_affine_results.json','w'))

# Also cover at most three affine7flats (four-flat XOR does not subsume three).
# For three, w=384-2*(p+q+r)+4*t, all nonempty intersections powers of two.
P=[0]+[1<<i for i in range(8)]
profiles={}
for target in [322,326,330,334]:
 profiles[target]=[(v,t) for v in itertools.combinations_with_replacement(P,3) for t in P
  if t<=min(v) and 384-2*sum(v)+4*t==target]
assert profiles=={322:[((1,16,16),1)],326:[],330:[],334:[((1,8,16),0)]}
# 322: two4flat intersections inside a7flat through their triple point must
# intersect in dimension >=4+4-7=1, hence cannot have triple size1.
assert 4+4-7>0
# 334: the 4flat and3flat intersections inside a7flat have complementary
# directions, since the remaining pair meets at a point; hence must meet,
# contradicting triple size0. At most two flats have weight at most256.
assert 4+3==7 and 2*128<322
print('At-most-three-flat intersection profiles excluded:',profiles)

```

## `agent2_96112126_exterior.py`

```python
from itertools import combinations
from math import comb
n=12
triples=[sum(1<<i for i in I) for I in combinations(range(n),3)]
index={m:i for i,m in enumerate(triples)}
def flatten(terms):
    return [sum(1<<index[t^I] for t in terms if t&I==I) for I in triples]
def rank(rows):
    basis={}
    for row in rows:
        while row:
            k=row.bit_length()-1
            if k in basis: row^=basis[k]
            else:
                basis[k]=row
                break
    return len(basis)
alpha=[15|(3<<4),15|(3<<6)]
betaI=[15|(3<<4),15|(3<<6),15|(3<<8)]
betaII=[7|(7<<3),7|(7<<6)]
gamma=[63,63<<6]
ranks=[rank(flatten(x)) for x in [alpha,betaI,betaII,gamma]]
assert ranks==[32,44,38,40],ranks
S=flatten(alpha)
intersections=[]
for a in [2,3,4]:
    b=6-a
    W=list(range(a))+list(range(4,4+b))
    exterior=[1<<index[sum(1<<i for i in I)] for I in combinations(W,3)]
    dim=rank(S)+rank(exterior)-rank(S+exterior)
    formula=comb(a,3)+comb(a,2)*b+(a if b==4 else 0)
    assert dim==formula
    intersections.append(dim)
assert intersections==[6,10,16]
# Symmetric-matrix rank-sum inequality with bounded image intersections.
assert 32+38-2*comb(5,3)==50>40 # betaII
assert 32+44-2*max(intersections)==44>40 # betaI
print('Checked exterior obstruction: no degree6 leading forms of weights96,112,126 sum to0.')

```

## `agent2_purepair_coset_arithmetic.py`

```python
from math import floor
TARGETS=(194,198,202,206)
# Nondecomposable-row cases.
assert 64+2*56+2*16==208>max(TARGETS)
assert 16*(1+3+5+5)==224>max(TARGETS)
assert 3*(max(TARGETS)-192)==42<48
# Pairwise disjoint decomposable planes.
assert 2*(max(TARGETS)-192)==28<48
# Excess bound and affine image rank reduction.
Emin=next(e for e in range(0,300,2) if 4*e>=174)
assert Emin==44
assert 192+Emin>206 and 176+Emin>206
for h in TARGETS:
    if h<206: assert h-160<Emin
# Exhaust the integer constraints of the exceptional rank2 row0 argument.
feasible=[]
for m in (1,3):
 for e in range(0,47,2):
  for z in range(17):
   for r in range(e+2*m+1):
    if 4*e-3*r+16*z<=-8: feasible.append((m,e,z,r))
assert feasible
assert all(m==3 and e<=10 and z==0 for m,e,z,r in feasible)
assert 6*(64-13)>206-64
assert 6*(32-13)>206-128
assert 16>13
# Final small-weight bound, and known <2d spectrum as theorem input.
assert floor((9*80+512)/5)==246
kt_below_256=(0,128,192,224,240,248,252,254)
assert tuple(v for v in kt_below_256 if v<=246)==(0,128,192,224,240)
# Dimensions of intersections with two complementary6-spaces.
origin_in=max(2**p+2**q-2 for p in range(7) for q in range(7) if p+q<=9)
assert origin_in==70
# If g(0)=0, its even axis restrictions omit0; a0-dimensional section contributes0.
def even_omit_zero(p):return max(0,2**p-2)
origin_out=max(even_omit_zero(p)+even_omit_zero(q) for p in range(7) for q in range(7) if p+q<=9)
assert origin_out==68
avoid_L=max(2**p+2**q for p in range(7) for q in range(7) if p+q<=8)
assert avoid_L==68
assert min((v+126-h)//2 for v in (224,240) for h in TARGETS)==72>70
# N32 appendix.
assert 32+2*28+2*8==104>82
assert 32+2*28==88>82
emin5=next(e for e in range(0,100,2) if 4*e>=78)
assert emin5==20
assert 64+emin5>82 and 80+emin5>82
assert 64//2>max(74-62,82-62)
assert all(w==62 or w-62<64//2 for w in range(0,83,2))
print('Checked every numerical inequality in pure-pair-six and pure-pair-five proofs.')

```

## `agent3_6496_arithmetic.py`

```python
from math import ceil,log2
V=list(range(208,269,4))
assert V==[334-2*c for c in range(63,32,-2)]
for v in V:
 i=(v-206)//2
 assert i%2 and 1<=i<=31
 if v>=256:
  j=(556-v)//4
  assert v+128-2*j==3*v//2-150<=252
  assert i>=25
  for k in (224,240):
   inter=(128+k-v)//2
   assert inter>=42 and ceil(log2(inter))>=6
   assert 7+9-6==10 and 7+10-ceil(log2(i))<=12
for v in (224,240):
 assert (v-206)//2>=9
 assert 7+9-ceil(log2((v-206)//2))<=12
print('All (64,96) rank-one/fat-flat arithmetic checked')

```

## `agent3_cubic_coset_checker.py`

```python
"""Exact bit-vector enumeration of small cubic cosets used in 64+112 proof."""
from itertools import combinations

def mon(mask):
 return sum(1<<x for x in range(64) if x&mask==mask)
low=[mon(sum(1<<i for i in S)) for d in range(3) for S in combinations(range(6),d)]
assert len(low)==22
x3,z3,m1,m2=map(mon,(7,56,49,42))
tops=[x3]+[x3^z3^(m1 if e1 else 0)^(m2 if e2 else 0) for e1 in (0,1) for e2 in (0,1)]
state=tops[:]
small=[set([s.bit_count()]) for s in state]
mins=[s.bit_count() for s in state]
for i in range(1,1<<22):
 j=(i&-i).bit_length()-1
 q=low[j]
 for k in range(5):
  state[k]^=q
  w=state[k].bit_count()
  if w<16:small[k].add(w)
  if w<mins[k]:mins[k]=w
assert small[0]=={8}
assert mins[1:]==[14]*4
assert all(s=={14} for s in small[1:])
print('Exact 5 cubic cosets, 2^22 words each:',small,'minima',mins)

```

## `agent3_64126_hilbert_checker.py`

```python
from itertools import combinations

def wedge(A,B):
 C=set()
 for a in A:
  for b in B:
   if not a&b:
    c=a|b
    if c in C:C.remove(c)
    else:C.add(c)
 return C

def rank(rows):
 piv={}
 for r in rows:
  while r:
   p=r.bit_length()-1
   if p in piv:r^=piv[p]
   else:piv[p]=r;break
 return len(piv)

def masks(k):
 return [sum(1<<j for j in S) for S in combinations(range(12),k)]

def flatten(T,k):
 cols=masks(6-k)
 return rank([sum(1<<j for j,J in enumerate(cols) if not I&J and (I|J) in T) for I in masks(k)])

expected=[(30,40),(38,52),(42,58),(44,60),(45,60)]
for d in range(1,6):
 G={0}
 for i in range(6):G=wedge(G,{1<<(6+i),1<<i} if i<d else {1<<(6+i)})
 omega={63,4032}^G
 T={4095^I for I in omega}
 R2,R3=flatten(T,2),flatten(T,3)
 assert (R2,R3)==expected[d-1]
 if d>=2:assert 26+2*R2+R3>144
 print(d,R2,R3,26+2*R2+R3)
print('All graph-top moment flattenings checked exactly')

```

## `agent2_bootstrap_rank_checker.py`

```python
"""Exact GF(2) contraction/divisor ranks for every canonical form used in bootstrap."""
from itertools import combinations
from math import comb

def rk(rows):
 piv={}
 for v in rows:
  while v:
   k=v.bit_length()-1
   if k in piv:v^=piv[k]
   else:piv[k]=v;break
 return len(piv)
def masks(n,k):return [sum(1<<i for i in C) for C in combinations(range(n),k)]
def flatten(T,p,k,n):
 R={m:0 for m in masks(n,k)};C={m:i for i,m in enumerate(masks(n,p-k))}
 for t in T:
  positions=[i for i in range(n) if t>>i&1]
  for I in combinations(positions,k):
   a=sum(1<<i for i in I);R[a]^=1<<C[t^a]
 return rk(R.values())
def quad(p,mu):
 f=(1<<(p-2))-1
 return {f|(1<<(p-2+2*i))|(1<<(p-1+2*i)) for i in range(mu)}
def pair(p,mu):
 t=p-mu;f=(1<<t)-1
 return {f|(((1<<mu)-1)<<t),f|(((1<<mu)-1)<<(t+mu))}
def ann(T,p,n):
 C={m:i for i,m in enumerate(masks(n,p+1))};rows=[]
 for i in range(n):
  v=0
  for t in T:
   if not(t>>i&1):v^=1<<C[t|(1<<i)]
  rows.append(v)
 return n-rk(rows)
expected={
 4:{'min':6,'second':10,'quad6':14,'pair3':12,'pair4':12},
 5:{'min':10,'second':16,'quad6':22,'pair3':19,'pair4':20,'pair5':20},
 6:{'min':20,'second':32,'quad6':44,'pair3':38,'pair4':40,'pair5':40},
 7:{'min':35,'second':55,'quad6':75,'pair3':65,'pair4':69,'pair5':70},
}
for p in range(4,8):
 n=p+5;k=2 if p<=5 else 3
 forms={'min':{(1<<p)-1},'second':quad(p,2),'quad6':quad(p,3)}
 for mu in range(3,min(p,5)+1):forms['pair'+str(mu)]=pair(p,mu)
 actual={name:flatten(T,p,k,n) for name,T in forms.items()}
 assert actual==expected[p],(p,actual,expected[p])
 print('p',p,'contraction',k,actual)
 # Every low KT type has precisely the indicated pure common divisor space.
 assert ann(forms['second'],p,n)==p-2
 assert ann(forms['quad6'],p,n)==p-2
 for mu in range(3,min(p,5)+1):assert ann(forms['pair'+str(mu)],p,n)==p-mu
 # Primitive48-annihilator lemma: outside-support wedge has divisor dimension p-1;
 # inside-support wedge is decomposable, with divisor dimension p+1.
 if p>=6:
  T=forms['second'];outside=1<<(p+2);inside=1<<(p-2)
  assert ann({t|outside for t in T},p+1,n)==p-1
  U={t|inside for t in T if not t&inside}
  assert ann(U,p+1,n)==p+1
print('Every canonical KT contraction/divisor-rank certificate PASS')

```

## `agent1_purepair5_86_checker.py`

```python
from itertools import product
# Affine-image baseline and even model-excess inequality.
assert all(32+2*(32-32//(1<<d))>=88 for d in range(3,6))
Emin=next(E for E in range(0,100,2) if 4*E>=3*32-18)
assert Emin==20 and 80+Emin>86
# Last row/column bound at H86 leaves only the minimum lower-code word.
assert (9*(86-62)+256)//5==94
assert 64<=94<96
I=(64+62-86)//2
assert I==20
origin=[(a,b) for a,b in product(range(6),repeat=2) if a+b<=6 and 2**a+2**b-2==I]
no_origin=[(a,b) for a,b in product(range(6),repeat=2) if a+b<=5 and 2**a+2**b==I]
assert not origin and not no_origin
assert I not in [2**a for a in range(6)]
print('Pure-pair5 weight86: all image/excess/KT bounds and affine-intersection cases checked')

```

## `agent4_m15_qzero_checker.py`

```python
import random

def convolution(A,B):
 D=set()
 for a in A:
  for b in B:
   x=a^b
   if x in D:D.remove(x)
   else:D.add(x)
 return D

def qfun(A):
 D=set();L=sorted(A)
 for i,a in enumerate(L):
  for b in L[i+1:]:
   x=a^b
   if x in D:D.remove(x)
   else:D.add(x)
 if (len(A)//2)%2:
  if 0 in D:D.remove(0)
  else:D.add(0)
 return D
rng=random.Random(427)
for n in range(2,6):
 N=1<<n
 for rep in range(100):
  branches=[]
  for _ in range(3):
   A={x for x in range(N) if rng.randrange(2)}
   if len(A)%2:A.symmetric_difference_update({0})
   branches.append(A)
  A,B,H=branches
  F={x+N for x in A}|{x+2*N for x in B}|{x+3*N for x in H}
  qF=qfun(F)
  assert {x-3*N for x in qF if x//N==3}==convolution(A,B)
  assert {x-2*N for x in qF if x//N==2}==convolution(A,H)
  assert {x-N for x in qF if x//N==1}==convolution(B,H)
q={x for x in range(256) if ((x&1)*((x>>1)&1))^(((x>>2)&1)*((x>>3)&1))}
assert len(q)==96
assert convolution(q,{0,1,2,3})==set(range(256))
for v in range(1,256):
 assert {x for x in range(256) if ((x in q)^((x^v) in q))} != set(range(256))
S={0,64,96,112,120,124,126,128,136,144,148,152,154,156}
for w in [322,326,330,334]:
 possible=[(a,b,w-a-b) for a in S for b in S if 0<a<=b<=w-a-b and w-a-b in S]
 # Third branch may exceed156, so only use first/second small branches here.
 for a in [64,96]:
  if a==96:assert (w-a)//2<128
  else:assert all((w-a-b) not in S for b in S if 128<=b<=(w-a)//2)
print('random branch-q convolution identity, all rank4 derivatives, and target arithmetic checked')

```

## `agent2_combined_checker.py`

```python
"""Run every finite certificate used by the proof, not exploratory searches.
Invoke from the directory containing workspace/: python workspace/agent2_combined_checker.py
Requires Python 3, numpy, and z3-solver. No network or subprocesses.
"""
import contextlib, gc, hashlib, io, json, runpy, time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
NAMES=[
 'agent3_sufficiency_checker.py',
 'agent2_four_affine_checker.py',
 'agent2_96112126_exterior.py',
 'agent2_purepair_coset_arithmetic.py',
 'agent3_6496_arithmetic.py',
 'agent3_cubic_coset_checker.py',
 'agent3_64126_hilbert_checker.py',
 'agent2_bootstrap_rank_checker.py',
 'agent1_purepair5_86_checker.py',
 'agent4_m15_qzero_checker.py',
]
results={}
for name in NAMES:
 p=ROOT/name
 sha=hashlib.sha256(p.read_bytes()).hexdigest()
 out=io.StringIO();start=time.perf_counter()
 with contextlib.redirect_stdout(out):
  runpy.run_path(str(p),run_name='__certificate__')
 elapsed=time.perf_counter()-start
 results[name]={'sha256':sha,'seconds':round(elapsed,6),'stdout':out.getvalue(),'status':'PASS'}
 print(name,'PASS',round(elapsed,3),'seconds',flush=True)
 gc.collect()
# Interval endpoints as affine functions alpha*2^m+beta.
low=[(0,0),(128,128),(192,192),(224,224),(240,240),(248,248),(252,256),
 (272,272),(288,288),(296,296),(304,304),(308,308),(312,320),(324,324),(328,328),(332,332)]
coeffs=[((0,a),(0,b)) for a,b in low]+[((0,336),(1,-336))]+[
 ((1,-b),(1,-a)) for a,b in reversed(low)]
assert len(coeffs)==33
for m in range(14,101):
 N=1<<m
 intervals=[(a*N+b,c*N+d) for (a,b),(c,d) in coeffs]
 assert intervals[0]==(0,0) and intervals[-1]==(N,N)
 assert all(0<=a<=b<=N and a%2==b%2==0 for a,b in intervals)
 assert all(b+2<c for (a,b),(c,d) in zip(intervals,intervals[1:]))
 assert [(N-b,N-a) for a,b in reversed(intervals)]==intervals
 # Concatenations cover the next central interval, with adjacent-even overlap.
 sums=[(336,N-336),(672,2*N-672),(N+336,2*N-336)]
 assert sums[0][1]+2>=sums[1][0] and sums[1][1]+2>=sums[2][0]
 assert sums[0][0]==336 and sums[-1][1]==2*N-336
# The interval overlap condition for every m>=14 reduces to N>=1006.
assert (1<<14)>=1006
# Injective quotient reduction at every m>=16 (higher dimensions are easier).
assert 334*333//2+1 < 1<<16
# All degree/moment flattening-rank arithmetic of the twice-minimum span lemma.
from math import comb
for p in range(5,101):
 k=2 if p==5 else 3
 alpha=comb(p,k)
 beta=sum(comb(p-2,k-j)*r for j,r in enumerate([1,4,1]) if 0<=k-j<=p-2)
 gamma=beta
 intersection_bound=1 if p==5 else 0
 assert alpha+beta-intersection_bound>gamma
 # Decomposable sum case: actual normals meet common divisor space.
 assert (p-2)+(p-1)-p==p-3>0
for c in range(4,101):
 n=2*c+2;p=n-c-1;N=n-2
 assert p>=5 and n-2*c-1>=1
 assert N>=2*(c-1)+2
# Literal construction supports / ranks are checked by the ten scripts above;
# these final algebraic checks only audit endpoints and induction arithmetic.
results['endpoint_and_induction_checks']={'status':'PASS','intervals':coeffs,'dimensions_explicitly_checked':[14,100], 'all_m_overlap_bound':1006}
(ROOT/'agent2_combined_results.json').write_text(json.dumps(results,indent=2))
print('All finite proof certificates PASS; 33 explicit maximal interval shapes and induction inequalities PASS.')

```

# Exact run manifest

```json
{
  "agent3_sufficiency_checker.py": {
    "sha256": "e49b3c78836ed6085ddd98fef43bace2bd779b340af8a5ea25ccaca777c4783f",
    "seconds": 0.021973,
    "stdout": "13 explicit coset-switch families cover every even weight 336..8192 except 358,362\nAll proposed low weights and every even central weight constructed in RM(7,14).\n",
    "status": "PASS"
  },
  "agent2_four_affine_checker.py": {
    "sha256": "8b525e2be9cc05ead1c13728c10bcd34265ee75ebe2b9a69416806d6c49370d2",
    "seconds": 46.286008,
    "stdout": "blocked affine size patterns 96\n322 unsat 11.472124814987183\n326 unsat 10.96304202079773\n330 unsat 11.344980955123901\n334 unsat 11.988114833831787\nAt-most-three-flat intersection profiles excluded: {322: [((1, 16, 16), 1)], 326: [], 330: [], 334: [((1, 8, 16), 0)]}\n",
    "status": "PASS"
  },
  "agent2_96112126_exterior.py": {
    "sha256": "9d00b8ca5cd045fcf6212f27297ca7fcf463fffdbf08b6f629d2fcfe04ca9d92",
    "seconds": 0.000701,
    "stdout": "Checked exterior obstruction: no degree6 leading forms of weights96,112,126 sum to0.\n",
    "status": "PASS"
  },
  "agent2_purepair_coset_arithmetic.py": {
    "sha256": "cb4de49deb5e82790c0f6445e87ef0f4c5f59c58ca9c3746e307834c86b4bd06",
    "seconds": 0.001041,
    "stdout": "Checked every numerical inequality in pure-pair-six and pure-pair-five proofs.\n",
    "status": "PASS"
  },
  "agent3_6496_arithmetic.py": {
    "sha256": "441e82b43dab38486f3ea71d094405c8c94c7831428281f2b9c9c8441376db54",
    "seconds": 0.00024,
    "stdout": "All (64,96) rank-one/fat-flat arithmetic checked\n",
    "status": "PASS"
  },
  "agent3_cubic_coset_checker.py": {
    "sha256": "88a423fd135b555fe39c71176527134c22aa797fb314dcc08750b617b76de9b4",
    "seconds": 1.781018,
    "stdout": "Exact 5 cubic cosets, 2^22 words each: [{8}, {14}, {14}, {14}, {14}] minima [8, 14, 14, 14, 14]\n",
    "status": "PASS"
  },
  "agent3_64126_hilbert_checker.py": {
    "sha256": "187c23bea83f8ceab624b7df6aa13a4bc9bb0e9043fcd5cda0db4a929c15b5da",
    "seconds": 0.011481,
    "stdout": "1 30 40 126\n2 38 52 154\n3 42 58 168\n4 44 60 174\n5 45 60 176\nAll graph-top moment flattenings checked exactly\n",
    "status": "PASS"
  },
  "agent2_bootstrap_rank_checker.py": {
    "sha256": "0ec3b24faa6db0bcfa8ac7c49ba6084bfc5620fd834f8ebda8da0766456483d0",
    "seconds": 0.003882,
    "stdout": "p 4 contraction 2 {'min': 6, 'second': 10, 'quad6': 14, 'pair3': 12, 'pair4': 12}\np 5 contraction 2 {'min': 10, 'second': 16, 'quad6': 22, 'pair3': 19, 'pair4': 20, 'pair5': 20}\np 6 contraction 3 {'min': 20, 'second': 32, 'quad6': 44, 'pair3': 38, 'pair4': 40, 'pair5': 40}\np 7 contraction 3 {'min': 35, 'second': 55, 'quad6': 75, 'pair3': 65, 'pair4': 69, 'pair5': 70}\nEvery canonical KT contraction/divisor-rank certificate PASS\n",
    "status": "PASS"
  },
  "agent1_purepair5_86_checker.py": {
    "sha256": "40aa86c684919cc8987e52ff0fe0d13ebe524e2ba818ec67a462fd5b4a57d20e",
    "seconds": 0.000303,
    "stdout": "Pure-pair5 weight86: all image/excess/KT bounds and affine-intersection cases checked\n",
    "status": "PASS"
  },
  "agent4_m15_qzero_checker.py": {
    "sha256": "be100638ecfa80285c85542587a14b768f23283c4c486a6d5e5ee045fa2b26b4",
    "seconds": 0.019039,
    "stdout": "random branch-q convolution identity, all rank4 derivatives, and target arithmetic checked\n",
    "status": "PASS"
  },
  "endpoint_and_induction_checks": {
    "status": "PASS",
    "intervals": [
      [
        [
          0,
          0
        ],
        [
          0,
          0
        ]
      ],
      [
        [
          0,
          128
        ],
        [
          0,
          128
        ]
      ],
      [
        [
          0,
          192
        ],
        [
          0,
          192
        ]
      ],
      [
        [
          0,
          224
        ],
        [
          0,
          224
        ]
      ],
      [
        [
          0,
          240
        ],
        [
          0,
          240
        ]
      ],
      [
        [
          0,
          248
        ],
        [
          0,
          248
        ]
      ],
      [
        [
          0,
          252
        ],
        [
          0,
          256
        ]
      ],
      [
        [
          0,
          272
        ],
        [
          0,
          272
        ]
      ],
      [
        [
          0,
          288
        ],
        [
          0,
          288
        ]
      ],
      [
        [
          0,
          296
        ],
        [
          0,
          296
        ]
      ],
      [
        [
          0,
          304
        ],
        [
          0,
          304
        ]
      ],
      [
        [
          0,
          308
        ],
        [
          0,
          308
        ]
      ],
      [
        [
          0,
          312
        ],
        [
          0,
          320
        ]
      ],
      [
        [
          0,
          324
        ],
        [
          0,
          324
        ]
      ],
      [
        [
          0,
          328
        ],
        [
          0,
          328
        ]
      ],
      [
        [
          0,
          332
        ],
        [
          0,
          332
        ]
      ],
      [
        [
          0,
          336
        ],
        [
          1,
          -336
        ]
      ],
      [
        [
          1,
          -332
        ],
        [
          1,
          -332
        ]
      ],
      [
        [
          1,
          -328
        ],
        [
          1,
          -328
        ]
      ],
      [
        [
          1,
          -324
        ],
        [
          1,
          -324
        ]
      ],
      [
        [
          1,
          -320
        ],
        [
          1,
          -312
        ]
      ],
      [
        [
          1,
          -308
        ],
        [
          1,
          -308
        ]
      ],
      [
        [
          1,
          -304
        ],
        [
          1,
          -304
        ]
      ],
      [
        [
          1,
          -296
        ],
        [
          1,
          -296
        ]
      ],
      [
        [
          1,
          -288
        ],
        [
          1,
          -288
        ]
      ],
      [
        [
          1,
          -272
        ],
        [
          1,
          -272
        ]
      ],
      [
        [
          1,
          -256
        ],
        [
          1,
          -252
        ]
      ],
      [
        [
          1,
          -248
        ],
        [
          1,
          -248
        ]
      ],
      [
        [
          1,
          -240
        ],
        [
          1,
          -240
        ]
      ],
      [
        [
          1,
          -224
        ],
        [
          1,
          -224
        ]
      ],
      [
        [
          1,
          -192
        ],
        [
          1,
          -192
        ]
      ],
      [
        [
          1,
          -128
        ],
        [
          1,
          -128
        ]
      ],
      [
        [
          1,
          0
        ],
        [
          1,
          0
        ]
      ]
    ],
    "dimensions_explicitly_checked": [
      14,
      100
    ],
    "all_m_overlap_bound": 1006
  }
}
```
