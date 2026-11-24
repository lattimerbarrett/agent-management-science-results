from itertools import combinations
from collections import defaultdict
from pathlib import Path

def add(*polys):
 d=defaultdict(int)
 for P in polys:
  for w,c in P.items():d[w]+=c
 return {w:c for w,c in d.items() if c}
def neg(P):return {w:-c for w,c in P.items()}
def mul(P,Q):
 d=defaultdict(int)
 for w,c in P.items():
  for v,e in Q.items():d[w+v]+=c*e
 return {w:c for w,c in d.items() if c}
def X(i):return {(i,):1}
def bracket(P,Q):return add(mul(P,Q),neg(mul(Q,P)))
def deriv(D,P):
 out=defaultdict(int)
 for w,c in P.items():
  for k,t in enumerate(w):
   for v,e in D.get(t,{}).items():out[w[:k]+v+w[k+1:]]+=c*e
 return {w:c for w,c in out.items() if c}
def db(D,E):return {i:P for i in D.keys()|E.keys() if (P:=add(deriv(D,E.get(i,{})),neg(deriv(E,D.get(i,{})))))}
def tr(D):
 out=defaultdict(int)
 for i,P in D.items():
  for w,c in P.items():
   if w[0]==i:out[tuple(sorted(w[1:]))]+=c
 return {w:c for w,c in out.items() if c}
def a(i,j,k):return {i:bracket(X(j),X(k))}
checks=0
for n in range(2,9):
 basis=[a(i,j,k) for i in range(n) for j,k in combinations(range(n),2)]
 for D,E in combinations(basis,2):
  assert tr(db(D,E))=={}
  checks+=1
print('PASS exact symmetric-trace cancellation for',checks,'degree-one derivation pairs (n=2..8)')
a0,b0,s=0,1,2
U={s:bracket(bracket(X(s),X(a0)),X(b0))}
V={s:bracket(bracket(X(s),X(b0)),X(a0))}
Za={a0:bracket(X(a0),bracket(X(a0),X(b0)))}
Zb={b0:bracket(bracket(X(a0),X(b0)),X(b0))}
def DA(*Ds):
 return {i:P for i in set().union(*(D.keys() for D in Ds)) if (P:=add(*(D.get(i,{}) for D in Ds)))}
def DN(D):return {i:neg(P) for i,P in D.items()}
assert db(a(s,s,a0),a(s,s,b0))==DA(U,DN(V))
assert db(a(s,a0,b0),a(a0,a0,s))==DA(U,Za)
assert db(a(a0,a0,b0),a(b0,a0,b0))==DA(DN(Za),Zb)
print('PASS exact W_s,L_s,G derivative formulas')
