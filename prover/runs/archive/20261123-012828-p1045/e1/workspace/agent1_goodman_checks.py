"""Exact checks for Goodman endpoint proof and general weak bound."""
import sympy as S
import networkx as nx
from fractions import Fraction
p,C,a=S.symbols('p C a', positive=True)
q=3*p*p+(-3-a/C+1/C)*p+1-1/C
disc=S.factor(S.discriminant(q,p)*C*C)
assert S.expand(disc-(-3*C*C+6*(a+1)*C+(a-1)**2))==0
assert S.simplify((1+a+2/S.sqrt(3)*S.sqrt(a*a+a+1)).subs(a,1)-4)==0
# Exhaust every unlabeled graph through seven vertices, as an independent check
# of exact Goodman identity and its variance lower bound.
count=0
for G in nx.graph_atlas_g():
 N=len(G)
 if N<3: continue
 A=nx.to_numpy_array(G,dtype=int)
 mono=0
 for i in range(N):
  for j in range(i):
   for k in range(j):
    es=A[i,j]+A[i,k]+A[j,k]
    mono+=(es==0 or es==3)
 d=[G.degree(i) for i in range(N)]
 rhs=Fraction(N*(N-1)*(N-2),6)-sum(Fraction(x*(N-1-x),2) for x in d)
 assert mono==rhs
 assert mono>=Fraction(N*(N-1)*(N-5),24)
 count+=1
print('Exact symbolic discriminant and endpoint verified.')
print('Goodman identity/bound verified on all',count,'unlabeled graphs with 3..7 vertices.')
