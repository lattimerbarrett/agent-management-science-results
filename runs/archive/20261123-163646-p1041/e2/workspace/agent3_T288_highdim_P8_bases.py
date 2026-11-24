import json,pathlib,sys,collections
sys.path.insert(0,'workspace')
from agent3_graph_lifts import veronese,kernel
from agent3_lift_closure import closure
raw=json.loads(pathlib.Path('workspace/agent1_boundary272_relatives.json').read_text())['seeds']
vv=veronese(8,3);out=[]
for obj in raw:
 B=sorted({(p&127)|((p>>10)<<7) for p in obj['support']});assert len(B)==34
 E=[p for p,_ in closure(B,veronese(8,2))[0]]
 D={}
 for p in B:
  z=vv[p]
  while z:
   h=z.bit_length()-1
   if h in D:z^=D[h]
   else:D[h]=z;break
 def red(z):
  for h in sorted(D,reverse=True):
   if z>>h&1:z^=D[h]
  return z
 buckets={}
 for p in E:buckets.setdefault(red(vv[p]),[]).append(p)
 assert 0 not in buckets
 pairs=[(p,q) for group in buckets.values() for i,p in enumerate(group) for q in group[:i]]
 out.append({'type':obj['type'],'Q':obj['Q'],'base':B,'extra':E,'pairs':pairs})
print('hist',collections.Counter((len(o['extra']),len(o['pairs'])) for o in out))
pathlib.Path('workspace/agent3_T288_highdim_P8_bases.json').write_text(json.dumps(out,indent=2))
pathlib.Path('workspace/agent3_T288_highdim_P8_bases.py').write_text(pathlib.Path(__file__).read_text())
