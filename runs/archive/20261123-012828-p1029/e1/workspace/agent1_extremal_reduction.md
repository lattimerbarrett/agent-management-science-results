# Extremal positive-series reduction (conditional on existence of any bad positive series)

This is a reduction, NOT a proof of exclusion.

Let Lambda be the supremum of eta>0 for which some finite AW*-factor,
with its faithful normalized 2-quasitrace, contains b_i>=0 with finite
partial sums <=1 and q(b_i)=eta. Assume Lambda>0. The quasitracial
ultraproduct construction in agent3_qt_ultraproduct_notes.md attains Lambda.

For every integer L and epsilon>0, there is a length-L consecutive block
whose sum has q<=Lambda+epsilon. Otherwise infinitely many disjoint
length-L blocks have q>=Lambda+epsilon; their partial sums are still <=1,
and convex interpolation of the increasing partial sums gives a constant
increment >Lambda, contradiction. Take length-L blocks with errors ->0,
then a quasitracial ultraproduct as L->infinity. The resulting positive
sequence has q(sum over any finite nonempty interval)=Lambda.

If 0<=a<=S and q(a)=q(S), spectral dimension monotonicity gives
F_a(t)<=F_S(t); integrating gives equality of the distributions (first
almost everywhere, then everywhere by right continuity). Consequently all
b_i and all finite nonempty block sums have one spectral distribution F.
Their support projections agree: support(b_i)<=support(S), equal dimension,
and faithful dimension makes the difference zero. Their common support is
1, since restriction to a proper common support p would normalize q by
1/q(p) and increase Lambda. Their common norm is 1, since otherwise scalar
rescaling increases Lambda. Thus F(0+)=1, F(t)>0 for 0<t<1, F(1)=0.

For a=b_1, b=b_2, S=a+b, form
Q=[[a,sqrt(a)sqrt(b)],[sqrt(b)sqrt(a),b]], U=diag(1,-1).
Row-polar equivalence gives F_Q(t)=F_S(t)=F(t) for t>0. Also
Q+UQU*=2 diag(a,b), whose spectral dimension distribution is 2F(t/2).
Weyl's dimension inequality yields
  2 F((s+t)/2) <= F(s)+F(t), s,t>0.
Hence F is convex, F(t)<=1-t on [0,1], and Lambda=int_0^1 F(t)dt<=1/2.

This is NOT a contradiction: F(t)=(1-t)_+ satisfies all these scalar
constraints. No operator realization of that scalar model is asserted.
The missing step is an angle-sensitive or quasitracial structural theorem
excluding the extremal sequence; it is not established here.
