import itertools,time,pickle,collections
start=time.time();V=[u for u in range(64) if u.bit_count()<=3 or (u&3)==0]
mons=[m for m in range(64) if m.bit_count()<=2];bas={};G=[]
for j,u in enumerate(V):
 v=sum(1<<i for i,m in enumerate(mons) if u&m==m);w=1<<j
 while v:
  p=v.bit_length()-1
  if p not in bas:bas[p]=(v,w);break
  a,b=bas[p];v^=a;w^=b
 if not v:G.append(w)
print('shortdim',len(G),'lenV',len(V),'rank',len(bas))
weights=[3**u.bit_count() for u in V]
chunks=[]
for k in range(4):
 ws=weights[11*k:11*(k+1)];tab=[0]*(1<<len(ws))
 for m in range(1,len(tab)):
  lo=m&-m;tab[m]=tab[m^lo]+ws[lo.bit_length()-1]
 chunks.append(tab)
A,B,C,D=chunks
lo=2047;pool={};hist=collections.Counter();word=0;prev=0
for i in range(1<<len(G)):
 gr=i^(i>>1)
 if i:word^=G[(gr^prev).bit_length()-1]
 prev=gr;wt=A[word&lo]+B[(word>>11)&lo]+C[(word>>22)&lo]+D[word>>33]
 if wt<=270:pool[word]=wt;hist[wt]+=1
print('poolsize',len(pool),'hist',sorted(hist.items()),'sec',time.time()-start)
pickle.dump((V,G,pool),open('workspace/agent4_C3six_shortened_pool.pkl','wb'))
DH=sum(1<<j for j,u in enumerate(V) if u&3==0)
# Everyhardword haszero(s,t)-slice(bylocalRM6,12min64/second96 etc), so3wordpairsuffices.
small=[(a,w) for a,w in pool.items() if w<=206];found={}
for i,(a,wa) in enumerate(small):
 for b,wb in small[i:]:
  if wa+wb>334:continue
  c=a^b^DH;wc=pool.get(c)
  if wc is None:continue
  target=wa+wb+wc
  if target in [322,326,330,334] and target not in found:
   found[target]=(a,b,c,V,wa,wb,wc);print('FOUND',target,'weights',wa,wb,wc);pickle.dump(found,open('workspace/agent4_C3six_shortened_hits.pkl','wb'))
print('DONE',found.keys(),'sec',time.time()-start)
open('workspace/agent4_C3six_shortened_exact.py','w').write(open(__file__).read())
