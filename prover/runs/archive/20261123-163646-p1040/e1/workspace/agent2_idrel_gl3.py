"""Partial logged Knuth-Bendix produces exact GL3 relator identities.
No convergence or completeness claim. Every extracted identity is checked
as a literal free-group word before being used.
"""
import json
from pathlib import Path
from sage.all import *
from sage.libs.gap.libgap import libgap
from degree2_certificate import red,inv,compose

def run(passes=1):
 assert bool(libgap.eval('LoadPackage("idrel",false:OnlyNeeded:=true)'))
 d=json.load(open('workspace/agent2_compact_cover_seeds.json'))
 raw=d['aut_operator_relators']+d['magnus_aut_words_normalized'];na=len(d['aut_operator_relators'])
 F=libgap.FreeGroup(4);gg=list(libgap.GeneratorsOfGroup(F))
 def word(w):
  q=libgap.One(F)
  for x in w:q=q*gg[abs(x)-1]**(1 if x>0 else -1)
  return q
 G=F/libgap([word(w) for w in raw]);libgap.set_global('AG2GL',G)
 libgap.eval('(function() ArrangeMonoidGenerators(AG2GL); AG2M:=MonoidPresentationFpGroup(AG2GL); return true; end)()')
 libgap.eval('AG2Ids:=[]')
 methods=libgap.MethodsOperation(libgap.LoggedOnePassKB,2)
 f=methods[len(methods)-1]['func']
 src=str(f).replace('redrule := LogSequenceReduce( mG, L );','Add( AG2Ids, L ); redrule := LogSequenceReduce( mG, L );')
 libgap.eval('AG2OnePass:='+src)
 libgap.eval('(function() AG2Rules:=InitialLoggedRulesOfPresentation(AG2M); return true; end)()')
 print('Initialrules',libgap.eval('Length(AG2Rules)'),flush=True)
 for j in range(passes):
  libgap.eval('(function() AG2Rules:=AG2OnePass(AG2M,AG2Rules); return true; end)()')
  print('pass',j+1,'rules',libgap.eval('Length(AG2Rules)'),'identities',libgap.eval('Length(AG2Ids)'),flush=True)
  libgap.eval('(function() AG2Rules:=LoggedRewriteReduce(AG2M,AG2Rules); return true; end)()')
  print('reducedrules',libgap.eval('Length(AG2Rules)'),flush=True)
 # Export via the monoid presentation homomorphism to the original F4.
 data=libgap.eval('List(AG2Ids,J->List(J,c->[c[1],LetterRepAssocWord(Image(HomomorphismOfPresentation(AG2M),c[2]))]))').sage()
 original=libgap.eval('List(RelatorsOfFpGroup(AG2GL),LetterRepAssocWord)').sage()
 mapped=libgap.eval('List(GroupRelatorsOfPresentation(AG2M),r->LetterRepAssocWord(Image(HomomorphismOfPresentation(AG2M),r)))').sage()
 assert [red(w) for w in original]==[red(w) for w in mapped]
 good=[];freecount=0;badcount=0
 ad=json.load(open('workspace/agent2_nielsen_actions_n3.json'))
 aa={}
 for i,name in enumerate(['T','P','I','C'],1):
  aa[i]=tuple(map(tuple,ad['actions'][name]['auto']));aa[-i]=tuple(map(tuple,ad['actions'][name]['inverse']))
 ident=((1,),(2,),(3,))
 for J in data:
  p=()
  for ri,u in J:
   r=tuple(original[abs(ri)-1]);r=r if ri>0 else inv(r)
   p=red(p+inv(u)+r+tuple(u))
  if not p:freecount+=1
  f=ident
  for x in p:f=compose(f,aa[x])
  if f!=ident:badcount+=1;continue
  good.append([[int(ri),list(map(int,u))] for ri,u in J])
 out={'aut_relator_count':na,'presentation_relators':[[int(x) for x in w] for w in original],'identities':good}
 Path('workspace/agent2_idrel_gl3_identities.json').write_text(json.dumps(out))
 print('PASS',len(good),'actualAutrelatoridentities; freelyexact',freecount,'invaliddiscarded',badcount,flush=True)
 return out
if __name__=='__main__':run()
