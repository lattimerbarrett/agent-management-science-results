import itertools,random,time,collections,pickle,functools
start=time.time();random.seed(4367)
def mul2(a):return ((a<<1)^ (11 if a&4 else 0))&7
INV=[functools.reduce(lambda a,b:mul2(a),range(6),u) for u in range(8)]
GX=[sum((mul2((x>>(3*j))&7) if j<2 else INV[(x>>(3*j))&7])<<(3*j) for j in range(4))|(x&12288) for x in range(16384)]
orb={};ow=[]
for x in range(16384):
 if x in orb:continue
 ps=[];u=x
 while u not in ps:ps.append(u);u=GX[u]
 assert len(ps) in (1,7)
 j=len(ow);ow.append(len(ps))
 for u in ps:orb[u]=j
B=[1<<orb[x] for x in range(16384)];FIX=sum(1<<j for j,w in enumerate(ow) if w==1)
def pack(ps):
 v=0
 for x in ps:v^=B[x]
 return v
def weight(v):return 7*(v&~FIX).bit_count()+(v&FIX).bit_count()
def flat(bs,sh):
 ps=[sh]
 for b in bs:ps +=[x^b for x in ps]
 return tuple(ps)
def randflat():
 bs=[];piv={}
 while len(bs)<7:
  b=random.randrange(1,16384);v=b
  while v and v.bit_length()-1 in piv:v^=piv[v.bit_length()-1]
  if v:piv[v.bit_length()-1]=v;bs.append(b)
 return flat(bs,random.randrange(16384))
cnt=collections.Counter();wts=collections.Counter()
for _ in range(1000):
 A=randflat();w=weight(pack(A));cnt[w%4]+=1;wts[w]+=1
print('randommod4',cnt,'range',min(wts),max(wts),'sec',time.time()-start)
# Coherentorbitflatanneal
POW=[list(range(16384))]
for k in range(1,7):POW.append([GX[x] for x in POW[-1]])
T=[322,330];found={};accept=0;best=1000;stats=collections.Counter()
def en(w):return min(abs(w-t) for t in T)+(0 if w%4==2 else 5)
for restart in range(200):
 bgoal=restart%2
 while True:
  A=randflat()
  if bgoal:A=tuple(x^A[0] for x in A)
  v=pack(A);w=weight(v)
  if w%4==2 and (v&FIX).bit_count()==bgoal:break
 e=en(w)
 for it in range(10000):
  i=random.randrange(14)
  if random.random()<.8:
   k=random.randrange(1,7);aset=set(A);idx={x:t for t,x in enumerate(A)};I=aset&{POW[k][x] for x in A};p=next(iter(I)) if I else A[0];c=idx[p]
   J=I|{POW[7-k][x] for x in I};jb={}
   for x in J:
    z=idx[x]^c
    while z and z.bit_length()-1 in jb:z^=jb[z.bit_length()-1]
    if z:jb[z.bit_length()-1]=z
   if len(jb)>=7:continue
   al=0
   for retry in range(128):
    al=random.randrange(1,128)
    if all((al&z).bit_count()%2==0 for z in jb.values()):break
   else:continue
   H=tuple(x for t,x in enumerate(A) if (al&(t^c)).bit_count()%2==0)
   vvpoints=[POW[k][x] for x in H if POW[k][x] not in aset]
   if not vvpoints:continue
   diff=random.choice(vvpoints)^H[0];AA=H+tuple(x^diff for x in H)
  elif random.random()<.1:AA=tuple(x^(1<<i) for x in A)
  else:
   j=random.randrange(13);j+=j>=i;AA=tuple(x^(((x>>j)&1)<<i) for x in A)
  vv=pack(AA);ww=weight(vv)
  if ww%4!=2 or (vv&FIX).bit_count()!=bgoal:continue
  ee=en(ww);temp=1.0
  if ee<=e or (ww>=300 and random.random()<pow(2.718281828,(e-ee)/temp)):
   if vv==v:continue
   A=AA;v=vv;w=ww;e=ee;accept+=1;stats[w]+=1;best=min(best,w)
   if w in T and w not in found:
    found[w]=(A,hex(v));pickle.dump(found,open('workspace/agent4_singleC7_orbit_hits.pkl','wb'));print('HIT',w,'restart',restart,'it',it,'sec',time.time()-start,flush=True)
  if len(found)==2:break
 if restart%10==0:print('restart',restart,'best',best,'accept',accept,'found',found.keys(),'sec',time.time()-start,flush=True)
 if len(found)==2:break
print('DONE',found.keys(),'nearstats',sorted((w,c) for w,c in stats.items() if w<380),'sec',time.time()-start)
open('workspace/agent4_singleC7_orbit_search.py','w').write(open(__file__).read())
