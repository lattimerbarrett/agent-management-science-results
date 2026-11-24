import sympy as s
import mpmath as mp
import json, os
# Exact derivation of regular radial Jacobi mode on hemisphere.
z=s.symbols('z',positive=True)
l,n=s.symbols('l n',integer=True,positive=True)
a=(l-1)/2; b=(l+n)/2; c=l+n/2
# theta-coordinate equation with z=sin(theta)^2 and R=z^(l/2)F(z).
F=s.Function('F')(z)
R=z**(l/2)*F
# d2_theta R=4z(1-z)Rzz+2(1-2z)Rz, cot(theta)*dthetaR=2(1-z)Rz
ode=4*z*(1-z)*s.diff(R,z,2)+(2*(1-2*z)+2*(n-1)*(1-z))*s.diff(R,z)+(n-l*(l+n-2)/z)*R
normal=s.simplify(s.expand(ode/z**(l/2)/4))
target=z*(1-z)*s.diff(F,z,2)+(c-(a+b+1)*z)*s.diff(F,z)-a*b*F
assert s.simplify(normal-target)==0
assert s.simplify(c-a-b)==s.Rational(1,2)
# Check formula against direct derivative of hypergeometric at near-equator.
mp.mp.dps=70
results=[]
for nv in [3,10,20,21,30]:
 for lv in [2,3,4,7]:
  av=mp.mpf(lv-1)/2;bv=mp.mpf(lv+nv)/2;cv=mp.mpf(lv)+mp.mpf(nv)/2
  radial=lambda t:mp.sin(t)**lv*mp.hyp2f1(av,bv,cv,mp.sin(t)**2)
  eps=mp.mpf('1e-20');theta=mp.pi/2-eps
  ratio=radial(theta)/mp.diff(radial,theta)
  expected=mp.gamma(av)*mp.gamma(bv)/(2*mp.gamma((lv+nv+1)/mp.mpf(2))*mp.gamma(mp.mpf(lv)/2))
  relative=abs(ratio-expected)/expected
  assert expected>0 and relative<mp.mpf('1e-17'),(nv,lv,relative)
  results.append({'n':nv,'ell':lv,'kappa':str(expected),'relative_error':str(relative)})
os.makedirs('workspace',exist_ok=True)
with open('workspace/agent3_jacobi_check.json','w') as f:json.dump({'symbolic_ode_identity':True,'tests':results},f,indent=2)
import shutil
if os.path.abspath(__file__) != os.path.abspath('workspace/agent3_jacobi_check.py'):
 shutil.copyfile(__file__, 'workspace/agent3_jacobi_check.py')
print('Exact hypergeometric ODE identity verified; Gauss exponent = 1/2.')
print(len(results),'independent near-equator derivative checks passed; max relative error =',max(mp.mpf(r['relative_error']) for r in results))
