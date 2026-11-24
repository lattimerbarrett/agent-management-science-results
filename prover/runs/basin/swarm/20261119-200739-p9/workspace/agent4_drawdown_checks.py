import sympy as s
from pathlib import Path
u,b,mu=s.symbols('u b mu', positive=True)
f=s.exp(2*mu*u)-2*mu*u-1
assert s.simplify(s.diff(f,u,2)/2-mu*s.diff(f,u)-2*mu**2)==0
assert s.diff(f,u).subs(u,0)==0
# Expected time to drawdown b, reflected-at-zero negative-drift Brownian U.
m=(s.exp(2*mu*b)-s.exp(2*mu*u))/(2*mu**2)+(u-b)/mu
assert s.simplify(s.diff(m,u,2)/2-mu*s.diff(m,u)+1)==0
assert s.diff(m,u).subs(u,0)==0
assert s.simplify(m.subs(u,b))==0
q,L=s.symbols('q L', positive=True)
beta=q-1
bb=q*(1-beta)*L
assert s.simplify(bb-(1-beta**2)*L)==0
assert s.simplify((1/q)*bb-(1-beta)*L)==0
print('Reflected drawdown test function and exact mean hitting-time ODE passed.')
print('Critical weighted-barrier exponent:',s.simplify(2*(1/(2*q))*bb/L))
Path('workspace/agent4_drawdown_checks.py').write_text(Path(__file__).read_text())
Path('workspace/agent4_drawdown.md').write_text(r'''# Drawdown calculations and obstruction to a proposed lower construction

For U_t=sup_{s<=t}(B_s+mu s)-(B_t+mu t), U is reflected Brownian
motion with drift -mu. Put f(u)=exp(2mu u)-2mu u-1. Then f'(0)=0
and (.5 d^2-du mu)f=2mu^2. Therefore for tau_b=inf{U=b},
P(tau_b<=T)<=2mu^2 T/f(b). Solving the mean-hitting-time equation gives
E_0 tau_b=(exp(2mu b)-1-2mu b)/(2mu^2).
Both generator/boundary calculations are checked symbolically in the
accompanying executable script.

This validates a simple-ratio competing-stop bound: for q in(1,2),
Y=B+t/(2q), its drawdown of qlogQ has probability at most C T/Q
before time T. A separate reflected log-D process with positive drift
.5-eps^2 has lifetime of order Q^(1-2eps^2), so such a simple-ratio
stop does not destroy its leading occupation (use its second moment).

However, the stronger barrier suggested to cancel conditional moments,
R=Q inf_{s<=t}(R_s D_s^(-beta)), beta=q-1, DOES destroy that occupation.
Here R=exp(-Y/q), logD=L-(supV-V), L=logQ, and
V=Y+delta t with delta=(.5-eps^2)-1/(2q)>0; start D=Q.
Every running-maximum time of Y is also one of V, hence D=Q there.
Consequently, pathwise,

 sup_{s<=t}[Y_s+q beta logD_s]=sup_{s<=t}Y_s+q beta L.

The stronger barrier is therefore EXACTLY drawdown(Y)=q(1-beta)L.
Its mean lifetime has order
exp[(1/q) q(1-beta)L]=Q^(1-beta), rather than Q.
In particular D^alpha occupation before this stop is at most
C Q^(alpha+1-beta), incompatible with the hoped-for exponent1+alpha.
This is an obstruction to this particular construction, not a theorem
about the exact optimal Hilbert-transform exponent.
''')
