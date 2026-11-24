import sys,json,itertools,pathlib,numpy as np
sys.path.insert(0,'workspace')
from agent1_checked_grid import witnesses,truth_table
from agent3_lift_closure import veronese,closure

def compress(S):
 o=S[0];B={};n=0
 for s in S:
  v=s^o;c=0
  while v:
   k=v.bit_length()-1
   if k not in B:B[k]=(v,c^(1<<n));n+=1;break
   v^=B[k][0];c^=B[k][1]
 out=[]
 for s in S:
  v=s^o;c=0
  while v:
   k=v.bit_length()-1;v^=B[k][0];c^=B[k][1]
  out.append(c)
 return out,n

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
W=witnesses();out=[]
for w in [272,288,296,304,308,312,316,320,324,328,332]:
 a,b,t=W[w];S=np.where(truth_table(a,b,t))[0].tolist();S,m=compress(S);K=kernel(S,veronese(m,5));G=[[((x&y).bit_count()%2) for x in K] for y in K];nz=sum(map(sum,G));print(w,m,len(K),'selforth',not nz)
 out.append({'w':w,'m':m,'K':len(K),'selforth':not nz,'support':S})
json.dump(out,open('workspace/agent1_canonical_fringe_kernels.json','w'));pathlib.Path('workspace/agent1_canonical_fringe_kernels.py').write_text(pathlib.Path(__file__).read_text())
