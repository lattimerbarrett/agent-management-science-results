import sys,itertools,json,pathlib
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese,closure

def kernel(S,vs):
 B={};out=[]
 for i,s in enumerate(S):
  v=vs[s];c=1<<i
  while v:
   k=v.bit_length()-1
   if k not in B:B[k]=(v,c);break
   v^=B[k][0];c^=B[k][1]
  if not v:out.append(c)
 return out
out=[]
for rank in [2,4,6,8]:
 S=[p for p in range(512) if (1^sum(((p>>(2*j))&1)*((p>>(2*j+1))&1) for j in range(rank//2)))&1];K=kernel(S,veronese(9,5));nz=sum((a&b).bit_count()%2 for a in K for b in K);print(rank,len(S),len(K),'selforth',not nz);out.append({'rank':rank,'weight':len(S),'K':len(K),'selforth':not nz})
json.dump(out,open('workspace/agent1_negative_quadrics_kernels.json','w'));pathlib.Path('workspace/agent1_negative_quadrics_kernels.py').write_text(pathlib.Path(__file__).read_text())
