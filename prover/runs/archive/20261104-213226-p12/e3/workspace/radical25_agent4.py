from fractions import Fraction
import itertools,math,functools,json,time,pickle
import sympy as s
from sympy.polys.matrices import DomainMatrix
D=json.load(open('workspace/pairing25_agent4.json'))
def oddfact(n):return math.prod(range(1,n+1,2))
invdf={i:Fraction(1,oddfact(2*i+1)) for i in range(24)}
@functools.lru_cache(None)
def poly(t):
 if not t:return (Fraction(1),)
 first=t[0];rem=t[1:];distinct=sorted(set(rem));counts=[rem.count(x) for x in distinct];out=[Fraction(0)]*(len(t)+1)
 for sel in itertools.product(*[range(c+1) for c in counts]):
  total=first+sum(a*b for a,b in zip(distinct,sel));size=1+sum(sel)
  c=math.prod(math.comb(a,b) for a,b in zip(counts,sel))*invdf[total]*(-1 if size%2==0 else 1)
  leftover=tuple(x for x,m,k in zip(distinct,counts,sel) for _ in range(m-k))
  for k,v in enumerate(poly(leftover)):out[k+1]+=c*v
 return tuple(out)
const=Fraction(oddfact(49),math.factorial(49));facts=[math.factorial(47+k) for k in range(24)]
def integral(t):return const*sum(v*facts[k] for k,v in enumerate(poly(t)))
start=time.time();basis=D['rows'][33:]
A=[[integral(tuple(sorted(a+b))) for a in basis] for b in D['cols']]
print('exact pairing done',time.time()-start,flush=True)
DM=DomainMatrix.from_Matrix(s.Matrix(A)).to_field()
ker=DM.nullspace().to_Matrix();print('kernel computed',ker.shape,time.time()-start,flush=True)
v=list(ker[0,:]);den=s.ilcm(*[x.q for x in v]);v=[int(x*den) for x in v];gc=math.gcd(*v);v=[x//gc for x in v]
print('kernel primitive',list(zip(basis,v)),flush=True)
assert len(ker.tolist())==1
assert all(sum(a*b for a,b in zip(row,v))==0 for row in A)
json.dump({'basis':basis,'coefficients':v},open('workspace/radical25_agent4.json','w'))
pickle.dump(A,open('workspace/pairing25_free_exact_agent4.pkl','wb'))
