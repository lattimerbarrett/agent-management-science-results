import time,itertools,random,pickle,collections
start=time.time();random.seed(410071);n=14;N=1<<n
X=[sum(1<<j for j in range(N) if j>>i&1) for i in range(n)]
LOW=sum(1<<j for j in range(N) if j.bit_count()<=7)
ALL=(1<<N)-1

def mob(f):
 for i in range(n):f^=(f&(ALL^X[i]))<<(1<<i)
 return f

def mul(f,i):return (f&X[i])^((f&(ALL^X[i]))<<(1<<i))
def span(bs):
 p=[0]
 for b in bs:p +=[x^b for x in p]
 return p
fs=[span([1<<j for j in range(7)]),span([1<<j for j in [0,1,2,3,4,7,8]]),span([1<<5,(1<<6)^(1<<8)]+[1<<j for j in range(9,14)])]
f0=0
for p in fs:
 for x in p:f0^=1<<x
assert f0.bit_count()==318
a0=mob(f0);assert a0&~LOW==0
found={};small={};tested=0;genuine=0;wtstats=collections.Counter()
import json
jdata=json.load(open('workspace/agent4_flat_seeds.json'))
jdata.update({'450':[127,16256,1927,1976], '454':[5574,6377,5326,5677,6761,11057,5678], '458':[7438,14634,6415,9944,6947,9436,13609,7465], '462':[5574,6377,5326,5692,6761,11057,5678]})
pool=[]
for w,ms in jdata.items():
 f=0
 for m in ms:
  for x in span([1<<j for j in range(n) if m>>j&1]):f^=1<<x
 assert f.bit_count()==int(w)
 aa=mob(f);assert aa&~LOW==0;pool.append((int(w),aa))
seen=set(a for w,a in pool)
open('workspace/agent4_direct_shear_search.py','w').write(open(__file__).read())
nonlinear_preserved=0
for orbit in range(2000):
 bw,a=random.choice(pool)
 for _ in range(random.randrange(12)):
  i,j=random.sample(range(n),2);di=(a&X[i])>>(1<<i)
  a^=di if random.random()<.15 else mul(di,j)
 for i in range(n):
  di=(a&X[i])>>(1<<i)
  ab={}
  for q in [di]+[mul(di,l) for l in range(n) if l!=i]:
   while q and q.bit_length()-1 in ab:q^=ab[q.bit_length()-1]
   if q:ab[q.bit_length()-1]=q
  for j,k in itertools.combinations([u for u in range(n) if u!=i],2):
   v=mul(mul(di,j),k);b=a^v
   if b&~LOW==0:
    q=v
    while q and q.bit_length()-1 in ab:q^=ab[q.bit_length()-1]
    if q and b not in seen and random.random()<.01:
     nonlinear_preserved+=1;seen.add(b);pool.append((bw,b))
     if len(pool)>10000:
      ix=random.randrange(63,len(pool)-1);pool[ix]=pool[-1];pool.pop()
    continue
   genuine+=1;b&=LOW;f=mob(b);w=f.bit_count();tested+=1
   if w<=400:
    wtstats[w]+=1;small.setdefault(w,b)
    if w>=300 and b not in seen and random.random()<(.2 if w<=350 else .01):
     seen.add(b);pool.append((w,b))
     if len(pool)>10000:
      ix=random.randrange(14,len(pool)-1);pool[ix]=pool[-1];pool.pop()
   if w in [322,326,330,334] and w not in found:
    found[w]=(hex(b),hex(f));pickle.dump(found,open('workspace/agent4_direct_shear_hits.pkl','wb'));print('HIT',w,'orbit',orbit,'tested',tested,'sec',time.time()-start,flush=True)
 if orbit%100==0:print('orbit',orbit,'tested',tested,'found',found.keys(),'smallwts',sorted(wtstats),'sec',time.time()-start,flush=True)
 if len(found)==4:break
pickle.dump(small,open('workspace/agent4_direct_shear_small.pkl','wb'))
print('DONE',tested,genuine,found.keys(),'nonlinear_preserved',nonlinear_preserved,wtstats,time.time()-start)
