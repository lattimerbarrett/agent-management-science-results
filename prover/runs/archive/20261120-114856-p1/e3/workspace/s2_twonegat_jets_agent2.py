import sympy as S
m,h,z,s,d=S.symbols('m h z s d',real=True)
x=S.symbols('x');a,b,H=S.symbols('a b H',real=True)
# Extras ±sqrt2 with Q=-H for a1 b4 H2.
M=[S.Integer(1),m,a+h,a*m+z]
for j in range(4,8):
 k=j-4;extra=2**(k//2)*(s if k%2==0 else d)
 M.append(S.expand((a+b)*M[j-2]-(a*b-H)*M[j-4]-2*H*extra))
aa=(m*M[2]-M[3])/(M[2]-m*m);bb=-M[2]-aa*m
q=x*x+aa*x+bb;q2=S.Poly(S.expand(q*q),x)
def E_x(j):return sum(co*M[po[0]+j] for po,co in q2.terms())
HH=S.factor(E_x(0));f=[S.factor(E_x(j)/HH) for j in [1,2,3]]
EE=(2+bb)**2+2*aa*aa;oo=2*aa*(2+bb)
out=[f[0],S.factor(f[1]-b),S.factor(f[2]-b*f[0]),S.factor((EE*s+oo*d)/HH),S.factor((EE*d+2*oo*s)/HH)]
sub={h:0,z:0,s:0,d:0};var=[m,h,z,s,d]
J=S.Matrix([[S.factor(S.diff(fo,va).subs(sub,simultaneous=True)) for va in var] for fo in out])
JJ=(J.subs({a:b,b:a},simultaneous=True)*J).applyfunc(S.factor)
JJ=JJ.subs({a:1,b:4,H:2}).applyfunc(S.factor)
print('J2',JJ,flush=True)
from pathlib import Path
import pickle
Path('workspace/s2_twonegat_jets_agent2.py').write_text(Path(__file__).read_text())
with open('workspace/s2_twonegat_map_agent2.pkl','wb') as fp:pickle.dump((m,h,z,s,d,a,b,H,out),fp)
