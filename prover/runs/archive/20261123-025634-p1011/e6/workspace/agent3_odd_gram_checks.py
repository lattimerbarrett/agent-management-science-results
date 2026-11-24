"""Rigorous rational-interval checks of restricted odd-dimensional jet matrices.
This checks algebraic matrices only, NOT Yamabe compactness.
No floating-point operation is used for any assertion.
"""
from fractions import Fraction as F
from math import factorial, comb
import sympy as sp
from functools import lru_cache

SCALE=10**80

def atan_interval(m,N=65):
    total=sum((F((-1)**j,(2*j+1)*m**(2*j+1)) for j in range(N)), F(0))
    nxt=F((-1)**N,(2*N+1)*m**(2*N+1))
    return min(total,total+nxt),max(total,total+nxt)
# Machin identity: tan(4 atan(1/5)-atan(1/239))=1,
# and the angle lies in (0,1), within the principal tangent interval.
tan2=2*F(1,5)/(1-F(1,5)**2)
tan4=2*tan2/(1-tan2**2)
assert (tan4-F(1,239))/(1+tan4*F(1,239))==1
assert 4*(F(1,5)-F(1,3*5**3))-F(1,239)>0
assert 4*F(1,5)<1
a,b=atan_interval(5); c,d=atan_interval(239)
PI=(16*a-4*d,16*b-4*c)
assert PI[0]>3 and PI[1]<F(22,7)

def floor_scaled(x): return x.numerator*SCALE//x.denominator
def ceil_scaled(x): return -((-x.numerator*SCALE)//x.denominator)

def factors(n,q,s,t):
    a=(n-3)//2+q
    num=[(1,q+1)]*2+[(1,q+n+1),(1,q+n),(2,2*a+5),(1,2*a+1),(1,2*a+2),(1,s),(1,s+1),(1,t),(1,t+1)]
    den=[(1,q-1),(1,q+n-1),(1,q+n-1),(1,q),(2,2*a+1),(1,1),(1,2),(1,2*a-s+2),(1,2*a-s+3),(1,2*a-t+2),(1,2*a-t+3)]
    return num,den

def ev(factors,k):
    out=1
    for a,b in factors:out*=a*k+b
    return out

def product_shifted(factors,K):
    co=[1]
    for a,b in factors:
        nxt=[0]*(len(co)+1)
        for j,c in enumerate(co):nxt[j]+=c*(a*K+b); nxt[j+1]+=c*a
        co=nxt
    return co

def certify_tail_ratio(n,q,s,t,K):
    a=(n-3)//2+q
    p=2*a-2*s-2*t
    assert p>=2
    e=2*p-1
    num,den=factors(n,q,s,t)
    # D(k)^2*k^e - N(k)^2*(k+2)^e >= 0 for all k>=K.
    left=product_shifted(den*2+[(1,0)]*e,K)
    right=product_shifted(num*2+[(1,2)]*e,K)
    cs=[x-y for x,y in zip(left,right)]
    assert all(c>=0 for c in cs) and any(c>0 for c in cs), (n,q,s,t,K)
    return p

@lru_cache(None)
def initial(n,q,s,t,k):
    a=(n-3)//2+q; l=k+q
    def integ(s):
        return F(2**(2*a-s+1)*factorial(s+k-1)*factorial(a+k)*factorial(a-s),factorial(s-1)*factorial(k)*factorial(2*a+k-s+1))
    h=F(2**(2*a+1)*factorial(k+a)**2,(2*k+2*a+1)*factorial(k)*factorial(k+2*a))
    D=sp.simplify(2*sp.gamma(sp.Rational(l,2))*sp.gamma(sp.Rational(l+n+1,2))/(sp.gamma(sp.Rational(l-1,2))*sp.gamma(sp.Rational(l+n,2))))
    lam=(l-1)*(l+n-1)
    z=sp.simplify(sp.Rational(lam**2)*sp.Rational(integ(s))*sp.Rational(integ(t))/sp.Rational(h)/D)
    if sp.simplify(z/sp.pi).is_Rational:
        r=F(sp.simplify(z/sp.pi)); lo,hi=r*PI[0],r*PI[1]
    else:
        assert sp.simplify(z*sp.pi).is_Rational,z
        r=F(sp.simplify(z*sp.pi)); lo,hi=r/PI[1],r/PI[0]
    assert lo>0
    return floor_scaled(lo),ceil_scaled(hi)

@lru_cache(None)
def base_interval(n,q,s,t,N):
    if s>t:return base_interval(n,q,t,s,N)
    lo_total=hi_total=0
    kstart=max(0,2-q)
    for k0 in (kstart,kstart+1):
        lo,hi=initial(n,q,s,t,k0)
        numf,denf=factors(n,q,s,t)
        k=k0
        for j in range(N):
            lo_total+=lo; hi_total+=hi
            num,den=ev(numf,k),ev(denf,k)
            assert num>0 and den>0
            lo=lo*num//den
            hi=(hi*num+den-1)//den
            k+=2
        p=certify_tail_ratio(n,q,s,t,k)
        # Bound the entire remaining parity tail including its first term.
        hi_total+=(hi*(2*p-3+k)+(2*p-4))//(2*p-3)
    return F(lo_total,SCALE),F(hi_total,SCALE)


def plus(x,y):return x[0]+y[0],x[1]+y[1]
def neg(x):return -x[1],-x[0]
def times(x,y):
    ps=[a*b for a in x for b in y]
    return min(ps),max(ps)
def reciprocal(x):
    assert x[0]>0
    return 1/x[1],1/x[0]
def point(x):return F(x),F(x)
def coefficients(q,i):
    return {q-1+j:comb(i,j)*2**j*(-1)**(i-j) for j in range(i+1) if q-1+j>0}

def check(n,q,N=5000):
    maxd=(n-1)//2
    imin=max(0,2-q); imax=(maxd-q)//2
    if imax<imin:return None
    ids=list(range(imin,imax+1)); size=len(ids)
    mat=[]
    for i in ids:
        row=[]
        for j in ids:
            val=point(0)
            for s,ci in coefficients(q,i).items():
                for t,cj in coefficients(q,j).items():
                    val=plus(val,times(point(ci*cj),base_interval(n,q,s,t,N)))
            row.append(times(point(q-1+i+j),val))
        mat.append(row)
    # Interval LDL/Schur elimination is a rigorous sufficient positivity test.
    pivots=[]
    for k in range(size):
        pivot=mat[k][k]
        assert pivot[0]>0,(n,q,k,'insufficient interval',float(pivot[0]),float(pivot[1]))
        pivots.append(pivot)
        inv=reciprocal(pivot)
        for i in range(k+1,size):
            for j in range(k+1,size):
                mat[i][j]=plus(mat[i][j],neg(times(times(mat[i][k],mat[k][j]),inv)))
    return size,[(float(l),float(h)) for l,h in pivots]

if __name__=='__main__':
    lines=[]
    for n in range(3,18,2):
        for q in range((n-1)//2+1):
            r=check(n,q)
            if r is not None:
                line=f'n={n}, angular degree={q}: positive restricted matrix dim={r[0]}, pivot brackets={r[1]}'
                print(line,flush=True);lines.append(line)
    from pathlib import Path
    Path('workspace/agent3_odd_gram_results.txt').write_text('\n'.join(lines)+'\n')
