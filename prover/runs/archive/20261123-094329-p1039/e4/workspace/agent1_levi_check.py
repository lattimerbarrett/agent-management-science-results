import sympy as s

a,g=s.symbols('a g', positive=True)
b,c,d=s.symbols('b c d', real=True)
A=(1+d*d+(b*b+c*c)/a)/(2*g*g)
H=s.Matrix([[a,b+s.I*c],[b-s.I*c,d]])
M=H+s.diag(0,2*A*g*g)
assert s.simplify(M.det()-a*(d*d+d+1)) == 0
assert s.expand(d*d+d+1-((d+s.Rational(1,2))**2+s.Rational(3,4))) == 0
x,y,u,v,t=s.symbols('x y u v t', real=True)
r=s.Function('r')(x,y,u,v)
pairs=[(x,y),(u,v)]
def dz(f,j):
    X,Y=pairs[j]
    return (s.diff(f,X)-s.I*s.diff(f,Y))/2
def db(f,j):
    X,Y=pairs[j]
    return (s.diff(f,X)+s.I*s.diff(f,Y))/2
for j in range(2):
    for k in range(2):
        expression=dz(db(r+t*r*r,k),j)-(1+2*t*r)*dz(db(r,k),j)-2*t*dz(r,j)*db(r,k)
        assert s.simplify(expression)==0
print('All Levi-repair identities and positivity certificates verified.')
from pathlib import Path
Path('workspace/agent1_levi_check.py').write_text(Path(__file__).read_text())
