import random,time,math,json,numpy as np,shutil,collections
rng=random.Random(422422);MASK=(1<<128)-1;ops=[]
for i in range(7):
 low=sum(1<<x for x in range(128) if not(x>>i&1));ops.append((i,low))
for dst in range(7):
 for src in range(7):
  if dst!=src:ops.append((dst,sum(1<<x for x in range(128) if x>>src&1 and not(x>>dst&1))))
def mutate(f,op):
 i,lo=ops[op];st=1<<i;d=(f^(f>>st))&lo;return f^d^(d<<st)
def flat(free,shift=0):
 S=[shift]
 for b in free:S += [x^b for x in S]
 return sum(1<<x for x in S)
def randaff(f):
 for _ in range(80):f=mutate(f,rng.randrange(49))
 return f
def weights(A):return [0]+[( (A[0] if u&1 else 0)^(A[1] if u&2 else 0)^(A[2] if u&4 else 0)).bit_count() for u in range(1,8)]
def counts(A):
 return [((A[0] if u&1 else MASK^A[0])&(A[1] if u&2 else MASK^A[1])&(A[2] if u&4 else MASK^A[2])).bit_count() for u in range(8)]
def score(w):return w+(80 if w%4==0 else 0)
min16=flat([1,2,4,8]);wt14=flat([1,2,4])^flat([8,16,32]);best=10000;bestq=10000;hits={};states=[];start=time.time();hist=collections.Counter();pool=[]
for restart in range(60):
 if pool and rng.randrange(3):
  old,new=[list(x) for x in rng.choice(pool)]
  for _ in range(30):
   A=rng.choice([old,new]);i=rng.randrange(3);A[i]=mutate(A[i],rng.randrange(49))
 else:old=[randaff(min16),randaff(min16),randaff(wt14)];new=[randaff(wt14),randaff(wt14),randaff(min16)]
 W=[weights(old),weights(new)];C=[counts(old),counts(new)];A=[old,new];w=sum(W[0][u]*C[1][u] for u in range(8));cost=score(w);localbest=10000
 for it in range(50000):
  side=rng.randrange(2);i=rng.randrange(3);idxs=[u for u in range(1,8) if u>>i&1];f=mutate(A[side][i],rng.randrange(49))
  if rng.randrange(20)==0:
   for _ in range(rng.randrange(1,6)):f=mutate(f,rng.randrange(49))
  dw=0;ww={}
  for u in idxs:
   vv=f
   for j in range(3):
    if j!=i and u>>j&1:vv^=A[side][j]
   wc=vv.bit_count();ww[u]=wc;dw+=(wc-W[side][u])*C[1-side][u]
  nw=w+dw;nc=score(nw);T=12*(1-(it%10000)/10000)**2+.2
  if nc<=cost or rng.random()<math.exp((cost-nc)/T):
   A[side][i]=f
   for u,v in ww.items():W[side][u]=v
   C[side]=counts(A[side]);w=nw;cost=nc
   if w%4==2 and w<bestq:
    bestq=w;print('NEWQBEST',w,'restart',restart,'it',it,'W',W,'C',C,'t',round(time.time()-start,2),flush=True);states.append({'old':list(map(hex,old)),'new':list(map(hex,new)),'weight':w,'W':W,'C':C});json.dump(states,open('workspace/agent3_mixed3_reversed_states.json','w'))
   if w<best:best=w
   if cost<localbest:
    localbest=cost
    if len(pool)>=30:pool.pop(0)
    pool.append((old.copy(),new.copy()))
   if w in [322,326,330,334] and w not in hits:
    F=0
    for x in range(128):
     yy=(new[0] if old[0]>>x&1 else 0)^(new[1] if old[1]>>x&1 else 0)^(new[2] if old[2]>>x&1 else 0);F|=yy<<(128*x)
    assert F.bit_count()==w;arr=np.unpackbits(np.frombuffer(F.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little').copy()
    for k in range(14):
     st=1<<k;bl=arr.reshape(-1,2*st);bl[:,st:]^=bl[:,:st]
    anf=list(map(int,np.flatnonzero(arr)));assert max(map(int.bit_count,anf))<=7
    hits[w]={'truth_hex':hex(F),'weight':w,'anf':anf,'old':list(map(hex,old)),'new':list(map(hex,new))};json.dump(hits,open('workspace/agent3_mixed3_reversed_hits.json','w'));print('VERIFIEDHIT',w,flush=True)
  if len(hits)==4:break
 if restart%5==0:print('restart',restart,'best',best,'bestq',bestq,'current',w,'time',round(time.time()-start,1),flush=True)
 if len(hits)==4 or time.time()-start>110:break
print('DONE',restart,it,'best',best,'bestq',bestq,'hits',list(hits),'t',time.time()-start,flush=True);shutil.copyfile(__file__,'workspace/agent3_mixed3_reversed_search.py')
