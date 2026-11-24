import sympy as S
from pathlib import Path
x,t=S.symbols('x t')
def jac(P,M,q,s):
 h=S.Poly(S.rem(q*M,P,x),x).nth(s-1)
 tau=S.cancel(M/(S.div(P+h,q,x)[0])) # M=r*tau
 series=S.series((M/P).subs(x,1/t),t,0,2*s+1).removeO().expand()
 moments=[series.coeff(t,j+1) for j in range(2*s)]
 def E(poly,ms=moments):return sum(co*ms[mon[0]] for mon,co in S.Poly(poly,x).terms())
 G=S.Matrix(s,s,lambda i,j:moments[i+j]);Gi=G.inv();out=[]
 for k in range(2*s-1):
  dM=x**k
  ds=S.series((dM/P).subs(x,1/t),t,0,2*s+1).removeO().expand()
  dm=[ds.coeff(t,j+1) for j in range(2*s)]
  dqco=-Gi*S.Matrix([E(S.expand(x**j*q),dm) for j in range(s)])
  dq=sum(dqco[j]*x**j for j in range(s))
  dt=S.rem(S.expand(dq*M+q*dM),P,x);dh=S.Poly(dt,x).nth(s-1)
  dnext=S.Poly(S.expand(dq*tau+q*dt/h-q*tau*dh/h),x)
  out.append(S.Matrix([dnext.nth(j) for j in range(2*s-1)]))
 return S.Matrix.hstack(*out)
