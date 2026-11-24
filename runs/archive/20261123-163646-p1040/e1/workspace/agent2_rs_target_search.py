"""Target short Magnus expressions at long RS-completion edge expressions."""
import json,pickle
from pathlib import Path
from agent2_nielsen_actions import magnus
from degree2_certificate import compose,inv,red
from agent1_degree3 import expand
from agent1_degree3_closure import initial_vector
from sage.all import Matrix,ZZ

def run(depth=5):
 ident,gs,gis,names=magnus(3)
 cache=pickle.loads(Path('workspace/agent2_rs_edgecache.pkl').read_bytes())
 letters=[(i+1,g) for i,g in enumerate(gs)]+[(-i-1,gis[i]) for i,g in enumerate(gs)]
 tab={ident:()};front=[ident]
 rel=[];seen=set();matches=0
 for dep in range(1,depth+1):
  new=[]
  for f in front:
   w=tab[f]
   for x,g in letters:
    if w and w[-1]==-x:continue
    h=compose(f,g);ww=w+(x,)
    if h in cache and len(cache[h])>len(ww):
     r=red(cache[h]+inv(ww));v=tuple(initial_vector(expand(r)));matches+=1
     if any(v) and v not in seen:seen.add(v);rel.append((r,v))
    if dep<depth and h not in tab:tab[h]=ww;new.append(h)
  front=new
  print('depth',dep,'stored',len(tab),'matches',matches,'distinctvectors',len(rel),flush=True)
 Path('workspace/agent2_rs_target_relator_words.json').write_text(json.dumps([r for r,v in rel]))
 Path('workspace/agent2_rs_target_relator_vectors.json').write_text(json.dumps([v for r,v in rel]))
 H,C,B=pickle.loads(Path('workspace/agent2_degree3_cache.pkl').read_bytes())
 if rel:
  HH=H.stack(Matrix(ZZ,[v for r,v in rel])).hermite_form(include_zero_rows=False)
  print('relation lattice unchanged?',HH==H,flush=True)
 return rel
if __name__=='__main__':run()
