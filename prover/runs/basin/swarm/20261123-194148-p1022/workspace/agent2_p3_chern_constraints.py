import sympy as s
from functools import lru_cache
x,y,t=s.symbols('x y t')

def schur(a,b):
    return sum(x**(a-i)*y**(b+i) for i in range(a-b+1))

def reduce_xy(p):
    p=s.Poly(s.expand(p),x,y)
    out=0
    for (a,b),coeff in p.terms():
        out+=coeff*redmon(a,b)
    return s.expand(out)
@lru_cache(None)
def redmon(a,b):
    if a>=4:return 0
    if b<3:return x**a*y**b
    return s.expand(-sum(redmon(a+i,b-i) for i in range(1,4)))

def constraints(ranks,weights=None):
    if weights is None:weights=list(range(len(ranks)))
    coeffs=[s.Integer(1)]
    vs=[]
    for i,(r,w) in enumerate(zip(ranks,weights)):
        C=[s.Integer(1)]
        for j in range(1,r+1):
            c=0
            for a in range(3):
                b=j-a
                if 0<=b<=a:
                    v=s.Symbol('c%d_%d%d'%(i,a,b));vs.append(v)
                    c+=v*schur(a,b)
            C.append(c)
        # substitute t+w*x in c polynomial
        D=[0]*(r+1)
        for j,c in enumerate(C):
            for k in range(r-j+1):
                D[j+k]+=s.binomial(r-j,k)*(w*x)**k*c
        new=[0]*(len(coeffs)+r)
        for j,a in enumerate(coeffs):
            for k,b in enumerate(D):
                new[j+k]+=a*b
        coeffs=[reduce_xy(c) for c in new]
    eq=[]
    for k,c in enumerate(coeffs):
        for (a,b),v in s.Poly(c,x,y).terms():
            if b>0 or k>3:
                if v!=0:eq.append(v)
    # eliminate all linear equations first
    sub={}
    while True:
        linear=None
        for e in eq:
            e=s.expand(e.subs(sub))
            if e==0:continue
            avail=[v for v in vs if v not in sub]
            if s.Poly(e,avail).total_degree()==1:
                linear=e;break
        if linear is None:break
        v=next(v for v in reversed(vs) if v not in sub and linear.coeff(v)!=0)
        sol=s.solve(linear,v)[0]
        sub[v]=sol
        eq=[s.expand(e.subs(v,sol)) for e in eq]
        eq=[e for e in eq if e!=0]
    avail=[v for v in vs if v not in sub]
    return eq,avail,sub
