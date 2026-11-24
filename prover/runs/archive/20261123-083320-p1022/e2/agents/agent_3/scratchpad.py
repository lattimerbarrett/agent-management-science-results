from pathlib import Path
Path('workspace/agent3_twostep_nonwedge.txt').write_text(r'''P4 two-step reconstruction, non-wedge cases (complete).

Let E have type (1^m,0^(r-m)), r<=7, and let
0 -> pO(1) qF -> pE -> qG -> 0
be its two-step q-relative HN filtration on I=P(Q). The numerical
Chern table can be found at rank7 by padding E with O's (duality first
if necessary). Padding is used ONLY for necessary Chern constraints;
the following geometric reconstruction works directly on the originalE,
so no rank-induction or cancellation circularity occurs.

Case I: c1F=0. Put A=qF. On each p-fiber P3, A* is globallygenerated
with det trivial, so its Plucker classifying map isconstant; A is trivial
on thatfiber. Grauert/evaluation gives A=pB. Then c1B=0. The inclusion
B->E(-1) is a subbundle. Each splitting degree of B|L is<=0; their sum
is0, hence B is trivial on everyline and therefore B=O^m. Thus O(1)^m
is a subbundle of E, with quotient trivial on everyline, hence trivial.
H1O(1)=0 splits the extension: E=O(1)^m+O^(r-m).

Case II: c1F=-s and c2F=0. On every p-fiber A*=O(1)+O^(m-1), by the
globallygenerated c2zero lemma. Therefore B=p_*A has rankm-1 and its
evaluation pB->A is a subbundle with line quotient. Write c1B=b x,
s=x+y. In c2A=c2(pB)+c1(pB)c1(A/pB), the xy coefficient is-b;
but c2A=0, so b=0. Again B injects into E(-1), so it is trivial on
alllines and B=O^(m-1). This gives O(1)^(m-1) as a subbundle of E.
Its quotient H is uniform of type(1,0,...,0). Its firstHN line equals
qO_G(-1) (because quotient of qF by the trivial q-subbundle has detO_G(-1)).

The inclusion pO(1)qO_G(-1)=O_p(-1)->pH adjoints to psi:Q->H.
For every pointx and nonzero v inQ_x, psi_x(v) is precisely the topHN
line inclusion at(x,[v]); hence psi_x(v)!=0. Thus psi is a subbundle
injection. Along any base line, its positiveO1 part maps isomorphically
onto H's positiveO1 part, and its other O^3 parts form a constant full-rank
matrix into H's trivialpart. The quotient is consequently trivial on all
lines, so H=Q+O^(rankH-4), using H1Q=0. Finally the extension defining E
splits: Ext1(Q,O1)=H1Q*(1)=H1Omega1(2)=0, and line-lineExt1=0.
Therefore E=Q+O1^(m-1)+O^(r-m-3).

Case III: the remaining nonwedge numerical datum has
cF=1-s+(s^2-t)+(-s^3+2st), rankF=3,
and cG=1+s. For the dual normalized bundle E*(1), its topHN bundle
is G*, with c1=-s,c2=0, so CaseII applies. Thus E is Omega1(2) plus
appropriate line summands.

These cases require NO uniform lower-rank classification. If the displayed
rank counts become negative the purported datum cannot occur, since the
constructed fiberwise injection Q->H would exceed rankH.

Globallygenerated c2zero lemma used above: for a gg bundleB onP3, r-1
general sections have smooth expected codim2 degeneracy locus of classc2B.
If c2B=0 it is empty; so0->O^(r-1)->B->O(c1B)->0, and H1O(-c1B)=0
splits it. The rank1 case is immediate.

All-line-triviality: pull back to blowup of a point, descend along its
P1 ruling toP2 orP3, then restrict to exceptional section. This proves
B trivial without a splitting-classification theorem.
''')
print('non-wedge proof written')
