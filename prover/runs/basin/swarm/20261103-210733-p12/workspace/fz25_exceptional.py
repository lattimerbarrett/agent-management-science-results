from functools import lru_cache
from itertools import product
from math import factorial, comb, gcd, lcm
from collections import Counter
import gmpy2 as gp
import json,time
import sympy as sp
T=time.time()
Q=gp.mpq
@lru_cache(None)
def odd_df(n):
 z=1
 for i in range(n,0,-2):z*=i
 return z
@lru_cache(None)
def poly(a):
 if not a:return (Q(1),)
 first=a[0];c=Counter(a[1:]);ks=tuple(c);cs=tuple(c[k] for k in ks)
 out=[Q(0)]*(len(a)+1)
 for vv in product(*(range(v+1) for v in cs)):
  size=1+sum(vv);ss=first+sum(k*v for k,v in zip(ks,vv));mult=1
  for c0,v in zip(cs,vv):mult*=comb(c0,v)
  coeff=Q(mult*(-1)**(size-1),odd_df(2*ss+1))
  rem=tuple(sorted((k for k,c0,v in zip(ks,cs,vv) for _ in range(c0-v)),reverse=True))
  for j,z in enumerate(poly(rem)):out[j+1]+=coeff*z
 return tuple(out)
@lru_cache(None)
def integral(a):return sum(z*factorial(47+j) for j,z in enumerate(poly(a)))
d=json.load(open('workspace/agent4_pairing.json'));a=[tuple(v) for v in d['rows']][33:];b=[tuple(v) for v in d['cols']]
M=[]
for i,x in enumerate(a):
 M.append([integral(tuple(sorted(x+y,reverse=True))) for y in b])
 if i%5==0:print(i, time.time()-T,poly.cache_info(),flush=True)
mat=sp.Matrix([[sp.Rational(str(c)) for c in row] for row in M]);print('created',time.time()-T,flush=True)
dm=sp.polys.matrices.DomainMatrix.from_Matrix(mat.T).convert_to(sp.QQ)
ns=dm.nullspace().to_Matrix();print('nullspace',ns.shape,time.time()-T,flush=True)
assert ns.rows==1
v=list(ns.row(0));den=lcm(*(int(c.q) for c in v));v=[int(c*den) for c in v];gc=gcd(*v);v=[c//gc for c in v]
assert mat.T*sp.Matrix(v)==sp.zeros(56,1)
print('digits', [len(str(c)) for c in v],flush=True)
json.dump({'basis':a,'vector':[str(c) for c in v],'pairing':[[str(c) for c in row] for row in M]},open('workspace/fz25_exceptional.json','w'))
fz=json.load(open('workspace/fz25_upper_data.json'))
F=sp.Matrix([[sp.Rational(c) for c in row] for row in fz['matrix']])
vv=[0]*33+v
stack=F.col_join(sp.Matrix([vv]))
assert sp.polys.matrices.DomainMatrix.from_Matrix(stack).rank()==34
print('Exceptional vector independent of FZ relation space: augmented rank34',flush=True)
