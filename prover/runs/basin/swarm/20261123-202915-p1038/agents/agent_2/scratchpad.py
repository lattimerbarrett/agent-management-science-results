import os
code=r'''"""Exact rational/algebraic certificates used by the uniform construction.
Run with Python. No numerical square-root comparisons are used.
"""
from fractions import Fraction as F
from math import comb
import sympy as s

def run():
    # R=100, alpha=epsilon=1/2, beta=(sqrt(160009)-3)/400,
    # delta=sqrt(5626)-75 =1/(sqrt(5626)+75).
    assert F(399)**2 < 160009 < F(403)**2 # .99 < beta <1
    assert 75**2 < 5626
    assert F(1,150) < F(7,1000) # 0<delta<1/150<.007
    blo=F(99,100);dhi=F(7,1000)
    assert dhi < blo*blo/2 # Chernoff tail condition delta<alpha*beta^2
    assert F(7,10)**2 < blo/2 # sqrt(beta*epsilon)>.7
    lower=F(3,2)*2*(1+F(7,10))**2
    upper=F(5,2)*(1+2*dhi)*(1+1/blo)*(1+F(1,2)/blo)
    assert lower==F(867,100)
    assert upper < 8 < lower
    # Verify the exact central coefficient identity as polynomial identities.
    T,b,e=s.symbols('T b e')
    for k in range(1,13):
        lhs=s.expand((T+b)**k*(1+e*T)**k).coeff(T,k)
        rhs=sum(comb(k,i)**2*(b*e)**i for i in range(k+1))
        assert s.expand(lhs-rhs)==0
    # Check the Cauchy-Schwarz identity, sum_{i<j}(v_i-v_j)^2
    # =(k+1)sum v_i^2-(sum v_i)^2, behind central coefficient bound.
    for k in range(1,9):
        vv=s.symbols('v:'+str(k+1))
        lhs=(k+1)*sum(v*v for v in vv)-sum(vv)**2
        rhs=sum((vv[i]-vv[j])**2 for i in range(k+1) for j in range(i+1,k+1))
        assert s.expand(lhs-rhs)==0
    # Exact transfer identity: h_l is the upper continuation of lower mode t.
    t,u,v=s.symbols('t u v')
    def h(j):return ((v-t)*u**j+(t-u)*v**j)/(v-u)
    assert s.simplify(h(0)-1)==0 and s.simplify(h(1)-t)==0
    for j in range(1,10):
        assert s.simplify(h(j+1)-(u+v)*h(j)+u*v*h(j-1))==0
        diff=-(t-u)*(t-v)*(v**(j-1)-u**(j-1))/(v-u)
        assert s.simplify(h(j)-t*h(j-1)-diff)==0
    print('All exact inequality, coefficient, Cauchy-Schwarz and transfer certificates passed.')

if __name__=='__main__':run()
'''
open('workspace/agent2_certificate.py','w').write(code)
exec(code)
