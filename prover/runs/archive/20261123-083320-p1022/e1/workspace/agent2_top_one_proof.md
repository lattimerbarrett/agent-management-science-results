# Classification of uniform splitting type (1,0,...,0), all ranks

Let n>=2 and E be uniform of rank r on P^n, of splitting type (1,0^(r-1)). Let I=F(1,2;n+1), p:I->P^n, q:I->Gr(2,n+1). Write h=p*c1(O(1)), H=q*c1(O_Gr(1)). The relative splitting filtration is
0 -> O_I(h+bH) -> p*E -> q*W -> 0
for an integer b and a rank-(r-1) bundle W on Gr. The top line comes from relative evaluation, and the quotient has trivial splitting on every q-fiber, hence descends by cohomology/base change.

Put x=h, y=H-h. Rationally, A*(I)=Q[x,y]/(h_n(x,y),h_(n+1)(x,y)), where h_j(x,y)=sum_(i=0)^j x^i y^(j-i). The pullback of A*(Gr) is symmetric in x,y: indeed its Chern generators are H=x+y and c2(S*)=xy. Write c(E)=1+h+d2 h^2+d3 h^3+..., with terms beyond dimension zero. The exact sequence gives
c(q*W)=D(x)/(1+(b+1)x+b y).
This is symmetric, so
D(x)(1+b x+(b+1)y)-D(y)(1+(b+1)x+b y)=0.
The degree-two part is (d2+b)(x^2-y^2). It implies d2=-b for all n>=2, since the degree-two relation when n=2 is symmetric and cannot kill this antisymmetric polynomial.
The degree-three part is
(d3+b d2)(x^3-y^3)+(b+1)d2(x^2y-xy^2).
For n>=4 there are no degree-three relations, so (b+1)d2=0. For n=3 the only degree-three relation is symmetric, and the displayed polynomial is antisymmetric, so the same conclusion follows. For n=2, x^3=y^3=0 and x^2y=-xy^2!=0, again giving (b+1)d2=0. Thus b=0 or -1.

If b=0, the top line is p*O(1), so it descends to O(1) as a subbundle of E. The quotient is trivial on every line, hence trivial globally, and H^1(O(1))=0 splits the extension.

If b=-1, the top line is O(h-H), the tautological line of directions inside p*Q, where Q=T_Pn(-1). On every p-fiber P(Q_x), the inclusion O(-1)->E_x tensor O is a basepoint-free system of linear forms. Therefore the induced linear map Q_x->E_x is injective: its dual is surjective onto H^0(O(1)), since any proper subspace of linear forms has a common zero. These linear maps vary algebraically by adjunction, giving a subbundle Q->E. Equivalently, p_*O(H-h)=Q*.
On each line L, the top O_L(1) in Q|L maps isomorphically to the top O_L(1) in E|L, because both are precisely the relative top line at every (x,L). Thus the quotient restricts trivially to every line. It is globally trivial, and H^1(Q)=0 splits the extension. We obtain
E=Q plus O^(r-n).

Conclusion: E is O(1) plus O^(r-1), or Q plus O^(r-n), with the second case possible only for r>=n. Both are homogeneous. By dualizing and twisting, the same holds when the smaller splitting block has multiplicity one. Every algebraic polynomial step is checked in agent2_top_one_checks.py; its n-loop is a guard against errors, while the degree argument above proves all n.
