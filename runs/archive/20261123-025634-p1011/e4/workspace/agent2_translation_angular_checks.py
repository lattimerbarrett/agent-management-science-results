"""Exact angular decompositions used by translation-Hessian calculations.
These checks are algebraic auxiliary results, not nonlinear existence.
"""
import sympy as s

def sphere_mean(poly,z):
    dim=len(z)
    result=0
    for powers,coeff in s.Poly(s.expand(poly),*z).terms():
        if any(e%2 for e in powers): continue
        ks=[e//2 for e in powers]
        num=s.prod(s.rf(s.Rational(1,2),k) for k in ks)
        result+=coeff*num/s.rf(s.Rational(dim,2),sum(ks))
    return s.simplify(result)

for m in range(2,9):
    z=s.symbols('z:'+str(m),real=True)
    T=[s.Integer(1),s.Integer(-1)]+[s.Integer(0)]*(m-2)
    S=sum(t*t for t in T)
    H=sum(T[i]*z[i]**2 for i in range(m))
    r2=sum(x*x for x in z)
    nh=s.Rational(2)*S/(m*(m+2))
    assert sphere_mean(H*H,z)==nh
    for a,tau in enumerate(T):
        H3=z[a]*H-s.Rational(2,m+2)*r2*tau*z[a]
        assert s.expand(sum(s.diff(H3,x,2) for x in z))==0
        expected=s.Rational(2)*S/(m*(m+2)*(m+4))+4*tau*tau/s.Integer((m+2)**2*(m+4))
        assert sphere_mean(H3*H3,z)==expected
        assert sphere_mean(H*z[a]**2,z)==s.Rational(2)*tau/(m*(m+2))
        assert sphere_mean(H*H*z[a]**2,z)==(2*S+8*tau*tau)/s.Integer(m*(m+2)*(m+4))
        assert sphere_mean(H*H3*z[a],z)==expected
print('PASS: harmonic cubic decomposition and exact angular moments, dimensions m=2..8')
