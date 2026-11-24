import itertools,json,pathlib,sys,numpy as np
sys.path.insert(0,'workspace')
from agent1_checked_grid import degree

def rank_kernel(cols):
 B={};K=[]
 for i,v in enumerate(cols):
  c=1<<i
  while v:
   k=v.bit_length()-1
   if k in B:v^=B[k][0];c^=B[k][1]
   else:B[k]=(v,c);break
  if not v:K.append(c)
 return len(B),K
P=[sum(1<<i for i in x) for x in itertools.combinations(range(8),2)];F=[sum(1<<i for i in x) for x in itertools.combinations(range(8),4)];FI={x:i for i,x in enumerate(F)};out=[]
for rr in [4,6,8]:
 Q=[(1<<(2*i))|(1<<(2*i+1)) for i in range(rr//2)];cols=[]
 for p in P:
  v=0
  for q in Q:
   if p&q==0:v^=1<<FI[p|q]
  cols.append(v)
 rank,K=rank_kernel(cols)
 assert len(K)==(5 if rr==4 else 1)
 if rr==4:assert all(all(not(v>>j&1) or not(P[j]&~15) for j in range(len(P))) for v in K)
 else:assert K==[sum(1<<P.index(q) for q in Q)]
 out.append({'quadratic_rank':rr,'wedge_map_rank':rank,'kernel_dim':len(K)})
P4=[sum(1<<i for i in x) for x in itertools.combinations(range(4),2)];r,K=rank_kernel([sum(1<<j for j,q in enumerate(P4) if not p&q) for p in P4]);assert r==6
for k in range(1,8):
 S=[]
 for x in range(256):
  y=sum((((x&1)*((x>>j)&1))<< (j-1)) for j in range(1,k+1));S.append(x|(y<<8))
 a=np.zeros(1<<(8+k),dtype=np.uint8);a[S]=1;deg=degree(a);assert deg<=k+1
 for eps in [0,1]:
  T=[p for p in S if p&1==eps];assert len(T)==128
  B={};o=T[0]
  for p in T:
   p^=o
   while p:
    j=p.bit_length()-1
    if j in B:p^=B[j]
    else:B[j]=p;break
  assert len(B)==7
out.append({'wedge_pairing_Lambda2_F4_rank':r,'star_graphs_k1_to7_are_two7flats':True})
json.dump(out,open('workspace/agent1_boundary256_dichotomy_audit.json','w'));pathlib.Path('workspace/agent1_boundary256_dichotomy_audit.py').write_text(pathlib.Path(__file__).read_text());print(json.dumps(out,indent=2))
