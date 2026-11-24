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
import itertools
min16=flat([1,2,4,8]);wt14=flat([1,2,4])^flat([8,16,32]);S3=[min16,min16^flat([1,2,16,32]),sum(1<<x for x in range(128) if x&1 and (((x>>1&1)*(x>>2&1))^((x>>3&1)*(x>>4&1))^((x>>5&1)*(x>>6&1)))),min16^flat([1,16,32,64])];S4=[flat([1,2,4]),flat([1,2,4])^flat([1,8,16]),wt14]
assert list(map(int.bit_count,S3))==[16,24,28,28] and list(map(int.bit_count,S4))==[8,12,14]
configs=[]
for a,b,k in itertools.product(range(4),repeat=3):
 for h,c,d in itertools.product(range(3),repeat=3):
  if [1,2,3,2][a]*[1,2,2][c]+[1,2,3,2][b]*[1,2,2][d]+[1,2,2][h]*[1,2,3,2][k]>5:configs.append((a,b,h,c,d,k))
rng.shuffle(configs);best=10000;bestq=10000;hits={};states=[];start=time.time();results=[]
for restart,(a,b,h,c,d,k) in enumerate(configs):
 old=[randaff(S3[a]),randaff(S3[b]),randaff(S4[h])];new=[randaff(S4[c]),randaff(S4[d]),randaff(S3[k])]
 W=[weights(old),weights(new)];C=[counts(old),counts(new)];A=[old,new];w=sum(W[0][u]*C[1][u] for u in range(8));cost=score(w);localbest=10000
 for it in range(20000):
  side=rng.randrange(2);i=rng.randrange(3);idxs=[u for u in range(1,8) if u>>i&1];f=mutate(A[side][i],rng.randrange(49))
  if rng.randrange(20)==0:
   for _ in range(rng.randrange(1,6)):f=mutate(f,rng.randrange(49))
  dw=0;ww={}
  for u in idxs:
   vv=f
   for j in range(3):
    if j!=i and u>>j&1:vv^=A[side][j]
   wc=vv.bit_count();ww[u]=wc;dw+=(wc-W[side][u])*C[1-side][u]
  if any(v==0 for v in ww.values()):continue
  nw=w+dw
  if w%4==2 and nw%4==0:continue
  nc=score(nw);T=14*(1-(it%5000)/5000)**2+.2
  if nc<=cost or rng.random()<math.exp((cost-nc)/T):
   A[side][i]=f
   for u,v in ww.items():W[side][u]=v
   C[side]=counts(A[side]);w=nw;cost=nc
   if w%4==2 and w<bestq:
    bestq=w;print('NEWQBEST',w,'restart',restart,'it',it,'W',W,'C',C,'t',round(time.time()-start,2),flush=True);states.append({'old':list(map(hex,old)),'new':list(map(hex,new)),'weight':w,'W':W,'C':C});json.dump(states,open('workspace/agent3_mixed3_reversed_states.json','w'))
   if w<best:best=w
   if cost<localbest:localbest=cost
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
 results.append({'configuration':[a,b,h,c,d,k],'bestcost':localbest})
 if restart%50==0:print('restart',restart,'best',best,'bestq',bestq,'config',[a,b,h,c,d,k],'current',w,'time',round(time.time()-start,1),flush=True);json.dump(results,open('workspace/agent3_mixed3_lowtypes_results.json','w'))
 if len(hits)==4 or time.time()-start>110:break
json.dump(results,open('workspace/agent3_mixed3_lowtypes_results.json','w'));print('DONE',restart,it,'best',best,'bestq',bestq,'hits',list(hits),'t',time.time()-start,flush=True);shutil.copyfile(__file__,'workspace/agent3_mixed3_lowtypes_search.py')
