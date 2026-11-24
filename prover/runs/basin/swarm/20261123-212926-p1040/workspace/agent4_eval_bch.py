from fractions import Fraction as F
from functools import lru_cache
from collections import defaultdict,Counter
import pickle,time
from pathlib import Path
# a=K21, b=K12, c=K13; zero-based indices.
pairs=[(1,0),(0,1),(0,2)]
def apply_letter(k,p):
 i,j=pairs[k];out=defaultdict(int)
 for w,v in p.items():
  for pos,x in enumerate(w):
   if x==i:
    out[w[:pos]+(j,i)+w[pos+1:]]+=v
    out[w[:pos]+(i,j)+w[pos+1:]]-=v
 return {w:v for w,v in out.items() if v}
@lru_cache(None)
def ev(w,i):
 if not w:return {(i,):1}
 return apply_letter(w[0],ev(w[1:],i))
if __name__=='__main__':
 base=Path(__file__).parent
 c7,h=pickle.loads((base/'agent4_bch_candidate.pkl').read_bytes())
 out=defaultdict(F)
 for w,v in h.items():
  for i in range(2):
   for z,t in ev(w,i).items():out[i,z]+=v*t
 out={k:v for k,v in out.items() if v}
 print('nonzero',len(out),'denominators',Counter(v.denominator for v in out.values()),flush=True)
 assert all(v.denominator==1 for v in out.values())
 out={k:int(v) for k,v in out.items()}
 print('multidegrees',Counter(tuple(z.count(j)-(i==j) for j in range(3)) for i,z in out),flush=True)
 with (base/'agent4_candidate_tau8.pkl').open('wb') as f:pickle.dump(out,f)
 print('mod3 support',sum(v%3!=0 for v in out.values()),flush=True)
