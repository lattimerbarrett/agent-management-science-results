import sympy as S
m,h,z,w,H,a,c,xi,x=S.symbols('m h z w H a c xi x',real=True);b=S.Rational(-3,4);d=b
P=[1,a+c,b+d+a*c,a*d+b*c,b*d-H]
M=[S.Integer(1),m,-a*m-b+h];M.append(-a*M[2]-b*m+z)
for j in range(4,8):M.append(-sum(P[k]*M[j-k] for k in range(1,5))-2*H*w*xi**(j-4))
qa=(m*M[2]-M[3])/(M[2]-m*m);qb=-M[2]-qa*m;p=S.Poly(S.expand((x*x+qa*x+qb)**2),x)
def E(j):return sum(co*M[po[0]+j] for po,co in p.terms())
HH=S.factor(E(0));f=[S.factor(E(j)/HH) for j in[1,2,3]]
out=[f[0],S.factor(f[1]+c*f[0]+d),S.factor(f[2]+c*f[1]+d*f[0]),S.factor(w*(xi*xi+qa*xi+qb)**2/HH)]
J=S.Matrix([[S.factor(S.diff(fo,va).subs({h:0,z:0,w:0})) for va in[m,h,z,w]] for fo in out])
J1=J.subs({a:1,c:-1});J2=J.subs({a:-1,c:1,m:m+2});JJ=(J2*J1).applyfunc(S.factor)
for i in[1,2]:print('force',i,S.factor(JJ[i,3].subs(H,-(xi*xi+xi-b*-1)*(xi*xi-xi+b))),flush=True)
# simpler proper Q=(xi²-.75)²-xi²
for i in[0,1,2]:print('force correct',i,S.factor(JJ[i,3].subs(H,-((xi*xi+b)**2-xi*xi))),flush=True)
from pathlib import Path
Path('workspace/endpoint_force_agent2.py').write_text(Path(__file__).read_text())
