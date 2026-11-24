import sympy as S,pickle
from pathlib import Path
z,t=S.symbols('z t');hh=S.symbols('h0:4');h=sum(hh[j]*z**j for j in range(4));C=S.Integer(28);P=z**4-10*z*z+11;Q=z**4-10*z*z+23;D=(z*z-1)*(z*z-5)*(z*z-9)
def gram(even):
 mom=[even[j//2] if j%2==0 else -t*even[(j-1)//2] for j in range(7)];return S.Matrix(4,4,lambda i,j:mom[i+j])
Mw=gram([1,5,39,335]);Mz=gram([1,5,27,155]);aco=(-C*Mw.inv(method='DM')*Mz*S.Matrix(hh)).applyfunc(S.cancel);print('a done',flush=True);a=sum(aco[j]*z**j for j in range(4));b=C*h;F=-336*(hh[0]+5*hh[2]-t*(hh[1]+5*hh[3]));dR=S.Poly(P*b+Q*a-F,z).as_expr();dR=S.cancel(dR);print('dR done',flush=True)
qq,rem=S.div(dR*(z-t),D,z);qq=S.factor(qq);rem=S.factor(rem)
assert S.degree(rem,z)==0
velocity=S.factor(-2*rem/C)
assert S.simplify(D.subs(z,t)*qq.subs(z,t)-C*velocity/2)==0
print('dR',dR);print('K=',qq,'v=',velocity,'F=',F)
T=S.Matrix([S.expand(qq).coeff(z,j) for j in range(3)]+[F]).jacobian(hh)
print('detT=',S.factor(T.det()))
with open('workspace/agent4_flip_physical.pkl','wb') as f:pickle.dump(dict(t=t,z=z,hvars=hh,T=T,K=qq,v=velocity,F=F,P=P,Q=Q,D=D,C=C),f)
