import json,numpy as np,time,collections,random,shutil
src=open('workspace/agent3_higher_shear_search.py').read();exec(src[:src.index('combos=')]);X=[sum(1<<x for x in range(N) if x>>i&1) for i in range(14)];rng=np.random.default_rng(3894);R=random.Random(8934);start=time.time()
def rank(rows):
 p={}
 for v in rows:
  while v:
   b=v.bit_length()-1
   if b not in p:p[b]=v;break
   v^=p[b]
 return len(p)
def qr(f,w):
 ds=[(f&x).bit_count() for x in X];t=[d//2%2 for d in ds];rows=[0]*14
 for i in range(14):
  for j in range(i):
   c=(f&X[i]&X[j]).bit_count()
   if t[i] and t[j]:c=w-ds[i]-ds[j]+c
   elif t[i]:c=ds[j]-c
   elif t[j]:c=ds[i]-c
   if c//2%2:rows[i]|=1<<j;rows[j]|=1<<i
 return rank(rows)
initial=[{'truth_hex':hex(mob(a)),'weight':w} for a,w in pool[:64] if w%4==2]+json.load(open('workspace/agent3_highqrank_flatadd_improvements.json'))
words={}
for r in initial:
 f=int(r['truth_hex'],16);w=r['weight'];q=qr(f,w)
 if q>=4:words[f]=(w,q)
best=min(w for w,q in words.values());words={f:r for f,r in words.items() if r[0]<=best+12};seen=set(words);hits={};accepted=[];stats=collections.Counter();print('INITIAL',len(words),'best',best,flush=True)
for sweep in range(2000):
 choices=list(words);f=R.choices(choices,weights=[2**(-(words[f][0]-best)/4) for f in choices])[0];w,q=words[f]
 S=[x for x in range(N) if f>>x&1];SS=set(S);samples=rng.choice(S,size=(10000,8),replace=True)
 for sam in samples:
  v=list(map(int,sam));p=v[0];ps=[p]
  for b in v[1:]:
   b^=p;ps +=[x^b for x in ps]
  if len(set(ps))<128:continue
  I=sum(x in SS for x in ps);ww=w+128-2*I
  if ww in (322,326,330,334):
   g=f^sum(1<<x for x in ps);assert g.bit_count()==ww
   aa=np.unpackbits(np.frombuffer(g.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little').copy()
   for i in range(14):
    st=1<<i;bl=aa.reshape(-1,2*st);bl[:,st:]^=bl[:,:st]
   anf=list(map(int,np.flatnonzero(aa)));assert max(map(int.bit_count,anf))<=7
   hits[ww]={'weight':ww,'truth_hex':hex(g),'anf':anf};print('VERIFIED HIT',ww,flush=True);json.dump(hits,open('workspace/agent3_qrank_guided_hits.json','w'))
  if I<64 or ww%4!=2 or ww>best+12:continue
  g=f^sum(1<<x for x in ps)
  if g in seen:continue
  seen.add(g);qq=qr(g,ww);stats[ww,qq]+=1
  if qq<4:continue
  words[g]=(ww,qq);accepted.append({'weight':ww,'truth_hex':hex(g),'qrank':qq})
  if ww<best:
   best=ww;print('NEW BEST',best,'rank',qq,'sweep',sweep,flush=True);words={ff:r for ff,r in words.items() if r[0]<=best+12}
 if len(words)>300:words=dict(R.sample(list(words.items()),300))
 if sweep%50==0:
  print('sweep',sweep,'best',best,'words',len(words),'seen',len(seen),'stats',dict(stats),'seconds',round(time.time()-start,1),flush=True);json.dump(accepted,open('workspace/agent3_qrank_guided_states.json','w'))
 if len(hits)==4 or time.time()-start>280:break
print('DONE',sweep,'best',best,'hits',list(hits),'seconds',time.time()-start,flush=True);json.dump(accepted,open('workspace/agent3_qrank_guided_states.json','w'));shutil.copyfile(__file__,'workspace/agent3_qrank_guided_search.py')
