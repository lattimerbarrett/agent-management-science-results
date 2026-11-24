import json
from sage.all import Matrix,ZZ
from agent1_degree3 import *
from agent1_degree3_closure import row_basis

def lw(w):
 if len(w)==1:return (w[0]+1,)
 j=next(j for j in range(1,len(w)) if lyndon(w[j:]))
 a,b=lw(w[:j]),lw(w[j:]);return red(a+b+inv(a)+inv(b))

def main():
 H=Matrix(ZZ,json.load(open('workspace/agent1_class3_HNF215.json')))
 K=H[:,:36].transpose().right_kernel().basis_matrix()
 C=K*H[:,36:];assert all(x%2==0 for x in C.list())
 C=row_basis(C.apply_map(lambda x:x//2))
 S,U,V=C.smith_form();Vi=V.inverse()
 reps=[]
 for i in range(min(S.dimensions())):
  if abs(S[i,i])>1:reps.append((int(abs(S[i,i])),[int(x) for x in Vi[i]]))
 print('torsion reps',len(reps),'supports',[sum(x!=0 for x in v) for d,v in reps],flush=True)
 json.dump(reps,open('workspace/agent1_class3_torsion_reps.json','w'))
 IG=[tuple(map(tuple,f)) for f in json.load(open('workspace/agent2_nielsen_actions_n3.json'))['inverses']]
 ident=tuple((j+1,) for j in range(N))
 for idx,(d,v) in sorted(enumerate(reps),key=lambda z:sum(x!=0 for x in z[1][1])):
  w=()
  for x,u in zip(v,L3):
   if x:w+=((lw(u) if x>0 else inv(lw(u)))*abs(x))
  w=red(w);f=ident
  aborted=False
  for t in w:
   if max(map(len,f))>100000:aborted=True;break
   f=compose(f,G[t-1] if t>0 else IG[-t-1])
  print(idx,'order',d,'abstract length',len(w),'image lengths',list(map(len,f)),'IDENTITY',f==ident,'ABORTED',aborted,flush=True)
 return reps
if __name__=='__main__':main()
