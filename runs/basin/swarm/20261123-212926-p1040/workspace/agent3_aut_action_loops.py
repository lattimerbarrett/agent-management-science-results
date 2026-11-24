from pathlib import Path
import json,time
x=json.loads(Path('workspace/agent4_gap_ia3_data.json').read_text())

def inv(w):return tuple(-i for i in w[::-1])
def reduce(w):
 out=[]
 for i in w:
  if out and out[-1]==-i:out.pop()
  else:out.append(i)
 return tuple(out)
def substitute(w,aut):
 return reduce(j for i in w for j in (aut[i-1] if i>0 else inv(aut[-i-1])))
def compose(a,b):return tuple(substitute(w,a) for w in b)
identity=((1,),(2,),(3,))
from itertools import permutations
ags=[((-1,),(2,),(3,))]
for p in permutations((1,2,3)):
 if p!=(1,2,3):ags.append(tuple((i,) for i in p))
ags += [((2,1),(2,),(3,)),((-2,1),(2,),(3,)),((1,-2),(2,),(3,)),((1,2),(2,),(3,))]
assert len(ags)==len(x['endomorphisms'])
seen={identity:()};front=[identity];loops=[];loopseen=set()
for radius in range(1,5):
 nxt=[]
 for old in front:
  w=seen[old]
  for j,g in enumerate(ags):
   a=compose(g,old);v=w+(j,)
   if a not in seen:
    seen[a]=v;nxt.append(a)
   elif seen[a]!=v:
    pair=(v,seen[a])
    if pair not in loopseen:loopseen.add(pair);loops.append(pair)
 front=nxt
 print('radius',radius,'seen',len(seen),'new',len(front),'loops',len(loops),flush=True)
Path('workspace/agent3_aut_action_loops.json').write_text(json.dumps({'endo_names':[e['name'] for e in x['endomorphisms']], 'loops':loops,'convention':'word actions append means compose new g on left: Sg o old. Both sides have equal actual AutF3 images.'}))
