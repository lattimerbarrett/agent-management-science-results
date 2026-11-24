import sympy as S
from pathlib import Path
r=S.sqrt(14);a=S.sqrt(6-r);b=S.sqrt(6+r);xs=[-b,-a,a,b,S.Integer(2)];V=S.Matrix([[1,x] for x in xs]);w=S.Matrix([(1-3/r)/4,(1+3/r)/4,(1+3/r)/4,(1-3/r)/4,0]);P=S.Matrix([x*x-3 for x in xs]);Q=S.Matrix([x*x-9 for x in xs]);C=S.Integer(5)
def sim(a):return a.applyfunc(S.simplify)
def mul(a,b):return S.matrix_multiply_elementwise(a,b)
M=sim(V.T*S.diag(*w)*V);z=sim(mul(w,mul(P,P))/C);N=sim(V.T*S.diag(*z)*V);mu=S.Matrix([1,2]);eps=S.Matrix([0,0,0,0,1])-w
aco=-M.inv()*mu*P[-1];av=V*aco;dC=S.simplify((eps.T*mul(P,P))[0]);dz=sim((mul(eps,mul(P,P))+2*mul(mul(w,P),av)-z*dC)/C)
bco=sim(-N.inv()*V.T*mul(dz,Q));assert sim(bco-3*P[-1]*N.inv()*mu)==S.zeros(2,1)
dC2=S.simplify((dz.T*mul(Q,Q))[0]);dw2=sim((mul(dz,mul(Q,Q))+2*mul(mul(z,Q),V*bco)-w*dC2)/C);force=sim(dw2-eps);mom=sim(V.T*mul(P,force));assert mom==4*P[-1]*mu
hd=sim((C*N).inv()*mom);expected=4*P[-1]/C*N.inv()*mu;assert sim(hd-expected)==S.zeros(2,1)
print('Exact−1forcingidentity PASS; hd=',hd.T,'Mw=',M,'Mz=',N)
