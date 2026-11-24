"""Exact algebra/Sturm checks for an s=4 positive-neutral fixed-cycle circle.
This certifies a candidate invariant geometry, NOT a nonconvergent orbit.
"""
import sympy as s
x,t=s.symbols('x t')
N=s.Rational(48,35)
P5=x*(x*x-1)*(x*x-4)
P7=P5*(x*x-s.Rational(82,35))
f=x**4-s.Rational(29,7)*x*x+s.Rational(6,7)
g=x**4-s.Rational(16,5)*x*x+s.Rational(8,5)
F=s.expand(35*(P7*(x-t)+N))
assert s.expand(f*g-N-P7*x)==0
base=[-2,-1,0,1,2]
for a,b in zip(base[:-1],base[1:]):
    assert s.Poly(f,x).count_roots(a,b)==1
    assert s.Poly(g,x).count_roots(a,b)==1
w=[1/s.diff(P5,x).subs(x,a) for a in base]
p=[s.cancel(N*wi/f.subs(x,a)) for a,wi in zip(base,w)]
assert p==[s.Rational(1,5),s.Rational(1,10),s.Rational(2,5),s.Rational(1,10),s.Rational(1,5)]
assert sum(p)==1
for j in range(4):
    assert sum(pi*a**j*f.subs(x,a) for pi,a in zip(p,base))==0
pp=[s.cancel(pi*f.subs(x,a)**2/N) for pi,a in zip(p,base)]
assert sum(pp)==1
for j in range(4):
    assert sum(pi*a**j*g.subs(x,a) for pi,a in zip(pp,base))==0
assert all(s.cancel(pi*g.subs(x,a)**2/N-p0)==0 for pi,p0,a in zip(pp,p,base))
D=s.Poly(s.discriminant(F,x),t)
DI=D.intervals(eps=s.Rational(1,10**14))
assert len(DI)==8 and all(mult==1 for _,mult in DI)
# Rational interval arithmetic, used to match the folds to their x-locations.
def add(A,B):return A[0]+B[0],A[1]+B[1]
def mul(A,B):
    q=[a*b for a in A for b in B];return min(q),max(q)
def div(A,B):
    assert not B[0]<=0<=B[1]
    return mul(A,(1/B[1],1/B[0]))
def peval(poly,I):
    ans=(s.S(0),s.S(0))
    for c in s.Poly(poly,x).all_coeffs():ans=add(mul(ans,I),(c,c))
    return ans
C=s.Poly(s.expand(P7**2-N*s.diff(P7,x)),x)
CI=C.intervals(eps=s.Rational(1,10**14))
assert len(CI)==8 and all(mult==1 for _,mult in CI)
near=[]
for I,mult in CI:
    theta=add(I,div((N,N),peval(P7,I)))
    if theta[0]>0 and theta[1]<1:
        near.append((I,theta))
        assert s.Rational(11846490,10**8)<theta[0]<theta[1]<s.Rational(11846491,10**8)
        assert s.Rational(65,100)<I[0]<I[1]<s.Rational(66,100)
        # F_xx at the fold cannot vanish.
        Fxx=s.diff(P7,x,2)*(x-t)+2*s.diff(P7,x)
        # Substitute interval t by direct two-variable decomposition.
        A=peval(s.diff(P7,x,2)*x+2*s.diff(P7,x),I)
        B=mul(peval(-s.diff(P7,x,2),I),theta)
        J=add(A,B)
        assert not J[0]<=0<=J[1]
    else:
        assert theta[1]<-1 or theta[0]>1 or (theta[0]>-1 and theta[1]<0)
assert len(near)==1
print('Exact s4 candidate circle checks passed; nearest positive fold:',near[0])
