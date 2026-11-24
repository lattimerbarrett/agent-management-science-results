import sympy as s
from pathlib import Path
u,v,x,y=s.symbols('u v x y', real=True)
w=u+s.I*v
peak=s.expand(s.re(-w+w*w))
assert s.expand(peak-(-u+u*u-v*v))==0
assert s.expand(peak-(-u/s.Integer(2)-v*v)-u*(u-s.Rational(1,2)))==0
assert s.reduce_inequalities([u>0,u<s.Rational(1,2),u*(u-s.Rational(1,2))>=0],u)==s.false
z=x+s.I*y
rho=(z*s.conjugate(z)-1)**2
levi=s.simplify((s.diff(rho,x,2)+s.diff(rho,y,2))/4)
assert s.expand(levi-(4*(x*x+y*y)-2))==0
out={'strict_peak_real_part':str(peak),'peak_remainder':str(u*(u-s.Rational(1,2))),'torus_factor_levi':str(levi),'all_assertions_passed':True}
Path('workspace/agent1_verified_partial.txt').write_text(str(out))
print(out)
