import os
import sympy as s
os.makedirs('workspace', exist_ok=True)
n=s.symbols('n', integer=True, positive=True)
r,e=s.symbols('r e', positive=True)
a=(n-2)/2
c=(n-2)/(4*(n-1))
p=(n+2)/(n-2)
U=(e/(e**2+r**2))**a
# Differentiate logarithm to avoid symbolic power-branch ambiguity.
logder=-(n-2)*r/(e**2+r**2)
laplacian_over_U=s.factor(s.diff(logder,r)+logder**2+(n-1)*logder/r)
assert s.factor(laplacian_over_U+n*(n-2)*e**2/(e**2+r**2)**2)==0
assert s.factor(c*4*n*(n-1)-n*(n-2))==0
# General conformal scalar-curvature formula, h=exp(2f)g,
# f=2 log u/(n-2). Treat log-Laplacian and gradient formally.
u, lapu, grad2=s.symbols('u lapu grad2', positive=True)
lapf=2/(n-2)*(lapu/u-grad2/u**2)
gradf2=4/(n-2)**2*grad2/u**2
scalar_correction=s.expand(-2*(n-1)*lapf-(n-1)*(n-2)*gradf2)
assert s.simplify(scalar_correction+lapu/(c*u))==0
# Boundary conformal formula H_h=e^(-f)(H+(n-1)nu(f)).
H, nuu=s.symbols('H nuu')
assert s.simplify(H+2*(n-1)/(n-2)*nuu/u-(nuu+2*c*H*u)/(2*c*u))==0
report={
 'bubble_laplacian_divided_by_U':str(laplacian_over_U),
 'target_scalar_curvature':str(s.factor(n*(n-2)/c)),
 'conformal_scalar_correction':str(s.factor(scalar_correction)),
 'positive_eigenvalue_lower_bound':'n*(n-2)*min_M(u)**(4/(n-2))',
}
for k,v in report.items():print(k, '=', v)
# Pointwise identity behind Picone's ground-state transformation.
v, gu2, gv2, cross=s.symbols('v gu2 gv2 cross', real=True)
u2_grad_ratio2=gv2-2*v/u*cross+v**2/u**2*gu2
cross_term=2*v/u*cross-v**2/u**2*gu2
assert s.expand(gv2-u2_grad_ratio2-cross_term)==0
# Gamma quotient for the hemisphere Dirichlet-to-Neumann operator.
l=s.symbols('l', positive=True)
A=(l-1)/2
BB=(l+n)/2
C=l+n/2
assert s.simplify(C-A-BB-s.Rational(1,2))==0
assert s.simplify(C-A-(l+n+1)/2)==0
assert s.simplify(C-BB-l/2)==0
assert s.simplify(-s.gamma(-s.Rational(1,2))/s.gamma(s.Rational(1,2))-2)==0
# Numerical check against the defining hypergeometric solution, not the quotient.
import mpmath as mp
mp.mp.dps=60
maxrel=mp.mpf(0)
for N in (3, 7, 18, 19, 30):
    for ell in (2, 3, 4, 7):
        aa=mp.mpf(ell-1)/2; bb=mp.mpf(ell+N)/2; cc=mp.mpf(ell)+mp.mpf(N)/2
        val0=mp.gamma(cc)*mp.gamma(mp.mpf('0.5'))/(mp.gamma(cc-aa)*mp.gamma(cc-bb))
        t=mp.mpf('1e-15')
        def extension(tt):
            return mp.cos(tt)**ell*mp.hyp2f1(aa,bb,cc,mp.cos(tt)**2)
        numeric=-mp.diff(extension,t)/val0
        quotient=2*mp.gamma(mp.mpf(ell+N+1)/2)*mp.gamma(mp.mpf(ell)/2)/(mp.gamma(mp.mpf(ell-1)/2)*mp.gamma(mp.mpf(ell+N)/2))
        rel=abs(numeric/quotient-1)
        assert rel<mp.mpf('1e-12'), (N,ell,rel)
        maxrel=max(maxrel,rel)
print('DtN hypergeometric numerical checks: 20 passed; max relative error',mp.nstr(maxrel,6))
