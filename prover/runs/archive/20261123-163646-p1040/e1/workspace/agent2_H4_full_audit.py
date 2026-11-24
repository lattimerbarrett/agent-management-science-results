"""Sanity audit of the purported central cover's class4 quotient.
No actual IA counterexample claim; all output hypotheses are tested.
"""
import json,time
from pathlib import Path
from sage.all import *
from sage.libs.gap.libgap import libgap
from agent1_degree3 import commuting_relators
from degree2_certificate import red,inv

def run():
 libgap.eval('LoadPackage("lpres",false:OnlyNeeded:=true)')
 d=json.load(open('workspace/agent2_compact_cover_seeds.json'))
 F=libgap.FreeGroup(9);gen=list(libgap.GeneratorsOfGroup(F))
 def word(w):
  q=libgap.One(F)
  for x in w:q=q*gen[abs(x)-1]**(1 if x>0 else -1)
  return q
 endos=[libgap.GroupHomomorphismByImages(F,F,gen,[word(w) for w in a]) for a in d['endomorphisms'][:4]]
 rels=[word(w) for w in d['iterated_relators'] if w]+[word(w) for w,ex in commuting_relators()]
 H=libgap.LPresentedGroup(F,[],endos,rels)
 t=time.time();Q=libgap.NilpotentQuotient(H,4);e=libgap.NilpotentQuotientSystem(H)['Epimorphism'];R=libgap.Range(e)
 ims=[libgap.Image(e,g) for g in libgap.GeneratorsOfGroup(H)]
 print('Q4computed',time.time()-t,flush=True)
 # Export an exact pc presentation, allowing fast reconstruction in a new run.
 iso=libgap.IsomorphismFpGroup(R);fp=libgap.Range(iso)
 save={'generators':len(list(libgap.GeneratorsOfGroup(fp))),'relators':[[int(x) for x in libgap.LetterRepAssocWord(r)] for r in libgap.RelatorsOfFpGroup(fp)],'original_images':[[int(x) for x in libgap.LetterRepAssocWord(libgap.UnderlyingElement(libgap.Image(iso,g)))] for g in ims]}
 Path('workspace/agent2_H4_pc_presentation.json').write_text(json.dumps(save))
 print('ExportedQ4presentation',save['generators'],'generators',len(save['relators']),'relations',flush=True)
 def ev(w):
  p=ims[0]**0
  for x in w:p=p*ims[abs(x)-1]**(1 if x>0 else -1)
  return p
 result={'seed_failures':[],'one_step_image_failures':[],'operator_homomorphisms':[]}
 def dump():Path('workspace/agent2_H4_full_audit.json').write_text(json.dumps(result))
 for i,w in enumerate(d['iterated_relators']):
  if not bool(libgap.IsOne(ev(w))):result['seed_failures'].append(i)
  for a,mp in enumerate(d['endomorphisms']):
   sw=red(y for x in w for y in (mp[x-1] if x>0 else inv(mp[-x-1])))
   if not bool(libgap.IsOne(ev(sw))):result['one_step_image_failures'].append([i,a])
 print('Seedfailures',result['seed_failures'],'imagefailures',result['one_step_image_failures'],flush=True);dump()
 def comm(x,y):return x*y*x**-1*y**-1
 beta=comm(comm(ims[2],ims[8]),ims[7]);result['beta_order']=str(libgap.Order(beta));result['beta_brackets_isone']=[bool(libgap.IsOne(comm(beta,g))) for g in ims]
 print('beta',result['beta_order'],result['beta_brackets_isone'],flush=True);dump()
 for i,mp in enumerate(d['endomorphisms']):
  hom=libgap.GroupHomomorphismByImages(R,R,ims,[ev(w) for w in mp]);valid=bool(hom!=libgap.fail)
  result['operator_homomorphisms'].append(valid);print('operator',i,'descends?',valid,flush=True);dump()
 return result
if __name__=='__main__':run()
