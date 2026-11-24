"""True IA3 Peiffer relators, truncated free Magnus expansions through degree3."""
import json
from pathlib import Path
from functools import lru_cache
from sage.all import Matrix,ZZ
from agent1_degree3 import mul,add,expand,compose,inv,G,m
from agent1_degree3_closure import initial_vector

def generate():
 d=json.load(open('workspace/agent2_nielsen_actions_n3.json'))
 wdata=json.load(open('workspace/agent2_magnus_aut_words_n3.json'))
 order=wdata['action_order'];maps=[]
 for name in order:maps.append([add(expand(w),{():1},-1) for w in d['actions'][name]['words']])
 @lru_cache(None)
 def subword(a,w):
  p={():1}
  for i in w:p=mul(p,maps[a][i])
  return p
 def apply(a,p):
  out={}
  for w,x in p.items():out=add(out,subword(a,w),x)
  return out
 # Positive words for inverses of T,P,I,C. I_1=P I P.
 inverse={1:(2,3,2,1,2,3,2),2:(2,),3:(3,),4:(4,4)}
 aa=[tuple(map(tuple,d['actions'][s]['auto'])) for s in order]
 ai=[tuple(map(tuple,d['actions'][s]['inverse'])) for s in order]
 ident=((1,),(2,),(3,))
 def ev(w):
  f=ident
  for x in w:f=compose(f,aa[x-1] if x>0 else ai[-x-1])
  return f
 for i,w in inverse.items():assert ev(w)==ai[i-1]
 rel=[];vectors=[]
 for gi,ww in enumerate(wdata['words']):
  positive=tuple(y for x in ww for y in ((x,) if x>0 else inverse[-x]))
  assert ev(positive)==G[gi]
  for h in range(m):
   p=expand((h+1,))
   for a in reversed(positive):p=apply(a-1,p)
   # inverse of g_i g_h g_i^-1 is g_i g_h^-1 g_i^-1.
   p=mul(p,expand((gi+1,-h-1,-gi-1)))
   assert not any(len(w)==1 for w in p)
   vector=initial_vector(p)
   rel.append({'g':gi,'h':h,'expansion':[[list(w),int(x)] for w,x in sorted(p.items())]})
   vectors.append(vector)
  print('Peiffer block',gi+1,'done',flush=True)
 Path('workspace/agent2_peiffer_degree3.json').write_text(json.dumps(rel))
 Path('workspace/agent2_peiffer_degree3_vectors.json').write_text(json.dumps([[int(x) for x in v] for v in vectors]))
 print('81 true relator vectors rank',Matrix(ZZ,vectors).rank(),flush=True)
 return vectors
if __name__=='__main__':generate()
