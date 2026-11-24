"""Compact exact invariant-L-presentation seeds for central IA3 cover.
Signed-permutation chunks are shortened modulo explicitly imposed B3 relations.
"""
import json
from pathlib import Path
from degree2_certificate import compose,red,inv

def generate(limit=2000000):
 d=json.load(open('workspace/agent2_nielsen_actions_n3.json'))
 iw=json.load(open('workspace/agent2_nielsen_inverse_words_n3.json'))
 wd=json.load(open('workspace/agent2_magnus_aut_words_n3.json'))
 ar=json.load(open('workspace/agent4_AutF3_four_generator_presentation.json'))
 order=['T','P','I','C'];mp={};aa={};ident=((1,),(2,),(3,))
 for i,s in enumerate(order,1):
  mp[i]=[tuple(w) for w in d['actions'][s]['words']];mp[-i]=[tuple(w) for w in iw[s]]
  aa[i]=tuple(map(tuple,d['actions'][s]['auto']));aa[-i]=tuple(map(tuple,d['actions'][s]['inverse']))
 def eva(w):
  f=ident
  for a in w:f=compose(f,aa[a])
  return f
 trans={ident:()};front=[ident]
 while front:
  new=[]
  for f in front:
   for a in (2,3,4,-4):
    h=compose(f,aa[a])
    if h not in trans:trans[h]=trans[f]+(a,);new.append(h)
  front=new
 assert len(trans)==48
 def normalize(w):
  out=();chunk=()
  for a in tuple(w):
   if abs(a)==1:
    out=red(out+trans[eva(chunk)]+(a,));chunk=()
   else:chunk+=(a,)
  return red(out+trans[eva(chunk)])
 def apply(a,w):
  out=red(y for x in w for y in (mp[a][x-1] if x>0 else inv(mp[a][-x-1])))
  if len(out)>limit:raise OverflowError(('wordcap',a,len(out)))
  return out
 def image(aw,h):
  w=(h+1,)
  for a in reversed(aw):w=apply(a,w)
  return w
 b3=[(2,2),(4,4,4),(2,4,2,4),(3,3),(3,2)*4]
 z=(4,2,-4);b3.append((3,)+z+(-3,)+inv(z))
 rel=[];lengths=[];operatorloops=list(b3);normalizedW=[]
 def addloop(aw):
  assert eva(aw)==ident
  for h in range(9):rel.append(red(image(aw,h)+(-h-1,)))
 for j,w in enumerate(b3):
  addloop(w);print('B3block',j,'maxlength',max(map(len,rel)),flush=True)
 for j,w in enumerate(ar['presentation_loops_left_composition']):
  nw=normalize(w);assert eva(nw)==ident
  if nw:operatorloops.append(nw)
  addloop(nw)
  print('Autblock',j,'actionlength',len(nw),'maxword',max(map(len,rel)),flush=True)
 for g,w in enumerate(wd['words']):
  aw=normalize(w);assert eva(aw)==tuple(map(tuple,d['generators'][g]))
  normalizedW.append(aw)
  for h in range(9):rel.append(red(image(aw,h)+(g+1,-h-1,-g-1)))
  print('Peifferblock',g,'maxword',max(map(len,rel)),flush=True)
 out={'n':3,'endomorphisms':[mp[i] for i in (1,2,3,4,-1,-2,-3,-4)],'iterated_relators':rel,'fixed_relators':[],'aut_operator_relators':operatorloops,'magnus_aut_words_normalized':normalizedW,'proof':'B3 short presentation plus normalized complete Aut relators plus Peiffer; exact inverse endomorphisms included'}
 Path('workspace/agent2_compact_cover_seeds.json').write_text(json.dumps(out))
 print('Saved',len(rel),'relators totalletters',sum(map(len,rel)),flush=True)
 return out
if __name__=='__main__':generate()
