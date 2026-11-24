from pathlib import Path
import sympy as S,pickle
th=S.symbols('th');d=S.sqrt(35);lam=[-3,-1,1,2,3];X=S.Matrix([[1,x,x*x] for x in lam]);p=S.Matrix([x**3-7*x+d for x in lam]);q=S.Matrix([x**3-7*x-d for x in lam]);aa=[1/S.prod([S.Integer(x-y) for y in lam if y!=x]) for x in lam];w=S.Matrix([aa[i]*q[i]*(lam[i]-th) for i in range(5)]);wt=w.diff(th);H=S.simplify(X.T*S.diag(*w)*X);Hi=H.inv();wp=w.multiply_elementwise(p.applyfunc(lambda x:x*x));Hp=S.simplify(X.T*S.diag(*wp)*X)
Bmap=S.simplify(-Hp.inv()*H);ER=2*d*w.T*X;RC=S.simplify(S.diag(*q)*X+S.diag(*p)*X*Bmap+S.ones(5,1)*ER);VR=S.simplify(-2*(lam[0]-th)*RC[0,:]);CV=S.simplify(S.Rational(1,4)*Hi*X.T*S.Matrix([wt[i]**2/w[i]*p[i] for i in range(5)]));bv=S.simplify(-CV*VR[1]);tr=S.factor(bv[1]+2*bv[2]);f=th**3-7*th
assert VR[0]==0 and S.simplify(VR[2]-2*VR[1])==0
assert S.simplify(tr-d*S.diff(f,th)/(f*f-35))==0
with open('workspace/agent4_h1_transport_symbolic.pkl','wb') as out:pickle.dump((th,H,VR,bv,tr),out)
print('Exact transport rank-one and trace primitive identities checked.')
