"""Exact polynomial-moment telescoper for boundary graph shape Hessians."""
import sympy as s
j,n=s.symbols('j n')
def endpoints(P,nvalue=None):
    """Solve [(j+n-1)^2 Q(j)-(j+3)^2 Q(j+2)]/(2j+n+2)=P(j).
    For l2 weights w0=1,w1=r, sum w_j P(j) equals
      (n-1)^2/(n+2)*Q(0)+r*n^2/(n+4)*Q(1).
    Valid if the moment converges, i.e. deg(P)<n-4.
    """
    nv=n if nvalue is None else s.Integer(nvalue)
    P=s.cancel(P.subs(n,nv)) if hasattr(P,'subs') else s.sympify(P)
    degree=s.degree(P,j)
    cs=s.symbols('c:'+str(degree+1))
    Q=sum(cs[k]*j**k for k in range(degree+1))
    poly=s.Poly(s.together((j+nv-1)**2*Q-(j+3)**2*Q.subs(j,j+2)-(2*j+nv+2)*P).as_numer_denom()[0],j)
    solution=s.solve(poly.all_coeffs(),cs)
    if not solution: raise ValueError('No polynomial telescoper (possibly divergent/resonant moment)')
    Q=s.factor(Q.subs(solution))
    assert s.cancel((j+nv-1)**2*Q-(j+3)**2*Q.subs(j,j+2)-(2*j+nv+2)*P)==0
    return s.factor(Q.subs(j,0)),s.factor(Q.subs(j,1))
if __name__=='__main__':
    S=(2*j*j+2*(n+2)*j+n+3)/(n-1)
    for P in [s.Integer(1),S,S*S]:print(endpoints(P))
