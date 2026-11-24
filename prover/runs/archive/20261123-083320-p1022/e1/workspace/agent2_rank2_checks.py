import sympy as s
import json, pathlib
h,H,b,d,c,t=s.symbols('h H b d c t')
# Incidence relation H^2-hH+h^2=0; express c2 of the relative splitting.
raw=b*H*(-d*h-b*H)
reduced=s.rem(s.Poly(raw,H),s.Poly(H**2-h*H+h**2,H)).as_expr().expand()
expected=b**2*h**2-b*(b+d)*h*H
assert s.expand(reduced-expected)==0
assert s.solve([b**2-c,b*(b+d)],[b,c])==[(0,0),(-d,d**2)]
# Canonical incidence divisor (1,1) in P2 x P2*: relative canonical.
KX=-2*h-2*H
Krel=s.expand(KX+3*h)
assert Krel==h-2*H
# b=-d: Hom(S,Q tensor Omega_p).
hom_class=s.expand((-d*h+d*H)+Krel-(-d*H))
assert s.expand(hom_class-(d-1)*(-h+2*H))==0
# HRR P3: Todd=(h/(1-exp(-h)))^4 through degree 3.
todd=s.series((h/(1-s.exp(-h)))**4,h,0,4).removeO()
assert s.expand(todd-(1+2*h+s.Rational(11,6)*h**2+h**3))==0
# rank2 c1=1, c2=1, c3=0: Chern character and Euler characteristic.
ch=2+h-s.Rational(1,2)*h**2-s.Rational(1,3)*h**3
chi=s.expand(ch*todd).coeff(h,3)
assert chi==s.Rational(5,2)
# Twist by any integer gives half-integral polynomial; verify integer increments.
chi_t=s.expand(ch*todd*(1+t*h+t**2*h**2/2+t**3*h**3/6)).coeff(h,3)
# In binomial basis, the constant is 5/2 and integer differences.
values=[s.expand(chi_t.subs(t,i)) for i in range(4)]
diffs=[]
while values:
    diffs.append(values[0]); values=[values[i+1]-values[i] for i in range(len(values)-1)]
assert diffs==[s.Rational(5,2),s.Integer(8),s.Integer(7),s.Integer(2)]
result={'incidence_c2':str(reduced),'second_fundamental_class':str(hom_class),'Todd_P3':str(todd),'chi_rank2':str(chi),'chi_twist':str(chi_t),'Newton_coefficients':[str(x) for x in diffs]}
pathlib.Path('workspace').mkdir(exist_ok=True)
pathlib.Path('workspace/agent2_rank2_checks.json').write_text(json.dumps(result,indent=2))
source = pathlib.Path(__file__)
target = pathlib.Path('workspace/agent2_rank2_checks.py')
if source.resolve() != target.resolve():
    target.write_text(source.read_text())
print(json.dumps(result,indent=2))
