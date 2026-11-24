import sympy as s,json,os,shutil
from pathlib import Path
n,r2,H,XH,DH=s.symbols('n r2 H XH DH',positive=True)
m=n-1;a=(n-2)/2;Omega=2/(1+r2);c=(n-2)/(4*m);u0=2**(-a)
# spherical boundary Laplacian of Omega*h in m=n-1 dimensions.
# grad Omega=-Omega^2 x, Delta Omega=-m Omega^2+2 Omega^3 r2.
lap_f=Omega*DH-2*Omega**2*XH+H*(-m*Omega**2+2*Omega**3*r2)
drift=(m-2)*(-Omega**2*XH+Omega**3*r2*H)
Tf=s.expand((lap_f+drift)/Omega**2+m*Omega*H)
assert s.simplify(Tf-(DH/Omega+m*(H-XH)))==0
Ae=(n-2)*u0*Omega**a*((H-XH)/(1+r2)+DH/(2*m))
As=2*c*u0*Tf
assert s.simplify(Ae/Omega**(a+1)-As)==0
# Jacobi coefficient exactly n, with no dimension shift.
assert s.simplify(-n*(n-2)/4+n*(n+2)/4-n)==0
C=2*c**2*u0**2
assert s.simplify(C-(n-2)**2/(2**(n+1)*(n-1)**2))==0
ell=s.symbols('ell',integer=True,positive=True)
assert s.factor(ell*(ell+n-2)-(n-1))==(ell-1)*(ell+n-1)
print('Exact source transformation: A_e/Omega^(n/2)=2 c_n u0 (Delta_boundary+n-1)(Omega*h).')
print('Exact reduced coefficient: F=-[(n-2)^2/(2^(n+1)(n-1)^2)]*K; no parameter dependence.')
Path('workspace/agent3_source_sphere_audit.md').write_text(r'''# Independent source-to-sphere audit
Put m=n-1, a=(n-2)/2, Omega=2/(1+r^2), u0=2^{-a}.
The unit round metric is g_s=Omega^2 delta and U=Omega^a u0.
For arbitrary h, let f=Omega h (INWARD spherical normal displacement).
Because the graph z=th moves inward from the upper halfspace,
H_s'=+(Delta_{S^{n-1}}+m)f.

Direct calculation with the boundary conformal Laplacian gives
 (Delta_{S^{n-1}}+m)(Omega h)
 =Omega^{-1}Delta' h+m(h-x.Dh).
Indeed gradOmega=-Omega^2 x and Delta'Omega=-m Omega^2+2Omega^3 r^2.
The boundary residual in Euclidean coordinates is
 A_e=(n-2)U[(h-x.Dh)/(1+r^2)+Delta'h/(2m)].
Therefore exactly
 Omega^{-n/2} A_e=2c_n u0(Delta_boundary+m)f.
This also follows directly from Robin conformal covariance.

The linearized interior operator about u0 on unit S^n is
 Delta-c_n n(n-1)+n(n+2)u0^{4/(n-2)}=Delta+n.
Thus the unit-sphere Jacobi form is Q_s(z)=int(|grad z|^2-nz^2).
The correction solves (Delta+n)z=0, partial_nu z=-g,
where g=2c_n u0(Delta_boundary+m)f.
For boundary harmonic degree ell>=2,
 kappa_ell=(1/2)Gamma((ell-1)/2)Gamma((ell+n)/2)
 /[Gamma((ell+n+1)/2)Gamma(ell/2)]
is the Neumann-to-Dirichlet eigenvalue.
Consequently the reduced second coefficient is exactly
 F=-C_n sum_{ell>=2}((ell-1)(ell+n-1))^2 kappa_ell ||f_ell||^2,
 C_n=2c_n^2u0^2=(n-2)^2/[2^{n+1}(n-1)^2]>0.
Degree0 contributes0 (its regular radial solution has zero boundary trace),
and degree1 is the conformal kernel (source coefficient0).

For bubble parameters xi,epsilon use x=xi+epsilon y and
v(y)=epsilon^a u(xi+epsilon y). Critical Euclidean energy is invariant;
the graph becomes y_n>t epsilon^{-1}h(xi+epsilon y'). Thus
f_{xi,epsilon}=Omega(y)epsilon^{-1}h(xi+epsilon y') and the SAME positive
C_n applies for every xi,epsilon. No scale-dependent prefactor appears.

The boundary sphere is S^{n-1}, its harmonic eigenvalues are
ell(ell+n-2), and ell(ell+n-2)-(n-1)=(ell-1)(ell+n-1).
There is no n-to-n+2 index shift.

All algebraic identities above checked exactly by SymPy in
agent3_source_sphere_audit.py. The hypergeometric ODE and near-equator
ratio were independently checked in agent3_jacobi_check.py.
''')
if os.path.abspath(__file__)!=os.path.abspath('workspace/agent3_source_sphere_audit.py'):shutil.copyfile(__file__,'workspace/agent3_source_sphere_audit.py')
