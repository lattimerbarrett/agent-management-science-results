import sympy as s,json
from pathlib import Path
# Independent rational audit of the saved profile positivity certificates.
cs=json.loads(Path('workspace/agent2_profile_certificates.json').read_text())
for c in cs:
 for name in ['numerator_coefficients','denominator_coefficients']:
  coeff=[s.Rational(a) for a in c[name]]
  assert all(a>=0 for a in coeff)
  assert coeff[-1]>0
# Certify the rational pi bounds used in the gamma-ratio enclosure by Machin.
z=s.Rational(1,5)
def tanadd(a,b):return s.cancel((a+b)/(1-a*b))
tan4=tanadd(tanadd(z,z),tanadd(z,z))
assert tanadd(tan4,-s.Rational(1,239))==1

def atan_bounds(z,N=12):
 # A sum with an even number of terms is below arctan(z).
 assert N%2==0
 lo=sum((-1)**j*z**(2*j+1)/s.Integer(2*j+1) for j in range(N))
 hi=lo+z**(2*N+1)/s.Integer(2*N+1)
 return lo,hi
l5,u5=atan_bounds(s.Rational(1,5));l239,u239=atan_bounds(s.Rational(1,239))
pi_lo=16*l5-4*u239;pi_hi=16*u5-4*l239
assert s.Rational(333,106)<pi_lo<pi_hi<s.Rational(22,7)
print('PASS:',len(cs),'saved rational positivity certificates, all coefficient signs exact')
print('PASS: Machin tangent identity and rational alternating-series proof of 333/106<pi<22/7')
Path('workspace/agent4_profile_independent_checks.py').write_text(Path('scratchpad.py').read_text())
