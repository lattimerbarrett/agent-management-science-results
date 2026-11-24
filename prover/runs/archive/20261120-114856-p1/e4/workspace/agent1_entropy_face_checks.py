import sympy as S
from pathlib import Path
z=S.symbols('z');lam=list(range(1,9));P=S.prod(z-l for l in lam);dp=S.diff(P,z)
for empty in range(4):
 occ=[j for j in range(4) if j!=empty];beta=[S.Rational(4*j+3,2) for j in occ]
 # roots between consecutive beta: choose the midpoint of the interband core gap,
 # except that if the empty band is interior either endpoint can be used.
 cases=[]
 for endpoint in ([2*empty+1,2*empty+2] if empty in [1,2] else [None]):
  roots=[]
  for a,b in zip(occ,occ[1:]):
   roots.append(S.Integer(endpoint) if b-a==2 else S.Rational(4*a+5,2))
  U=S.prod(z-r for r in roots);V=S.prod(z-b for b in beta)
  residues=[S.cancel(U.subs(z,b)/S.diff(V,z).subs(z,b)) for b in beta]
  assert all(a>0 for a in residues)
  coeff=[S.cancel(U.subs(z,l)/(V.subs(z,l)*dp.subs(z,l))) for l in lam]
  negative=[i+1 for i,c in enumerate(coeff) if c<0];zeros=[i+1 for i,c in enumerate(coeff) if c==0]
  expected=([2] if empty==0 else [7] if empty==3 else [4 if endpoint==3 else 3] if empty==1 else [6 if endpoint==5 else 5])
  assert negative==expected,(empty,endpoint,negative,expected)
  print('emptyband',empty+1,'Uroots',roots,'positive residues',residues,'negative coefficients at',negative,'zero at',zeros)
print('PASS all s4 entropy forced-face sign patterns (exact rationals)')
