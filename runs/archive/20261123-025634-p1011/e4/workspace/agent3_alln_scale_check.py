"""Exact all-n>=20 SCALE bracketing for the formal shape model.
No nonlinear PDE existence or compactness theorem is asserted.
"""
import sympy as S,json,runpy
from pathlib import Path
n,y,z,t=S.symbols('n y z t')
G=S.Matrix([[S.sympify(v,locals={'n':n,'y':y}) for v in row] for row in json.loads(Path('workspace/agent3_symbolic_gram.json').read_text())])
a=[S.Integer(1),-S.Rational(2,5),S.Rational(9,200),-S.Rational(9,8000)]
H=S.factor(sum((k+l+1)*G[k,l]*a[k]*a[l]*z**(k+l) for k in range(4) for l in range(4)))
base=runpy.run_path('workspace/agent3_exact_scale_signature.py')
plo=S.Rational('3.14159');phi=S.Rational('3.1416')
assert plo<base['lo']<base['hi']<phi
# Gamma log-convexity gives n/2<r<(n+1)/2 for
# r=Gamma((n+2)/2)^2/Gamma((n+1)/2)^2.
# Thus y=4/(pi*r) is bracketed by the following rational functions.
ylo=8/(phi*(n+1));yhi=8/(plo*n)
certificates=[]
for zv,desired in [(S.Rational(19,20),1),(S.Rational(11,10),-1)]:
    for yy in [ylo,yhi]:
        expr=S.factor(H.subs({z:zv,y:yy}))
        num,den=S.fraction(expr)
        shifted_num=S.Poly(S.expand(desired*num.subs(n,t+20)),t)
        shifted_den=S.Poly(S.expand(den.subs(n,t+20)),t)
        assert all(c>0 for c in shifted_num.all_coeffs())
        assert all(c>0 for c in shifted_den.all_coeffs())
        certificates.append({'z':str(zv),'desired_sign':desired,'yendpoint':str(yy),'positive_num_coefficients':[str(c) for c in shifted_num.all_coeffs()],'positive_den_coefficients':[str(c) for c in shifted_den.all_coeffs()]})
# H is affine in y, so the endpoint signs bracket all actual gamma ratios.
Path('workspace/agent3_alln_scale_certificate.json').write_text(json.dumps(certificates))
print('Exact for every real n>=20: H(19/20)>0 and H(11/10)<0 in the formal model.')
print('Four shifted rational-function numerator/denominator coefficient tests passed.')
