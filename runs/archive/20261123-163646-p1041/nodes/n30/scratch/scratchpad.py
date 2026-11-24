import random,time,math,json,collections
N=14;TARGET={310,322,326,330,334};rng=random.Random(98123)
def flat(free,val):
 v=1<<val
 while free:
  b=free&-free;free-=b;v|=v<<b
 return v
start=time.time();found={};seen=collections.Counter();best=1000
for rep in range(300):
 k=6 if rep%3==0 else rng.choice([7,8,9,10,12]);params=[];vs=[];f=0
 for _ in range(k):
  free=sum(1<<i for i in rng.sample(range(14),7));val=rng.getrandbits(14)&(16383^free);v=flat(free,val);params.append((free,val));vs.append(v);f^=v
 w=f.bit_count();target=[310,322,326,330,334][rep%5];e=abs(w-target)
 for step in range(20000):
  j=rng.randrange(k);free,val=params[j]
  if rng.random()<.7:
   i=rng.choice([i for i in range(14) if free>>i&1]);h=rng.choice([i for i in range(14) if not free>>i&1]);nf=free^(1<<i)^(1<<h);nv=(val&~(1<<h))^(rng.getrandbits(1)<<i)
  else:
   nf=free;nv=val^(1<<rng.choice([i for i in range(14) if not free>>i&1]))
  v=flat(nf,nv);ff=f^vs[j]^v;ww=ff.bit_count()
  if ww in TARGET and ww not in found:
   pp=params.copy();pp[j]=(nf,nv);found[ww]=pp;json.dump(found,open('direct14_witnesses.json','w'));print('FOUND',ww,'k',k,'time',time.time()-start,flush=True)
  ee=abs(ww-target);temp=1+18*(1-(step%4000)/4000)**2
  if ee<=e or rng.random()<math.exp((e-ee)/temp):
   params[j]=(nf,nv);vs[j]=v;f=ff;w=ww;e=ee
   if w<=350:seen[w]+=1
 if rep%10==0:print('rep',rep,'found',list(found),'seenlow',sorted(seen.items()),'time',time.time()-start,flush=True)
 if time.time()-start>560:break
print('FINAL',found,'time',time.time()-start)
