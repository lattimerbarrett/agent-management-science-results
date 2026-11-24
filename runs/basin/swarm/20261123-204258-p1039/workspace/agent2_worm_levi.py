import sympy as s
from pathlib import Path
x,y,h,hp,hpp=s.symbols('x y h hp hpp',real=True)
raw=hp**2-2*hp*y+(2*x+hpp)*(1-h)
squares=(hp-y)**2+(x-h)**2+h*(1-h)+hpp*(1-h)
relation=x*x+y*y-2*x+h
assert s.expand(squares-raw-relation)==0
# Thus on the worm boundary relation=0 the Levi numerator is a sum of squares
# plus nonnegative h(1-h)+hpp(1-h), whenever 0<=h<=1 and hpp>=0.
z,zb,w,wb=s.symbols('z zb w wb')
t=s.log(w*wb)
eta=h+hp*t+hpp*t*t/2
rho=z*zb-z*s.exp(-s.I*t)-zb*s.exp(s.I*t)+eta
L=s.Matrix([[s.diff(rho,a,b) for b in (zb,wb)] for a in (z,w)])
T=s.Matrix([s.diff(rho,w),-s.diff(rho,z)])
subs={w:1,wb:1,z:x+s.I*y,zb:x-s.I*y}
L0=s.simplify(L.subs(subs))
T0=s.simplify(T.subs(subs))
# L(v)=sum L_jk v_j conjugate(v_k), so use transpose, not conjugate transpose.
levi=s.simplify((T0.T*L0*s.conjugate(T0))[0])
assert s.simplify(levi-(hp**2-2*hp*y+(2*x+hpp)*((x-1)**2+y*y)))==0
assert s.simplify(s.expand(levi-raw).subs(y*y,2*x-h-x*x))==0
print('PASS: exact pseudoconvex worm Levi sum-of-squares identity and Wirtinger differentiation')
Path('workspace/agent2_worm_levi.py').write_text(Path(__file__).read_text())
