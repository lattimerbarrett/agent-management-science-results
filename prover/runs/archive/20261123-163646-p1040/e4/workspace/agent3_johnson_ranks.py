from collections import defaultdict
from itertools import product

def add(a,b,scale=1):
 d=defaultdict(int,a)
 for w,v in b.items():d[w]+=scale*v
 return {w:v for w,v in d.items() if v}
def mul(a,b):
 d=defaultdict(int)
 for u,x in a.items():
  for v,y in b.items():d[u+v]+=x*y
 return {w:v for w,v in d.items() if v}
def bracket(a,b):return add(mul(a,b),mul(b,a),-1)
def deriv(D,a):
 out={}
 for w,v in a.items():
  for k,x in enumerate(w):
   out=add(out,{w[:k]+u+w[k+1:]:v*z for u,z in D[x].items()})
 return out
def dbracket(D,E):return tuple(add(deriv(D,e),deriv(E,d),-1) for d,e in zip(D,E))
def generators(n):
 X=[{(i,):1} for i in range(n)]; G=[]
 for i in range(n):
  for j in range(n):
   for k in range(j+1,n):
    D=[{} for _ in range(n)];D[i]=bracket(X[j],X[k]);G.append(tuple(D))
 return G

def run():
 from sympy import Matrix, ZZ
 from sympy.matrices.normalforms import smith_normal_form
 G=generators(3)
 B=[dbracket(x,y) for i,x in enumerate(G) for y in G[i+1:]]
 C=[dbracket(x,y) for x in G for y in B]
 keys=[(i,w) for i in range(3) for w in product(range(3),repeat=4)]
 M=Matrix([[D[i].get(w,0) for D in C] for i,w in keys])
 S=smith_normal_form(M,domain=ZZ)
 inv=[abs(S[i,i]) for i in range(min(S.shape)) if S[i,i]]
 assert inv==[1]*43
 print('degree3 image has rank43; all nonzero integral Smith invariants are1')
 return inv
if __name__=='__main__':run()
