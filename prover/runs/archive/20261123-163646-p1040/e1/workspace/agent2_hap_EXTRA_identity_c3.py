"""Exact HAP spherical identities translated to genuine IA3 class3 vectors."""
import json,pickle
from pathlib import Path
from functools import lru_cache
from sage.all import Matrix,ZZ
from agent1_degree3 import mul,add,expand
from agent1_degree3_closure import initial_vector
from degree2_certificate import inv,red,compose

def run():
 cells=json.load(open('workspace/agent2_HAP_extra_free_identities.json'))
 hd=json.load(open('workspace/agent3_hap_relator_words_ALL.json'))
 ad=json.load(open('workspace/agent2_nielsen_actions_n3.json'));iw=json.load(open('workspace/agent2_nielsen_inverse_words_n3.json'))
 mp={}
 for i,s in enumerate(['T','P','I','C'],1):
  mp[i]=[add(expand(w),{():1},-1) for w in ad['actions'][s]['words']]
  mp[-i]=[add(expand(w),{():1},-1) for w in iw[s]]
 @lru_cache(None)
 def subword(a,w):
  p={():1}
  for i in w:p=mul(p,mp[a][i])
  return p
 def apply(a,p):
  o={}
  for w,x in p.items():o=add(o,subword(a,w),x)
  return o
 lifts=[x['word'] for x in hd['lifts']]
 gs=[tuple(map(tuple,f)) for f in ad['generators']];gis=[tuple(map(tuple,f)) for f in ad['inverses']];ident=((1,),(2,),(3,))
 def ev(w):
  f=ident
  for x in w:f=compose(f,gs[x-1] if x>0 else gis[-x-1])
  return f
 for i,w in enumerate(hd['magnus_relator_lifts']):
  if w is not None:assert ev(w)==tuple(map(tuple,hd['relator_auts'][i]))
 out=[]
 for cell in cells:
  original=();p={():1}
  for u,i,s in cell['terms']:
   r=tuple(hd['relators'][i]);r=r if s>0 else inv(r)
   original=red(original+tuple(u)+r+inv(u))
   ww=hd['magnus_relator_lifts'][i];assert ww is not None
   ww=tuple(ww) if s>0 else inv(ww);term=expand(ww)
   autword=red(x for a in u for x in (lifts[a-1] if a>0 else inv(lifts[-a-1])))
   for a in reversed(autword):term=apply(a,term)
   p=mul(p,term)
  assert not original
  assert not any(len(w)==1 for w in p)
  out.append(initial_vector(p));print('HAPcell',cell['cell'],'done',flush=True)
 Path('workspace/agent2_hap_EXTRA_identity_c3_vectors.json').write_text(json.dumps([[int(x) for x in v] for v in out]))
 H,C,B=pickle.loads(Path('workspace/agent2_degree3_cache.pkl').read_bytes())
 HH=H.stack(Matrix(ZZ,out)).hermite_form(include_zero_rows=False)
 print('HAPknowncellvectors',len(out),'oldlatticeunchanged?',HH==H,flush=True)
 return out
if __name__=='__main__':run()
