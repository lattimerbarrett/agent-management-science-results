"""Exact checker for invariant logarithmic volume of restarted monic map."""
import sympy as S
for n,s in [(4,1),(4,2),(6,3)]:
 nodes=list(map(S.Integer,range(1,n+1)))
 w=S.diag(*[S.Rational(i+2) for i in range(n)])
 L=S.Matrix([[t**j for j in range(s)] for t in nodes])
 h=S.Matrix([t**s for t in nodes])
 M=L.T*w*L
 coeff=-M.inv()*L.T*w*h
 q=h+L*coeff
 assert L.T*w*q==S.zeros(s,1)
 Q=S.diag(*list(q))
 assert Q.det()!=0
 P=Q.inv()*L*M.inv()*L.T*w*Q
 assert P*P==P
 assert P*S.ones(n,1)==S.zeros(n,1)
 R=S.eye(n)-2*P
 assert R*R==S.eye(n)
 assert R.det()==(-1)**s
 # Quotient by common logscale: output log(w_i/w_n).
 B=S.zeros(n,n)
 B[:,0]=S.ones(n,1)
 for j in range(1,n):B[j-1,j]=1
 Rbase=B.inv()*R*B
 assert Rbase[:,0]==S.Matrix([1]+[0]*(n-1))
 assert Rbase[1:,1:].det()==(-1)**s
 print('verified n,s=',n,s)
