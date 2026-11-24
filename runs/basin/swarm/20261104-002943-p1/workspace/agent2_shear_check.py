import sympy as S
x=S.Matrix([-8,-1,1,8]); n=4;s=2;V=S.Matrix([[1,z] for z in x]);q=x.applyfunc(lambda z:z*z+3*z-28);Q=x.applyfunc(lambda z:z*z-3*z-28)
assert all(q[i]*Q[i]==720 for i in range(n))
B=S.Matrix.vstack(S.ones(1,n),(S.diag(*q)*V).T)
w=B.T*(B*B.T).inv()*S.Matrix([1,0,0]); assert min(w)>0
assert (S.diag(*q)*V).T*w==S.zeros(s,1)
def DF(w,q):
 M=V.T*S.diag(*w)*V; dc=-M.inv()*V.T*S.diag(*q)
 dp=V*dc
 h=(w.T*q.applyfunc(lambda z:z*z))[0]
 D=S.diag(*q.applyfunc(lambda z:z*z))+2*S.diag(*[w[i]*q[i] for i in range(n)])*dp
 dh=S.ones(1,n)*D
 return D/h-(S.diag(*w)*q.applyfunc(lambda z:z*z))*dh/h**2
z=S.diag(*w)*q.applyfunc(lambda z:z*z)/((w.T*q.applyfunc(lambda z:z*z))[0]);J=S.simplify(DF(z,Q)*DF(w,q));N=J-S.eye(n)+w*S.ones(1,n)
assert N.rank()==1 and N*N==S.zeros(n,n)
assert J.eigenvals()=={S.Integer(1):3,S.Integer(0):1}
print('Exact nonmaximal s2 cycle and rank-one square-zero shear verified.')
