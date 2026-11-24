"""True IA3 relators from exact AutF3 relation action consistency."""
import json
from pathlib import Path
from functools import lru_cache
from sage.all import Matrix,ZZ
from agent1_degree3 import mul,add,expand,compose,G,m
from agent1_degree3_closure import initial_vector

def generate():
 d=json.load(open('workspace/agent2_nielsen_actions_n3.json'))
 ar=json.load(open('workspace/agent3_AutF3_presentation.json'))
 order=['T','P','I','C'];maps=[]
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
 aa=[tuple(map(tuple,d['actions'][s]['auto'])) for s in order];ident=((1,),(2,),(3,))
 def ev(w):
  f=ident
  for x in w:f=compose(f,aa[x-1])
  return f
 I0=(3,);I1=(4,3,4,4);I2=(4,4,3,4)
 S=I0+I1+I2+(4,);T=(3,2);U=(1,)
 ainv={1:S*5,2:T*3,3:(2,3,2,1,2,3,2)};apos={1:S,2:T,3:U}
 for k,w in apos.items():assert ev(w)==tuple(map(tuple,ar['aut_images'][k-1]))
 for k,w in ainv.items():assert ev(w)==tuple(map(tuple,ar['inverse_images'][k-1]))
 vectors=[]
 for j,raw in enumerate(ar['relators']):
  # GAP uses right action, hence reverse its word for left composition.
  w=tuple(a for x in reversed(raw) for a in (apos[x] if x>0 else ainv[-x]))
  assert ev(w)==ident,('Aut relation',j)
  for h in range(m):
   p=expand((h+1,))
   for a in reversed(w):p=apply(a-1,p)
   p=mul(p,expand((-h-1,)));assert not any(len(t)==1 for t in p)
   vectors.append(initial_vector(p))
  print('Aut relation block',j+1,'done',flush=True)
 # Add simple inverse/order consistency for the chosen T,P,I,C generators.
 loops=[(2,2),(3,3),(4,4,4),(1,2,3,2,1,2,3,2)]
 for w in loops:
  assert ev(w)==ident
  for h in range(m):
   p=expand((h+1,))
   for a in reversed(w):p=apply(a-1,p)
   vectors.append(initial_vector(mul(p,expand((-h-1,)))))
 Path('workspace/agent2_aut_consistency_degree3_vectors.json').write_text(json.dumps([[int(x) for x in v] for v in vectors]))
 print(len(vectors),'true consistency vectors rank',Matrix(ZZ,vectors).rank(),flush=True)
 return vectors
if __name__=='__main__':generate()
