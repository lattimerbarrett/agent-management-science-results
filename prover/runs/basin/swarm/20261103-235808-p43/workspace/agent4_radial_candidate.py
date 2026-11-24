import sympy as S
from pathlib import Path
w=S.symbols('w',real=True)
p=2*w/(1+w*w);t=(w*w-1)/(S.sqrt(2)*(1+w*w));z=2*(p+t)**2
b=S.symbols('b',real=True)
P=S.sqrt(2)+b*(z-1)**2
print('series',S.series(t-(1-3*t*t)*P,w,0,5))
P=P.subs(b,5/(8*S.sqrt(2)))
expr=S.factor(S.together(t-(1-3*t*t)*P),extension=S.sqrt(2))
print(expr)
num,den=S.fraction(expr)
print('factors:',S.factor_list(num,extension=S.sqrt(2)))
print('real roots',S.nroots(num,maxsteps=1000))
Path('workspace/agent4_radial_candidate.py').write_text(Path('scratchpad.py').read_text())