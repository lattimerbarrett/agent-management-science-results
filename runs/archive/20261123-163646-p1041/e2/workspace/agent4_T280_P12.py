import itertools,json,time,sys,math
from pathlib import Path
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese
base=set(json.loads(Path('workspace/agent4_boundary256_base32.json').read_text()));E=sorted(x|(r<<7) for x in base for r in range(8));ES=set(E);V=veronese(10,5)
B={}
for i,p in enumerate(E):
 a=V[p];co=1<<i
 while a:
  j=a.bit_length()-1
  if j in B:a^=B[j][0];co^=B[j][1]
  else:B[j]=(a,co);break
pivs=sorted(B.items(),reverse=True)
def red(a):
 co=0
 for j,(row,c) in pivs:
  if a>>j&1:a^=row;co^=c
 return a,co

def rank4(vecs):
 bs={}
 for v in vecs:
  while v:
   j=v.bit_length()-1
   if j in bs:v^=bs[j]
   else:bs[j]=v;break
 return len(bs)==4

orbs=json.loads(Path('workspace/agent4_T280_period_point_orbits.json').read_text());results=[];allfound=[];st=time.time()
for orb in orbs:
 vb=orb['vbase'];v=vb or 128;pbit=v.bit_length()-1
 points=[x for x in range(1024) if not(x>>pbit&1) and x not in ES and x^v not in ES]
 sig={p:(red(V[p]^V[p^v])[0]<<10)^p for p in points}
 for p0 in orb['point_reps']:
  p0=min(p0,p0^v);assert p0 in sig
  ps=[p for p in points if p!=p0];ls=[sig[p] for p in ps];pairs={}
  for i in range(len(ps)):
   for j in range(i+1,len(ps)):pairs.setdefault(ls[i]^ls[j],[]).append((i,j))
  get=pairs.get;N=len(ps);target=sig[p0];count=0;hits=0;found=set()
  for i in range(N-2):
   li=target^ls[i]
   for j in range(i+1,N-1):
    lij=li^ls[j]
    for k in range(j+1,N):
     count+=1
     cand=get(lij^ls[k])
     if cand is None:continue
     for d,e in cand:
      if d in (i,j,k) or e in(i,j,k):continue
      Q=tuple(sorted([p0,ps[i],ps[j],ps[k],ps[d],ps[e]]))
      if not rank4([p^p0 for p in Q]):continue
      hits+=1;found.add(Q)
  assert count==math.comb(N,3)
  rr={'vbase':vb,'p0':p0,'N':N,'triples':count,'hits':hits,'unique_P12':len(found)};results.append(rr)
  print(rr,'secs',time.time()-st,flush=True)
  for Q in found:
   P=sorted([p for a in Q for p in [a,a^v]]);a=0
   for p in P:a^=V[p]
   rem,co=red(a);assert rem==0
   H=P+[p for i,p in enumerate(E) if co>>i&1]
   SS=set(H)^set(E)
   F=sorted(set(H)|{p|1024 for p in SS});assert len(F)==280
   allfound.append({'vbase':vb,'p0':p0,'P':P,'support':F})
Path('workspace/agent4_T280_P12_results.json').write_text(json.dumps({'results':results,'found':allfound,'seconds':time.time()-st}))
print('COMPLETE totalfound',len(allfound),'seconds',time.time()-st,flush=True)
