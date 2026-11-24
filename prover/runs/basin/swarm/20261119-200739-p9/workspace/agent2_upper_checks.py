import sympy as s
import numpy as np
from pathlib import Path
p,t,d=s.symbols('p t d',positive=True);q=p/(p-1);a=q*t/(q*t-1)
assert s.simplify(p/(p-a)-(q*t-1)/(t-1))==0
assert s.simplify(1/p+1/q+1/(p*(p-1))-(1+1/(p*(p-1))))==0
assert s.simplify((1+1/(q*(q-1)))/(p-1)-(1+1/(p*(p-1))))==0
assert s.simplify(1-(1+d/4)*(1-d)-d*(3+d)/4)==0
rng=np.random.default_rng(67321)
max_rh_ratio=0.
for _ in range(10000):
 pp=rng.uniform(1.05,10);aa=rng.uniform(-.999,pp-1-.001)
 B=1/(1+aa)*((pp-1)/(pp-1-aa))**(pp-1)
 dd=2**(-pp)/B
 eps=np.log1p(dd/4)/np.log(4)
 assert aa*(1+eps)>-1
 lhs=(1/(1+aa*(1+eps)))**(1/(1+eps));rhs=2/(1+aa)
 max_rh_ratio=max(max_rh_ratio,lhs/rhs)
 assert lhs<=rhs*(1+1e-12)
for _ in range(10000):
 x,z=rng.uniform(-.5,.5,2);y=rng.choice([-1,1])*rng.uniform(1.5,100)
 assert abs(1/(z-y)-1/(x-y))<=4*abs(z-x)/abs(y-x)**2*(1+1e-12)
print('Exact upper-bound algebra identities verified.')
print('10000 actual power-weight reverse-Holder checks passed; maxLHS/RHS=',max_rh_ratio)
print('10000 actual separated-kernel derivative inequalities passed.')
Path('workspace/agent2_upper_checks.py').write_text(Path(__file__).read_text())