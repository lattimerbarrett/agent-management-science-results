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
