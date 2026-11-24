import sympy as S
m,h,z,u,v,H,e,x=S.symbols('m h z u v H e x',real=True)
# m2=um+h,m3=u*m2+z
M=[S.Integer(1),m,u*m+h,u*u*m+u*h+z]
for j in range(4,8):M.append(S.expand((u+v)*M[j-1]-u*v*M[j-2]+H*M[j-4]))
m2,m3=M[2:4];a=(m*m2-m3)/(m2-m*m);b=-m2-a*m
q=x*x+a*x+b
q2=S.Poly(S.expand(q*q),x)
def E_x(j):return sum(co*M[po[0]+j] for po,co in q2.terms())
HH=S.factor(E_x(0)); f=[S.factor(E_x(j)/HH) for j in [1,2,3]]
# next coords must switch base root u to v
out=[f[0],S.factor(f[1]-v*f[0]),S.factor(f[2]-v*f[1])]
def jets(expr,N=3):
 num,den=S.fraction(S.cancel(expr));num=S.Poly(num.subs({h:h*e,z:z*e},simultaneous=True),e);den=S.Poly(den.subs({h:h*e,z:z*e},simultaneous=True),e)
 out=[]
 for k in range(N):out.append(S.factor((num.nth(k)-sum(den.nth(j)*out[k-j] for j in range(1,k+1)))/den.nth(0)))
 return out
Jf=[jets(t) for t in out]
print('T jets',Jf,flush=True)
# base m shift v-u. For 2nd map use Jf swapu,v at m+v-u.
base=m+v-u
swap={u:v,v:u,m:base}
G=[[t.subs(swap,simultaneous=True) for t in row] for row in Jf]
L=[t[1] for t in Jf];Q=[t[2] for t in Jf];sub={h:L[1],z:L[2]}
for i in range(3):
 linear=G[i][1].subs(sub,simultaneous=True)+(L[0] if i==0 else 0)
 quad=Q[0] if i==0 else 0
 quad+=S.diff(G[i][1],h)*Q[1]+S.diff(G[i][1],z)*Q[2]
 # derivative m before swap, since base depends m equally, use G derivative
 quad+=S.diff(G[i][1],m).subs(sub,simultaneous=True)*L[0]
 quad+=G[i][2].subs(sub,simultaneous=True)
 print('T2',i,'linear',S.factor(linear),'quad',S.factor(quad),flush=True)
 print('T2 weighted2',i,S.factor(linear+S.expand(quad).coeff(z,0)),flush=True)
from pathlib import Path
Path('workspace/s2_asym_jet_agent2.py').write_text(Path(__file__).read_text())
