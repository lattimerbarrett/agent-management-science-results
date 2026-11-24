"""Exact algebraic check and diagnostics for the proved elliptic Schur Pfaffian."""
import sympy as sp
import mpmath as mp
from itertools import product
from random import Random

def exact_four_point():
    x=sp.symbols("x0:4");y=sp.symbols("y0:4");q,t=sp.symbols("q t")
    den=lambda i,j:1+x[i]*x[j]
    dy=lambda i,j:y[j]-y[i]
    pairs=[(i,j) for i in range(4) for j in range(i+1,4)]
    V=sp.prod(dy(i,j) for i,j in pairs)
    Pfnum=sp.expand(sum(sign*dy(a,b)*dy(c,d)*sp.prod(den(i,j) for i,j in pairs if (i,j) not in [(a,b),(c,d)]) for sign,a,b,c,d in [(1,0,1,2,3),(-1,0,2,1,3),(1,0,3,1,2)]))
    P=sp.Poly(sp.expand(q*q*sp.prod(y)*Pfnum-sp.prod(x)*V),*y)
    reductions=[]
    for i in range(4):
        a=q*(x[i]-1/x[i])-t
        # y_i^2=a_i*y_i+1 on the curve.
        reductions.append([[1,0],[0,1],[1,a],[a,1+a*a]])
    out={}
    for powers,coef in P.terms():
        for bits in product([0,1],repeat=4):
            term=coef
            for i in range(4):term*=reductions[i][powers[i]][bits[i]]
            if term!=0:out[bits]=out.get(bits,0)+term
    assert all(sp.factor(expr)==0 for expr in out.values())
    return {"formal_curve_parameters":2,"remainder_coefficients_checked":len(out)}

def pf(A):
    if len(A)==0:return mp.mpf(1)
    return sum((-1)**(j+1)*A[0][j]*pf([[A[k][l] for l in range(1,len(A)) if l!=j] for k in range(1,len(A)) if k!=j]) for j in range(1,len(A)))

def numerical_check(cases=50,dps=150):
    mp.mp.dps=dps;rng=Random(512);worst=mp.mpf(0)
    for trial in range(cases):
        n=rng.randint(1,5);c=mp.mpf(str(rng.uniform(.03,.97)));q=mp.mpf(str(rng.uniform(.02,.98)))
        xs=sorted(mp.exp(mp.mpf(str(rng.uniform(-4,4)))) for _ in range(2*n))
        def flow(x):
            a=q*((x-c)*(1+c*x)/x)-(1-c*c)
            return (a+mp.sqrt(a*a+4*c*c))/(2*c)
        ys=[flow(x) for x in xs]
        K=[[mp.mpf(0) if i==j else (ys[j]-ys[i])/(1+xs[i]*xs[j]) for j in range(2*n)] for i in range(2*n)]
        actual=pf(K)
        predicted=q**(-n*(n-1))*mp.fprod((xs[i]/ys[i])**(n-1) for i in range(2*n))*mp.fprod(K[i][j] for i in range(2*n) for j in range(i+1,2*n))
        assert actual>0 and predicted>0
        error=abs((actual-predicted)/predicted);worst=max(worst,error)
        assert error<mp.mpf(10)**(-dps//2)
    return {"cases":cases,"dps":dps,"worst_relative_error":mp.nstr(worst,20)}

if __name__=="__main__":print(exact_four_point(),numerical_check())
