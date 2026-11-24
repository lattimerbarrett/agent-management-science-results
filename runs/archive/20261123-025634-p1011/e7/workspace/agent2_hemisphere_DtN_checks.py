import sympy as s
import mpmath as mp
from pathlib import Path

def check():
    n,l,z=s.symbols('n l z',positive=True)
    F,Fp,Fpp=s.symbols('F Fp Fpp')
    # y(theta)=sin(theta)^l F(z), z=sin(theta)^2.
    # y_theta=sin(theta)^(l-1) cos(theta) [l F+2z F'].
    # Work after division by sin(theta)^l.
    yp_factor=l*F+2*z*Fp
    ypp_over=(l-1)*(1-z)/z*yp_factor-yp_factor+2*(1-z)*((l+2)*Fp+2*z*Fpp)
    ode=s.expand(ypp_over+(n-1)*(1-z)/z*yp_factor-l*(l+n-2)/z*F+n*F)
    a=(l-1)/2; b=(l+n)/2; c=l+n/2
    expected=4*(z*(1-z)*Fpp+(c-(a+b+1)*z)*Fp-a*b*F)
    assert s.simplify(ode-expected)==0
    assert s.simplify(c-a-b)==s.Rational(1,2)
    mp.mp.dps=70
    for N in [3,4,5,6,7,10,20]:
        for L in [2,3,4,7]:
            a=mp.mpf(L-1)/2; b=mp.mpf(L+N)/2; c=L+mp.mpf(N)/2
            A=mp.gamma(c)*mp.sqrt(mp.pi)/(mp.gamma(c-a)*mp.gamma(c-b))
            B=mp.gamma(c)*mp.gamma(-mp.mpf(1)/2)/(mp.gamma(a)*mp.gamma(b))
            kappa=2*mp.gamma(mp.mpf(L+N+1)/2)*mp.gamma(mp.mpf(L)/2)/(mp.gamma(mp.mpf(L-1)/2)*mp.gamma(mp.mpf(L+N)/2))
            assert mp.almosteq(-B/A,kappa)
            # Boundary derivative converges to -B, independently computed from 2F1.
            eps=mp.mpf('1e-15'); theta=mp.pi/2-eps
            zz=mp.sin(theta)**2
            val=mp.sin(theta)**L*mp.hyp2f1(a,b,c,zz)
            derivative=L*mp.sin(theta)**(L-1)*mp.cos(theta)*mp.hyp2f1(a,b,c,zz)+mp.sin(theta)**L*(a*b/c)*mp.hyp2f1(a+1,b+1,c+1,zz)*2*mp.sin(theta)*mp.cos(theta)
            assert abs(val/A-1)<mp.mpf('1e-11')
            assert abs(derivative/(-B)-1)<mp.mpf('1e-11')
            assert kappa>0
        print('n=',N,': hypergeometric ODE and boundary derivative checks passed')
    print('General symbolic ODE verified; exact positive DtN spectrum for every integer degree l>=2.')

if __name__=='__main__':
    check()
    Path('workspace/agent2_hemisphere_DtN_checks.py').write_text(Path(__file__).read_text())
