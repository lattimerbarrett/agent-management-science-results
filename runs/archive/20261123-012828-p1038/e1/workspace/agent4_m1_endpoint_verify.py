"""Exact independent endpoint positivity for m1, k2.
Only this finite subcase is proved here, not general k.
"""
import sympy as s
from itertools import product

def check():
    x0,x1,u0,u1,v0,v1,c,T,a,b=s.symbols('x0 x1 u0 u1 v0 v1 c T a b')
    ps=[(1-x0*T)*(1-u0*T),T*(1-x1*T)*(1-u1*T),
        (1-c*T)*(T+x0)*(T+x1),(T+c)*(T+v0)*(T+v1)]
    M=s.Matrix([[s.expand(p).coeff(T,j) for j in range(4)] for p in ps])
    D=s.expand(M.det());count=0;coefficients=0
    for bits in product([0,1],repeat=4):
        sub={u0:c if bits[0] else x0,u1:c if bits[1] else x1,
             v0:c if bits[2] else x0,v1:c if bits[3] else x1}
        P=D.subs(sub,simultaneous=True)
        for gaps in [{x1:x0+a,c:x0+a+b},
                     {x1:x0+a+b,c:x0+a},
                     {x0:c+a,x1:c+a+b}]:
            po=s.Poly(s.expand(P.subs(gaps,simultaneous=True)))
            assert all(cf>=0 for cf in po.coeffs())
            assert po.TC()>0
            count+=1;coefficients+=len(po.terms())
    return dict(polynomials=count,coefficients=coefficients)
if __name__=='__main__':print(check())
