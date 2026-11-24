import numpy as np,itertools,time,json
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
start=time.time();A=[16,24,28,32,36,40];C=[8,12]+list(range(14,41,2))
LOW=[];HIGH=[];INTEG=[];rows=[];lb=[];ub=[]
def var(lo=0,hi=41,integer=1):
 i=len(LOW);LOW.append(lo);HIGH.append(hi);INTEG.append(integer);return i
def add(row,lo=-np.inf,hi=np.inf):rows.append(row);lb.append(lo);ub.append(hi)
def linear_add(*pairs):
 out={}
 for dic,fac in pairs:
  for k,v in dic.items():out[k]=out.get(k,0)+fac*v
 return {k:v for k,v in out.items() if v}
m=[var() for _ in range(7)];n=[var() for _ in range(7)];ON=[];NN=[];OW=[];NW=[]
for counts,DS,WS,ins in [(m,ON,OW,[1,2,3]),(n,NN,NW,[4])]:
 for u in range(1,8):
  dd={w:var(0,1) for w in (A if u in ins else C)};DS.append(dd);add({v:1 for v in dd.values()},1,1)
  wrow={counts[x-1]:1 for x in range(1,8) if (u&x).bit_count()%2};WS.append(wrow);r=wrow.copy()
  for w,v in dd.items():r[v]=-w
  add(r,0,0)
for i,j in [(0,1),(1,2),(3,4),(3,5),(3,6)]:add(linear_add((OW[i],1),(OW[j],-1)),hi=0)
for counts,W,D,ins in [(m,OW,ON,[1,2,3]),(n,NW,NN,[4])]:
 out=[v for v in range(1,8) if v not in ins]
 for u,v in itertools.product(ins,out):
  w=u^v;cap={counts[x-1]:1 for x in range(1,8) if (u&x).bit_count()%2 and (v&x).bit_count()%2}
  for a,b in itertools.permutations([8,12,14],2):add({D[v-1][a]:1,D[w-1][b]:1},hi=1)
  for a,b,limit in [(16,8,1),(16,12,3),(24,8,3),(16,14,7)]:
   r=cap.copy();r[D[u-1][a]]=41;r[D[v-1][b]]=41
   for ww,jj in D[w-1].items():
    if (ww-b)%4==2:r[jj]=41
   add(r,hi=limit+123)
expr={}
for x in range(7):
 for w,sel in NN[x].items():
  z=var(0,41,0);expr[z]=w
  add({z:1,sel:-41},hi=0);add({z:1,m[x]:-1},hi=0);add({z:1,m[x]:-1,sel:-41},lo=-41)
base_rows=len(rows)
for target in [322,326,330,334]:
 add({v:1 for v in m},hi=target//8);add({v:1 for v in n},hi=target//8);add(expr.copy(),target,target)
 M=lil_matrix((len(rows),len(LOW)))
 for i,row in enumerate(rows):
  for j,v in row.items():M[i,j]=v
 tt=time.time();res=milp(np.zeros(len(LOW)),integrality=np.array(INTEG),bounds=Bounds(LOW,HIGH),constraints=LinearConstraint(M.tocsr(),lb,ub),options={'time_limit':60,'mip_rel_gap':0})
 print('TARGET',target,'STATUS',res.status,res.message,'SEC',time.time()-tt,flush=True)
 if res.x is not None:
  val=lambda r:int(round(sum(res.x[j]*v for j,v in r.items())))
  R={'old_counts':[int(round(res.x[j])) for j in m],'new_counts':[int(round(res.x[j])) for j in n],'old_weights':list(map(val,OW)),'new_weights':list(map(val,NW))};print(R,flush=True);json.dump(R,open('workspace/agent4_mixed_rank3_MIP_%d.json'%target,'w'))
 del rows[base_rows:];del lb[base_rows:];del ub[base_rows:]
open('workspace/agent4_mixed_rank3_MIP_model.py','w').write(open(__file__).read())
print('DONE',time.time()-start)
