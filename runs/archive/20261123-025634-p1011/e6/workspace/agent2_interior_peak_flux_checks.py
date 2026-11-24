import sympy as S
from pathlib import Path
n,r,a,bk,z,theta,b2=S.symbols('n r a bk z theta b2',positive=True)
Ap=-(n-2)*a*r**(1-n)
# z=b dot theta, theta=theta_k; both have zero sphere average.
flux=(Ap+z)*(Ap*theta+bk)-(Ap**2+2*Ap*z+b2)*theta/2
assert S.expand(flux-(Ap**2*theta/2+Ap*bk+z*bk-b2*theta/2))==0
average=S.expand(flux).subs({z:0,theta:0})*r**(n-1)
assert S.simplify(average+(n-2)*a*bk)==0
# At y=e_n, the regular image pole is a|y+e_n|^(2-n).
t=S.symbols('t',positive=True)
image=a*(t+1)**(2-n)
normal_gradient=S.diff(image,t).subs(t,1)
limit_flux=S.simplify(average.subs(bk,normal_gradient))
assert S.simplify(limit_flux-(n-2)**2*a*a*2**(1-n))==0
# Bubble source mass / sphere area = 1/n, hence singular coefficient a=1.
m=S.gamma(n/2)/(2*S.gamma(n/2+1))
assert S.simplify(m-1/n)==0
print('Interior image-pole normal stress flux / omega_(n-1) =',S.factor(limit_flux))
print('Nonzero positive for every n>2 and a>0; conditional simple-interior exclusion algebra checked.')
Path('workspace/agent2_interior_peak_flux_checks.py').write_text(Path(__file__).read_text())
