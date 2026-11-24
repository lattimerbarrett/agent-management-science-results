import itertools,time,json,numpy as np
out={};count=0;start=time.time()
def spanrank(S):
 piv={}
 for v in S:
  for i in sorted(piv,reverse=True):
   if v>>i&1:v^=piv[i]
  if v:piv[v.bit_length()-1]=v
 return len(piv)
def flat(bs):
 S={0}
 for v in bs:S|={v^q for q in S}
 return S
for t,a,b,c,d in itertools.product(range(8),repeat=5):
 if 2*t+a+b+c+d!=7:continue
 x=7-t-a-b-d;y=7-t-a-c-d;z=7-t-b-c-d
 if min(x,y,z)<0:continue
 dims=[t,a,b,c,x,y,z];A=[];B=[];C=[];first=[];pos=0
 for k,Ls in zip(dims,[[A,B,C],[A,B],[A,C],[B,C],[A],[B],[C]]):
  first.append(1<<pos if k else 0)
  for _ in range(k):
   for L in Ls:L.append(1<<pos)
   pos+=1
 efirst=1<<pos if d else 0;ffirst=1<<(pos+1) if d else 0;fsecond=1<<(pos+3) if d>=2 else 0
 for _ in range(d):A.append(1<<pos);B.append(1<<(pos+1));C.append(3<<pos);pos+=2
 assert pos==14 and len(A)==len(B)==len(C)==7
 FA,FB,FC=flat(A),flat(B),flat(C)
 ells=[]
 if t:ells.append(first[0])
 diag=[0]+([efirst,ffirst,efirst|ffirst] if d else [])+([efirst|fsecond] if d>=2 else [])
 for ea,eb,ec in itertools.product([0,1],repeat=3):
  if (ea and not a) or(eb and not b)or(ec and not c):continue
  w=192-ea*(1<<(t+a))-eb*(1<<(t+b))-ec*(1<<(t+c))
  if not(0<w<=156):continue
  for ex,ey,ez in itertools.product([0,1],repeat=3):
   if(ex and not x)or(ey and not y)or(ez and not z):continue
   base=sum(v*f for v,f in zip([ea,eb,ec,ex,ey,ez],first[1:]))
   ells.extend(base|dd for dd in diag)
 for ell in set(ells):
  SA={v for v in FA if(v&ell).bit_count()%2};SB={v for v in FB if(v&ell).bit_count()%2};SC={v for v in FC if(v&ell).bit_count()%2}
  if not(len(SA)==len(SB)==len(SC)==64):continue
  S=SA^SB^SC;w=len(S)
  if not(0<w<=156)or spanrank(S)!=14:continue
  arr=np.zeros(16384,dtype=np.int32);arr[list(S)]=1
  for j in range(14):
   h=1<<j;v=arr.reshape(-1,2*h);left=v[:,:h].copy();right=v[:,h:].copy();v[:,:h]=left+right;v[:,h:]=left-right
  assert np.any(arr==w-64),(w,(t,a,b,c,d,x,y,z),ell)
  count+=1
  if w not in out:out[w]=[t,a,b,c,d,x,y,z,ell,A,B,C,sorted(S)];print('FULLSPAN',w,(t,a,b,c,d,x,y,z),ell,flush=True)
print('DONE',count,sorted(out),time.time()-start)
json.dump(out,open('workspace/agent3_fullspan_threeflat_c6.json','w'))
from pathlib import Path
Path('workspace/agent3_fullspan_threeflat_checker.py').write_text(Path(__file__).read_text())