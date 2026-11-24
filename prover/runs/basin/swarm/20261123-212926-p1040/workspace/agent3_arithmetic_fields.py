"""Arithmetic data certificates for all-degree IA nonvanishing construction.
Checks exact integer polynomial/Eisenstein/unit/conductor identities;
it does not purport to reprove local class field theory computationally.
"""
import sympy as S
from sympy import Poly
X,Z=S.symbols('X Z')

def data(c):
    assert c>=3
    odds=[p for p in S.factorint(c) if p%2]
    if odds:p=int(min(odds));ell=p;r=c//p
    else:p=2;ell=4;r=c//4
    phi=Poly(S.cyclotomic_poly(ell,Z),Z);d=phi.degree()
    P=Poly(sum(int(coef)*(X+1-X**r)**j*(X+1)**(d-j)
               for (j,),coef in phi.terms()),X)
    e=r*d
    assert P.degree()==e
    assert P.LC()==1
    assert P.eval(0)==p and P.eval(-1)==1
    assert all(int(coef)%p==0 for coef in P.all_coeffs()[1:])
    assert int(P.eval(0))%(p*p)!=0
    assert e*p//(p-1)==c
    # Exact determinant/resultant norm of u=1+pi.
    assert S.resultant(P.as_expr(),X+1,X)==1
    # Base cyclotomic has no real roots; then neither does P, since
    # P(x)=(x+1)^d*Phi(1-x^r/(x+1))>0 off x=-1, and P(-1)=1.
    assert phi.count_roots(-S.oo,S.oo)==0
    return p,ell,r,e,P

if __name__=='__main__':
    for c in range(3,65):
        p,ell,r,e,P=data(c)
        if c<=12:print('c',c,'p',p,'ell',ell,'r',r,'e',e,'P',P.as_expr())
    print('ALL EXACT ARITHMETIC FIELD DATA CHECKS c3..64 PASSED')
