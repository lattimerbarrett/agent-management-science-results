"""Independent exact beta-integral verification of polynomial Gegenbauer moments.
Checks ell=0,...,5, three radial powers each and five Gegenbauer modes each
at n=18; exact symbolic identities, not numerical quadrature.
"""
import sympy as s
u=s.symbols('u')
def exact_moment(n,ell,j,M):
    alpha=s.Rational(n+2*ell-2,2);beta=alpha-s.Rational(1,2)
    cp=s.Poly(s.expand(s.gegenbauer(M,alpha,1-2*u)),u)
    a=beta-ell-j+1;b=beta+j
    return s.simplify(2**(2*beta+2-ell)*sum(coef*s.gamma(a+q+1)*s.gamma(b+1)/s.gamma(a+b+q+2) for (q,),coef in cp.terms()))
def predicted(n,ell,j,M):
    t=M+ell-2
    if ell>=2:
        D=s.rf(t-ell+3,ell-2)*s.rf(t+n+2,ell-2)
        return D*sum((-1)**(j-a)*s.binomial(j,a)*s.rf(t+1,a)*s.rf(t+n+2-a,a)/(s.rf(ell-1,a)*s.prod(s.Rational(n+1,2)-h for h in range(1,a+1))) for a in range(j+1))
    if ell==1:
        return sum((-1)**(j-1-a)*s.binomial(j,a+1)*s.rf(t+2,a)*s.rf(t+n+1-a,a)/(s.factorial(a)*s.prod(s.Rational(n-1,2)-h for h in range(1,a+1))) for a in range(j))
    return sum((-1)**(j-2-a)*s.binomial(j,a+2)*s.rf(t+3,a)*s.rf(t+n-a,a)/(s.factorial(a)*s.prod(s.Rational(n-3,2)-h for h in range(1,a+1))) for a in range(j-1))
if __name__=='__main__':
    count=0
    for ell in range(0,6):
        n=18;jstart=2 if ell==0 else 1 if ell==1 else 0;mstart=max(2-ell,0)
        ratio=None
        for j in range(jstart,jstart+3):
            for M in range(mstart,mstart+5):
                pred=predicted(n,ell,j,M);val=exact_moment(n,ell,j,M)
                if pred==0:assert val==0
                else:
                    r=s.simplify(val/pred)
                    if ratio is None:ratio=r
                    assert s.simplify(r-ratio)==0
                count+=1
        print('Exact beta-integral verification ell=',ell,'normalization',ratio)
    print('Moment identities checked:',count)
