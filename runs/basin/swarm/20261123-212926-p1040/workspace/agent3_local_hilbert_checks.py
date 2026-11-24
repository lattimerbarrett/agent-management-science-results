from pathlib import Path
import sympy as S,time
from sage.all import pari
X,Z=S.symbols('X Z')
for c in [4,8,16,32,64]:
 r=c//4;P=S.Poly(S.cyclotomic_poly(4,1+X**r),X)
 assert P.degree()==c//2
 assert P.eval(0)==2 and all(coef%2==0 for coef in P.all_coeffs()[1:])
 poly=pari(str(P.as_expr()).replace('X','x').replace('**','^'));nf=pari.nfinit(poly)
 pi=pari.Mod(pari('x'),poly);u=1+pi;v=1-pi**(c-1)
 pr=pari.idealprimedec(nf,2)
 ans=pari.nfhilbert(nf,v,u,pr[0]);assert ans==-1
 print('newlocal P c',c,P.as_expr(),'Hilbert2',ans,flush=True)
