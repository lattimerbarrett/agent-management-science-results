import sympy as s
from pathlib import Path
lam,a,c,x,y=s.symbols('lam a c x y', real=True)
A=(1+c*c+(x*x+y*y)/lam)/(2*a*a)
H=s.Matrix([[lam,x+s.I*y],[x-s.I*y,c+2*A*a*a]])
det=s.factor(H.det())
assert s.simplify(det-lam*(c*c+c+1))==0
assert s.simplify(c*c+c+1-((c+s.Rational(1,2))**2+s.Rational(3,4)))==0
# Exact Schur complement controls all off-diagonal terms.
assert s.simplify(H[1,1]-(x*x+y*y)/lam-(c*c+c+1))==0
out='For lambda>0 and a!=0, A=(1+c²+(x²+y²)/lambda)/(2a²).\n'
out+='Adjusted Levi determinant = '+str(det)+' > 0.\n'
out+='Schur complement = (c+1/2)^2+3/4 > 0.\n'
out+='Thus both Sylvester principal minors are positive.\n'
print(out)
Path('workspace/agent2_peak_hessian_check.txt').write_text(out)
Path('workspace/agent2_peak_hessian_check.py').write_text(Path('scratchpad.py').read_text())