"""Translate checked GL3 relator identities into genuine IA3 cubic vectors."""
import json,pickle
from pathlib import Path
from functools import lru_cache
from sage.all import Matrix,ZZ
from agent1_degree3 import mul,add,expand
from agent1_degree3_closure import initial_vector
from degree2_certificate import inv

def run():
 data=json.load(open('workspace/agent2_idrel_gl3_identities.json'));na=data['aut_relator_count']
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
 out=[]
 for J in data['identities']:
  p={():1}
  for ri,u in J:
   if abs(ri)<=na:continue
   gi=abs(ri)-na;term=expand((gi if ri>0 else -gi,))
   # Term is u^-1 r u, hence apply conjugation by u^-1.
   for a in reversed(inv(u)):term=apply(a,term)
   p=mul(p,term)
  assert not any(len(w)==1 for w in p)
  out.append(initial_vector(p))
 Path('workspace/agent2_idrel_c3_vectors.json').write_text(json.dumps([[int(x) for x in v] for v in out]))
 H,C,B=pickle.loads(Path('workspace/agent2_degree3_cache.pkl').read_bytes())
 HH=H.stack(Matrix(ZZ,out)).hermite_form(include_zero_rows=False)
 print('translated',len(out),'trueIArelations; oldHNFunchanged?',HH==H,flush=True)
 return out
if __name__=='__main__':run()
