import itertools,time,pickle,collections
start=time.time();weights=[5**(int(bool(u&3))+int(bool(u&12)))*3**((u>>4).bit_count()) for u in range(64)]
mons=[m for m in range(64) if m.bit_count()<=2];found={}
for typ in [0,1]:
 HP=lambda u:(u&48)==0 if typ==0 else (u&3)==0
 assert sum(weights[u] for u in range(64) if HP(u))==256
 V=[u for u in range(64) if weights[u]<=39 or HP(u)];bas={};G=[]
 for j,u in enumerate(V):
  v=sum(1<<i for i,m in enumerate(mons) if u&m==m);w=1<<j
  while v:
   p=v.bit_length()-1
   if p not in bas:bas[p]=(v,w);break
   a,b=bas[p];v^=a;w^=b
  if not v:G.append(w)
 print('type',typ,'dim',len(G),'lenV',len(V),'rank',len(bas))
 pool={};hist=collections.Counter();word=0;prev=0
 for i in range(1<<len(G)):
  gr=i^(i>>1)
  if i:word^=G[(gr^prev).bit_length()-1]
  prev=gr;wt=sum(weights[u] for j,u in enumerate(V) if word>>j&1)
  if wt<=270:pool[word]=wt;hist[wt]+=1
 print('pool',len(pool),'hist',sorted(hist.items()))
 DH=sum(1<<j for j,u in enumerate(V) if HP(u))
 small=[(a,w) for a,w in pool.items() if w<=206]
 for i,(a,wa) in enumerate(small):
  for b,wb in small[i:]:
   if wa+wb>334:continue
   c=a^b^DH;wc=pool.get(c)
   if wc is None:continue
   target=wa+wb+wc
   if target in [322,326,330,334] and target not in found:
    found[target]=(typ,a,b,c,V,wa,wb,wc);print('FOUND',target,'weights',wa,wb,wc);pickle.dump(found,open('workspace/agent4_C5C5C3C3_shortened_hits.pkl','wb'))
print('DONE',found.keys(),'sec',time.time()-start)
open('workspace/agent4_C5C5C3C3_shortened_exact.py','w').write(open(__file__).read())
