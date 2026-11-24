import sympy as s
from pathlib import Path
for m in range(1,6):
 a=s.symbols('a:'+str(m)); J=s.eye(m+1)
 for i in range(m):J[m,i]=a[i]
 G=J.T*J; Gi=G.inv()
 target=s.eye(m+1)
 for i in range(m):target[i,m]=target[m,i]=-a[i]
 target[m,m]=1+sum(t*t for t in a)
 assert s.simplify(G.det())==1
 assert s.simplify(Gi-target)==s.zeros(m+1)
print('Exact graph pullback determinant/inverse verified for tangential dimensions 1..5.')
x,y=s.symbols('x y'); f=s.Function('f')(x,y); a=s.diff(f,x);b=s.diff(f,y)
S=1+a*a+b*b
H=s.diff(a/s.sqrt(S),x)+s.diff(b/s.sqrt(S),y)
HdS=s.diff(f,x,2)+s.diff(f,y,2)-(a*a*s.diff(f,x,2)+2*a*b*s.diff(f,x,y)+b*b*s.diff(f,y,2))/S
assert s.simplify(H*s.sqrt(S)-HdS)==0
print('Exact graph H dS density verified independently in tangential dimension2.')
