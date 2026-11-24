import json
from functools import lru_cache
from agent1_degree3 import *
from agent1_degree3_closure import initial_vector
from agent1_peiffer_c3 import ew,ec,ei,ID,ONE,subst,tmul

def main():
 acts=json.load(open('workspace/agent2_nielsen_actions_n3.json'))['actions']
 order=['T','P','I','C'];AA=[ew(acts[x]['words']) for x in order]
 AI=[ei(a) for a in AA]
 data=json.load(open('workspace/agent3_hap_relator_words_ALL.json'))
 ids=json.load(open('workspace/agent1_HAP_SL3Z_random_free_identities.json'))
 def actword(w,gens,invs):
  e=ID
  for s in w:e=ec(e,gens[s-1] if s>0 else invs[-s-1])
  return e
 GG=[actword(d['word'],AA,AI) for d in data['lifts']];GI=[ei(a) for a in GG]
 @lru_cache(None)
 def aq(q):
  if not q:return ID
  return ec(aq(q[:-1]),GG[q[-1]-1] if q[-1]>0 else GI[-q[-1]-1])
 rows=[]
 for identity in ids:
  out=ONE
  fw=()
  for q,f,s in identity['terms']:
   r=tuple(data['relators'][f]);fw=red(fw+tuple(q)+(r if s>0 else inv(r))+inv(tuple(q)))
   w=data['magnus_relator_lifts'][f]
   assert w is not None
   p=expand(tuple(w) if s>0 else inv(tuple(w)))
   out=tmul(out,add(subst(add(p,ONE,-1),aq(tuple(q))),ONE))
  assert not fw,'source identity notfree'
  z=initial_vector(out);rows.append(z)
  print('translated genuine3cell IArelator',identity['cell'],'nonzeroentries',sum(x!=0 for x in z),flush=True)
 json.dump(rows,open('workspace/agent1_hap_random_identity_c3_vectors.json','w'))
 return rows
if __name__=='__main__':main()
