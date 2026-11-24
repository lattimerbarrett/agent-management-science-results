import sympy as s
from pathlib import Path
x,y,z=s.symbols('x y z',real=True)
P=(x*x+y*y)**2-2*(x*x-y*y)
F=P**2+z*z-s.Rational(1,4)
critical=s.solve([s.diff(P,x),s.diff(P,y)],(x,y))
assert set(critical)=={(0,0),(1,0),(-1,0)}
critical_values={s.expand(P.subs({x:a,y:b})) for a,b in critical}
assert critical_values=={-1,0}
# A point of F=0 with dF=0 would have z=0, P=+-1/2,
# and dP=0, impossible by those critical values.
G=s.groebner([F,s.diff(F,x),s.diff(F,y),s.diff(F,z)],x,y,z)
assert list(G)==[s.Integer(1)]
# Here the assertion even holds over C: direct check critical equations.
# P=-1 at (+-1,0), P=0 at origin.  The two minima and one saddle
# show {|P|<=1/2} is a planar pair of pants (by Morse handles).
for a,b in critical:
    h=s.hessian(P,(x,y)).subs({x:a,y:b})
    if a==0:
        assert h.det()<0
    else:
        assert h.det()>0 and h.trace()>0
# F>0 for r^2>=4: split rho^2>=3 (P>=3) or rho^2<=3 (z^2>=1).
t=s.symbols('t',real=True)
assert s.expand((t*t-2*t)-3-(t-3)*(t+1))==0
# Once multiplied by a smooth cutoff equal1 on r²<=4 and0 on r²>=9,
# g=chi*F+(1-chi) extends as constant1 over infinity in S³.
# Its zero set is unchanged and regular; its negative domain is
# a regular neighborhood of a planar pair of pants, a genus2 handlebody.
# Flat cone radial derivative is strictly positive for every r>0.
r=s.symbols('r',positive=True)
alpha=s.exp(1-1/r**2)
assert s.simplify(s.diff(alpha,r)-2*alpha/r**3)==0
assert s.diff(alpha,r).is_positive is True
# Every finite derivative order vanishes at the cone point.
for k in range(9):
    assert s.limit(s.diff(alpha,r,k),r,0,dir='+')==0
print('P critical points and values:', [(q,P.subs(dict(zip((x,y),q)))) for q in critical])
print('F=0 critical ideal Groebner basis:',list(G))
print('Hessians:',[(q,s.hessian(P,(x,y)).subs(dict(zip((x,y),q)))) for q in critical])
Path('workspace/agent4_genus2_link.py').write_text(Path('scratchpad.py').read_text())
