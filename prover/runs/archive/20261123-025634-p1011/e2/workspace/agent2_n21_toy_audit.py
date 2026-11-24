import sys
sys.path.insert(0,'workspace')
import sympy as s
from agent1_exact_cross_gram import exact_shape_gram
n=21;m=n-1;J=2
G=exact_shape_gram(n,2,J);G1=exact_shape_gram(n,1,J);G3=exact_shape_gram(n,3,J-1)
T=s.zeros(3)
for i in range(3):
 for j in range(3):
  T[i,j]=(2+s.Rational(4*i,m+2))*(2+s.Rational(4*j,m+2))*s.Rational(m+2,2*m)*G1[i,j]
  if i*j:T[i,j]+=s.Rational(4*i*j,m+2)*G3[i-1,j-1]
  if j:T[i,j]+=(2*j+s.Rational(4*j*(j+1),m))*G[i,j-1]
T=(T+T.T)/2
x=s.symbols('x');c=s.Matrix([1,x,s.Rational(7,150)])
H=s.Matrix(3,3,lambda i,j:2*(i+j+1)*G[i,j])
K=s.Matrix(3,3,lambda i,j:2*(i+j+1)*(2*(i+j+1)-1)*G[i,j])
p=(c.T*H*c)[0]
roots=s.nroots(p,maxsteps=100)
print('Scale stationarity roots with c2=7/150:',roots)
for rt in roots:
 cc=c.subs(x,rt)
 print('c1=',rt,'Scale second',(cc.T*K*cc)[0].evalf(15),'center per-axis',(cc.T*T*cc)[0].evalf(15),'norm',(cc.T*G*cc)[0].evalf(15))
from pathlib import Path
