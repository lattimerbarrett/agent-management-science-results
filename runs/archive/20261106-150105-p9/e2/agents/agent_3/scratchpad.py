import sympy as s, math, json
from pathlib import Path
p,r,t=s.symbols('p r t', positive=True)
q=p/(p-1); a=q*(1+t)/(q*(1+t)-1); b=p*r/(p*r-1)
assert s.simplify(p-a-p*t/(q*(1+t)-1))==0
assert s.simplify(1/a-1/p-t/(q*(1+t)))==0
assert s.simplify(q-b-q*(r-1)/(p*r-1))==0
assert s.simplify(1/b-1/q-(r-1)/(p*r))==0
assert s.simplify(1/p+1/q+1/(p*(p-1))-(1+1/(p-1)-1/p))==0
# Cancellation kernel estimate used in Hilbert CZ decomposition:
# If |y-c|<=ell/2 and |x-c|>=3ell/2 then
# |1/(x-y)-1/(x-c)| <= 3ell/(4|x-c|^2).
x,y,ell=s.symbols('x y ell',positive=True)
# denom |x-y|>=|x|-ell/2>=(2/3)|x|, numerator<=ell/2.
assert s.Rational(1,2)/s.Rational(2,3)==s.Rational(3,4)
checks=0
for pp in [1.01,1.1,1.5,1.9,2.1,3,10,100]:
 qq=pp/(pp-1)
 for k in range(1,1001):
  tt=k/1000
  assert tt**(-tt/(qq*(1+tt)))<=math.exp(1/(math.e*qq))*(1+1e-12)
  checks+=1
out={'exact_symbolic_identities':6,'maximal_exponent_numeric_checks':checks,'status':'all assertions passed'}
Path('workspace/agent3_upper_checks.py').write_text(Path(__file__).read_text())
Path('workspace/agent3_upper_checks.json').write_text(json.dumps(out,indent=2))
print(out)
