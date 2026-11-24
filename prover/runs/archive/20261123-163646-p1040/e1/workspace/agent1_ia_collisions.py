"""Exact IA3 relation search by equal reduced-word automorphism images."""
import json,time
from pathlib import Path
from agent1_degree3 import *
from agent1_degree3_closure import initial_vector,row_basis

def search(radius=4):
 data=json.load(open('workspace/agent2_nielsen_actions_n3.json'))
 IG=[tuple(map(tuple,f)) for f in data['inverses']]
 ident=tuple((i+1,) for i in range(N))
 for g,h in zip(G,IG):assert compose(g,h)==ident and compose(h,g)==ident
 table={ident:()};front=[(ident,())];rels=[];seen=set();start=time.time()
 for r in range(1,radius+1):
  nxt=[]
  for f,w in front:
   for s in range(-m,m+1):
    if s==0 or (w and s==-w[-1]):continue
    h=compose(f,G[s-1] if s>0 else IG[-s-1]);v=w+(s,)
    if h in table:
     rel=red(v+inv(table[h]))
     if not rel:continue
     ex=expand(rel);z=tuple(initial_vector(ex))
     if not any(z) or z in seen or tuple(-x for x in z) in seen:continue
     seen.add(z);rels.append(rel)
    else:table[h]=v;nxt.append((h,v))
  front=nxt
  print('radius',r,'images',len(table),'frontier',len(front),'distinct nonzero class3 relations',len(rels),'seconds',round(time.time()-start,2),flush=True)
 path=Path('workspace/agent1_ia3_collision_relators.json');path.write_text(json.dumps(rels))
 print('saved',path,flush=True)
 return rels
if __name__=='__main__':search(4)
