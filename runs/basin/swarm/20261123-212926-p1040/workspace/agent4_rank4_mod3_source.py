import json,pickle,sys,time,re
from pathlib import Path
from itertools import product
sys.path.insert(0,str(Path(__file__).parent))
from agent2_cubic_source import magnus3
from agent2_source_relations import generators
base=Path(__file__).parent;data=json.loads((base/'agent4_gap_ia4_data.json').read_text());N=24;off=N*N;p=3
names=[(g[0],)+tuple(int(x)-1 for x in re.findall(r'\d+',g)) for g in data['names']]
gi={g:i for i,g in enumerate(names)};perm=[gi[g] for g in generators(4)]

def vector(poly):
 o={}
 for w,c in poly.items():
  if len(w)==2:k=w[0]*N+w[1]
  elif len(w)==3:k=off+(w[0]*N+w[1])*N+w[2]
  else:continue
  if c%p:o[k]=c%p
 return o

def action(ws):
 ps=[magnus3(tuple(w[::-1]),N) for w in ws]
 lin=[{u:c%p for u,c in z.items() if len(u)==1 and c%p} for z in ps]
 quad=[{u:c%p for u,c in z.items() if len(u)==2 and c%p} for z in ps]
 act=[]
 for i,j in product(range(N),repeat=2):
  poly={}
  for P,Q in [(lin[i],lin[j]),(quad[i],lin[j]),(lin[i],quad[j])]:
   for x,c in P.items():
    for y,d in Q.items():poly[x+y]=(poly.get(x+y,0)+c*d)%p
  act.append(vector(poly))
 for i,j,k in product(range(N),repeat=3):
  poly={x+y+z:c*d*e%p for x,c in lin[i].items() for y,d in lin[j].items() for z,e in lin[k].items()}
  act.append(vector(poly))
 return act

def apply(act,v):
 o={}
 for k,c in v.items():
  for j,d in act[k].items():o[j]=(o.get(j,0)+c*d)%p
 return {j:c for j,c in o.items() if c}
B={};queue=[]
def insert(v):
 v={k:int(c)%p for k,c in v.items() if c%p}
 while v:
  k=min(v);c=v[k]
  if k in B:
   for j,d in B[k].items():
    t=(v.get(j,0)-c*d)%p
    if t:v[j]=t
    else:v.pop(j,None)
  else:
   cc=pow(c,-1,p);v={j:cc*d%p for j,d in v.items()};B[k]=v;queue.append(v);return True
 return False

def reduce(v):
 v={k:int(c)%p for k,c in v.items() if c%p}
 for k,row in sorted(B.items()):
  c=v.get(k,0)
  if c:
   for j,d in row.items():
    t=(v.get(j,0)-c*d)%p
    if t:v[j]=t
    else:v.pop(j,None)
 return v
if __name__=='__main__':
 t=time.time()
 Q=pickle.loads((base/'agent2_rank4_quadratic_cubic.pkl').read_bytes())
 for v in Q.values():
  w={}
  for k,c in v.items():
   a,k=divmod(k,N*N);b,c1=divmod(k,N);w[off+(perm[a]*N+perm[b])*N+perm[c1]]=c
  insert(w)
 print('Q3rank',len(B),time.time()-t,flush=True);assert len(B)==4380
 queue.clear()
 for r in data['rels']:insert(vector(magnus3(tuple(r[::-1]),N)))
 print('seeds rank',len(B),'newqueue',len(queue),time.time()-t,flush=True)
 acts=[action(ws) for ws in data['endomorphisms']]
 print('actsready',time.time()-t,flush=True)
 idx=0
 while idx<len(queue):
  v=queue[idx];idx+=1
  for act in acts:insert(apply(act,v))
  if idx%25==0:print('queue',idx,len(queue),'rank',len(B),time.time()-t,flush=True)
 print('FINAL rank',len(B),'purecubic',sum(k>=off for k in B),time.time()-t,flush=True)
 a=gi['M',2,0,1];b=gi['M',0,1,2];c=gi['C',0,1];W={}
 for (i,j,k),coef in [((a,b,c),1),((b,a,c),-1),((c,a,b),-1),((c,b,a),1)]:W[off+(i*N+j)*N+k]=coef
 res=reduce(W);print('oldW residue',len(res),flush=True)
 (base/'agent4_rank4_mod3_source_basis.pkl').write_bytes(pickle.dumps(B))
 (base/'agent4_rank4_mod3_source_result.json').write_text(json.dumps({'prime':p,'mixed_rank':len(B),'cubic_rank':sum(k>=off for k in B),'oldW_residue':res,'seconds':time.time()-t}))
