import sys
sys.path.insert(0,'workspace')
from agent4_exact_angular_gram import exact_grams
import sympy as S
from pathlib import Path
nn=20; dd=nn-1
GG=exact_grams(nn); G1,G2,G3=GG[1],GG[2],GG[3]
assert all(v.is_Rational for G in GG.values() for v in G)
x,t=S.symbols('x t')
a=S.Matrix([1,-S.Rational(2,5),S.Rational(9,200),-S.Rational(9,8000)])
v=S.Matrix([a[k]*x**k for k in range(4)])
H=S.Matrix(4,4,lambda k,l:(k+l+1)*G2[k,l])
HH=S.factor((v.T*H*v)[0]/G2[0,0])
Q=S.factor(x*(v.T*G2*v)[0]/G2[0,0])
assert S.simplify(S.diff(Q,x)-HH)==0

def trans(rho):
    B=S.zeros(4)
    for k in range(4):
        for l in range(4):
            ck=1+S.Rational(2*k,dd+2);cl=1+S.Rational(2*l,dd+2)
            B[k,l]=2*(dd+2)*rho*ck*cl*G1[k,l]
            if k and l:B[k,l]+=4*(S.Rational(1,dd+4)+S.Rational(2*dd,(dd+2)*(dd+4))*rho)*k*l*G3[k-1,l-1]
            if l:B[k,l]+=l*(2+8*rho+S.Rational(4*(l-1),dd+4)*(1+4*rho))*G2[k,l-1]
    return S.factor((v.T*B*v)[0]/G2[0,0])

left,right=S.Rational(19,20),S.Rational(11,10)
def bernstein_coeffs(poly):
    pp=S.Poly(S.expand(poly.subs(x,left+(right-left)*t)),t)
    degree=pp.degree()
    return [S.factor(sum(pp.nth(i)*S.binomial(k,i)/S.binomial(degree,i) for i in range(k+1))) for k in range(degree+1)]
assert HH.subs(x,left)>0
assert HH.subs(x,right)<0
bcurv=bernstein_coeffs(S.diff(HH,x))
print('n20 exact H endpoints:',HH.subs(x,left),HH.subs(x,right))
print('H derivative Bernstein signs:',[S.sign(vv) for vv in bcurv])
assert all(vv<0 for vv in bcurv)
for rho in [S.Rational(10,171),S.Rational(9,190)]:
    BB=trans(rho)
    bb=bernstein_coeffs(BB)
    print('rho',rho,'translation Bernstein signs:',[S.sign(vv) for vv in bb])
    assert all(vv<0 for vv in bb)
print('EXACT ALGEBRA CERTIFICATE: unique scale root x in [19/20,11/10], Q second derivative<0 and both translation brackets<0 throughout.')
Path('workspace/agent4_n20_exact_minimum.py').write_text(Path(__file__).read_text())
