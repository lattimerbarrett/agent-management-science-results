import sympy as s
import numpy as np
from pathlib import Path

def exact_gram(n,J):
    """Exact scalar shape Gram up to a common positive factor; n>4J+4."""
    a=s.Rational(n+2,2); z=s.symbols('z'); U=[s.Integer(1)]
    for j in range(1,2*J+1):
        U.append(s.expand(U[-1]*(z-(a-3-2*(j-1))**2)))
    b=[]
    for j in range(J+1):
        p=s.Integer(1);v=s.Integer(0)
        for r in range(j+1):
            if r: p=s.expand(p*(z-(a-r)**2))
            v+=(-1)**(j-r)*s.binomial(j,r)*p/(s.factorial(r)*s.rf(a-s.Rational(1,2)-r,r))
        b.append(s.expand(v))
    moments=[]
    for r in range(2*J+1):
        assert a>3+r
        E=s.gamma(s.Rational(3,2))*s.gamma(s.Rational(3,2)+r)/(s.gamma(a-s.Rational(3,2))*s.gamma(a-s.Rational(3,2)-r))
        O=s.gamma(2)*s.gamma(2+r)/(s.gamma(a-1)*s.gamma(a-1-r))
        moments.append(s.simplify(4**r*(E+O)/(a-3-r)))
    G=s.zeros(J+1)
    for i in range(J+1):
        for j in range(i,J+1):
            p=s.Poly(b[i]*b[j],z);value=0
            for r in range(i+j,-1,-1):
                c=p.nth(r);value+=c*moments[r];p=s.Poly(p.as_expr()-c*U[r],z)
            assert p.as_expr()==0
            G[i,j]=G[j,i]=s.simplify(value)
    return G

def normalized(G):
    A=np.array(G.evalf(),float)
    return A/np.sqrt(np.diag(A)[:,None]*np.diag(A)[None,:])

if __name__=='__main__':
    import sys
    sys.path.insert(0,'workspace')
    from agent4_spectral_experiment import gram
    for n in [24,25,30]:
        E=normalized(exact_gram(n,2))
        B=gram(n,J=2,Q=350,N=1000)
        B=B/np.sqrt(np.diag(B)[:,None]*np.diag(B)[None,:])
        error=np.max(np.abs(E-B))
        assert error<1e-10
        print(n,'exact Gram vs independent quadrature maximum difference:',error)
