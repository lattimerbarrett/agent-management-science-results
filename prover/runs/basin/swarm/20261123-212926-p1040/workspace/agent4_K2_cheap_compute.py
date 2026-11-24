from sage.all import libgap as gap
import time,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from agent4_neumann_relators import compose,identity,mul,inv
base=Path(__file__).parent
gap.eval('LoadPackage("lpres" : OnlyNeeded := true);')
t=time.time();F=gap.FreeGroup(3);A=gap.AutomorphismGroup(F);iso=gap.IsomorphismFpGroup(A);P=gap.Range(iso)
gap.set_global('AA4',P)
gap.eval('ff4:=GF(2);')
gap.eval('mm4:=List([[[0,1,0],[0,0,1],[1,0,0]],[[0,1,0],[1,0,0],[0,0,1]],[[1,1,0],[0,1,0],[0,0,1]]],m->m*One(ff4));')
gap.eval('GG4:=Group(mm4);');assert int(gap.eval('Size(GG4);'))==168
gap.eval('hh4:=GroupHomomorphismByImages(AA4,GG4,GeneratorsOfGroup(AA4),mm4);')
gap.eval('KK4:=Kernel(hh4);');gap.eval('ii4:=IsomorphismFpGroup(KK4 : cheap:=true,generatorsLimit:=100000,eliminationsLimit:=0);');Kfp=gap.eval('Range(ii4);')
print('K2 exactfp',len(gap.GeneratorsOfGroup(Kfp)),len(gap.RelatorsOfFpGroup(Kfp)),time.time()-t,flush=True)
D={'rels':[gap.LetterRepAssocWord(w).sage() for w in gap.RelatorsOfFpGroup(Kfp)],'ngens':len(gap.GeneratorsOfGroup(Kfp))}
(base/'agent4_K2_cheap_fp_data.json').write_text(json.dumps(D,default=int))
# Build short known STU words for all ten standard Nielsen generators.
O=(1,1,1,1,-2,1,-2);PP=mul((2,),O);QQ=(1,1,1,1)
Pmap=((2,),(1,),(3,));Qmap=((2,),(3,),(1,))
seen={identity:()};front=[identity]
while front:
 nxt=[]
 for aa in front:
  for bb,ww in [(Pmap,PP),(Qmap,QQ)]:
   cc=compose(bb,aa)
   if cc not in seen:seen[cc]=mul(seen[aa],ww);nxt.append(cc)
 front=nxt
from itertools import permutations
NW=[O]+[seen[tuple((i,) for i in perm)] for perm in permutations((1,2,3)) if perm!=(1,2,3)]+[mul(O,(-3,),O),mul(O,(3,),O),(-3,),(3,)]
# Convert explicit short STU words to fp Aut words, then exact K2 generators.
pg=list(gap.GeneratorsOfGroup(P))
def evalfp(w):
 z=gap.One(P)
 for x in w:z=z*(pg[x-1] if x>0 else pg[-x-1]**-1)
 return z
IAwords=[]
for r in json.loads((base/'agent3_magnus_as_nielsen.json').read_text())['words']:
 w=mul(*(NW[j] for j in r['endo_word']));z=evalfp(w);zz=gap.Image(gap.eval('ii4;'),z)
 ww=gap.LetterRepAssocWord(gap.UnderlyingElement(zz)).sage();IAwords.append(ww)
 print('IA mapped',r['generator_index'],'length',len(ww),time.time()-t,flush=True)
D['IAwords']=IAwords;(base/'agent4_K2_cheap_fp_data.json').write_text(json.dumps(D,default=int))
LP=gap.LPresentedGroup(gap.FreeGroupOfFpGroup(Kfp),gap.RelatorsOfFpGroup(Kfp),[],[])
for c in range(1,4):
 t0=time.time();ep=gap.NqEpimorphismNilpotentQuotient(LP,c);Q=gap.Range(ep)
 print('K2class',c,'seconds',time.time()-t0,'lcsinv',gap.AbelianInvariants(gap.LowerCentralSeries(Q)[c-1]),flush=True)
