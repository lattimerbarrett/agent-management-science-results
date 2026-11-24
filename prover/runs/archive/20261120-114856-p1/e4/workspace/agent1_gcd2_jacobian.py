import sympy as S
from pathlib import Path
x=S.symbols('x')
q0=(x*x-1)*(x-2)*(x+3);r0=(x*x-1)*(x+2)*(x-3)
P=S.Poly(S.expand(q0*r0-1),x)
tau=x*(x*x-S.Rational(9,4))
M0=S.Poly(S.expand(r0*tau),x)
def moments(M,kmax=8):
 # P(z) sum_j mu_j z^(-j-1)=M(z).
 pc=[P.nth(8-j) for j in range(9)]
 mu=[]
 for k in range(kmax+1):
  mu.append((M.nth(7-k) if 7-k>=0 else 0)-sum(pc[j]*mu[k-j] for j in range(1,min(k,8)+1)))
 return mu
def state(M):
 mu=moments(M)
 H=S.Matrix(4,4,lambda i,j:mu[i+j]); g=S.Matrix(mu[4:8])
 u=-H.inv()*g
 q=S.Poly(x**4+sum(u[j]*x**j for j in range(4)),x)
 h=mu[8]+sum(u[j]*mu[4+j] for j in range(4))
 t=(q*M).rem(P)
 out=S.Poly(q.as_expr()*t.as_expr()/h,x)
 assert out.degree()==7 and out.nth(7)==1
 return out,q,h,t,H,mu,u
def jac(M):
 out,q,h,t,H,mu,u=state(M)
 Hi=H.inv(); cols=[]
 for k in range(7):
  dM=S.Poly(x**k,x);dm=moments(dM)
  dH=S.Matrix(4,4,lambda i,j:dm[i+j]);dg=S.Matrix(dm[4:8])
  du=-Hi*(dg+dH*u)
  dq=S.Poly(sum(du[j]*x**j for j in range(4)),x)
  dh=dm[8]+sum(du[j]*mu[4+j]+u[j]*dm[4+j] for j in range(4))
  dt=(dq*M+q*dM).rem(P)
  dout=S.Poly((dq*t+q*dt).as_expr()/h-out.as_expr()*dh/h,x)
  assert dout.nth(7)==0
  cols.append(S.Matrix([dout.nth(j) for j in range(7)]))
 return S.Matrix.hstack(*cols)
M1,q,h,*_=state(M0)
assert S.expand(q.as_expr()-q0)==0 and h==1
assert state(M1)[0]==M0
J=jac(M1)*jac(M0)
print('P=',P.as_expr());print('charpoly',S.factor(J.charpoly().as_expr()))
D=J-S.eye(7)
print('rank J-I',D.rank(),'rank square',(D*D).rank())
print('J-I',D)
print('1 eigenvectors',D.nullspace())
L=S.diag(*[(-1)**(j+1) for j in range(7)])
JN=L*jac(M0)
print('charpoly N=',S.factor(JN.charpoly().as_expr()))
for val in [1,-1]:
 NN=JN-val*S.eye(7)
 print('N eigenvalue',val,'nullity',7-NN.rank(),'square nullity',7-(NN*NN).rank())
