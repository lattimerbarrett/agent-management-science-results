import itertools,json,random,time,numpy as np
from pathlib import Path
random.seed(309)
n=14;N=1<<n;ALL=(1<<N)-1
X=[sum(1<<x for x in range(N) if x>>i&1) for i in range(n)];LOW=[ALL^x for x in X];D7=sum(1<<x for x in range(N) if x.bit_count()<=7)
def mob(a):
 for i in range(n):a^=(a&LOW[i])<<(1<<i)
 return a
def times(a,i):return (a&X[i])^((a&LOW[i])<<(1<<i))
seeds=json.load(open('workspace/agent4_flat_seeds.json'));pool=[]
for w in sorted(map(int,seeds)):
 if str(w) not in seeds:continue
 f=0
 for mask in seeds[str(w)]:
  for x in range(N):
   if x&~mask==0:f^=1<<x
 assert f.bit_count()==w
 pool.append((mob(f),w))
start=time.time();hit=None;genuine=0;near=0;records=[]
for orbit in range(3000):
 a,w=random.choice(pool)
 for _ in range(50):
  i,j=random.sample(range(n),2);a^=times((a&X[i])>>(1<<i),j)
 for i in range(n):
  der=(a&X[i])>>(1<<i)
  others=[j for j in range(n) if j!=i]
  for j,k,l in itertools.combinations(others,3):
   diff=times(times(times(der,j),k),l)
   if not diff&~D7:continue
   genuine+=1;cand=a^(diff&D7);f=mob(cand);wt=f.bit_count()
   if wt in (322,326,330,334):
    assert cand==mob(f) and not cand&~D7
    hit={'weight':wt,'truth_hex':hex(f),'anf_hex':hex(cand),'baseweight':w,'shear':[i,j,k,l]};print('HIT',hit,flush=True);break
   if 312<=wt<=438:
    near+=1
    if len(pool)<200 or random.randrange(200)==0:
     if len(pool)>=200:pool.pop(random.randrange(len(pool)))
     pool.append((cand,wt));records.append({'weight':wt,'truth_hex':hex(f),'anf_hex':hex(cand)})
  if hit:break
 if hit:break
 if orbit%200==0:print('progress',orbit,'genuine',genuine,'near',near,'pool',len(pool),'seconds',time.time()-start,flush=True)
 if time.time()-start>110:break
print('DONE','orbit',orbit,'genuine',genuine,'near',near,'pool',len(pool),'hit',bool(hit),'seconds',time.time()-start,flush=True)
json.dump(hit,open('workspace/agent2_cubicshear_diverse_hit.json','w'));json.dump(records,open('workspace/agent2_cubicshear_diverse_states.json','w'))

