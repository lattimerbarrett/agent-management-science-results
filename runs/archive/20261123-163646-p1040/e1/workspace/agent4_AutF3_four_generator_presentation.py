import json,sys
from collections import deque
from pathlib import Path
sys.path.insert(0,'workspace')
from agent3_magnus import compose,identity,inverse,reduce_word
D=json.load(open('workspace/agent3_AutF3_presentation.json'))
G=[tuple(map(tuple,g)) for g in D['aut_images']]
Gi=[tuple(map(tuple,g)) for g in D['inverse_images']]
A=json.load(open('workspace/agent2_nielsen_actions_n3.json'))
actorder=['T','P','I','C'];acts=[tuple(map(tuple,A['actions'][name]['auto'])) for name in actorder]
def evalword(w,gs,gis):
 out=identity(3)
 for a in w:out=compose(out,(gs if a>0 else gis)[abs(a)-1])
 return out
q=deque([identity(3)]);W={identity(3):()}
while q:
 f=q.popleft()
 for a in [1,-1,2,-2]:
  h=compose(f,(G if a>0 else Gi)[abs(a)-1])
  if h not in W:W[h]=W[f]+(a,);q.append(h)
assert len(W)==48
# order actions1=Tnielsen,2=P,3=I,4=C
S4=reduce_word((3,4,3,-4,4,4,3,-4,-4,4));T4=(3,2);U4=(1,)
images4=[S4,T4,U4]
def expand(w):return reduce_word(a for l in w for a in (images4[l-1] if l>0 else inverse(images4[-l-1])))
actis=[tuple(map(tuple,A['actions'][name]['inverse'])) for name in actorder]
assert all(evalword(w,acts,actis)==g for w,g in zip(images4,G))
loops=[];named={}
for k in [1,2,3]:
 wg=W[acts[k]];we=expand(wg);r=reduce_word((k+1,)+inverse(we));assert evalword(r,acts,actis)==identity(3)
 named[actorder[k]]={'ST_word':wg,'four_action_word':we,'consistency_loop':r};loops.append(r)
# Reverse GAP right-action word before mapping to left-composition convention.
for r in D['relators']:
 rr=expand(tuple(r)[::-1]);assert evalword(rr,acts,actis)==identity(3);loops.append(rr)
out={'action_order':actorder,'Aut_STU_in_four':images4,'signed_permutation_expressions':named,'presentation_loops_left_composition':loops,'proof':'Tietze: R(STU) plus three redundant P/I/C definition loops; S,T generate48signedpermutations by exactBFS.'}
Path('workspace/agent4_AutF3_four_generator_presentation.json').write_text(json.dumps(out))
print('48signedpermutations; P/I/C definitions:',named)
print('14 genuineAutpresentationloops lengths',list(map(len,loops)))
