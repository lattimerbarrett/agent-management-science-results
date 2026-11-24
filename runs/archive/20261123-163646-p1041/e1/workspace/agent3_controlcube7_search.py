import itertools,random,time,math,json,numpy as np,functools,shutil
rng=random.Random(738492);nold=11;No=2048;Ao=(1<<No)-1;X=[sum(1<<x for x in range(No) if x>>i&1) for i in range(nold)];LX=[Ao^v for v in X];ctls=[1,2,4,3,5,6,7];ks=[4+c.bit_count() for c in ctls];bounds=[0,128,192,224,240,248,252,0]
@functools.lru_cache(maxsize=100000)
def term(i,mask,shift):
 v=Ao
 for j in range(nold):
  if not mask>>j&1:v&=X[j] if shift>>j&1 else LX[j]
 return sum(v<<(No*c) for c in range(8) if c&ctls[i]==ctls[i])
def randomparam(i):
 mask=sum(1<<j for j in rng.sample(range(11),ks[i]));return mask,rng.randrange(2048)&~mask
contain=[[s for s in range(1,127) if s>>i&1 and s.bit_count()>=2] for i in range(7)]
def subsetwords(ts):
 out=[0]*128
 for s in range(1,128):
  b=s&-s;out[s]=out[s^b]^ts[b.bit_length()-1]
 return out
start=time.time();hits={};saved=[];bestglobal=10000;accepted=0
shutil.copyfile(__file__,'workspace/agent3_controlcube7_search.py')
for restart in range(30):
 while True:
  ps=[randomparam(i) for i in range(7)];ts=[term(i,*p) for i,p in enumerate(ps)];ss=subsetwords(ts)
  if all(ss[s].bit_count()>=bounds[s.bit_count()] for s in range(1,127)):break
 w=ss[127].bit_count();best=w;stagnant=0
 for step in range(100000):
  i=rng.randrange(7);mask,shift=ps[i];r=rng.random()
  if r<.3:
   j=rng.choice([j for j in range(11) if not mask>>j&1]);new=(mask,shift^(1<<j))
  elif r<.995:
   a=rng.choice([j for j in range(11) if mask>>j&1]);b=rng.choice([j for j in range(11) if not mask>>j&1]);mm=mask^(1<<a)^(1<<b);sh=shift&~(1<<b)
   if rng.getrandbits(1):sh|=1<<a
   else:sh&=~(1<<a)
   new=mm,sh
  else:new=randomparam(i)
  tt=term(i,*new);delta=tt^ts[i];fw=ss[127]^delta;ww=fw.bit_count()
  if ww in (322,326,330,334) and ww not in hits:
   arr=np.unpackbits(np.frombuffer(fw.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little').copy()
   for bit in range(14):
    st=1<<bit;bl=arr.reshape(-1,2*st);bl[:,st:]^=bl[:,:st]
   anf=list(map(int,np.flatnonzero(arr)));assert max(map(int.bit_count,anf))<=7
   hits[ww]={'weight':ww,'truth_hex':hex(fw),'anf':anf,'params':ps[:i]+[new]+ps[i+1:]};print('VERIFIED HIT',ww,flush=True);json.dump(hits,open('workspace/agent3_controlcube7_hits.json','w'))
  temperature=2+12*(1-(step%20000)/20000)**2;diff=abs(ww-322)-abs(w-322)
  if diff>0 and rng.random()>=math.exp(-diff/temperature):continue
  if any((ss[s]^delta).bit_count()<bounds[s.bit_count()] for s in contain[i]):continue
  ps[i]=new;ts[i]=tt;w=ww;accepted+=1
  for s in range(1,128):
   if s>>i&1:ss[s]^=delta
  if w<best:best=w;stagnant=0
  else:stagnant+=1
  if w<bestglobal:
   bestglobal=w;print('NEWBEST',w,'restart',restart,'step',step,'secs',round(time.time()-start,1),flush=True)
   if w<=440:saved.append({'weight':w,'truth_hex':hex(ss[127]),'params':list(ps)});json.dump(saved,open('workspace/agent3_controlcube7_states.json','w'))
  if len(hits)==4:break
 print('restartDONE',restart,'best',best,'global',bestglobal,'accepted',accepted,'time',round(time.time()-start,1),flush=True)
 if len(hits)==4 or time.time()-start>280:break
print('DONE best',bestglobal,'hits',list(hits),'time',time.time()-start)
