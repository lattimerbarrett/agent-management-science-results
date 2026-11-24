"""Exact symbolic checks for the dimension-two necessity argument.
Analytic facts used in the proof (subharmonic Liouville, psh gluing) are
not represented as computational tests.
"""
import sympy as s

a=s.symbols('a', positive=True)
b,d,c=s.symbols('b d c', real=True)
A=(b*b+d*d+c*c+a*a+1)/(2*a)
H=s.Matrix([[a,b+s.I*d],[b-s.I*d,c+2*A]])
det=s.factor(H.det())
assert s.simplify(det-((c+a/2)**2+3*a*a/4+1)) == 0
assert s.simplify(A-(b*b+d*d+c*c+a*a+1)/(2*a)) == 0
# Verify the Hessian chain rule on a general real quadratic polynomial.
x,y,u,v=s.symbols('x y u v', real=True)
coords=[x,y,u,v]
coef=s.symbols('t0:15', real=True)
r=coef[0]+sum(coef[i+1]*coords[i] for i in range(4))
k=5
for i in range(4):
    for j in range(i,4):
        r+=coef[k]*coords[i]*coords[j]
        k+=1

def dz(f,j):
    return (s.diff(f,coords[2*j])-s.I*s.diff(f,coords[2*j+1]))/2

def db(f,j):
    return (s.diff(f,coords[2*j])+s.I*s.diff(f,coords[2*j+1]))/2

alpha=s.symbols('alpha',real=True)
for j in range(2):
    for k in range(2):
        lhs=dz(db(r+alpha*r*r,k),j)
        rhs=(1+2*alpha*r)*dz(db(r,k),j)+2*alpha*dz(r,j)*db(r,k)
        assert s.expand(lhs-rhs)==0
# Orientation: exterior defining function is minus the interior function.
for j in range(2):
    for k in range(2):
        assert s.expand(dz(db(-r,k),j)+dz(db(r,k),j))==0
# Peak inequality bookkeeping: s=2 Re(g)+L+R, L>=lambda*|z|^2,
# |R|<=(lambda/2)*|z|^2 gives 2 Re(g)<=-(lambda/2)|z|^2.
# Put c=lambda/2 and h=Re(g)+(c/4)|z|^2.
c0,t=s.symbols('c0 t', positive=True)
assert s.simplify(-c0*t/2+c0*t/4)==-c0*t/4
print('PASS: Levi sign reversal; exact Hessian chain rule; positive-definite normal correction; peak constants.')
print('det corrected Levi =',det)
