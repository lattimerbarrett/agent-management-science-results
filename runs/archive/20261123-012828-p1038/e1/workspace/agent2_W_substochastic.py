"""Exact identities and high-precision checks for the proved W-kernel lemma."""
import sympy as sp
import mpmath as mp
from random import Random

def exact_check():
    r,R,x,y,z=sp.symbols("r R x y z",positive=True)
    d=(r*(x-1/x)-R*(y-1/y))/2
    K=d*d+r*r+R*R
    L=K-R*r*(z+1/z)
    A=d-r*x+R*x/z;B=d+R*y-r*y*z
    assert sp.factor(A-B-(x-y*z)*(R/z-r))==0
    assert sp.factor(z*(L-B*B)-r*(r*z-R)*(x-y*z)*(x*y*z+1)/x)==0
    # The x/y range follows this discriminant identity.
    u=sp.symbols("u",positive=True)
    assert sp.expand(d*d-(r*u-R)*(R-r/u)-(K-R*r*(u+1/u)))==0
    return True

def numeric_check(cases=100,dps=100):
    mp.mp.dps=dps;rng=Random(259);worst=mp.inf;maxrow=mp.mpf(0)
    for trial in range(cases):
        m=rng.randint(2,30);r=mp.exp(str(rng.uniform(-5,-.001)));R=mp.mpf(1)
        d=mp.exp(str(rng.uniform(-5,5)))
        # Any real axis height, allowing inside slab too.
        height=mp.mpf(str(rng.uniform(-4,5)))*max(1,d)
        x=(height+mp.sqrt(height*height+r*r))/r
        u=height-d;y=(u+mp.sqrt(u*u+R*R))/R
        kappa=mp.sqrt(r*y/(R*x));values=[]
        for k in range(m):
            z=mp.exp(2j*mp.pi*k/m)
            dist=mp.sqrt(d*d+abs(R*z-r)**2)
            c=(R/z-r)/(d+dist);b=z*c
            w=kappa*(1+x*c)/(1+y*b)
            assert abs(w)<1
            values.append(w)
        coeff=[]
        for j in range(m):
            v=sum(values[k]*mp.exp(-2j*mp.pi*k*j/m) for k in range(m))/m
            assert abs(mp.im(v))<mp.mpf(10)**(-dps+20)
            assert mp.re(v)>0
            coeff.append(mp.re(v));worst=min(worst,mp.re(v))
        row=sum(coeff);assert 0<row<1
        assert abs(row-values[0])<mp.mpf(10)**(-dps+20)
        maxrow=max(maxrow,row)
    return {"cases":cases,"dps":dps,"min_matrix_entry":mp.nstr(worst,20),"max_row_sum":mp.nstr(maxrow,20)}

if __name__=="__main__":print(exact_check(),numeric_check())
