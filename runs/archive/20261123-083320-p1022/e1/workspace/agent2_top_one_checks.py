import sympy as s
from pathlib import Path
import json
x,y,b,d2,d3=s.symbols('x y b d2 d3')
D=lambda z:1+z+d2*z**2+d3*z**3
L=(b+1)*x+b*y
Ls=b*x+(b+1)*y
cross=s.Poly(s.expand(D(x)*(1+Ls)-D(y)*(1+L)),x,y)
def homogeneous(poly,k):
    return s.Add(*(coef*x**mon[0]*y**mon[1] for mon,coef in s.Poly(poly,x,y).terms() if sum(mon)==k))
cross2=homogeneous(cross.as_expr(),2)
cross3=homogeneous(cross.as_expr(),3)
assert s.expand(cross2-(d2+b)*(x*x-y*y))==0
assert s.expand(cross3-((d3+b*d2)*(x**3-y**3)+(b+1)*d2*(x*x*y-x*y*y)))==0
# All n>=4: relation degrees start at n, hence degrees2,3 are free.
# n=3: only degree3 relation is symmetric x^3+x^2y+xy^2+y^3;
# our degree3 polynomial is antisymmetric, so no nonzero multiple.
assert s.expand(cross3.xreplace({x:y,y:x})+cross3)==0
h3=x**3+x*x*y+x*y*y+y**3
assert s.expand(h3.xreplace({x:y,y:x})-h3)==0
# n=2: D degree2 only, since x^3=0 on P2. Groebner reduction
# shows degree3 vanishes only if (b+1)d2=0.
h2=x*x+x*y+y*y
G=s.groebner([h2,h3],x,y,domain=s.QQ.frac_field(b,d2,d3))
red3=G.reduce(cross3.subs(d3,0))[1]
assert s.expand(red3+2*d2*(b+1)*x*y*y)==0
# Combined with d2=-b, the only integral/complex b are 0 and -1.
assert s.solve((b+1)*(-b),b)==[-1,0]
# Explicit no-relation assertion for degrees2,3 checked by Groebner bases.
checks=[]
for n in range(2,16):
    hn=sum(x**i*y**(n-i) for i in range(n+1))
    hn1=sum(x**i*y**(n+1-i) for i in range(n+2))
    Gn=s.groebner([hn,hn1],x,y,domain=s.QQ.frac_field(b,d2,d3))
    r2=s.expand(Gn.reduce(cross2)[1])
    r3=s.expand(Gn.reduce(cross3)[1])
    equations=[v for v in s.Poly(r2,x,y).coeffs()+s.Poly(r3,x,y).coeffs() if v!=0]
    solutions=s.solve(equations,[b,d2,d3],dict=True)
    assert {sol[b] for sol in solutions}=={s.Integer(0),s.Integer(-1)}
    checks.append({'n':n,'solutions':[{str(k):str(v) for k,v in sol.items()} for sol in solutions]})
results={'degree2_cross':str(cross2),'degree3_cross':str(cross3),'n2_reduced_degree3':str(red3),'checks':checks}
Path('workspace').mkdir(exist_ok=True)
Path('workspace/agent2_top_one_checks.json').write_text(json.dumps(results,indent=2))
source=Path(__file__); target=Path('workspace/agent2_top_one_checks.py')
if source.resolve()!=target.resolve(): target.write_text(source.read_text())
print(json.dumps(results,indent=2))
proof=r'''# Classification of uniform splitting type (1,0,...,0), all ranks

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
'''
Path('workspace/agent2_top_one_proof.md').write_text(proof)
