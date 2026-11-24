import sympy as S
from pathlib import Path
x1,x2,x3,y1,y2,y3=S.symbols('x1 x2 x3 y1 y2 y3',real=True)
x=S.Matrix([x1,x2,x3]);y=S.Matrix([y1,y2,y3]);s=x+y;r=S.sqrt(s.dot(s));n=s/r
co=-S.Rational(1,3);si=-2*S.sqrt(2)/3
rot=lambda v:co*v+si*n.cross(v)+(1-co)*n.dot(v)*n
A=S.Matrix([[1,0,0],[0,0,-1],[0,1,0]])
B=S.Matrix([[0,0,1],[0,1,0],[-1,0,0]])
F=(A*rot(x)).col_join(B*rot(y))
t=1/S.sqrt(2);p=S.Matrix([0,t,t,t,0,-t]);subs=dict(zip(list(x)+list(y),list(p)))
J=S.simplify(F.jacobian(list(x)+list(y)).subs(subs))
assert S.simplify(F.subs(subs)-p)==S.zeros(6,1)
# orthonormal oriented tangent frames e1, x cross e1 and e2,y cross e2
xp=p[:3,0];yp=p[3:,0]
e1=S.Matrix([1,0,0]);e2=xp.cross(e1);f1=S.Matrix([0,1,0]);f2=yp.cross(f1)
T=S.zeros(6,4);T[:3,0]=e1;T[:3,1]=e2;T[3:,2]=f1;T[3:,3]=f2
D=S.simplify(T.T*J*T);K=S.simplify(D-S.eye(4))
print('D=',D,'nullity=',4-K.rank(),'charpoly=',D.charpoly().as_expr().factor())
print('kernel',K.nullspace())
h=S.symbols('h',real=True)
Ft=(A*n.cross(rot(x))).col_join(B*n.cross(rot(y))).subs(subs)
dr=S.Matrix([[*list(n),*list(n)]]).subs(subs)
Dh=S.simplify(T.T*(J+h*Ft*dr)*T);Kh=Dh-S.eye(4)
minors=[]
import itertools
for rows in itertools.combinations(range(4),3):
 for cols in itertools.combinations(range(4),3):
  z=S.factor(Kh.extract(rows,cols).det())
  if z!=0:minors.append(z)
print('3minors',set(minors));sol=S.solve(minors,h);print('slope',sol)
for hs in ([sol[h]] if isinstance(sol,dict) else []):
 Ks=S.simplify(Kh.subs(h,hs));print('tuned',hs,'nullity',4-Ks.rank(),'kernel',Ks.nullspace(),'charpoly',Dh.subs(h,hs).charpoly().as_expr().factor())
Path('workspace/agent4_node_derivative.txt').write_text(str(D)+'\nnullity='+str(4-K.rank())+'\n'+str(K.nullspace()))
Path('workspace/agent4_node_derivative.py').write_text(Path('scratchpad.py').read_text())