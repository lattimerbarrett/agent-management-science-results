"""Exact logged fillings of Aut two-cells in the HAP GL3 presentation.
Accept only literal free-word equality of each exported filling.
"""
import json
from pathlib import Path
from sage.all import *
from sage.libs.gap.libgap import libgap
from degree2_certificate import red,inv

def run(passes=3):
 libgap.eval('LoadPackage("idrel",false:OnlyNeeded:=true)')
 hd=json.load(open('workspace/agent3_GL3_product_identities.json'));R=hd['relators']
 cp=json.load(open('workspace/agent2_compact_cover_seeds.json'));ar=cp['aut_operator_relators']
 ic=json.load(open('workspace/agent3_HAP_inverse_comparison.json'))
 q={1:tuple(ic['T']),2:(4,)+tuple(ic['P']),3:(4,)+tuple(ic['I']),4:tuple(ic['C'])}
 def subst(w):return red(y for x in w for y in (q[x] if x>0 else inv(q[-x])))
 queries=[subst(w) for w in ar]
 F=libgap.FreeGroup(4);gen=list(libgap.GeneratorsOfGroup(F))
 def word(w):
  g=libgap.One(F)
  for x in w:g=g*gen[abs(x)-1]**(1 if x>0 else -1)
  return g
 G=F/libgap([word(w) for w in R]);libgap.set_global('AG2HG',G)
 libgap.eval('(function() ArrangeMonoidGenerators(AG2HG); AG2HM:=MonoidPresentationFpGroup(AG2HG); AG2HRules:=InitialLoggedRulesOfPresentation(AG2HM); return true; end)()')
 arr=[int(x) for x in libgap.ArrangeMonoidGenerators(G)];mg=list(libgap.eval('GeneratorsOfGroup(FreeGroupOfPresentation(AG2HM))'))
 def monword(w):
  g=mg[0]**0
  for x in w:g=g*mg[arr.index(x)]
  return g
 mq=[monword(w) for w in queries];out={}
 mu=libgap.eval('HomomorphismOfPresentation(AG2HM)')
 for k in range(passes+1):
  rules=libgap.eval('AG2HRules')
  for i,w in enumerate(mq):
   if i in out:continue
   result=libgap.LoggedReduceWordKB(w,rules)
   if int(libgap.Length(result[1])):continue
   logs=result[0];terms=[];p=()
   for c in logs:
    ri=int(c[0]);u=tuple(int(x) for x in libgap.LetterRepAssocWord(libgap.Image(mu,c[1])))
    r=tuple(R[abs(ri)-1]);r=r if ri>0 else inv(r)
    p=red(p+inv(u)+r+u);terms.append([ri,list(u)])
   if p!=queries[i]:
    print('INVALIDloggedfilldiscarded',i,'lengths',len(p),len(queries[i]),flush=True);continue
   out[i]={'aut_operator_relator':ar[i],'hap_GL_word':queries[i],'terms_u_inverse_r_u':terms}
   print('FREECHECKEDfill',i,'inputlength',len(queries[i]),'terms',len(terms),flush=True)
  Path('workspace/agent2_hap_comparison_fillings.json').write_text(json.dumps({'relators':R,'fillings':out}))
  print('pass',k,'rules',int(libgap.Length(rules)),'filled',len(out),'of',len(queries),flush=True)
  if len(out)==len(queries) or k==passes:break
  libgap.eval('(function() AG2HRules:=LoggedOnePassKB(AG2HM,AG2HRules); AG2HRules:=LoggedRewriteReduce(AG2HM,AG2HRules); return true; end)()')
 return out
if __name__=='__main__':run()
