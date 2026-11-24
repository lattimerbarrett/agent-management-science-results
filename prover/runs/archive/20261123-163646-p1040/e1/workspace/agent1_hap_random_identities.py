import json,random,time
from collections import defaultdict
from agent1_hap_spherical_identities import *

def trial(cell,rng):
 ps=[]
 for f,i in D['boundaries']['3'][cell]:
  s=1 if f>0 else -1
  ps.append((translate(baseface(abs(f)-1),E[i-1],s),[((),abs(f)-1,s)]))
 found=[]
 while len(ps)>1:
  pool=defaultdict(list)
  for j,(P,T) in enumerate(ps):
   for k,ee in enumerate(P):pool[ee[3]].append((j,k,ee[4]))
  choices=[]
  for vv in pool.values():
   for a in vv:
    for b in vv:
     if a[0]<b[0] and a[2]==-b[2]:choices.append((a[0],b[0],a[1],b[1]))
  if not choices:break
  ia,ib,a,b=rng.choice(choices);A,ta=ps[ia];B,tb=ps[ib]
  conj=red(labels(A[:a+1])+inv(labels(B[:b])))
  new=cancel(A[:a]+(B[b:]+B[:b])[1:]+A[a+1:])
  terms=[(red(conj+q),f,s) for q,f,s in tb]+ta
  for i in sorted((ia,ib),reverse=True):ps.pop(i)
  if not red(labels(new)):
   assert not termsword(terms)
   found.append(terms)
  else:ps.append((new,terms))
 for P,T in ps:
  if not red(labels(P)):
   assert not termsword(T);found.append(T)
 return found

def main(count=100):
 rng=random.Random(104257);out=[];seen=set();start=time.time()
 for cell in range(7,12):
  got=0
  for j in range(count):
   for terms in trial(cell,rng):
    key=tuple((q,f,s) for q,f,s in terms)
    if key in seen:continue
    seen.add(key);out.append({'cell':cell+1,'terms':terms});got+=1
  print('random cell',cell+1,'identities',got,'time',round(time.time()-start,2),flush=True)
 json.dump(out,open('workspace/agent1_HAP_SL3Z_random_free_identities.json','w'))
 return out
if __name__=='__main__':main(30)
