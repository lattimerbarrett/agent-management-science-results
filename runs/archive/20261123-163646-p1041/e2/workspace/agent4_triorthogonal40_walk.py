import json,time,random,collections,itertools
from pathlib import Path
D=json.loads(Path('workspace/agent4_neutral320_stage1.json').read_text());T20=D['T'];S=[x|(r<<9) for x in T20 for r in range(2)];N=40;full=(1<<40)-1;C=[full]+[sum(((x>>j)&1)<<i for i,x in enumerate(S)) for j in range(10)];rng=random.Random(4040320);st=time.time()
def echelon(rows):
 B={}
 for v in rows:
  while v:
   k=v.bit_length()-1
   if k in B:v^=B[k]
   else:B[k]=v;break
 return B
def reduce(B,v):
 while v:
  k=v.bit_length()-1
  if k not in B:return v
  v^=B[k]
 return 0
def orth(rows):
 B=echelon(rows);free=[j for j in range(N) if j not in B];out=[]
 for j in free:
  v=1<<j
  for p in sorted(B):
   if (B[p]&v).bit_count()%2:v^=1<<p
  out.append(v)
 return out
def randomspan(B):
 m=rng.getrandbits(len(B));v=0
 for j,b in enumerate(B):
  if m>>j&1:v^=b
 return v
def extend(C,target):
 BB=echelon(C)
 while len(C)<target:
  V=orth([a&b for i,a in enumerate(C) for b in C[:i+1]])
  if len(V)<=len(C):return None
  for _ in range(20):
   v=randomspan(V)
   if reduce(BB,v):break
  else:return None
  C.append(v);BB=echelon(C)
 return C
def points(C):return [sum(((v>>j)&1)<<i for i,v in enumerate(C[1:])) for j in range(N)]
def periods(S):
 SS=set(S);p=S[0];return [p^q for q in S if all(x^p^q in SS for x in S)]
assert len(echelon(C))==11
assert all((a&b&c).bit_count()%2==0 for a in C for b in C for c in C)
seen=set();hist=collections.Counter();accepted=0;found=[];proposals=0
for k in range(1000000):
 proposals+=1;drop=rng.choice([2,3,3,4]);keep=[full]+rng.sample(C[1:],10-drop);cand=extend(keep,11)
 if cand is None:hist['dead']+=1;continue
 pts=points(cand)
 if len(set(pts))<40:hist['duplicate']+=1;continue
 sig=tuple(sorted(pts))
 C=cand;accepted+=1
 if sig in seen:continue
 seen.add(sig);PV=periods(pts);pd=len(PV).bit_length()-1;hist['pd'+str(pd)]+=1
 if pd==0:
  found.append({'support':list(sig),'C':C});print('APERIODIC40',accepted,'proposals',proposals,'seconds',time.time()-st,flush=True)
  if len(found)>=30:break
 if time.time()-st>110:break
print('FINISHED',accepted,proposals,len(seen),hist,'aperiodic',len(found),time.time()-st)
R={'accepted':accepted,'proposals':proposals,'distinct':len(seen),'hist':dict(hist),'aperiodic':found,'seconds':time.time()-st}
Path('workspace/agent4_triorthogonal40_walk.json').write_text(json.dumps(R));Path('workspace/agent4_triorthogonal40_walk.py').write_text(Path('scratchpad.py').read_text().split('