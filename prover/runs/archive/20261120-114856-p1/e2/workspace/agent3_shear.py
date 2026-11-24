"""Exact derivative and nilpotent-shear check at a full6 stationary cycle."""
import sympy as S
nodes=list(map(S.Integer,[-3,-2,-1,1,2,3]));n=6;s=3
w=S.Matrix([S.Rational(z,9) for z in [2,1,1,2,2,1]])
L=S.Matrix([[t**j for j in range(s)] for t in nodes]);v=S.Matrix([t**s for t in nodes])
def step(w):
 W=S.diag(*list(w));M=L.T*W*L
 p=v-L*M.inv()*L.T*W*v
 p2=p.multiply_elementwise(p);F=(w.T*p2)[0]
 wp=w.multiply_elementwise(p2)/F
 J=S.diag(*list(p2))/F-2*S.diag(*list(w.multiply_elementwise(p)))*L*M.inv()*L.T*S.diag(*list(p))/F-w.multiply_elementwise(p2)*p2.T/F**2
 return wp,p,F,J
wp,p,h,J=step(w);wpp,q,hp,Jp=step(wp)
assert wpp==w and h==hp==32
assert p==S.Matrix([t**3-7*t+2 for t in nodes])
assert q==S.Matrix([t**3-7*t-2 for t in nodes])
G=Jp*J
B=S.zeros(n,n-1)
for j in range(n-1): B[j,j]=1;B[n-1,j]=-1
Gt=G[:n-1,:]*B
N=Gt-S.eye(n-1)
assert N*N==S.zeros(n-1,n-1)
assert N.rank()==s-1
assert (N**0+N).det()==1
print('Verified full6 stationary pair; N^2=0, rank N=2 exactly.')
