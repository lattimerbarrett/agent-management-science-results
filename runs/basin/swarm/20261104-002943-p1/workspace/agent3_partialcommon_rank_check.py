from sage.all import *
from pathlib import Path
R=PolynomialRing(QQ,'x');x=R.gen()
for s,P,Q,f in [(4,(x*x-1)*(x*x-9),(x*x-1)*(x*x-16),x*(x*x-4)),(3,(x*x-1)*(x-3),(x*x-1)*(x-4),x*x-x-1)]:
 C=QQ(1);D=P*Q-C;n=2*s
 # Integration against the cycle measure from its residues f Q / D.
 def integ(p):return (f*Q*R(p)).mod(D)[n-1]
 M=matrix(QQ,s,s,lambda a,b:integ(x**(a+b)));N=matrix(QQ,s,s,lambda a,b:integ(P*P*x**(a+b)));L=M.inverse()*N;cols=[]
 for j in range(s):
  h=x**j;lh=sum(L[k,j]*x**k for k in range(s));F=integ(P**3*h);b=(2*(P*h-Q*lh-F)).mod(D);cols.append(vector(QQ,[b[k] for k in range(n)]))
 roots=[rr for rr,mult in D.roots(AA) for _ in range(mult)];assert len(roots)==n and all(f(rr)*Q(rr)/D.derivative()(rr)>0 for rr in roots)
 B=matrix(cols).transpose();g=P.gcd(Q);assert B.rank()==s-g.degree();print('s=',s,'gcd=',g,'shearrank EXACT=',B.rank(),'kernel=',B.right_kernel().basis())
 for v in B.right_kernel().basis():assert (sum(v[k]*x**k for k in range(s))).mod(Q//g)==0
print('Partial-common-root Jacobian rank formula checked exactly.')
