import sympy as S
from math import comb
from pathlib import Path
from collections import defaultdict
# Symbolic exact rank-two Gauss decomposition, valid in all sizes by blocks.
a,b,t=S.symbols('a b t');I=S.eye(2)
x=lambda a:S.Matrix([[1,a],[0,1]])
y=lambda b:S.Matrix([[1,0],[b,1]])
h=lambda u:S.diag(u,1/u)
comm=lambda A,B:A*B*A.inv()*B.inv()
d=1-a*b
assert S.simplify(comm(x(a),y(b))-x(-a*a*b/d)*h(1/d)*y(a*b*b/d))==S.zeros(2)
D=S.diag(t,1)
assert S.simplify(comm(D,x(a))-x((t-1)*a))==S.zeros(2)
assert S.simplify(comm(D,y(b))-y((1/t-1)*b))==S.zeros(2)
print('All-parameter Gauss and diagonal-root commutator identities verified')
# Explicit Eisenstein polynomials giving required local fields.
X=S.symbols('X')
for c in range(3,81):
 odd=[p for p in S.factorint(c) if p!=2]
 if odd:
  p=min(odd);k=c//p
  f=S.Poly(sum(comb(p,j)*X**(k*(j-1)) for j in range(1,p+1)),X)
  e=(p-1)*k
  assert e*p==c*(p-1)
 else:
  p=2;d=c//4;assert c%4==0
  f=S.Poly(X**(2*d)-2*X**d+2,X);e=2*d
 assert f.degree()==e and f.LC()==1
 coeff=f.all_coeffs()[1:]
 assert all(v%p==0 for v in coeff)
 assert f.TC()%p==0 and f.TC()%(p*p)!=0
 assert e*p//(p-1)==c
print('Eisenstein local-field constructions checked all c=3,...,80')
# Free associative algebra exact derivation identities for w_c.
def plus(A,B,s=1):
 C=A.copy()
 for w,v in B.items():
  C[w]=C.get(w,0)+s*v
  if not C[w]:del C[w]
 return C
def mult(A,B):
 C={}
 for u,a in A.items():
  for v,b in B.items():C[u+v]=C.get(u+v,0)+a*b
 return {w:v for w,v in C.items() if v}
def bracket(A,B):return plus(mult(A,B),mult(B,A),-1)
V=[{(i,):1} for i in range(3)]
def deriv(D,A):
 C={}
 for w,a in A.items():
  for i,j in enumerate(w):
   for u,b in D[j].items():
    ww=w[:i]+u+w[i+1:];C[ww]=C.get(ww,0)+a*b
 return {w:v for w,v in C.items() if v}
def db(D,E):return [plus(deriv(D,E[i]),deriv(E,D[i]),-1) for i in range(3)]
D=[bracket(V[1],V[0]),{},{}]
A=[bracket(V[1],V[2]),{},{}]
B=[{},{},bracket(V[0],V[1])]
for c in range(3,21):
 assert db(D,db(A,B))==[{},{},{}]
 B=db(D,B)
print('Integral free-associative verification of Johnson-zero word family c=3,...,20')
Path('workspace/agent3_stable_symbolic_checks.py').write_text(Path(__file__).read_text())
