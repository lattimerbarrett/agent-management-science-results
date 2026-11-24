import sys,itertools,json
from functools import lru_cache
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,'workspace')
from agent4_exact_mccool import br,add

def lyndon(w):return all(w<w[i:] for i in range(1,len(w)))
@lru_cache(None)
def words(d):return [w for w in itertools.product(range(3),repeat=d) if lyndon(w)]
# standard bracketing uses longest proper Lyndon suffix
@lru_cache(None)
def split(w):
 for i in range(1,len(w)):
  if lyndon(w[i:]):return w[:i],w[i:]
def K(i,j):return {(i,(j,i)):1,(i,(i,j)):-1}
inners=[add(K((j+1)%3,j),K((j+2)%3,j),1) for j in range(3)]
outers=[K(1,0),K(0,1),K(0,2)]
@lru_cache(None)
def evalw(w,inner):
 if len(w)==1:return (inners if inner else outers)[w[0]]
 u,v=split(w);return br(evalw(u,inner),evalw(v,inner))
ws=[w for w in words(6) if all(w.count(i)==2 for i in range(3))]
cols=[(inner,w) for inner in [True,False] for w in ws]
pivs={};relations=[]
for c,key in enumerate(cols):
 a=evalw(key[1],key[0]).copy();track={c:Fraction(1)}
 while a:
  k=min(a)
  if k in pivs:
   b,t=pivs[k];coef=-a[k];a=add(a,b,coef);track=add(track,t,coef)
  else:
   v=a[k];a={k:Fraction(z,v) for k,z in a.items()};track={k:z/v for k,z in track.items()};pivs[k]=(a,track);break
 if not a:relations.append(track)
print(len(ws),len(cols),len(pivs),len(relations))
for rel in relations:
 for i,v in rel.items():print(cols[i],v)
out=[{'inner':cols[i][0],'word':cols[i][1],'coefficient':str(v)} for i,v in relations[0].items()]
Path('workspace/agent4_mccool_degree6_relation.json').write_text(json.dumps(out,indent=2))
