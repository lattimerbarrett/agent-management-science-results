"""Check coefficients in the exact critical Robin Pohozaev identity.
T=(x.grad u+a u)grad u - |grad u|² x/2 + N u^(p+1)x/(p+1).
On a boundary piece Sigma, write X=x.nu, m=n-1, and du/dnu=-beta H u.
Integrate -beta H u x^T.grad_Sigma u by parts, using
 div_Sigma(x^T)=m-XH. The rim term is -beta H x^T.eta u²/2.
"""
import sympy as s
n,beta,H,X,u,g2,hder=s.symbols('n beta H X u g2 hder')
a=(n-2)/2;m=n-1;p=(n+2)/(n-2)
assert s.simplify(1+a-n/2)==0
assert s.simplify(n/(p+1)-a)==0
# g2 denotes tangential gradient norm squared.
# After the tangential integration by parts, before coefficient simplification:
flux=beta*s.Rational(1,2)*(hder+H*(m-X*H))*u*u+beta**2*H*H*X*u*u-a*beta*H*u*u-X*(g2+beta**2*H*H*u*u)/2
expected=beta*(H+hder)*u*u/2+beta*(beta-1)*X*H*H*u*u/2-X*g2/2
assert s.expand(flux-expected)==0
# Potential term N/(p+1)X u^(p+1) simply carries through unchanged.
print('Exact critical-stress and integrated Robin-boundary flux coefficients checked.')
