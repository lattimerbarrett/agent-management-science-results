"""Exact n=19 finite-dimensional MODEL certificate, standalone.
Not itself a PDE existence or compactness theorem.
"""
import sympy as S
from pathlib import Path
n=19; d=3; m=n-1
x,t,p=S.symbols('x t p');a=S.Rational(n,2);q=x*x-a*a

def anti(F):
    rem=S.Poly(S.cancel(F),x);P=S.Integer(0)
    if rem.is_zero:return P
    for j in range((rem.degree()-1)//2,-1,-1):
        c=rem.nth(2*j+1)/(4*(a-j));P+=c*x**(2*j)
        rem-=S.Poly(S.expand(c*((x+a)**2*(x-1)**(2*j)-(x-a)**2*(x+1)**(2*j))),x)
    assert rem.is_zero
    return P

def moment(F):
    P=anti(x*q*q*S.cancel(F))
    return S.factor((2*a+1)**2*S.pi*P.subs(x,a)/S.gamma(a+S.Rational(3,2))**2
        +(2*a+2)**2*P.subs(x,a+1)/S.gamma(a+2)**2)

def b2(h):
    return S.prod(x*x-(a-j)**2 for j in range(h))/(S.factorial(h)*S.prod(2*a+1-2*j for j in range(1,h+1)))
def b3(h):
    return S.prod(x*x-(a+1-j)**2 for j in range(h+1))/(S.factorial(h+1)*S.prod(2*a+3-2*j for j in range(1,h+2)))
def b1(h):
    return S.prod(x*x-(a-1-j)**2 for j in range(h-1))/(S.factorial(h-1)*S.prod(2*a-1-2*j for j in range(1,h)))
R2=[S.expand(sum(S.binomial(j,h)*2**h*(-1)**(j-h)*b2(h) for h in range(j+1))) for j in range(d+1)]
R3=[S.expand(sum(S.binomial(j,h)*2**h*(-1)**(j-h)*b3(h) for h in range(j+1))) for j in range(d)]
R1=[S.expand(sum(S.binomial(j,h)*2**h*(-1)**(j-h)*b1(h) for h in range(1,j+1))) for j in range(d+1)]
G2=S.Matrix(d+1,d+1,lambda i,j:moment(R2[i]*R2[j]))
G1=S.Matrix(d+1,d+1,lambda i,j:moment(q*R1[i]*R1[j])/(n-1)**2)
G3=S.Matrix(d,d,lambda i,j:(n+1)**2*moment(S.cancel(R3[i]*R3[j]/(x*x-(a+1)**2))))
coef=[S.Integer(1),-S.Rational(469,1000),S.Rational(29,500),-S.Rational(1461,1000000)]
aa=S.Matrix([coef[j]*t**j for j in range(d+1)])
powers=S.Matrix(d+1,d+1,lambda i,j:2+2*i+2*j)
cp=S.expand((aa.T*G2.multiply_elementwise(powers)*aa)[0])
g=S.Matrix([aa[j]*(1+S.Rational(2*j,m+2)) for j in range(d+1)])
b=S.Matrix([2*(j+1)*aa[j+1] for j in range(d)])
c=S.Matrix([2*(j+1)*(1+S.Rational(2*j,m+4))*aa[j+1] if j<d else 0 for j in range(d+1)])
C=(aa.T*G2*c)[0]
Hs=S.expand((m+2)*(g.T*G1*g)[0]+S.Rational(2*(m+1),(m+2)*(m+4))*(b.T*G3*b)[0]+3*C)
Ht=S.expand(S.Rational(1,m+4)*(b.T*G3*b)[0]+C)

def atan_bounds(inv,N=32):
    z=S.Rational(1,inv)
    v=sum((-1)**j*z**(2*j+1)/S.Integer(2*j+1) for j in range(N))
    w=v+(-1)**N*z**(2*N+1)/S.Integer(2*N+1)
    return min(v,w),max(v,w)
# Machin identity: tan(4 atan(1/5)-atan(1/239))=1.
z=S.Rational(1,5);tan2=2*z/(1-z*z);tan4=2*tan2/(1-tan2*tan2)
assert S.factor((tan4-S.Rational(1,239))/(1+tan4/S.Integer(239)))==1
l5,u5=atan_bounds(5);l239,u239=atan_bounds(239)
plo,phi=16*l5-4*u239,16*u5-4*l239
assert plo>3 and phi<S.Rational(22,7)

def mul(A,B):
    vals=[a*b for a in A for b in B]
    return min(vals),max(vals)
def interval(expr,lo,hi):
    # Multiply by positive pi to get a polynomial in pi, then Horner bound.
    poly=S.Poly(S.cancel(S.expand(expr*S.pi)).subs(S.pi,p),t)
    result=(S.Integer(0),S.Integer(0))
    for coefficient in poly.all_coeffs():
        val=(S.Integer(0),S.Integer(0))
        for rational in S.Poly(coefficient,p).all_coeffs():
            val=mul(val,(plo,phi));val=(val[0]+rational,val[1]+rational)
        result=mul(result,(lo,hi));result=(result[0]+val[0],result[1]+val[1])
    return result
lo=S.Rational(4453007,5000000);hi=S.Rational(1781203,2000000)
assert interval(cp,lo,lo)[0]>0
assert interval(cp,hi,hi)[1]<0
assert interval(S.diff(cp,t),lo,hi)[1]<0
assert interval(Hs,lo,hi)[1]<0
assert interval(Ht,lo,hi)[1]<0
print('PASS: all anti-difference polynomial identities exact.')
print('PASS: exact rational interval certifies a scale root in',lo,hi)
print('PASS: scale and both translation Hessian types have strict signs.')
print('This is a full-parameter MODEL minimum, not alone a PDE example.')
Path('workspace/agent1_n19_certificate.py').write_text(Path(__file__).read_text())
