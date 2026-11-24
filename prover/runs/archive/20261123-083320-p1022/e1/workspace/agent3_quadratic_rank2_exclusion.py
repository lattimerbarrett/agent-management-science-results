import sympy as s,json
from pathlib import Path
x,y,k,t=s.symbols('x y k t');H=x+y;P=x*y
ct=s.prod(1+v*t for v in [2*x,x+y,2*y])
q=s.series(ct/(1+k*H*t),t,0,4).removeO().expand().coeff(t,3)
expected=s.expand((4-4*k)*P*H+(-2*k+3*k*k-k**3)*H**3)
assert s.expand(q-expected)==0
reduced=s.factor((4-4*k)+2*(-2*k+3*k*k-k**3))
assert s.expand(reduced+2*(k-1)*((k-1)**2+1))==0
out={'c3image':str(s.factor(q)),'coefficient_after_H3_2PH':str(reduced),'integer_roots':[1]}
Path('workspace/agent3_quadratic_rank2_exclusion.json').write_text(json.dumps(out))
import os
if os.path.abspath(__file__)!=os.path.abspath('workspace/agent3_quadratic_rank2_exclusion.py'):
 Path('workspace/agent3_quadratic_rank2_exclusion.py').write_text(Path(__file__).read_text())
print(out)
