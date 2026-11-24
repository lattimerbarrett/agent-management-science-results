"""Exact and directed-rounded checks for the cotangent arc merger profile."""
import sympy as s
from sage.all import RealIntervalField
r,d,t=s.symbols('r d t', positive=True)
G=s.exp(-4*r*r/(d*d-r*r))
expr=s.simplify(G+r*s.diff(G,r))
# r²/d²=t/(t+4)
expected=s.exp(-t)*(1-2*t-t*t/2)
assert s.simplify(expr.subs(r,d*s.sqrt(t/(t+4)))-expected)==0
assert s.simplify(s.diff(expected,t)/s.exp(-t)-(t*t/2+t-3))==0
t0=s.sqrt(7)-1
assert s.simplify((1-2*t-t*t/2).subs(t,t0)+(1+s.sqrt(7)))==0
# Derivative polynomial has just one nonnegative root t0. Therefore
# minimum is -(1+sqrt7)*exp(1-sqrt7), globally for all t>=0.
R=RealIntervalField(100)
minimum=-(1+R(7).sqrt())*(1-R(7).sqrt()).exp()
assert minimum.lower()>(-R(3)/4).upper()
print('Global minimum enclosed by',minimum)
print('Certified: g+r g_prime > -3/4 on the entire radial domain')
# Flat-at-zero modification with a completely explicit small parameter.
# eta(t)=smooth_step(t-1), with smooth_step(v)=exp(-1/v)/
# (exp(-1/v)+exp(-1/(1-v))).  It is 0 before1 and1 after2.
# For v<=1/2, eta' <= exp(2-1/v)*(1/v²+4) <=8;
# the last inequality follows by setting T=1/v>=2 and differentiating.
T=s.symbols('T',real=True)
assert s.simplify(s.diff((T*T+4)*s.exp(2-T),T)/s.exp(2-T)+(T-1)**2+3)==0
E=s.Rational(1,100)
assert 2*E<=s.Rational(1,10)
# For u<=1/10, g2>=1-5u² and u*g2'>=-9u².
assert 4/(1-s.Rational(1,100))<5
assert 8/(1-s.Rational(1,100))**2<9
# g1=1-exp(-1/u²), and exp(-1/u²)<=u^4 gives
# g1+u*g1'>=1-3u².  The transition derivative term is
# >= -(u*8/E)*5u² >= -320E². Other terms >=1-56E².
transition_lower=1-376*E*E
assert transition_lower>0
print('Flat-origin splice transition lower bound:',transition_lower)
# Define g=(1-eta(u/E))*g1+eta(u/E)*g2 on [E,2E].
# Since g1>g2 there and both decrease, g also decreases strictly.
# The estimate g1-g2>=4u²/(1+3u²)-u^4>0 is immediate for u<=1/10.
assert 4/(1+3*s.Rational(1,100))-s.Rational(1,100)>0
# The resulting explicit C-infinity profile has g(0)=1, all derivatives
# of g-1 zero at0, g<1 foru>0, g=0 flat at1, and g+u*g'>-3/4.
# For -3/4 < b <= g <= 1 and 0<=v<=pi, v*b is >-pi and <=pi.
# The endpoints equality conditions require r=0 and v=pi.
