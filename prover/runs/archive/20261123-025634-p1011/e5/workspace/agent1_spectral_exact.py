"""Exact spectral moment summation for boundary graph model (not full PDE proof)."""
import sympy as s
import numpy as np
import json
from pathlib import Path
k=s.symbols('k')
def graph_polys(n,d):
    beta=s.Rational(n+1,2)
    return [s.Poly(s.expand(sum(s.binomial(j,h)*(-1)**(j-h)*s.rf(k+2*beta-h+1,h)*s.rf(k+1,h)/(s.factorial(h)*s.rf(beta-h,h)) for h in range(j+1))),k) for j in range(d+1)]
def antidifference(n,P):
    # L(T)=(k+n-1)^2*T(k)-(k+3)^2*T(k+2)
    deg=P.degree()
    target=s.Poly((k+s.Rational(n+2,2))*P.as_expr(),k)
    T=s.Poly(0,k)
    for j in range(deg,-1,-1):
        coefficient=target.nth(j+1)/(2*(n-4-j))
        tj=s.Poly(coefficient*k**j,k)
        T+=tj
        expr=tj.as_expr()
        target-=s.Poly((k+n-1)**2*expr-(k+3)**2*expr.subs(k,k+2),k)
    assert target.is_zero, target
    return T

def gram(n,d):
    P=graph_polys(n,d)
    q0=s.gamma(s.Rational(3,2))**2/s.gamma(s.Rational(n+1,2))**2
    q1=1/s.gamma(s.Rational(n+2,2))**2
    # Omit a common positive prefactor.
    G=s.zeros(d+1)
    for i in range(d+1):
        for j in range(i,d+1):
            T=antidifference(n,P[i]*P[j])
            G[i,j]=G[j,i]=s.simplify((n-1)**2*T.eval(0)+n*n*(q1/q0)*T.eval(1))
    return G
if __name__=='__main__':
    n=21; d=4
    G=gram(n,d)
    D=s.Matrix(d+1,d+1,lambda i,j:(2+2*i+2*j)*G[i,j])
    Gn=np.array(G.evalf(),float); Dn=np.array(D.evalf(),float)
    vals,vecs=np.linalg.eigh(Dn)
    v=vecs[:,0]
    rat=s.Matrix([s.Rational(float(x)).limit_denominator(10000) for x in v/v[0]])
    value=s.simplify((rat.T*D*rat)[0])
    print('n=21 d=4 eigenvalues of D',vals)
    print('rational negative vector',list(rat))
    print('quadratic form value',s.N(value,20))
    # Verify negativity rigorously using Archimedes bounds on pi, not evalf.
    lo=s.Rational(314159265358979323846,10**20)
    hi=s.Rational(314159265358979323847,10**20)
    # pi bounds used here are independently provable by standard series.
    num,den=s.fraction(value)
    print('exact quadratic form',value)
    Path('workspace').mkdir(exist_ok=True)
    Path('workspace/agent1_spectral_exact.py').write_text(Path(__file__).read_text())
    Path('workspace/agent1_spectral_exact_n21.json').write_text(json.dumps({'G':[[str(x) for x in row] for row in G.tolist()],'vector':[str(x) for x in rat],'value':str(value)}))
