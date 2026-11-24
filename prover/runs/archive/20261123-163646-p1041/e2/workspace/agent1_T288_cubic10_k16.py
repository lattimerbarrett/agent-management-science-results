import sys,itertools,json,pathlib,time,collections
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese,closure

def basis(S,vs):
 B={};K=[]
 for i,p in enumerate(S):
  v=vs[p];c=1<<i
  while v:
   k=v.bit_length()-1
   if k not in B:B[k]=(v,c);break
   v^=B[k][0];c^=B[k][1]
  if not v:K.append(c)
 return B,K

def red(v,B):
 c=0;r=0
 while v:
  k=v.bit_length()-1
  if k not in B:r^=1<<k;v^=1<<k;continue
  v^=B[k][0];c^=B[k][1]
 return r,c

def ins(B,v):
 while v:
  k=v.bit_length()-1
  if k in B:v^=B[k]
  else:B[k]=v;return v
 return 0

def span(B):
 P=[0]
 for b in B:P +=[p^b for p in P]
 return P
v9=veronese(9,5);v103=veronese(10,3);v105=veronese(10,5);stats=[];hits=[];start=time.time()
for rr in range(1,5):
 def q(x):return sum(((x>>(2*i))&1)*((x>>(2*i+1))&1) for i in range(rr))%2
 T=[x|(q(x)<<8) for x in range(256)];B,K=basis(T,v9);LB={}
 for a in range(-1,9):ins(LB,sum(1<<j for j,p in enumerate(T) if a==-1 or p>>a&1))
 extra=[]
 for u in K:
  z=ins(LB,u)
  if z:extra.append(z)
 labels=span(extra)
 for j in range(max(0,4-rr),min(4,8-2*rr)+1):
  AB=[1<<(2*i) for i in range(4-j)]+[1<<(2*rr+i) for i in range(j)];A=span(AB);assert len(A)==16
  P=[x|((q(x)^1)<<8) for x in A];z=0
  for p in P:z^=v9[p]
  rem,c=red(z,B);stat={'rank':2*rr,'j':j,'sourceK5':len(K),'nonlinearHdim':len(extra),'solvable':not rem};hist=collections.Counter()
  if not rem:
   H=P+[p for ii,p in enumerate(T) if c>>ii&1]
   F0=set(H)^set(p|512 for p in H)^set(p|512 for p in T)
   for labid,u in enumerate(labels):
    F=set(F0)
    for ii,p in enumerate(T):
     if u>>ii&1:F.symmetric_difference_update([p,p|512])
    F=sorted(F);assert len(F)==288
    b3,K3=basis(F,v103);b5,K5=basis(F,v105);nz=sum((x&y).bit_count()%2 for x in K3 for y in K5);hist[(len(K3),len(K5),bool(nz))]+=1
    if nz:hits.append({'rank':2*rr,'j':j,'label':labid,'support':F,'K3':len(K3),'K5':len(K5),'cross':nz})
   stat['hist']={str(k):v for k,v in hist.items()}
  stats.append(stat);print(stat,flush=True)
json.dump({'stats':stats,'hits':hits},open('workspace/agent1_T288_cubic10_k16.json','w'));pathlib.Path('workspace/agent1_T288_cubic10_k16.py').write_text(pathlib.Path(__file__).read_text());print('DONE',len(hits),time.time()-start)
