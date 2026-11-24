import json,pathlib,sys,itertools,collections,time
sys.path.insert(0,'workspace')
from agent3_graph_lifts import veronese,kernel
from agent3_lift_closure import closure
raw=json.loads(pathlib.Path('workspace/agent4_boundary256_orbits.json').read_text())[0]
B={(p&63)|((p>>9)<<6) for p in raw['support']}
E0=[p for p,_ in closure(B,veronese(7,2))[0]]
print('baseextra',len(E0),E0)
bb={}
for x in E0:
 z=x^E0[0]
 while z:
  h=z.bit_length()-1
  if h in bb:z^=bb[h]
  else:bb[h]=z;break
print('extra affine rank',len(bb))
S=sorted(p+(r<<7) for p in B for r in range(8));E=sorted(p+(r<<7) for p in E0 for r in range(8));vs=veronese(10,5)
def bas(cols):
 d={}
 for z in cols:
  while z:
   h=z.bit_length()-1
   if h in d:z^=d[h]
   else:d[h]=z;break
 return d
D=bas(vs[p] for p in S)
def red(z):
 for h in sorted(D,reverse=True):
  if z>>h&1:z^=D[h]
 return z
syn=[red(vs[p]) for p in E]
print('relative rank',len(bas(syn)),'nullity',len(E)-len(bas(syn)),flush=True)
# kernel helper uses indices list as S, custom vs syndromes
K=kernel(range(len(E)),syn)
print('kernel',len(K),'basisweights',dict(collections.Counter(x.bit_count() for x in K)))
ward={'singles_mod8':dict(collections.Counter(x.bit_count()%8 for x in K)), 'pairs_mod4':dict(collections.Counter((a&b).bit_count()%4 for a,b in itertools.combinations(K,2))), 'triples_mod2':dict(collections.Counter((a&b&c).bit_count()%2 for a,b,c in itertools.combinations(K,3)))}
print('Ward',ward)
basecodes={}
for degree in [2,3,4,5]:
 vv=veronese(7,degree);DD=bas(vv[p] for p in B)
 def rd(z):
  for h in sorted(DD,reverse=True):
   if z>>h&1:z^=DD[h]
  return z
 ss=[rd(vv[p]) for p in E0];KK=kernel(range(len(E0)),ss)
 hh=collections.Counter();z=0
 for i in range(1<<len(KK)):
  if i:z^=KK[(i&-i).bit_length()-1]
  hh[z.bit_count()]+=1
 basecodes[degree]={'dimension':len(KK),'histogram':dict(sorted(hh.items())),'basis':KK}
print('BASECODES',basecodes)
res={'extra_base':E0,'relative_nullity':len(K),'ward':ward,'basecodes':basecodes}
if len(K)<=25:
 val=0;hist=collections.Counter();words=[];t=time.time()
 for i in range(1<<len(K)):
  if i:val^=K[(i&-i).bit_length()-1]
  w=val.bit_count();hist[w]+=1
  if w==12:words.append([E[j] for j in range(len(E)) if val>>j&1])
 print('hist',dict(sorted(hist.items())),'P12',len(words),'secs',time.time()-t)
 res.update(histogram=dict(hist),P12=words)
pathlib.Path('workspace/agent3_T280_relativeP12.json').write_text(json.dumps(res,indent=2))
pathlib.Path('workspace/agent3_T280_relativeP12.py').write_text(pathlib.Path(__file__).read_text())
