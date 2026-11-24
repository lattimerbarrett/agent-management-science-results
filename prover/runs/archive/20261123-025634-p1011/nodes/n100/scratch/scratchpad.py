import sys,runpy
from pathlib import Path
sys.path.insert(0,str(Path('experiments/e3').resolve()))
mod=runpy.run_path('experiments/e3/agent2_finite_maxima_certificates.py',run_name='certificate_module')
mod['certificate'](19)
import sympy as s
n=19
p=s.Rational(n+2,n-2);q=p+1
print('\nENERGY AUDIT n=19: p=',p,'q=',q)
checks={
 'bubble cutoff residual / mu':s.Rational(n-18,2),
 'bubble cutoff energy / mu^2':n-18,
 'linear graph cutoff / mu^2':n-17,
 'quadratic bulk residual / mu':s.Integer(8)-max(s.Rational(30-n,2),0),
 'cubic boundary energy / mu^2':8-max(23-n,0),
 'cubic boundary residual / mu':s.Integer(16)-max(s.Integer(22)-s.Rational(n,2),0),
 'nonlinear residual / mu':p-1,
 'nonlinear energy error / mu^2':q-2}
for label,exponent in checks.items():
 assert exponent>0
 print(label,': positive exponent',exponent)
print('\nSTRICT-MINIMUM PERSISTENCE: if F(theta0)+gamma <= min_boundary F and sup |j-E0-mu^2*F| < gamma*mu^2/3, then j(theta0) < min_boundary j. Only C0 expansion and C1 reduced energy are needed.')
