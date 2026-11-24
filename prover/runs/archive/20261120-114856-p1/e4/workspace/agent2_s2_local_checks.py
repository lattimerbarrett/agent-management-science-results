from pathlib import Path
import sympy as S
x,c,a,b,mu=S.symbols('x c a b mu')
p=x*x-c;P=p*p-1
q=p-a-b*x
# Two fixed hypersurfaces of the two-step map.
assert S.expand((p-a)*(p+a)-(P+1-a*a))==0
assert S.expand((p+b*b/2-b*x)*(p+b*b/2+b*x)-(P+1-c*b*b+b**4/4))==0
# Moment coordinates for a measure with q as its monic OP.
t=a+b*mu;v=a*mu+b*(c+t)
def E(f):
    z=S.Poly(S.rem(S.expand(f),P,x),x)
    return S.expand(sum(z.nth(j)*[1,mu,c+t,c*mu+v][j] for j in range(4)))
assert E(q)==0 and E(x*q)==0
assert S.factor(E(q*q)) == 1-a*a-a*b*b-2*a*b*mu-b**3*mu-b*b*c
# Coordinate chart is nonsingular on the entire critical fixed segment.
chart=S.Matrix([mu,c+t,c*mu+v])
assert S.factor(chart.jacobian([mu,a,b]).det().subs({a:0,b:0}))==c-mu*mu
# Verify quadratic drift from general feature formula at the critical line.
G=S.Matrix([[1,mu],[mu,c]])
u=S.Matrix([a,b]);Huu=S.Matrix([b*b,2*a*b+mu*b*b])
d=(u.T*G*u)[0]
Exz2=mu*a*a+2*c*a*b+c*mu*b*b
normal_correction=(G.inv()*Huu)[1]
dmu=S.factor(2*(mu*d-Exz2+normal_correction))
assert S.factor(dmu-4*a*b*(1/(c-mu*mu)-(c-mu*mu)))==0
print('s=2 critical four-node local fixed hypersurfaces, coordinate chart, drift: PASS')
