"""Exact checks for the critical Pohozaev identity and Robin reduction.
No check here proves compactness or the dimension threshold.
Run with Python+SymPy. All equalities are symbolic, no sampling.
"""
import sympy as S

def check_divergence(n):
    # Coefficients of formal monomials after differentiating the flux.
    # A = X.grad u, G = |grad u|^2, T = Delta u,
    # C = sum_ij x_j (partial_ij u)(partial_i u).
    u,A,G,T,C=S.symbols('u A G T C', positive=True)
    s=S.Rational(n-2,2)
    k=S.Integer(n*(n-2))
    q=S.Rational(2*n,n-2)
    F=k/q*u**q
    # div[(X.grad u)grad u - |grad u|^2 X/2 + s*u*grad u + F X]
    div=(G+C+A*T) - (S.Rational(n,2)*G+C) + s*(G+u*T) + n*F+k*u**(q-1)*A
    target=(A+s*u)*(T+k*u**(q-1))
    assert S.simplify(div-target)==0

def check_robin():
    n=S.symbols('n', integer=True, positive=True)
    beta,H,z,u,b,d,G,F=S.symbols('beta H z u b d G F')
    # z=X.nu, b=X^T.grad_boundary beta, d=X^T.grad_boundary u,
    # G=|grad_boundary u|^2.  Partial_nu u=-beta*u.
    raw=(d-z*beta*u)*(-beta*u)-z*(G+beta**2*u**2)/2-(n-2)*beta*u**2/2+z*F
    # Integration by parts: -beta*u*d -> (b+beta*div_boundary X^T)*u^2/2.
    # div_boundary X^T=(n-1)-H*z.
    integrated=S.expand(raw+beta*u*d+(b+beta*(n-1-H*z))*u**2/2)
    target=(b+beta+(beta**2-beta*H)*z)*u**2/2-z*G/2+z*F
    assert S.simplify(integrated-target)==0
    a=(n-2)/(2*(n-1))
    assert S.simplify((a*H)**2-a*H**2+n*(n-2)*H**2/(4*(n-1)**2))==0
    # Unit sphere, centered unit-scale bubble: z=1,H=n-1,b=G=0,
    # u^(q-2)=1/4, beta=(n-2)/2; the boundary integrand is zero.
    s=(n-2)/2
    normalized=target.subs({b:0,beta:s,H:n-1,z:1,G:0,F:(n-2)**2*u**2/8})
    assert S.simplify(normalized)==0

if __name__=='__main__':
    for n in range(3,61):
        check_divergence(n)
    check_robin()
    print('Verified critical Pohozaev divergence for every integer n=3,...,60.')
    print('Verified Robin integration-by-parts reduction for symbolic n.')
    print('Verified centered unit-ball bubble normalization for symbolic n.')
