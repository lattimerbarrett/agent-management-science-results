"""Exact inverse-DN two-profile dilation instability, all n>=33.
Telescoping eliminates all infinite sums. r=w1/w0 satisfies
0<r<8(n+4)/(pi(n+1)^2)<400(n+4)/(157(n+1)^2).
Gamma log-convexity gives the first inequality; pi>3.14 gives second.
"""
import sympy as s
j,n,r,t,x=s.symbols('j n r t x')
S=2*(j+2)*(n+j)/(n-1)-3
moments=[]
for k in range(3):
    cs=s.symbols('c:'+str(2*k+1))
    Q=sum(cs[i]*j**i for i in range(2*k+1))
    eq=s.Poly((j+n-1)**2*Q-(j+3)**2*Q.subs(j,j+2)-(2*j+n+2)*s.expand(S**k),j)
    sol=s.solve(eq.all_coeffs(),cs)
    Q=s.factor(Q.subs(sol))
    assert s.cancel((j+n-1)**2*Q-(j+3)**2*Q.subs(j,j+2)-(2*j+n+2)*S**k)==0
    moments.append(s.factor((n-1)**2*Q.subs(j,0)/(n+2)+r*n*n*Q.subs(j,1)/(n+4)))
det=s.factor(12*moments[0]*moments[2]-16*moments[1]**2)
num,den=s.fraction(det)
assert all(c>0 for c in s.Poly(s.expand(den.subs(n,x+33)),x).all_coeffs())
# Substitute r=t*rmax. A quadratic p(t) is negative on [0,1]
# if all its Bernstein coefficients are strictly negative.
num2=s.together(num.subs(r,s.Rational(400,157)*(n+4)/(n+1)**2*t)).as_numer_denom()[0]
p=s.Poly(num2,t)
a0,a1,a2=[p.nth(i) for i in range(3)]
for B in (a0,a0+a1/2,a0+a1+a2):
    assert all(c<0 for c in s.Poly(s.expand(B.subs(n,x+33)),x).all_coeffs())
print('Exact proof: degree-one profile dilation matrix indefinite for every integer n>=33.')
