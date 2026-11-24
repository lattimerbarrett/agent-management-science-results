import json,sys
from functools import lru_cache
from agent1_fast_c3_action import *

def main():
 sys.setrecursionlimit(50000)
 acts=json.load(open('workspace/agent2_nielsen_actions_n3.json'))['actions']
 names=['T','P','I','C'];AA=[ew(acts[x]['words']) for x in names];AI=[ei(a) for a in AA]
 data=json.load(open('workspace/agent3_hap_relator_words_ALL.json'))
 def aw(w,G,GI):
  e=ID
  for s in w:e=ec(e,G[s-1] if s>0 else GI[-s-1])
  return e
 GG=[aw(d['word'],AA,AI) for d in data['lifts']]
 CC=AA[3];CCI=AI[3];II=AA[2];I1=ec(CC,ec(II,CCI));I2=ec(CC,ec(I1,CCI))
 GG.append(ec(II,ec(I1,I2)));GI=[ei(a) for a in GG]
 MM={i+1:amatrix(g) for i,g in enumerate(GG)};MM.update({-i-1:amatrix(g) for i,g in enumerate(GI)})
 prod=json.load(open('workspace/agent3_GL3_product_identities.json'))
 diffs={d['name']:d for d in json.load(open('workspace/agent3_HAP_comparison_differences_EXACT.json'))}
 vals=[tuple(logs12(expand(tuple(w)))) for w in prod['relator_magnus_words']]
 vals +=[tuple(logs12(expand(tuple(diffs[n]['magnus_word'])))) for n in names]
 L=[((4,) if diffs[n]['epsilon'] else ())+tuple(diffs[n]['q']) for n in names]
 @lru_cache(None)
 def act(q,f):
  if not q:return vals[f]
  return applymat(MM[q[0]],act(q[1:],f))
 rows=[]
 fill=json.load(open('workspace/agent2_hap_comparison_fillings.json'))
 for key,rec in fill['fillings'].items():
  X=({}, {}, {});prefix=()
  for s in rec['aut_operator_relator']:
   i=abs(s)-1
   if s>0:
    v=act(prefix,11+i);X=bch12(X,polys(v));prefix=red(prefix+L[i])
   else:
    prefix=red(prefix+inv(L[i]));v=act(prefix,11+i);X=bch12(X,polys(tuple(-x for x in v)))
  assert prefix==tuple(rec['hap_GL_word'])
  fw=()
  for idx,u in rec['terms_u_inverse_r_u']:
   j=abs(idx)-1;r=tuple(prod['relators'][j]);u=tuple(u)
   fw=red(fw+inv(u)+(r if idx>0 else inv(r))+u)
   v=act(inv(u),j)
   if idx<0:v=tuple(-x for x in v)
   X=bch12(X,polys(v))
  assert fw==prefix
  assert not X[0]
  z=coords2(div(X[1],12))+coords(div(X[2],6));rows.append(z)
  print('VALUEcomparison relator',key,'nterms',len(rec['terms_u_inverse_r_u']),'nonzeros',sum(x!=0 for x in z),flush=True)
 json.dump(rows,open('workspace/agent1_hap_value_c3_vectors.json','w'))
 return rows
if __name__=='__main__':main()
