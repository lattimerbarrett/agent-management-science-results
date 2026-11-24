import random,time,math,json,numpy as np,shutil,collections
rng=random.Random(663224);ALL=(1<<128)-1;X=[sum(1<<x for x in range(128) if x>>i&1) for i in range(7)];LOW=[ALL^x for x in X]
def flat(free):
 out=[0]
 for i in free:out +=[x^(1<<i) for x in out]
 return sum(1<<x for x in out)
def perm(f,dst,src):
 p=((f&LOW[dst])<<(1<<dst))|((f&X[dst])>>(1<<dst))
 return f^((p^f)&X[src])
def trans(f,i):return ((f&LOW[i])<<(1<<i))|((f&X[i])>>(1<<i))
def mix(f):
 for _ in range(30):
  i,j=rng.sample(range(7),2);f=perm(f,i,j)
 for i in range(7):
  if rng.getrandbits(1):f=trans(f,i)
 return f
def codeweights(fs):return [( (fs[0] if s&1 else 0)^(fs[1] if s&2 else 0)^(fs[2] if s&4 else 0)).bit_count() for s in range(8)]
def hist(gs):
 a,b,c=gs
 return [( (a if s&1 else ALL^a)&(b if s&2 else ALL^b)&(c if s&4 else ALL^c)).bit_count() for s in range(8)]
f28=flat(range(4))^flat([0,4,5,6]);h14=flat([0,1,2])^flat([3,4,5]);g8=flat([0,1,2]);k16=flat(range(4));assert f28.bit_count()==28 and h14.bit_count()==14
start=time.time();hits={};bestglobal=10000;histlow=collections.Counter();saved=[];acc=0;shutil.copyfile(__file__,'workspace/agent3_mixed3_third_tensor_q1_search.py')
for restart in range(100):
 while True:
  fs=[f28,mix(f28),mix(h14)];gs=[g8,mix(g8),flat([3,4,5,6])];ow=codeweights(fs);nh=hist(gs);w=sum(a*b for a,b in zip(ow,nh))
  if w%4==2 and (fs[0]&fs[2]).bit_count()%2:break
 target=[322,326,330,334][restart%4];best=w
 for step in range(30000):
  side=rng.getrandbits(1);i=rng.choice([1,2]) if side==0 else 1;dst,src=rng.sample(range(7),2);islin=rng.random()<.85
  old=(fs if side==0 else gs)[i];new=perm(old,dst,src) if islin else trans(old,dst)
  if side==0:
   nfs=list(fs);nfs[i]=new
   if nfs[0]==nfs[1]:continue
   now=codeweights(nfs);nnh=nh;ww=sum(a*b for a,b in zip(now,nh))
  else:
   ngs=list(gs);ngs[i]=new
   if ngs[0]==ngs[1] or ngs[0]^ngs[1]==ngs[2]:continue
   nnh=hist(ngs);now=ow;ww=sum(a*b for a,b in zip(ow,nnh))
  if ww in (322,326,330,334) and ww not in hits:
   ff=nfs if side==0 else fs;gg=ngs if side==1 else gs;F=0
   for y in range(128):
    row=0
    for f,g in zip(ff,gg):
     if g>>y&1:row^=f
    F|=row<<(128*y)
   assert F.bit_count()==ww
   a=np.unpackbits(np.frombuffer(F.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little').copy()
   for b in range(14):
    st=1<<b;bl=a.reshape(-1,2*st);bl[:,st:]^=bl[:,:st]
   anf=list(map(int,np.flatnonzero(a)));assert max(map(int.bit_count,anf))<=7
   hits[ww]={'weight':ww,'truth_hex':hex(F),'anf':anf,'old_factors':ff,'new_factors':gg};print('VERIFIED HIT',ww,flush=True);json.dump(hits,open('workspace/agent3_mixed3_third_tensor_q1_hits.json','w'))
  if ww%4!=2:continue
  temp=1+15*(1-(step%10000)/10000)**2;diff=abs(ww-target)-abs(w-target)
  if diff>0 and rng.random()>math.exp(-diff/temp):continue
  if side==0:fs=nfs;ow=now
  else:gs=ngs;nh=nnh
  w=ww;acc+=1;best=min(best,w)
  if w<bestglobal:
   bestglobal=w
   if w<400:print('NEWBEST',w,'restart',restart,'step',step,flush=True)
  if w<=350:histlow[w]+=1
 if restart%10==0:print('restart',restart,'best',best,'global',bestglobal,'acc',acc,'low',dict(histlow),'sec',round(time.time()-start,1),flush=True)
 if len(hits)==4 or time.time()-start>110:break
print('DONE','best',bestglobal,'hits',list(hits),'low',dict(histlow),'secs',time.time()-start,flush=True)
