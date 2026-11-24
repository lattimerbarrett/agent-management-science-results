"""Exact finite invariant L-presentation seeds for a central IA3 cover.
No claim that this cover equals IA3. Finite words are generated exactly.
"""
import json
from pathlib import Path
from degree2_certificate import red,inv

def generate(limit=2000000):
 d=json.load(open('workspace/agent2_nielsen_actions_n3.json'))
 wd=json.load(open('workspace/agent2_magnus_aut_words_n3.json'))
 ar=json.load(open('workspace/agent3_AutF3_presentation.json'))
 order=['T','P','I','C'];maps=[[tuple(w) for w in d['actions'][s]['words']] for s in order]
 imaps=[[inv(w) for w in a] for a in maps]
 def apply(a,w):
  out=red(y for x in w for y in (maps[a][x-1] if x>0 else imaps[a][-x-1]))
  if len(out)>limit:raise OverflowError(('wordcap',a,len(out)))
  return out
 def image(aw,h):
  w=(h+1,)
  for a in reversed(aw):w=apply(a-1,w)
  return w
 inverse={1:(2,3,2,1,2,3,2),2:(2,),3:(3,),4:(4,4)}
 peiffer=[]
 for g,ww in enumerate(wd['words']):
  aw=tuple(y for x in ww for y in ((x,) if x>0 else inverse[-x]))
  for h in range(9):peiffer.append(red(image(aw,h)+(g+1,-h-1,-g-1)))
  print('Peifferblock',g,'maxlength',max(map(len,peiffer)),flush=True)
 # Aut relation loops, GAP right action is reversed.
 I0=(3,);I1=(4,3,4,4);I2=(4,4,3,4)
 S=I0+I1+I2+(4,);T=(3,2);U=(1,)
 apos={1:S,2:T,3:U};ainv={1:S*5,2:T*3,3:inverse[1]}
 aut=[]
 for j,raw in enumerate(ar['relators']):
  aw=tuple(y for x in reversed(raw) for y in (apos[x] if x>0 else ainv[-x]))
  for h in range(9):aut.append(red(image(aw,h)+(-h-1,)))
  print('Autblock',j,'maxlength',max(map(len,aut)),flush=True)
 for aw in [(2,2),(3,3),(4,4,4),(1,2,3,2,1,2,3,2)]:
  for h in range(9):aut.append(red(image(aw,h)+(-h-1,)))
 out={'n':3,'endomorphisms':maps,'peiffer':peiffer,'aut_relations':aut}
 Path('workspace/agent2_crossed_cover_seeds.json').write_text(json.dumps(out))
 print('Savedfullcoverseeds',len(peiffer)+len(aut),'totalletters',sum(map(len,peiffer+aut)),flush=True)
 return out
if __name__=='__main__':generate()
