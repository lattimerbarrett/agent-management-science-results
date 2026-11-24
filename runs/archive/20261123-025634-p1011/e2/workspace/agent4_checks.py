import sympy as s
from pathlib import Path
# Symbolic verifications use a=(n-2)/2 and n=2*a+2.
a,lam,r,R=s.symbols('a lam r R',positive=True)
n=2*a+2
U=(lam/(lam**2+r**2))**a
lap=s.diff(U,r,2)+(n-1)*s.diff(U,r)/r
p=1+2/a
# Avoid ambiguous symbolic power simplification: U^p = U * lam^2/(lam^2+r^2)^2.
interior=s.factor(lap+n*(n-2)*U*lam**2/(lam**2+r**2)**2)
assert interior==0
# Centered bubble on ball of radius R: outward derivative + 2*c*H U.
boundary=s.factor((s.diff(U,r)+a/R*U).subs(r,R)/U.subs(r,R))
assert s.factor(boundary-a*(lam**2-R**2)/(R*(lam**2+R**2)))==0
# Off-center bubble |x|=R, center xi: r^2=R^2+|xi|^2-2x.xi.
t,q=s.symbols('t q',real=True)
offcenter=s.factor(-2*a*(R**2-t)/(R*(lam**2+R**2+q-2*t))+a/R)
assert s.factor(offcenter-a*(lam**2+q-R**2)/(R*(lam**2+R**2+q-2*t)))==0
# Metric ghat=e^(2f)g: Hhat=e^-f(H+(n-1)nu(f)),
# uhat=e^-a*f u. Both cross terms cancel in Bhat uhat.
f,df,u,du,H=s.symbols('f df u du H',real=True)
Bhat=s.exp(-(a+1)*f)*(du-a*df*u+a/(n-1)*(H+(n-1)*df)*u)
B=s.exp(-(a+1)*f)*(du+a/(n-1)*H*u)
assert s.simplify(Bhat-B)==0
print('PASS: interior bubble identity, all symbolic n=2a+2>2')
print('PASS: centered and off-center ball boundary identities')
print('PASS: conformal Robin cancellation, H is trace convention')
print('Boundary logarithmic residual on |x|=R:',offcenter)
Path('workspace').mkdir(exist_ok=True)
Path('workspace/agent4_checks.py').write_text(Path('scratchpad.py').read_text())
