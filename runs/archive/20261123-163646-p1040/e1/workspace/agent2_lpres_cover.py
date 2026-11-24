"""Exact integral nilpotent quotients of the certified central IA3 cover.
This is NOT a presentation of IA3; central source artifacts may remain.
"""
import json,time,sys
from pathlib import Path
from collections import Counter
from sage.all import *
from sage.libs.gap.libgap import libgap

def build():
 assert bool(libgap.eval('LoadPackage("lpres",false:OnlyNeeded:=true)'))
 d=json.load(open('workspace/agent2_compact_cover_seeds.json'))
 F=libgap.FreeGroup(9);gen=list(libgap.GeneratorsOfGroup(F))
 def word(w):
  q=libgap.One(F)
  for x in w:q=q*gen[abs(x)-1]**(1 if x>0 else -1)
  return q
 endos=[libgap.GroupHomomorphismByImages(F,F,gen,[word(w) for w in a]) for a in d['endomorphisms']]
 rels=[word(w) for w in d['iterated_relators'] if w]
 H=libgap.LPresentedGroup(F,[],endos,rels)
 return H

def run(c=3):
 H=build();t=time.time();Q=libgap.NilpotentQuotient(H,c)
 print('class',c,'integralNQtime',time.time()-t,flush=True)
 lcs=list(libgap.LowerCentralSeries(Q));invariants=[]
 for i in range(len(lcs)-1):
  inv=[int(x) for x in libgap.AbelianInvariants(libgap.FactorGroup(lcs[i],lcs[i+1]))]
  invariants.append(inv);print('LCSfactor',i+1,'counts',dict(Counter(inv)),flush=True)
 Path('workspace/agent2_cover_class%d_invariants.json'%c).write_text(json.dumps(invariants))
 return H,Q,invariants
if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 3)
