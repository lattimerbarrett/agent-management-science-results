import json,time
from sage.all import Matrix,ZZ
from agent1_degree3 import *
from agent1_degree3_closure import initial_vector,row_basis

def reduce(H,v):
 v=list(v)
 for row in H:
  p=next((j for j,x in enumerate(row) if x),None)
  if p is None:continue
  if v[p]:
   q=v[p]//row[p]
   if q:
    for j,x in enumerate(row):
     if x:v[j]-=q*x
 return v

def run(start=0,end=None):
 hp='workspace/agent1_class3_HNF215.json'
 H=json.load(open(hp));rels=json.load(open('workspace/agent1_ia3_collision_relators.json'))
 if end is None:end=len(rels)
 updates=0;t=time.time()
 for idx in range(start,min(end,len(rels))):
  w=rels[idx]
  v=initial_vector(expand(w));r=reduce(H,v)
  if any(r):
   H=[[int(x) for x in z] for z in row_basis(Matrix(ZZ,H+[r])).rows()]
   updates+=1;print('lattice enlarged at relation',idx,'update',updates,flush=True)
  if idx%5000==0:print('processed',idx,'seconds',round(time.time()-t,2),flush=True)
 json.dump(H,open(hp,'w'))
 print('done',start,end,'updates',updates,'seconds',round(time.time()-t,2),flush=True)
 return H
if __name__=='__main__':run()
