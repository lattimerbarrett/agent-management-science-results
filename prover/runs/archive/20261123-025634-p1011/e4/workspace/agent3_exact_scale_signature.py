"""Exact finite-dimensional spectral-shape scale-sign checks.
This is NOT a compactness/noncompactness proof for the nonlinear PDE.
"""
import sympy as S
import json, math
from pathlib import Path
j,n,D,x=S.symbols('j n D x')
Qs=[S.sympify(q,locals={'j':j,'n':n}) for q in json.loads(Path('workspace/agent3_telescopers.json').read_text())]

def make_gram(dim):
    # Scale all moments by pi^2/R0; positive and common across entries.
    # Odd dimensions: R1/R0=constant/pi^2, exact gamma identities.
    assert dim%2==1
    const=S.simplify(4*S.pi*S.gamma(S.Rational(dim+1,2))**2/S.gamma(S.Rational(dim+2,2))**2)
    assert const.is_Rational
    M=[]
    for Q in Qs:
        M.append(S.expand((dim-1)**2*Q.subs({n:dim,j:0})*x+dim**2*Q.subs({n:dim,j:1})*const))
    r=[]
    for k in range(4):
        rk=0
        for a in range(k+1):
            prod=S.prod(D+(s-1)*(dim+1-s) for s in range(1,a+1))
            denom=S.factorial(a)*S.prod(S.Rational(dim-1,2)-s for s in range(a))
            rk+=(-1)**(k-a)*S.binomial(k,a)*prod/denom
        r.append(S.expand(rk))
    G=S.zeros(4)
    for k in range(4):
        for l in range(4):
            p=S.Poly(r[k]*r[l],D)
            G[k,l]=sum(c*M[mon[0]] for mon,c in p.terms())
    return G

# Rational bounds from the first 50 correct decimal digits of pi.
# These bounds may alternatively be established by the Machin-formula check below.
lo=S.Rational('3.14159265358979323846264338327950288419716939937510')
hi=lo+S.Rational(1,10**50)

def atan_interval(inv,N):
    # Alternating-series rational enclosure of atan(1/inv).
    total=sum((-1)**k*S.Rational(1,(2*k+1)*inv**(2*k+1)) for k in range(N))
    nxt=(-1)**N*S.Rational(1,(2*N+1)*inv**(2*N+1))
    return min(total,total+nxt),max(total,total+nxt)
a,b=atan_interval(5,40); c,d=atan_interval(239,12)
# Machin: pi=16 atan(1/5)-4 atan(1/239), with elementary tangent identity.
assert S.expand(S.im((1+S.I/S.Integer(5))**4*(1-S.I/S.Integer(239)))) == S.expand(S.re((1+S.I/S.Integer(5))**4*(1-S.I/S.Integer(239))))
plo,phi=16*a-4*d,16*b-4*c
assert lo<plo<phi<hi
xlo,xhi=lo**2,hi**2

def interval_poly(poly):
    lower=0; upper=0
    for (k,),coef in S.Poly(poly,x).terms():
        if coef>=0:
            lower+=coef*xlo**k; upper+=coef*xhi**k
        else:
            lower+=coef*xhi**k; upper+=coef*xlo**k
    return lower,upper

if __name__=='__main__':
    G=make_gram(19)
    H=S.Matrix(4,4,lambda k,l:(2*k+2*l+2)*G[k,l])
    signs=[]
    for k in range(1,5):
        det=S.factor(H[:k,:k].det())
        low,up=interval_poly(det)
        sign=1 if low>0 else (-1 if up<0 else 0)
        assert sign!=0
        signs.append(sign)
        print('n19 scale leading minor',k,'exact sign',sign)
    assert signs==[1,1,1,-1]
    print('Exact LDL signature: 3 positive, 1 negative; no truncation or floating-point evidence used.')
    Path('workspace/agent3_n19_scaled_gram.json').write_text(json.dumps([[str(v) for v in G.row(k)] for k in range(4)]))
