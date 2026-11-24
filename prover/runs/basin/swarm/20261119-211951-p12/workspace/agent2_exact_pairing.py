from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from math import factorial,comb
from sage.all import matrix, QQ
import time,json,pickle
start=time.time();g=25
invdf={};v=1
for d in range(24):
 if d:v*=2*d+1
 invdf[d]=Q(1,v)
@lru_cache(None)
def poly(parts):
 if not parts:return (Q(1),)
 first=parts[0]; vals=sorted(set(parts[1:]));counts=[parts[1:].count(v) for v in vals];out=[Q(0)]*(len(parts)+1)
 for nums in product(*(range(c+1) for c in counts)):
  s=first+sum(v*n for v,n in zip(vals,nums));b=sum(nums);mult=1;rem=[]
  for v,c,n in zip(vals,counts,nums):mult*=comb(c,n);rem +=[v]*(c-n)
  w=(-1)**b*mult*invdf[s]
  for k,a in enumerate(poly(tuple(rem))):out[k+1]+=w*a
 return tuple(out)
fact=[factorial(i) for i in range(80)]
scale=1/(invdf[23]*Q(fact[48])) # invdf23 denominator47!!
@lru_cache(None)
def val(parts):return sum(a*fact[47+n] for n,a in enumerate(poly(parts)))*scale
p=json.load(open('workspace/pairing25_agent2.json'))
M=[[val(tuple(sorted(a+b))) for b in p['cols']] for a in p['rows']]
print('built exact',time.time()-start,flush=True)
P=p['prime']
assert [[x.numerator*pow(x.denominator,P-2,P)%P for x in row] for row in M]==p['matrix']
print('modular comparison passed',flush=True)
S=matrix(QQ,M);print('exact rank',S.rank(),'elapsed',time.time()-start,flush=True)
pickle.dump(M,open('workspace/agent2_exact_pairing.pkl','wb'))
from pathlib import Path
if Path(__file__).name=='scratchpad.py':
 Path('workspace/agent2_exact_pairing.py').write_text(Path(__file__).read_text())