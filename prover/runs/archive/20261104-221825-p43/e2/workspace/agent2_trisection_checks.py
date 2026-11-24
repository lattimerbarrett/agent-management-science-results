from sympy import Matrix, zeros, eye
from pathlib import Path
# Homology data of standard genus-two trisection triple for S2 x S2.
I=eye(2); O=zeros(2); J=O.row_join(I).col_join((-I).row_join(O))
A=I.col_join(O); B=O.col_join(I)
H=Matrix([[0,1],[1,0]])
C=I.col_join(H)
for X in (A,B,C):
    assert X.T*J*X == O
for X,Y in ((A,B),(B,C),(C,A)):
    assert abs((X.T*J*Y).det()) == 1
assert H.det()==-1 and H.trace()==0
assert H**2==I
print('All three sublattices Lagrangian; pairwise Heegaard homology sphere determinants ±1.')
print('Middle intersection matrix:', H)
# Executable verification of radial derivative in the cone model.
import sympy as s
r,g=s.symbols('r g', real=True, positive=True)
f=s.exp(-1/r**2)*g
assert s.simplify(s.diff(f,r)-2*f/r**3)==0
print('For f=exp(-1/r²)g, ∂r f=2f/r³; no nonzero critical points unless g=0, where dg != 0.')
# Exact product-height regular connecting arc.
t=s.symbols('t', real=True)
p=Matrix([s.sin(t),0,s.cos(t)]); q=Matrix([s.sin(t),0,-s.cos(t)])
e3=Matrix([0,0,1])
assert s.trigsimp((p.dot(p)-1))==0 and s.trigsimp(q.dot(q)-1)==0
assert s.simplify(p[2]+q[2])==0
gradp=e3-p[2]*p; gradq=e3-q[2]*q
assert s.trigsimp(gradp.dot(gradp)+gradq.dot(gradq)-2*s.sin(t)**2)==0
assert p.subs(t,0)==e3 and q.subs(t,0)==-e3
assert p.subs(t,s.pi)==-e3 and q.subs(t,s.pi)==e3
print('Arc p=(sin t,0,cos t), q=(sin t,0,-cos t): f=0, |grad f|²=2sin²t >0 for 0<t<pi.')
