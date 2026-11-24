import sympy as S, json, ast
from pathlib import Path
n,j,D=S.symbols('n j D')
Qs=[S.sympify(q,locals={'n':n,'j':j}) for q in json.loads(Path('workspace/agent3_telescopers.json').read_text())]
def radial_polynomial(ss,kk,nn):
    aa=S.Rational(nn+1,2); out=0
    if ss in [2,3]:
        for mm in range(kk+1):
            pp=S.prod(D+r*(nn-r) for r in range(mm))
            den=S.factorial(mm+(ss==3))*S.prod(aa-r for r in range(1,mm+1))
            out+=(-1)**(kk-mm)*S.binomial(kk,mm)*pp/den
    elif ss==1:
        for mm in range(1,kk+1):
            pp=S.prod(D+(r+1)*(nn-1-r) for r in range(mm-1))
            den=S.factorial(mm-1)*S.prod(S.Rational(nn-1,2)-r for r in range(1,mm))
            out+=2*(-1)**(kk-mm)*S.binomial(kk,mm)*pp/den
    return S.expand(out)
def exact_grams(nn,KK=3):
    MM=[]
    for Q in Qs:
        Q=Q.subs(n,nn)
        MM.append((nn-1)**2*Q.subs(j,0)*S.pi/4/S.gamma(S.Rational(nn+1,2))**2+nn**2*Q.subs(j,1)/S.gamma(S.Rational(nn+2,2))**2)
    def moment(poly):
        pp=S.Poly(S.expand(poly),D)
        return S.factor(sum(coeff*MM[power[0]] for power,coeff in pp.terms()))
    GG={}
    for ss in [1,2,3]:
        rr=[radial_polynomial(ss,k,nn) for k in range(KK+1)]
        # only k<=KK-1 needed for angular3 in translations: top entry would require degree7.
        if ss==3:rr=rr[:-1]
        fac={1:D/S.Integer(nn-1)**2,2:S.Integer(1),3:D-(nn+1)}[ss]
        GG[ss]=S.Matrix([[moment(fac*r*t) for t in rr] for r in rr])
    return GG
if __name__=='__main__':
    import numpy as np
    tree=ast.parse(Path('workspace/agent4_hemisphere_dn_checks.py').read_text())
    gramnode=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='gram')
    ns={'np':np};exec(compile(ast.Module(body=[gramnode],type_ignores=[]),'gram','exec'),ns)
    for nn in [19,20,21]:
        GG=exact_grams(nn)
        for ss in [1,2,3]:
            exact=np.array((GG[ss]/GG[2][0,0]).evalf(20)).astype(float)
            numer=ns['gram'](nn,ss)
            numer=numer[:len(exact),:len(exact)]/ns['gram'](nn,2)[0,0]
            error=np.max(np.abs((exact-numer)/np.maximum(1,np.abs(exact))))
            assert error<2e-8,(nn,ss,error)
            print('Cross-angular exact moments check n,s,error=',nn,ss,error)
    Path('workspace/agent4_exact_angular_gram.py').write_text(Path(__file__).read_text())
