import sys,itertools,json,random,time
from pathlib import Path
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese
rng=random.Random(334470);Q=[a for a in range(16) if 1^((a&1)*(a>>1&1))^((a>>2&1)*(a>>3&1))];A=[0,1,4,5];S=[a|(r<<4) for a in Q for r in range(32)];idx={p:i for i,p in enumerate(S)};N=len(S);assert N==320

def gb(vecs):
 B={}
 for v in vecs:
  while v:
   j=v.bit_length()-1
   if j in B:v^=B[j]
   else:B[j]=v;break
 return B

def red(v,B):
 for j in sorted(B,reverse=True):
  if v>>j&1:v^=B[j]
 return v

def kernel(T,m):
 V=veronese(m,5);B={};K=[]
 for i,p in enumerate(T):
  v=V[p];c=1<<i
  while v:
   j=v.bit_length()-1
   if j in B:v^=B[j][0];c^=B[j][1]
   else:B[j]=(v,c);break
  if not v:K.append(c)
 return K

def intersect(K,LB):
 B={};out=[]
 for c in K:
  v=red(c,LB)
  while v:
   j=v.bit_length()-1
   if j in B:v^=B[j][0];c^=B[j][1]
   else:B[j]=(v,c);break
  if not v:out.append(c)
 assert all(red(v,LB)==0 for v in out)
 return out

mon2=[sum(1<<j for j in I) for k in range(3) for I in itertools.combinations(range(4),k)];D2=[]
for z in range(1<<11):
 vals=sum((sum((z>>i)&1 for i,M in enumerate(mon2) if a&M==M)&1)<<a for a in range(16))
 if not any(vals>>a&1 for a in range(16) if a not in Q):D2.append(vals)
assert len(D2)==32
L=[]
for j in range(5):
 allowed=[A[1],A[2],A[3]] if j==0 else ([A[2],A[3]] if j==1 else [A[3]])
 forms=list(gb([u for u in D2 if all(not(u>>a&1) for a in A if a not in allowed)]).values())
 for u in forms:L.append(sum(((u>>a&1)&(r>>j&1))<<idx[a|(r<<4)] for a in Q for r in range(32)))
rem=[a for a in Q if a not in A]
for a in rem[1:]:L.append(sum(int(b in (rem[0],a))<<idx[b|(r<<4)] for b in Q for r in range(32)))
LB=gb(L);assert len(LB)==18

def projections(h):return [sum(((h>>idx[a|(1<<j<<4)])&1)<<j for j in range(5)) for a in A]
def rankprofiles(rows):return [len(gb([rr[k] for rr in rows])) for k in range(4)]
st=time.time();stats={};best=0;found=[];paths=0;K0=kernel(S,9);assert len(K0)==34
for path in range(10000):
 paths+=1;T=S[:];labels=[];rows=[];KK=K0
 for depth in range(6):
  LK=intersect(KK,LB);AB=gb([(1<<N)-1]+[sum(((p>>j)&1)<<i for i,p in enumerate(T)) for j in range(9+depth)])
  cur=rankprofiles(rows);candidates=[]
  # Exhaustall ifsubspacedim<=10; else sample256vectors.
  zs=range(1,1<<len(LK)) if len(LK)<=10 else [rng.randrange(1,1<<len(LK)) for _ in range(256)]
  for z in zs:
   h=0
   for j,v in enumerate(LK):
    if z>>j&1:h^=v
   if not red(h,AB):continue
   rr=projections(h);new=rankprofiles(rows+[rr]);score=3*(new[3]-cur[3])+(new[1]-cur[1])+(new[2]-cur[2])
   if score>0:candidates.append((score,h,rr,new))
  if not candidates:break
  mx=max(x[0] for x in candidates);choice=rng.choice([x for x in candidates if x[0]==mx]);_,h,rr,new=choice
  T=[p|(((h>>i)&1)<<(9+depth)) for i,p in enumerate(T)];labels.append(h);rows.append(rr);stats[depth+1,tuple(new),len(LK)]=stats.get((depth+1,tuple(new),len(LK)),0)+1
  if new[3]>best:best=new[3];print('BESTa3rank',best,'depth',depth+1,'profile',new,'Ldim',len(LK),'sec',time.time()-st,flush=True)
  if new==[0,1,2,5]:
   m=10+depth;H={a|(r<<4) for a in A for r in range(32)};F=sorted(set(T)^H);assert len(F)==334
   V=veronese(m,6);assert __import__('functools').reduce(int.__xor__,[V[p] for p in F])==0
   found.append({'m':m,'support':F,'labels':labels,'profile':new});print('FOUND334m',m,flush=True);break
  KK=kernel(T,10+depth)
 if found or time.time()-st>110:break
R={'paths':paths,'seconds':time.time()-st,'best_a3rank':best,'stats':{str(k):v for k,v in stats.items()},'found':found}
Path('workspace/agent4_S320_fibre57.json').write_text(json.dumps(R));print('DONE',paths,'sec',time.time()-st,'best',best,'found',len(found),'stats',R['stats'],flush=True)
