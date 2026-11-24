"""Standalone literal-word audit of compact central-cover data."""
import json
from degree2_certificate import red,inv,compose
from agent2_compact_cover_seeds import generate

def check():
 d=json.load(open('workspace/agent2_nielsen_actions_n3.json'))
 iw=json.load(open('workspace/agent2_nielsen_inverse_words_n3.json'))
 def sub(w,mp):return red(y for x in w for y in (mp[x-1] if x>0 else inv(mp[-x-1])))
 for s in ['T','P','I','C']:
  fw=d['actions'][s]['words'];bw=iw[s]
  for i in range(9):assert sub(fw[i],bw)==(i+1,) and sub(bw[i],fw)==(i+1,)
 gs=[tuple(map(tuple,f)) for f in d['generators']];gis=[tuple(map(tuple,f)) for f in d['inverses']];ident=((1,),(2,),(3,))
 def ev(w):
  f=ident
  for x in w:f=compose(f,gs[x-1] if x>0 else gis[-x-1])
  return f
 for s in ['T','P','I','C']:
  a=d['actions'][s];t=tuple(map(tuple,a['auto']));ti=tuple(map(tuple,a['inverse']))
  assert compose(t,ti)==ident and compose(ti,t)==ident
  for g,w in zip(gs,a['words']):assert ev(w)==compose(t,compose(g,ti))
 out=generate()
 for w in out['iterated_relators']:assert ev(w)==ident
 print('PASS literalfreeinverseactions, exactAutconjugations, all261seedidentities')
 return out
if __name__=='__main__':check()
