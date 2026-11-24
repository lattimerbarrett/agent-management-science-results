import sys,json,itertools,time,numpy as np
from pathlib import Path
sys.path.insert(0,'workspace')
from agent1_checked_grid import witnesses,truth_table
from agent3_lift_closure import veronese
s=Path('workspace/agent1_T288_quadgraph_ALLh.py').read_text();exec(s[:s.index('D=json.load')])
a,b,t=witnesses(c=7)[336];SS=np.flatnonzero(truth_table(a,b,t,c=7)).tolist();B={};insert(B,(1<<336)-1);coords=[]
for j in range(14):
 v=sum(((p>>j)&1)<<i for i,p in enumerate(SS))
 if insert(B,v):coords.append(j)
assert len(coords)==11
S=sorted(sum(((p>>j)&1)<<i for i,j in enumerate(coords)) for p in SS);assert len(set(S))==336
K=kernel(S,veronese(11,5));assert len(K)==18;B={}
for j in range(-1,11):insert(B,sum(1<<i for i,p in enumerate(S) if j==-1 or p>>j&1))
E=[]
for u in K:
 r=insert(B,u)
 if r:E.append(r)
assert len(E)==6

def degree(f):
 a=f.copy();m=a.size.bit_length()-1
 for j in range(m):a=a.reshape(-1,2,1<<j);a[:,1,:]^=a[:,0,:];a=a.reshape(-1)
 return max((int(x).bit_count() for x in np.flatnonzero(a)),default=-1)
def rank(S):
 B={}
 for p in S:insert(B,p^S[0])
 return len(B)
rows,cols=np.triu_indices(336,1);valid=0;ones=0;found=[];hist={};st=time.time()
for normal in range(1,64):
 p=(normal&-normal).bit_length()-1;vs=[(1<<j)|(((normal>>j)&1)<<p) for j in range(6) if j!=p];labs=[]
 for z in vs:
  h=0
  for j,e in enumerate(E):
   if z>>j&1:h^=e
  labs.append(h)
 T=np.array([p|sum(((h>>i)&1)<<(11+j) for j,h in enumerate(labs)) for i,p in enumerate(S)],dtype=np.int32)
 f=np.zeros(65536,dtype=np.uint8);f[T]=1;deg=degree(f);hist[deg]=hist.get(deg,0)+1
 if deg>9:continue
 valid+=1;assert rank(T.tolist())==16
 dif=T[rows]^T[cols];ct=np.bincount(dif,minlength=65536);oo=np.flatnonzero(ct==1);ones+=len(oo)
 print('VALID336',normal,'degree',deg,'unique-directions',len(oo),flush=True)
 if len(oo):
  for v in oo[:10]:
   v=int(v);bit=v.bit_length()-1;F=set()
   for xx in T:
    x=min(int(xx),int(xx)^v);x=(x&((1<<bit)-1))|((x>>(bit+1))<<bit)
    if x in F:F.remove(x)
    else:F.add(x)
   F=sorted(F);assert len(F)==334;ff=np.zeros(32768,dtype=np.uint8);ff[F]=1;dd=degree(ff);assert dd<=8
   ia,ib=np.triu_indices(334,1);aa=np.array(F,dtype=np.int32);cts=np.bincount(aa[ia]^aa[ib],minlength=32768);cover=bool(np.all(cts[1:]>0));odd=bool(np.all(cts[1:]%2==1))
   rr={'normal':normal,'direction':v,'support':F,'degree':dd,'affrank':rank(F),'full_difference_cover':cover,'all_k_odd':odd};found.append(rr);print('FOUND334',rr['affrank'],cover,odd,flush=True)
R={'source':[a,b,t],'sourcecoords':coords,'valid336':valid,'unique_direction_total':ones,'degree_hist':hist,'found334':found,'seconds':time.time()-st};Path('workspace/agent4_336_to334_firstsource.json').write_text(json.dumps(R));print('FINISHED', {k:v for k,v in R.items() if k!='found334'},'found',len(found))
