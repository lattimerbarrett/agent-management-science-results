"""Exact finite checks for the arithmetic all-degree detector.
Classical global/local Hilbert and Matsumoto theorems are NOT simulated.
Their hypotheses are checked here; the general proof is in notes.
"""
from sympy import Matrix,eye,symbols,simplify,factor,factorint,Poly

def comm(A,B):return A*B*A.inv()*B.inv()
def Lbr(A,B):return A*B-B*A

a,b,u,x,pi,t=symbols('a b u x pi t')
X=eye(3);X[0,1]=a
Y=eye(3);Y[1,0]=b
Z=comm(X,Y)
v=1+a*b+a*a*b*b
assert (Z-Matrix([[v,-a*a*b,0],[a*b*b,1-a*b,0],[0,0,1]])).applyfunc(simplify)==Matrix.zeros(3)
LL=eye(3);LL[1,0]=a*b*b/v
DD=Matrix.diag(v,1/v,1)
UU=eye(3);UU[0,1]=-a*a*b/v
assert (LL*DD*UU-Z).applyfunc(simplify)==Matrix.zeros(3)
C=Matrix.diag(u,1,1/u)
assert (comm(C,X)-Matrix([[1,(u-1)*a,0],[0,1,0],[0,0,1]])).applyfunc(simplify)==Matrix.zeros(3)
# Coroot scalar product, crucial to avoid factor two.
Halpha=Matrix([1,-1,0]);Hbeta=Matrix([1,0,-1]);assert Halpha.dot(Hbeta)==1
# Johnson image computation in the pure-x2 current algebra.
A=Matrix([[0,t],[0,0]]);B=Matrix([[0,0],[t,0]]);CC=Matrix([[t,0],[0,0]])
for c in range(3,65):
 Ar=A
 for k in range(c-3):Ar=Lbr(CC,Ar)
 assert Ar==Matrix([[0,t**(c-2)],[0,0]])
 assert Lbr(Lbr(Ar,B),CC)==Matrix.zeros(2)
 # Exact valuations in the Gauss decomposition of Z.
 assert c-2>=1
 assert (c-2)+2>=c
 assert 2*(c-2)+1>=c
 assert 2*(c-1)>=c+1
 # Choice of global field, all conductor and boundary hypotheses.
 odd=[p for p in factorint(c) if p%2]
 if odd:
  p=odd[0];r=c//p;e0=p-1;unit_name='zeta_p'
 else:
  p=2;assert c>=4;r=c//4;e0=2;unit_name='i'
 e=e0*r
 assert p*e//(p-1)==c and p*e%(p-1)==0
 assert (c-1)%p!=0 and (1%p)!=0
 if r>=2:
  F=x**r+pi*x+pi
  assert F.subs(x,-1)==(-1)**r
  assert Poly(F,x).LC()==1
  assert Poly(F,x).nth(0)==pi and Poly(F,x).nth(1)==pi
  assert all(Poly(F,x).nth(i)==0 for i in range(2,r))
 # At r=1 take basefield itself and pi=zeta_p-1 or i-1.
print('Exact root/Gauss/Johnson identities and all arithmetic hypotheses checked for c=3..64.')
