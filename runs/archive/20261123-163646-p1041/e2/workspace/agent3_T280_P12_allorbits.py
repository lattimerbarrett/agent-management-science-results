import json,pathlib,sys,itertools,collections
sys.path.insert(0,'workspace')
from agent3_graph_lifts import veronese,kernel
from agent3_lift_closure import closure
raw=[{'solvable': True, 'type': 'linear', 'support': [0, 1, 12, 13, 35, 39, 43, 44, 45, 46, 48, 49, 50, 54, 58, 63, 512, 513, 515, 519, 523, 526, 531, 535, 539, 540, 541, 542, 564, 565, 568, 569]}, {'solvable': True, 'type': 'affine_singular', 'support': [4, 5, 12, 13, 35, 39, 43, 44, 45, 46, 50, 52, 53, 54, 58, 63, 515, 516, 517, 519, 523, 526, 531, 535, 539, 540, 541, 542, 560, 561, 568, 569]}, {'solvable': True, 'type': 'affine_nonsingular', 'support': [1, 2, 13, 14, 53, 54, 57, 58, 513, 514, 515, 519, 523, 524, 531, 535, 539, 540, 541, 542, 547, 551, 555, 556, 557, 558, 560, 561, 562, 564, 568, 575]}]
def bas(cols):
 d={}
 for z in cols:
  while z:
   h=z.bit_length()-1
   if h in d:z^=d[h]
   else:d[h]=z;break
 return d
allres=[]
for obj in raw:
 if not obj['solvable']:continue
 B={(p&63)|((p>>9)<<6) for p in obj['support']};assert len(B)==32
 E0=[p for p,_ in closure(B,veronese(7,2))[0]];assert len(E0)==16
 basecodes={}
 for degree in [3,4,5]:
  vv=veronese(7,degree);DD=bas(vv[p] for p in B)
  def rd(z):
   for h in sorted(DD,reverse=True):
    if z>>h&1:z^=DD[h]
   return z
  ss=[rd(vv[p]) for p in E0];KK=kernel(range(len(E0)),ss);hh=collections.Counter();z=0
  for i in range(1<<len(KK)):
   if i:z^=KK[(i&-i).bit_length()-1]
   hh[z.bit_count()]+=1
  basecodes[degree]={'dimension':len(KK),'histogram':dict(sorted(hh.items())),'basis':KK}
 assert basecodes[5]['dimension']==0
 assert basecodes[4]['histogram']=={0:1,16:1}
 assert min(w for w in basecodes[3]['histogram'] if w)>3
 allres.append({'type':obj['type'],'base':sorted(B),'extra':E0,'relative_codes':basecodes})
 print(obj['type'],basecodes,flush=True)
# Exhaust all subsets F2^3 to check fibre minimum conditions
small={}
for d in [0,1,2]:
 vv=veronese(3,d);allowed=[]
 for z in range(256):
  syn=0
  for i in range(8):
   if z>>i&1:syn^=vv[i]
  if syn==0:allowed.append(z)
 small[d]={'count':len(allowed),'minimum':min(z.bit_count() for z in allowed if z)}
assert small=={0:{'count':128,'minimum':2},1:{'count':16,'minimum':4},2:{'count':2,'minimum':8}}
pathlib.Path('workspace/agent3_T280_P12_allorbits.json').write_text(json.dumps({'base_orbits':allres,'fibre_minima':small},indent=2))
pathlib.Path('workspace/agent3_T280_P12_allorbits.py').write_text(pathlib.Path(__file__).read_text())
