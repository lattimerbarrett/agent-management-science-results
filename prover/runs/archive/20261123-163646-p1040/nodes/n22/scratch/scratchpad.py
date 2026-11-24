import sympy as S
from collections import defaultdict
s,a,b=S.symbols('s a b')
x=lambda z:S.Matrix([[1,z],[0,1]])
y=lambda z:S.Matrix([[1,0],[z,1]])
comm=lambda A,B:A*B*A.inv()*B.inv()
d=1-a*b
rhs=x(-a*a*b/d)*S.diag(1/d,d)*y(a*b*b/d)
assert (comm(x(a),y(b))-rhs).applyfunc(S.simplify)==S.zeros(2)
print('Exact opposite-root Gaussian identity: PASS')
D=S.diag(1+s,1)
for c in range(3,21):
 A=y(s);B=x(-s**(c-2))
 W=comm(D,comm(A,B))
 # The actual matrix word is trivial through depth c; any detector must
 # therefore genuinely use the central cover rather than the matrix image.
 for v in W-S.eye(2):
  assert S.series(v,s,0,c+1).removeO().expand()==0
print('Matrix word is identity modulo s^(c+1), c=3..20: PASS')
# Check the local-field defining polynomials are Eisenstein and their
# ramification indices give the claimed critical Hilbert-symbol depth.
z=S.symbols('z')
for c in range(3,65):
 odd=[p for p in S.factorint(c) if p!=2]
 if odd:
  p=int(odd[0]);k=c//p
  f=S.Poly(sum((1+z**k)**j for j in range(p)),z)
 else:
  p=2;k=c//4;f=S.Poly(z**(2*k)-2*z**k+2,z)
 cs=list(map(int,f.all_coeffs()))
 assert cs[0]==1 and all(v%p==0 for v in cs[1:]) and cs[-1]%(p*p)!=0
 assert p*f.degree()==c*(p-1)
print('Eisenstein fields and critical depth C=c, c=3..64: PASS')
