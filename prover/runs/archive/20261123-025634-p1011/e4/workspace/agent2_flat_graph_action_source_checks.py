"""Exact identities behind the flat-graph source/action estimates."""
import sympy as S
n,r,z,s,h,zh,grad2,lap,C=S.symbols('n r z s h zh grad2 lap C',positive=True)
U=(1+r*r+z*z)**(-(n-2)/2)
k=n*(n-2);q=2*n/(n-2);beta=(n-2)/(2*(n-1))
F=(n-2)**2/S.Integer(2)*(r*r+z*z-1)*(1+r*r+z*z)**(-n)
actual=S.diff(U,r)**2/2+S.diff(U,z)**2/2-(n-2)**2/S.Integer(2)*(1+r*r+z*z)**(-n)
assert S.simplify(F-actual)==0
U02=(1+r*r)**(-(n-2))
lap_boundary=S.diff(U02,r,2)+(n-2)/r*S.diff(U02,r)
assert S.simplify(F.subs(z,0)-beta*lap_boundary/2)==0
W=S.sqrt(1+s*s*grad2)
normal=(n-2)*s*(h-zh)*(1+r*r+s*s*h*h)**(-n/2)/W
H=s*lap/W-s**3*C/W**3
residual=normal+beta*H*U.subs(z,s*h)
linear=(n-2)*(h-zh)*(1+r*r)**(-n/2)+beta*lap*(1+r*r)**(-(n-2)/2)
assert S.simplify(S.diff(residual,s).subs(s,0)-linear)==0
assert S.simplify(residual.subs(s,-s)+residual)==0
assert S.simplify(H*W-(s*lap-s**3*C/(1+s*s*grad2)))==0
p=2*(n-1)/n
assert S.simplify((n-1+p*(8-n))/p-(8-n/2))==0
print('PASS: exact bubble bulk-action density')
print('PASS: exact linear shape cancellation F0=beta*Delta(U0²)/2')
print('PASS: exact flat graph Robin residual, oddness, H*dA identity')
print('PASS: boundary-source Lp tail exponent 8-n/2')
