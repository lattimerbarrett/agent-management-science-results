"""Checks of the hemisphere (Delta+n) Dirichlet-to-Neumann multipliers.
These spectral checks do not establish dimension-specific compactness.
"""
import sympy as S
import mpmath as mp

def check_ode():
    z=S.symbols('z', real=True)
    ell,n=S.symbols('ell n', positive=True)
    F=S.Function('F')(z)
    v=(1-z*z)**(ell/2)*F
    op=(1-z*z)*S.diff(v,z,2)-n*z*S.diff(v,z)+(n-ell*(ell+n-2)/(1-z*z))*v
    reduced=(1-z*z)*S.diff(F,z,2)-(n+2*ell)*z*S.diff(F,z)-(ell-1)*(ell+n)*F
    assert S.simplify(op/(1-z*z)**(ell/2)-reduced)==0

def check_dn(n,ell):
    a=mp.mpf(ell-1); b=mp.mpf(ell+n); c=mp.mpf(ell)+mp.mpf(n)/2
    direct=a*b/(2*c)*mp.hyp2f1(a+1,b+1,c+1,mp.mpf('.5'))/mp.hyp2f1(a,b,c,mp.mpf('.5'))
    gamma=(ell-1)*mp.gamma(mp.mpf(ell)/2)*mp.gamma(mp.mpf(ell+n+1)/2)/(mp.gamma(mp.mpf(ell+1)/2)*mp.gamma(mp.mpf(ell+n)/2))
    assert abs(direct/gamma-1)<mp.mpf('1e-65')
    assert gamma>0

if __name__=='__main__':
    check_ode()
    mp.mp.dps=80
    count=0
    for n in range(3,31):
        for ell in range(2,21):
            check_dn(n,ell)
            count+=1
    print('Symbolic hemisphere separation-of-variables ODE verified.')
    print(f'{count} hypergeometric/gamma DN identities verified to 65 relative digits.')
