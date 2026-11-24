import sympy as S
m,M2,M3,u,v,H=S.symbols('m M2 M3 u v H',real=True)
x=S.symbols('x')
M=[S.Integer(1),m,M2,M3]
for j in range(4,8):M.append(S.expand((u+v)*M[j-1]-u*v*M[j-2]+H*M[j-4]))
a=(m*M2-M3)/(M2-m*m);b=-M2-a*m
q=x*x+a*x+b
q2=S.Poly(S.expand(q*q),x)
def E_x(j):return sum(co*M[po[0]+j] for po,co in q2.terms())
h=S.factor(E_x(0)); f=[S.factor(E_x(j)/h) for j in [1,2,3]]
vars=[m,M2,M3]
subs={M2:u*m,M3:u*u*m}
J=S.Matrix([[S.factor(S.diff(z,w).subs(subs,simultaneous=True)) for w in vars] for z in f])
print('J built',flush=True)
J2=J.subs({u:v,v:u,m:m+v-u},simultaneous=True)
P=(J2*J).applyfunc(S.factor)
print('trace',S.factor(S.trace(P)),flush=True)
print('det',S.factor(P.det()),flush=True)
print('PminusI',P-S.eye(3),flush=True)
from pathlib import Path
Path('workspace/s2_asym_jac_agent2.py').write_text(Path(__file__).read_text())
