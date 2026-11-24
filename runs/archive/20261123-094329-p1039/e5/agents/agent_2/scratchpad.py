import sympy as s
from pathlib import Path
x,y=s.symbols('x y',real=True)
z=x+s.I*y
zb=x-s.I*y
# Model K at a Levi-negative point: rho=Re(w)-|z|^2.
# Exterior defining function r=-rho has Levi +1 in its tangent z direction.
rho= -x*x-y*y
levi=s.simplify((s.diff(rho,x,2)+s.diff(rho,y,2))/4)
assert levi == -1
assert -levi == 1
# Strict local holomorphic peak for {Re(w)>|z|²}: exp(-(w-w²)).
# For 0 <= u=Re(w) <= 1/2, Re(w-w²)=u-u²+v² >= u/2+v².
u,v=s.symbols('u v',real=True)
reg=u-u*u+v*v
assert s.factor(reg-(u/s.Integer(2)+v*v)) == -u*(2*u-1)/2
out={'model_K_Levi':str(levi),'model_exterior_Levi':str(-levi),'strict_peak_log_modulus':'-Re(w-w²)','peak_inequality_remainder':str(s.factor(reg-(u/s.Integer(2)+v*v)))}
Path('workspace/agent2_necessity_model_checks.txt').write_text(str(out)+'\n')
print(out)
# Explicit smooth bounded connected mixed-Levi test obstacle:
# rho=|z1|^4-|z1|^2+sum_{j>=2}|zj|^2-1.
p=(x*x+y*y)**2-(x*x+y*y)
h=s.expand((s.diff(p,x,2)+s.diff(p,y,2))/4)
assert s.simplify(h-(4*(x*x+y*y)-1))==0
assert h.subs({x:0,y:0})==-1
# Gradient in first coordinate vanishes only at t=0 or t=1/2;
# if all other coordinates vanish, rho is strictly negative at both.
t=s.symbols('t', real=True)
assert (t*t-t-1).subs(t,0)==-1
assert (t*t-t-1).subs(t,s.Rational(1,2))==-s.Rational(5,4)
Path('workspace/agent2_mixed_levi_test.txt').write_text('First Levi eigenvalue: '+str(h)+'; all others 1.\nAt q=(0,1,0,...), tangential eigenvalues are -1 and n-2 copies of +1.\n')
print('Mixed-Levi test exact Hessian and regularity checks passed')
print('Shared files:', sorted(p.name for p in Path('workspace').iterdir()))
