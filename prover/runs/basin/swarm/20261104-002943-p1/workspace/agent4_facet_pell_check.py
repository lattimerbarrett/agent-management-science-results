import sympy as S,pickle
from pathlib import Path
x,l,c=S.symbols('x l c');Z0,Z1=S.symbols('Z0 Z1');P=x**4-5*x*x+4;h=-x**3-2*x*x+x+8;Z=Z0+Z1*x+x*x
rem=S.rem((x-l)*(h*Z-c),P,x);eq=[rem.coeff(x,j) for j in [1,2,3]];sol=S.solve(eq,[Z0,Z1,c]);print(sol)
Z=S.factor(Z.subs(sol));disc=S.factor(S.discriminant(Z,x));print('Zfacet=',Z,'disc=',disc)
for Hsgn in [-1,1]:
 roots=S.nroots(P-Hsgn)
 for lam in roots:
  print('node',lam,'Z',Z.subs(l,lam).evalf(),'disc',disc.subs(l,lam).evalf())
D=pickle.load(open('workspace/agent4_pell_transverse_jets.pkl','rb'));dp6=D['pafter'][6]-D['pbefore'][6];r6=S.factor(dp6.nth(3)/D['h'].nth(3));qz=S.expand(-dp6.as_expr()+D['h'].as_expr()*r6);print('r6',r6,'qz',S.factor(qz))
