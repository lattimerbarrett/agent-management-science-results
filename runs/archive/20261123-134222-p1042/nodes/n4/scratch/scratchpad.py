import itertools as it
import sympy as s
from collections import Counter
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
triples=[]
for h in range(4):
 S=[i for i in range(4) if i!=h]
 for a in it.product(range(3),repeat=3):
  if len(set(a))>1:triples.append((tuple(zip(S,a)),h))
ids={v:i for i,v in enumerate(triples)};qs=[]
for a in it.product(range(3),repeat=4):
 if max(Counter(a).values())<=2:qs.append(tuple(enumerate(a)))
A=s.zeros(len(triples),len(qs))
for j,sig in enumerate(qs):
 for h in range(4):A[ids[sig[:h]+sig[h+1:],h],j]=1
D=smith_normal_form(A,domain=ZZ)
print(A.shape,Counter(abs(D[i,i]) for i in range(min(D.shape))))
