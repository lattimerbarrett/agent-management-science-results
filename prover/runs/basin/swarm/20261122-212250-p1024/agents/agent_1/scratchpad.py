from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
import sympy as sp

# Exact Laurent algebra: pairs (P,Q) mean P(t)+Q(t)*h(t),
# where h^2=1-t^(4g+2). No series truncation is used.
def pa(a,b,c=1):
    z=a.copy()
    for i,v in b.items():
        z[i]=z.get(i,0)+c*v
        if not z[i]: del z[i]
    return z

def pm(a,b):
    z={}
    for i,v in a.items():
        for j,w in b.items(): z[i+j]=z.get(i+j,0)+v*w
    return {i:v for i,v in z.items() if v}

def add(a,b,c=1): return pa(a[0],b[0],c),pa(a[1],b[1],c)
def sc(a,c): return tuple({i:v*c for i,v in p.items() if v*c} for p in a)
def sh(a,n): return tuple({i+n:v for i,v in p.items()} for p in a)
def mon(n,c=1): return ({n:Q(c)} if c else {},{})
def mul(a,b):
    q=pm(a[1],b[1])
    return pa(pa(pm(a[0],b[0]),q),{i+H:v for i,v in q.items()},-1),pa(pm(a[0],b[1]),pm(a[1],b[0]))

@lru_cache(None)
def hc(n):
    return Q(1) if n==0 else hc(n-1)*Q(2*n-3,2*n)

def coeff(a,n):
    return a[0].get(n,0)+sum(v*hc((n-i)//H) for i,v in a[1].items() if n>=i and (n-i)%H==0)

def af(s):
    return mon(-s) if s%2==0 else ({},{-s:Q(1)})

def split(a,lam):
    # Returns eta,w with a = f + eta + t^(-lam)w,
    # f in A and w in C[[t]].
    a=(a[0].copy(),a[1].copy()); eta={}
    for n in range(min([0]+list(a[0])+list(a[1])),-lam):
        c=coeff(a,n)
        if not c: continue
        s=-n
        if (s>=0 and s%2==0) or s>=2*g+1:
            a=add(a,sc(af(s),c),-1)
        else:
            eta[n]=c
            a=add(a,mon(n,c),-1)
    w=sh(a,lam)
    # Check formal regularity, including cancellations between P and Qh.
    for n in range(min([0]+list(w[0])+list(w[1])),0):
        assert coeff(w,n)==0
    return eta,w

def rank(cols):
    piv={}
    for c in cols:
        c={i:Q(v) for i,v in c.items() if v}
        while c:
            i=min(c); v=c[i]
            if i in piv: c=pa(c,piv[i],-v)
            else:
                piv[i]={j:w/v for j,w in c.items()}; break
    return len(piv)

def cech(gg,b,kind):
    global g,H
    g=gg; H=4*g+2; d=2*g-2; k=g-(g+2)//3; M=2*d+1
    phi=({-(2*g-1-2*j):Q(v) for j,v in enumerate(b) if v},{})
    phip=({e-1:e*v for e,v in phi[0].items()},{})
    kp=sc(phi,k); powers=[mon(0)]
    for a in range((M-1)//k): powers.append(mul(powers[-1],kp))
    def power(alpha,a):
        c=Q(1)
        for j in range(a): c*=Q(alpha-j,j+1)
        return sc(powers[a],c)
    inds=[(n,c) for n in range(M) for c in ('h','v')] if kind=='S' else [(n,kind) for n in range(M)]
    lam=[n-d if c in ('h','L') else n for n,c in inds]
    R=[{} for _ in inds]
    for j,(n,c) in enumerate(inds):
        alpha=-Q(n,k)
        for a in range((M-1-n)//k+1):
            m=n+a*k
            if kind!='S':
                R[j][m]=sh(power(alpha+(kind=='L'),a),-n+(d if kind=='L' else 0))
            elif c=='v':
                R[j][2*m+1]=sh(power(alpha+1,a),-n)
            else:
                R[j][2*m]=sh(power(alpha,a),d-n)
                v=sh(power(alpha,a),-n-1)
                if a: v=add(v,sh(mul(power(alpha,a-1),add(sh(kp,-1),phip)),-n))
                R[j][2*m+1]=sc(mul(v,({}, {0:Q(1)})),-Q(1,2))
    rows={}; h0=[]
    for i,l in enumerate(lam):
        exps=[-s for s in range(1,2*g,2) if s>l]+list(range(1,max(1,-l)))
        for e in exps: rows[i,e]=len(rows)
        for s in range(max(-1,l)+1):
            if s%2==0 or s>=2*g+1: h0.append((i,s))
    cols=[]
    for j,s in h0:
        w=sh(af(s),lam[j])
        v={i:mul(p,w) for i,p in R[j].items() if i!=j}; col={}
        for i in range(j+1,len(inds)):
            if i not in v: continue
            eta,w=split(v[i],lam[i])
            for e,c in eta.items(): col[rows[i,e]]=c
            for ell,p in R[i].items():
                if ell!=i: v[ell]=add(v.get(ell,({},{})),mul(p,w),-1)
        cols.append(col)
    return len(rows)-rank(cols),rank(cols)

def checks():
    # Symbolically check the inverse fiber transition and its derivatives.
    t,u,k,F,Fp=sp.symbols('t u k F Fp',nonzero=True)
    # e_W=(1+kFu^k)e_U; dt|v(u)/u is the following expression.
    B=1+k*F*u**k
    logv_t=-1/t-Fp*u**k/B
    logv_e=1/B
    inv_e=sp.simplify(-logv_t/logv_e)
    assert sp.simplify(inv_e-(1/t+(k*F/t+Fp)*u**k))==0
    assert sp.simplify(logv_e*B)==1
    # Uniform symbolic pivot minors for every rectangular Hankel shape tested.
    for m in range(6):
        bs=sp.symbols('b:'+str(m+1))
        for a in range(1,m+5):
            for q in range(1,m+5):
                if max(a,q)<m+1: continue
                s=min(a,q,m+1)
                start=m-s+1
                mat=sp.Matrix(s,s,lambda i,j: bs[start+i+j] if start+i+j<=m else 0)
                assert sp.expand(mat.det(method='domain-ge')-(-1)**(s*(s-1)//2)*bs[m]**s)==0
    # Check the integer inequalities and the closed rank sum over a wide range.
    for g in range(2,101):
        r=(g+2)//3; k=g-r; d=2*g-2; N=d-k
        assert d<=3*k and N>=4*(r-1)
        for m in range(r):
            aa=[min(n//2+1,(N-n)//2+1,m+1) for n in range(N+1)]
            assert sum(aa[1:])==(m+1)*(g+r-1-2*m)-1
            assert aa[k]==m+1
    # Independent full-transition, exact-rational Cech computations.
    count=0
    for gg in range(2,13):
        r=(gg+2)//3
        vectors=list(product((-1,0,1),repeat=r)) if r<=3 else []
        vectors += [tuple(int(i==j) for i in range(r)) for j in range(r)]
        vectors += [tuple(Q((-2)**i,i+1) for i in range(r))]
        for b in vectors:
            if not any(b): continue
            m=max(i for i,v in enumerate(b) if v)
            R=(m+1)*(gg+r-1-2*m)-1
            vals=[cech(gg,b,c) for c in ('O','S','L')]
            expected=[(gg*gg-R,R),(6*gg*gg-7*gg+2-2*R+m,2*R+1-m),(5*gg*gg-7*gg+2-R,R+1)]
            assert vals==expected,(gg,b,vals,expected)
            assert vals[0][0]-vals[1][0]+vals[2][0]==-m
            count+=1
    print('All exact checks passed;',count,'full-transition examples.')

if __name__=='__main__': checks()
