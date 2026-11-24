"""Finite interval pointwise-engine tests, NOT the final Floquet certificate."""
import sys,numpy as np
sys.path.insert(0,'workspace')
from agent4_interval_blowup import IntervalBlowup
from agent4_floquet_pointwise import FloquetPointwiseBounds,norminf,_eval
from sage.all import vector,matrix
D=np.load('workspace/agent1_GENUINE_s4_periodic.npz');ob=IntervalBlowup();R=ob.R
inds=[2500,2520];knots=D['x'][inds];gamma=D['y'][:,inds].T.copy();gamma[:,0]*=-1;T=float(D['p'][0])
gd=np.array([[float(a) for a in ob.field_generic(list(map(R,y)))] for y in gamma])*T
frames=np.array([np.eye(7)]*2);fp=np.zeros_like(frames)
eng=FloquetPointwiseBounds(ob,knots,gamma,gd,frames,fp,T,np.zeros((7,7)),periodic=False)
r=eng.bound(*knots,rho=1e-7)
assert all(np.isfinite(float(r[k])) for k in ['delta','E','H','a_normal','b'])
print('Whole-segment delta/E/H',r['delta'],r['E'],r['H'])
assert r['physical_tube'][5].lower()>0 and r['physical_tube'][6].lower()>0
for ss in np.linspace(knots[0],knots[1],13):
 s=R(float(ss));gc=eng.gamma.centered(s);y=gc[0];F,J,H=ob.field_jac_hess(y)
 defect=gc[1]-R(T)*vector(R,F)
 assert norminf(defect)<=r['delta']
 assert norminf(R(T)*matrix(R,J))<=r['E']
print('13 pointwise defects/Jacobians enclosed by full polynomial-composed bound')
# Hermite endpoint value and derivative checks, exact rational data interpretation.
for k,cs in enumerate(eng.gamma.coeffs):
 h=eng.gamma.knots[k+1]-eng.gamma.knots[k]
 left=_eval(cs,R(0));right=_eval(cs,h)
 deriv=_eval([cs[1],cs[2]*2,cs[3]*3],h)
 for i in range(7):
  assert (left[i]-eng.gamma.values[k][i]).contains_zero()
  assert (right[i]-eng.gamma.values[k+1][i]).contains_zero()
  assert (deriv[i]-eng.gamma.derivatives[k+1][i]).contains_zero()
print('Hermite C1 endpoint algebra checks PASS')
