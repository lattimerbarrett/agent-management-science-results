from pathlib import Path
from scipy.integrate import quad
from scipy.special import gamma
import sympy as s
N,t=s.symbols('N t', positive=True)
F=t*t+1/N
ode=s.expand((1+t*t)*s.diff(F,t,2)+(N-1)*t*s.diff(F,t)-2*N*F)
assert s.simplify(ode)==0
for Nv in range(2,31):
 I=quad(lambda x:(1+x*x)**(-(Nv-1)/2)/(x*x+1/Nv)**2,0,float('inf'),epsabs=1e-12)[0]
 C=Nv*Nv/I
 pred=4*gamma((Nv+1)/2)/(gamma(.5)*gamma(Nv/2))
 assert abs(C/pred-1)<2e-11
print('Checked harmonic-extension ODE symbolically; independently checked 29 leading Green Robin correction coefficients by integral quadrature.')
Path('workspace/agent2_green_correction_check.py').write_text(Path(__file__).read_text())
