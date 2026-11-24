import sympy as s, numpy as np
from pathlib import Path
x,z=s.symbols('x z')
N=19; K=3; d=s.Rational(N-2,2); m=N-1; j=2*x-3
cache={}
def moment(poly):
    poly=s.Poly(s.expand(poly),x)
    if poly.is_zero:return s.Integer(0)
    key=tuple(poly.all_coeffs())
    if key in cache:return cache[key]
    rhs=s.Poly((2*x+d-1)*poly.as_expr(),x)
    deg=rhs.degree()-1; rem=rhs.as_expr();Q=0
    for mm in range(deg,-1,-1):
        op=s.Poly(x**mm*(x+d-1)**2-(x+1)**mm*x*x,x)
        co=s.Poly(rem,x).coeff_monomial(x**(mm+1))/op.coeff_monomial(x**(mm+1))
        Q+=co*x**mm;rem=s.expand(rem-co*op.as_expr())
    assert rem==0
    out=s.simplify(sum(Q.subs(x,X)*(s.gamma(X)/s.gamma(X+d-1))**2 for X in [s.Rational(3,2),s.Integer(2)]))
    cache[key]=out
    return out

def coeff_base(ell):
    return s.rf(j+1,ell)*s.rf(j+N+2-ell,ell)/(s.factorial(ell)*s.prod(N+1-2*rr for rr in range(1,ell+1)))
R2=[s.expand(sum(s.binomial(k,ell)*2**ell*(-1)**(k-ell)*coeff_base(ell) for ell in range(k+1))) for k in range(K+1)]
R3=[s.expand(sum(s.binomial(k,ell)*2**ell*(-1)**(k-ell)*coeff_base(ell)/(ell+1) for ell in range(k+1))) for k in range(K)]
R1=[s.Integer(0)]+[s.expand(sum(s.binomial(k,ell)*2**(ell-1)*(-1)**(k-ell)*s.rf(j+2,ell-1)*s.rf(j+N+2-ell,ell-1)/(s.factorial(ell-1)*s.prod(N-1-2*rr for rr in range(1,ell))) for ell in range(1,k+1))) for k in range(1,K+1)]
G2=s.Matrix(K+1,K+1,lambda k,l:moment(R2[k]*R2[l]))
G3=s.Matrix(K,K,lambda k,l:moment(j*(j+N+2)*R3[k]*R3[l]))
G1=s.Matrix(K+1,K+1,lambda k,l:moment(4*(j+1)*(j+N+1)*R1[k]*R1[l]/s.Integer(N-1)**2))
a=[s.Integer(1),-s.Rational(4628,10000),s.Rational(5655,100000),-s.Rational(1408,1000000)]
Q=s.expand(sum(a[k]*a[l]*z**(k+l+1)*G2[k,l] for k in range(K+1) for l in range(K+1))/G2[0,0])
Hs={}
roots=s.nroots(s.Poly(s.diff(Q,z).evalf(30),z),maxsteps=100)
print('Q derivative roots',roots)
for root in roots:
    if abs(s.im(root))<s.Rational(1,100000000) and s.re(root)>0:
        zz=float(s.re(root));print('root',zz,'Qsecond',s.N(s.diff(Q,z,2).subs(z,zz)))
        for ai2 in [0,1]:
            h=0
            for k in range(1,K+1):
                Ck=2*k+s.Rational(4*k*(k-1)*(1+2*ai2),m+4)+4*k*ai2
                for l in range(K+1):
                    h+=a[k]*a[l]*z**(k+l)*Ck*s.Rational(4,m*(m+2))*G2[l,k-1]
            H3norm=s.Rational(4,m*(m+2)*(m+4))+s.Rational(4*ai2,(m+2)**2*(m+4))
            for k in range(1,K+1):
                for l in range(1,K+1):
                    h+=a[k]*a[l]*z**(k+l)*(4*k*l*H3norm*G3[k-1,l-1]+s.Rational(4*ai2*(m+2+2*k)*(m+2+2*l),m*(m+2)**2)*G1[k,l])
            h=s.factor(h/G2[0,0]);Hs[ai2]=h;print('translation',ai2,s.N(h.subs(z,zz)))
            Path(f'workspace/agent2_n19_translation_{ai2}.txt').write_text(str(h))
Path('workspace/agent2_n19_scale_Q.txt').write_text(str(Q))
# Exact rational interval certificate; no floating-point root assumptions.
P=s.symbols('P')
def atan_bounds(q,terms=20):
    assert terms%2==0
    lo=sum((-1)**k*q**(2*k+1)/s.Integer(2*k+1) for k in range(terms))
    return lo,lo+q**(2*terms+1)/s.Integer(2*terms+1)
l5,u5=atan_bounds(s.Rational(1,5));l239,u239=atan_bounds(s.Rational(1,239))
plo,phi=16*l5-4*u239,16*u5-4*l239
Z=(s.Rational(9024309988,10**10),s.Rational(9024309989,10**10))
PI2=(plo,phi)
def mul(a,b):
    pp=[aa*bb for aa in a for bb in b]
    return min(pp),max(pp)
def interval(expr,zi=Z):
    expr=s.sympify(expr)
    if expr.is_Rational:return (expr,expr)
    if expr==z:return zi
    if expr==P:return PI2
    if expr.is_Add:
        vals=[interval(arg,zi) for arg in expr.args]
        return sum(v[0] for v in vals),sum(v[1] for v in vals)
    if expr.is_Mul:
        v=(s.Integer(1),s.Integer(1))
        for arg in expr.args:v=mul(v,interval(arg,zi))
        return v
    if expr.is_Pow and expr.exp.is_Integer:
        nn=int(expr.exp);v=interval(expr.base,zi)
        if nn<0:
            assert v[0]*v[1]>0
            v=(1/v[1],1/v[0]);nn=-nn
        out=(s.Integer(1),s.Integer(1))
        for kk in range(nn):out=mul(out,v)
        return out
    raise ValueError(expr)
def exprP(expr):
    expr=s.cancel(expr.subs(s.pi,P))
    assert not expr.has(s.pi)
    return expr
qp=exprP(s.diff(Q,z));qpp=exprP(s.diff(Q,z,2))
assert interval(qp,(Z[0],Z[0]))[0]>0
assert interval(qp,(Z[1],Z[1]))[1]<0
assert interval(qpp)[1]<0
for ai2 in [0,1]:assert interval(exprP(Hs[ai2]))[1]<0
print(f'EXACT rational interval certificate: n{N} full strict local minimum of negative Q.')
Path('workspace/agent2_polynomial_search.py').write_text(Path(__file__).read_text())
