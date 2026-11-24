import sympy as S,pickle
from pathlib import Path
m,h,z,v,d,H=S.symbols('m h z v d H',real=True)
def first(m,a,b,c,d):
 V=-a*m-b-m*m;A=(m*h-z)/V;B=-h-m*A;mp=m+a-c
 M2=-a*m-b;M3=(a*a-b)*m+a*b
 M4=-(a+c)*M3-(b+d+a*c)*M2-(a*d+b*c)*m-b*d+H
 PP=A*A*M2+2*A*B*m+B*B
 XP=A*A*M3+2*A*B*M2+B*B*m
 XXP=A*A*M4+2*A*B*M3+B*B*M2
 el=(b-d)*h+(a-c)*z
 Qh=(h*el+A*A*H+(c-a)*XP+(d-b)*PP)/H
 Qz=(z*el+H*(A*A*(m-c)+2*A*B)+(c-a)*XXP+(d-b)*XP)/H
 Lm=2*A+(-d*(a-c)*h+(b-d-c*(a-c))*z-mp*el)/H
 return [S.factor(t)for t in[Lm,Qh,Qz]]
F=first(m,S.Integer(-1),S.Integer(0),-v,d)
G=first(m-1+v,-v,d,S.Integer(-1),S.Integer(0))
Lm=S.factor(F[0]-G[0]);Qh=S.factor(G[1]-F[1]);Qz=S.factor(G[2]-F[2])
print('Lm',Lm,flush=True)
print('Qh',Qh,flush=True);print('Qz',Qz,flush=True)
A=S.Matrix([[S.factor(S.diff(S.cancel(Q/Lm),zz))for zz in[h,z]]for Q in[Qh,Qz]])
print('FLIGHT A',A,flush=True)
pickle.dump((m,v,d,H,A,Lm,Qh,Qz),open('workspace/generic_flight_agent2.pkl','wb'))
Path('workspace/generic_flight_agent2.py').write_text(Path(__file__).read_text())
