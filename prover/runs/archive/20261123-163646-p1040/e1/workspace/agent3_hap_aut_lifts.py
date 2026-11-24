import json,sys
import numpy as np
from collections import deque
from pathlib import Path
sys.path.insert(0,'workspace')
from agent3_magnus import compose,identity,inverse,auto_commutator

def abel(f):
 A=np.zeros((3,3),dtype=np.int64)
 for j,w in enumerate(f):
  for a in w:A[abs(a)-1,j]+=1 if a>0 else -1
 return A

def invmat(A):
 a,b,c,d,e,f,g,h,i=map(int,A.reshape(-1))
 C=np.array([[e*i-f*h,c*h-b*i,b*f-c*e],[f*g-d*i,a*i-c*g,c*d-a*f],[d*h-e*g,b*g-a*h,a*e-b*d]],dtype=np.int64)
 det=a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)
 assert abs(det)==1
 return C*det

def key(A):return tuple(map(int,A.reshape(-1)))
def build():
 data=json.loads(Path('workspace/agent2_nielsen_actions_n3.json').read_text())
 labels=['T','P','I','C'];aut={};mats={}
 for i,l in enumerate(labels,1):
  for s,typ in [(i,'auto'),(-i,'inverse')]:
   aut[s]=tuple(map(tuple,data['actions'][l][typ]));mats[s]=abel(aut[s])
 ident=np.eye(3,dtype=np.int64);words={key(ident):()};queue=deque([(ident,())])
 pool=[1,-1,2,3,4,-4]
 while queue:
  M,w=queue.popleft()
  if len(w)==5:continue
  for a in pool:
   N=M@mats[a];k=key(N)
   if k not in words:words[k]=w+(a,);queue.append((N,w+(a,)))
 print('matrixball5',len(words),flush=True)
 D=json.loads(Path('workspace/agent1_HAP_SL3Z_presentation_3cells_simple.json').read_text())
 out=[]
 for M in D['generator_matrices']:
  M=np.array(M,dtype=np.int64);best=words.get(key(M))
  if best is None:
   for k,w in words.items():
    N=np.array(k,dtype=np.int64).reshape(3,3);v=words.get(key(M@invmat(N)))
    if v is not None and (best is None or len(v)+len(w)<len(best)):best=v+w
  assert best is not None
  f=identity(3);fi=identity(3)
  for a in best:f=compose(f,aut[a])
  for a in reversed(best):fi=compose(fi,aut[-a])
  assert np.array_equal(abel(f),M) and compose(f,fi)==identity(3)
  out.append({'matrix':M.tolist(),'word':best,'auto':f,'inverse':fi})
  print('lift',best,'wordlengths',list(map(len,f)),flush=True)
 rels=[]
 for r in D['relators']:
  f=identity(3)
  for a in r:f=compose(f,tuple(map(tuple,out[abs(a)-1]['auto' if a>0 else 'inverse'])))
  assert np.array_equal(abel(f),ident)
  rels.append(f);print('IArelatorlift imageslengths',list(map(len,f)),flush=True)
 result={'action_order':labels,'lifts':out,'relators':D['relators'],'relator_auts':rels}
 Path('workspace/agent3_hap_aut_lifts.json').write_text(json.dumps(result))
 return result
if __name__=='__main__':build()
