import sympy as s
n=s.Integer(18);d=s.Integer(9);m=n-1
print('n=18, critical graph degree d=9; radial energy exponent:',2*d-n-1)
print('j, angular degree ell, Robin source coefficient kappa, critical DtN, positive log-energy coefficient / pi')
for j in range(5):
    ell=d-2*j
    kappa=s.simplify(1-d+s.Rational(j)*(2*ell+m+2*j-2)/m)
    # On S^17_+: (Delta_S-64) phi=0; source=(n-2)*kappa*P_ell.
    T=s.simplify(2*s.gamma((ell+9)/2)**2/s.gamma((ell+8)/2)**2)
    logcoef=s.simplify(((n-2)*kappa)**2/T)
    print(j,ell,kappa,T,s.simplify(logcoef/s.pi))
    assert kappa!=0 and T>0 and logcoef>0
print('Every critical sector is strictly positive; no gauge sector occurs at degree nine.')
