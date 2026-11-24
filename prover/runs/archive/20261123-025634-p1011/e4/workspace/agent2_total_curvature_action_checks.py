import sympy as S
n,t,h,A,C,lap=S.symbols('n t h A C lap',real=True)
m=n-1; ss=t*h; sec2=1/S.cos(ss)**2; W=S.sqrt(1+t*t*A*sec2)
H=m*S.tan(ss)/W+t*sec2*lap/W+t*t*A*sec2*S.tan(ss)/W**3-t**3*sec2**2*C/W**3
area=S.cos(ss)**m*W
raw=S.series(H*area,t,0,5).removeO().expand()
expected=t*(m*h+lap)+t**3*(m*(S.Rational(1,3)-m/2)*h**3-(m-2)*h*h*lap/2+A*h-C)
assert S.simplify(raw-expected)==0
# After integration by parts: integral lap=0 and integral h²lap=-2 integral h|grad h|².
integrated_cubic=m*(S.Rational(1,3)-m/2)*h**3+(m-1)*A*h-C
actual_cubic=S.expand(raw).coeff(t,3).subs(lap,-2*A/h)
assert S.simplify(actual_cubic-integrated_cubic)==0
beta=(n-2)/(2*(n-1)); vol_coeff=(n-2)/4
assert S.simplify(-vol_coeff+beta*m/2)==0
print('PASS: exact total-mean-curvature density through cubic order')
print('PASS: integrated cubic and first-action-variation cancellation')
print('Integrated H cubic:',S.factor(integrated_cubic))
