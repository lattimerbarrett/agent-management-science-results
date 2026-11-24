"""Checks for round-hemisphere Yamabe shape Hessian. No compactness claim."""
import sympy as s
import mpmath as mp
n=s.symbols('n', positive=True)
a=4*(n-1)/(n-2); R=n*(n-1); q=2*n/(n-2); b=(n-2)/n
assert s.simplify(2*R-b*R*q*(q-1)+2*a*n)==0
assert s.simplify(4*R-2*b*R*q)==0
assert s.simplify(8/a-2*(n-2)/(n-1))==0
ell=s.symbols('ell', positive=True)
A=(ell-1)/2; B=(ell+n)/2; C=ell+n/2
assert s.simplify(C-A-B-s.Rational(1,2))==0
assert s.simplify(C-A-(ell+n+1)/2)==0
assert s.simplify(C-B-ell/2)==0
mp.mp.dps=50
for N in range(3,12):
    for L in range(2,9):
        aa=mp.mpf(L-1)/2; bb=mp.mpf(L+N)/2; cc=L+mp.mpf(N)/2
        mu=2*mp.gamma(mp.mpf(L)/2)*mp.gamma(mp.mpf(L+N+1)/2)/(mp.gamma(mp.mpf(L-1)/2)*mp.gamma(mp.mpf(L+N)/2))
        # Hypergeometric regular solution near hemisphere pole; finite-difference outward derivative.
        def f(theta): return mp.sin(theta)**L * mp.hyp2f1(aa,bb,cc,mp.sin(theta)**2)
        # 1-z approaches zero quadratically; one-sided derivative converges linearly.
        h=mp.mpf('1e-10'); t=mp.pi/2
        quotient=(f(t-h)-f(t-2*h))/(h*f(t))
        assert abs(quotient-mu)<mp.mpf('2e-7'), (N,L,quotient,mu)
print('PASS: symbolic Hessian constants, hypergeometric parameters; 63 numerical DN checks.')
print('Hessian = -[2(n-2)/(n-1)] Vol(S^n_+)^(-(n-2)/n) sum_{ell>=2} ((ell-1)(ell+n-1))^2/mu_ell * ||f_ell||^2')
print('Jet degree d has H^(3/2) threshold 2d<n; 2d=n is logarithmic.')
