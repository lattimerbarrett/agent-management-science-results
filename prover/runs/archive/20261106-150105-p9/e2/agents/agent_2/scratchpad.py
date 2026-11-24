"""Exact algebra plus numerical cross-checks for the scalar lower bound.
The proof, not finite numerical testing, controls arbitrary p and intervals.
"""
import sympy as sp
import mpmath as mp
import json
from pathlib import Path
p,e,L=sp.symbols('p e L', positive=True)
r=(1-e)/(p-1)
# Exact interval bound multiplication.
assert sp.simplify((2**(1+e)*L**(e-1)/e)*(2*L)**(1-e)-4/e)==0
# Exact input integral and output annulus mass.
t=sp.symbols('t',positive=True)
assert sp.simplify(sp.integrate(t**(e-1),(t,0,1))-1/e)==0
assert sp.simplify(((sp.exp(-1/e))**e-(sp.exp(-2/e))**e)/e-(sp.exp(-1)-sp.exp(-2))/e)==0
mp.mp.dps=70
rows=[]
for pp in [mp.mpf('1.1'),mp.mpf('1.5'),mp.mpf('2.1'),mp.mpf('3'),mp.mpf('10')]:
 for ee in [mp.mpf('0.25'),mp.mpf('0.125'),mp.mpf('0.0625')]:
  delta=mp.exp(-4/ee); a=mp.exp(-2/ee); b=mp.exp(-1/ee)
  # Integral over known plateau gives a rigorous analytic lower bound.
  h=lambda tt:mp.log((tt+mp.mpf('.5'))/(tt+delta))/mp.pi
  assert h(b)>=1/(2*mp.pi*ee)
  mass=mp.quad(lambda u:mp.exp(ee*u),[-2/ee,-1/ee])
  assert mp.almosteq(mass,(mp.exp(-1)-mp.exp(-2))/ee)
  # Compute lower output integral by log substitution; input <=1/e.
  out=mp.quad(lambda u:h(mp.exp(u))**pp*mp.exp(ee*u),[-2/ee,-1/ee])
  ratio=(ee*out)**(1/pp)
  claimed=(mp.exp(-1)-mp.exp(-2))**(1/pp)/(2*mp.pi*ee)
  assert ratio>=claimed
  # Check power-weight characteristic on many crossing, distant, adjacent intervals.
  def power_int(alpha,a,b):
   if a>=0:return (b**(alpha+1)-a**(alpha+1))/(alpha+1)
   if b<=0:return ((-a)**(alpha+1)-(-b)**(alpha+1))/(alpha+1)
   return ((-a)**(alpha+1)+b**(alpha+1))/(alpha+1)
  for aa,bb in [(-1,1),(0,1),(-3,-2),(1,2),(mp.mpf('.001'),1),(-mp.mpf('.001'),1),(10,mp.mpf('10.01'))]:
   length=bb-aa
   ap=power_int(-1+ee,aa,bb)/length*(power_int((1-ee)/(pp-1),aa,bb)/length)**(pp-1)
   assert ap<=4/ee
  rows.append({'p':str(pp),'epsilon':str(ee),'computed_plateau_ratio':str(ratio),'proved_ratio_lower_bound':str(claimed)})
Path('workspace').mkdir(exist_ok=True)
Path('workspace/agent2_lower_checks.json').write_text(json.dumps(rows,indent=2))
# Make this independent checker reusable by the team.
Path('workspace/agent2_lower_checks.py').write_text(Path(__file__).read_text())
print('All 3 symbolic identities and 150 numerical assertions passed.')
print(json.dumps(rows[:3],indent=2))
