import sympy as s
import mpmath as mp
from pathlib import Path

# The coordinate expression for the O(a) pullback of an ambient radial bubble.
# This calculation checks a genuine dimension-seven integrability threshold;
# it does not establish a nonlinear gluing result.
def check():
    mp.mp.dps=40
    n=s.symbols('n', positive=True)
    gamma_form=(n-2)**2*s.pi**(n/2)*s.gamma((n-6)/2)/(4*s.gamma(n))
    raw=(n-2)**2 * 4/(n*(n+2)*(n+4))*s.pi**(n/2)/s.gamma(n/2)*s.gamma((n+6)/2)*s.gamma((n-6)/2)/(2*s.gamma(n))
    assert s.simplify(s.expand_func(raw/gamma_form))==1
    for N in range(7,15):
        angular=4*mp.pi**(mp.mpf(N)/2)/(mp.gamma(mp.mpf(N)/2)*N*(N+2)*(N+4))
        radial=mp.quad(lambda r:r**(N+5)/(1+r*r)**N,[0,1,mp.inf])
        numerical=(N-2)**2*angular*radial
        exact=(N-2)**2*mp.pi**(mp.mpf(N)/2)*mp.gamma(mp.mpf(N-6)/2)/(4*mp.gamma(N))
        assert mp.almosteq(numerical,exact)
        print(f'n={N}: squared L2 norm = {mp.nstr(exact,16)}; quadrature verified')
    # Exact radial tail power implies convergence iff 5-n < -1.
    assert [N for N in range(3,15) if 5-N < -1]==list(range(7,15))
    # Spherical angular factor checked by Gaussian moments in all sample dimensions.
    for N in range(3,15):
        # E[(theta_1^2-theta_2^2)^2 theta_n^2]
        moment=(s.rf(s.Rational(1,2),2)*s.Rational(1,2)*2 - 2*s.Rational(1,2)**3)/s.rf(s.Rational(N,2),3)
        assert s.simplify(moment-s.Rational(4,N*(N+2)*(N+4)))==0
    print('Angular factor, gamma identity, and exact integrability threshold verified.')
    A=(n+6)/2
    def beta_symbolic(a,b):
        return s.gamma(a)*s.gamma(b)/s.gamma(a+b)
    cubic_radial=(16*beta_symbolic(A,(n-2)/2)+8*(4-n)*beta_symbolic(A+1,(n-4)/2)+(4-n)**2*beta_symbolic(A+2,(n-6)/2)+4*(n+2)*beta_symbolic(A,(n-6)/2))/2
    cubic_angular=24*s.pi**(n/2)/(s.gamma(n/2)*n*(n+2)*(n+4)*(n+6))
    print('Cubic energy closed form:', s.simplify(s.expand_func((n-2)**2*cubic_angular*cubic_radial)))
    # Cubic graph f=x1^3-3*x1*x2^2: P=f*t is harmonic homogeneous degree 4.
    # Angular energy eigenvalue l(l+n-2)=4(n+2).
    # Its graph pullback correction f*U_t has finite Dirichlet energy iff n>6.
    for N in range(7,15):
        N=mp.mpf(N)
        C=24*mp.pi**(N/2)/(mp.gamma(N/2)*N*(N+2)*(N+4)*(N+6))
        R=lambda r:r**4/(1+r*r)**(N/2)
        Rp=lambda r:r**3*(4+(4-N)*r*r)/(1+r*r)**(N/2+1)
        value=(N-2)**2*C*mp.quad(lambda r:(Rp(r)**2+4*(N+2)*R(r)**2/r**2)*r**(N-1),[0,1,mp.inf])
        beta=lambda a,b:mp.gamma(a)*mp.gamma(b)/mp.gamma(a+b)
        radial=(16*beta((N+6)/2,(N-2)/2)+8*(4-N)*beta((N+8)/2,(N-4)/2)+(4-N)**2*beta((N+10)/2,(N-6)/2)+4*(N+2)*beta((N+6)/2,(N-6)/2))/2
        exact=(N-2)**2*C*radial
        assert mp.almosteq(value,exact)
        print(f'n={int(N)}: cubic correction Dirichlet norm squared={mp.nstr(exact,16)}; quadrature verified')

if __name__=='__main__':
    check()
    Path('workspace/agent2_graph_correction_checks.py').write_text(Path(__file__).read_text())
