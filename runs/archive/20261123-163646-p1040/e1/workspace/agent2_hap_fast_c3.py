"""Fast exact BCH translation of independently checked HAP identities."""
import json,pickle
from pathlib import Path
from sage.all import vector,ZZ,Matrix,zero_vector
from agent2_fast_bch3 import actions,actionword,wordlog,bch,oldcoords,dim
from degree2_certificate import inv,red

def run(fn='workspace/agent2_HAP_extra_free_identities.json'):
 cells=json.load(open(fn));hd=json.load(open('workspace/agent3_hap_relator_words_ALL.json'))
 ac=actions();S={}
 for i,d in enumerate(hd['lifts'],1):S[i]=actionword(d['word'],ac);S[-i]=actionword(inv(d['word']),ac)
 logs=[wordlog(w) for w in hd['magnus_relator_lifts']];out=[]
 for cell in cells:
  p=zero_vector(ZZ,dim);original=()
  for u,i,s in cell['terms']:
   r=tuple(hd['relators'][i]);r=r if s>0 else inv(r);original=red(original+tuple(u)+r+inv(u))
   v=s*logs[i]
   for a in reversed(u):v=S[a]*v
   p=bch(p,v)
  assert not original
  out.append(oldcoords(p));print('fastHAPcell',cell['cell'],'done',flush=True)
 H,C,B=pickle.loads(Path('workspace/agent2_degree3_cache.pkl').read_bytes());HH=H.stack(Matrix(ZZ,out)).hermite_form(include_zero_rows=False)
 print('HAPvectors',len(out),'oldHNFunchanged?',HH==H,flush=True)
 name=Path(fn).stem
 Path('workspace/agent2_fast_'+name+'_c3_vectors.json').write_text(json.dumps([[int(x) for x in v] for v in out]))
 return out
if __name__=='__main__':run()
