import sympy as S
m,h,z,w,u,v,H,t,x=S.symbols('m h z w u v H t x',real=True)
M=[S.Integer(1),m,u*m+h,u*u*m+u*h+z]
for j in range(4,8):M.append(S.expand((u+v)*M[j-1]-u*v*M[j-2]+H*M[j-4]-2*H*w*t**(j-4)))
m2,m3=M[2:4];a=(m*m2-m3)/(m2-m*m);b=-m2-a*m
q=x*x+a*x+b;q2=S.Poly(S.expand(q*q),x)
def E_x(j):return sum(co*M[po[0]+j] for po,co in q2.terms())
HH=S.factor(E_x(0)); f=[S.factor(E_x(j)/HH) for j in [1,2,3]]
out=[f[0],S.factor(f[1]-v*f[0]),S.factor(f[2]-v*f[1]),S.factor(w*q.subs(x,t)**2/HH)]
vars=[m,h,z,w];sub={h:0,z:0,w:0}
J=S.Matrix([[S.factor(S.diff(fo,va).subs(sub,simultaneous=True)) for va in vars] for fo in out])
J2=J.subs({u:v,v:u,m:m+v-u},simultaneous=True)
JJ=(J2*J).applyfunc(S.factor)
for i in range(4):
 print('T2 eps force',i,S.factor(JJ[i,3].subs(H,-t*t*(t-u)*(t-v))),flush=True)
from pathlib import Path
Path('workspace/s2_fifth_jet_agent2.py').write_text(Path(__file__).read_text())
