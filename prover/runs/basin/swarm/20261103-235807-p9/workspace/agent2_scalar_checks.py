"""Checked scalar lower-bound infrastructure; not the sharp matrix lower bound."""
import math
import mpmath as mp
import sympy as sp

def check_algebra():
    p,e=sp.symbols('p e', positive=True)
    alpha=(p-1)*(1-e)
    assert sp.simplify(p*(-1+e)+alpha-(-1+e))==0
    q=p/(p-1)
    b=lambda t:1+1/(t*(t-1))
    assert sp.simplify(b(q)/(p-1)-b(p))==0
    return True

def scalar_Ap_endpoint(p,e,kind):
    # Exact scalar Ap expression for interval (0,1), weight |x|^alpha.
    a=-1+e if kind=='negative' else (p-1)*(1-e)
    return 1/((a+1)*(1-a/(p-1))**(p-1))

def lower_ratios(p,e):
    # f=1_(0,1), w=|x|^(-1+e): integrate exact H on 0<x<1/4.
    # t=-log x resolves the endpoint singularity.
    out1=mp.quad(lambda u: mp.e**(-u)*(u/e+mp.log(1-mp.e**(-u/e)))**p,
                 [e*mp.log(4),1,mp.inf])/(mp.pi**p*e)
    ratio1=(out1/(1/e))**(1/p)
    # f=x^(-1+e)1_(0,1), positive-endpoint weight:
    # kernel pointwise estimate yields exact rigorous lower ratio.
    ratio2=1/(2*mp.pi*e)
    return float(ratio1),float(ratio2)

if __name__=='__main__':
    mp.mp.dps=30
    assert check_algebra()
    for p in (1.5,3.0,4.0):
        for e in (.1,.03,.01):
            r1,r2=lower_ratios(p,e)
            print('p=',p,'eps=',e,'Ap(-)=',scalar_Ap_endpoint(p,e,'negative'),
                  'Ap(+)=',scalar_Ap_endpoint(p,e,'positive'),
                  'eps*actual_lower_ratio(-)=',e*r1,
                  'eps*rigorous_lower_ratio(+)=',e*r2)
