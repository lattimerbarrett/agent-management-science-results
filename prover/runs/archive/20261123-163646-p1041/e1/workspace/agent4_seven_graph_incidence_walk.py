import random,time,pickle,collections,math
start=time.time();random.seed(432332);N=1<<14;ALL=(1<<N)-1
A=[((x&1)^((x>>1)&1))|(((x>>1)&1)<<1) for x in range(128)]
BASE=[[0]*128,A,[x^A[x] for x in range(128)]]
T=[322,326,330,334];found={};accept=0;stats=collections.Counter();best=1000
for geom in range(100):
 u=random.randrange(1,128);a,b=random.sample(range(1,128),2);R=random.choice(BASE)
 maps=[M.copy() for M in BASE]+[[R[x]^(u if (x&m).bit_count()%2 else 0) for x in range(128)] for m in [0,a,b,a^b]]
 gs=[sum(1<<(x+(y<<7)) for x,y in enumerate(M)) for M in maps];f=0;shifts=[0]*7
 for g in gs:f^=g
 assert f.bit_count()==318
 w=318
 def en(w):return min(abs(w-t) for t in T)+(0 if w%4==2 else 5)
 e=en(w)
 for it in range(10000):
  j=random.randrange(7);M=maps[j];sh=shifts[j];q=random.random()
  if q<.1:
   nm=M;ns=sh^(1<<random.randrange(7))
  else:
   ns=sh
   if q<.85:
    k=random.randrange(6);k+=k>=j;D=[x^y for x,y in zip(M,maps[k])];x0=random.randrange(1,128);v=D[x0]
    if not v:continue
    be=random.randrange(1,128)
    if not (be&v).bit_count()%2:continue
    al=sum(1<<i for i in range(7) if (be&D[1<<i]).bit_count()%2)
   else:v=random.randrange(1,128);al=random.randrange(1,128)
   nm=[y^(v if (x&al).bit_count()%2 else 0) for x,y in enumerate(M)]
  ng=sum(1<<(x+((y^ns)<<7)) for x,y in enumerate(nm));nf=f^gs[j]^ng;nw=nf.bit_count();ne=en(nw);temp=2+24*(1-(it%2000)/2000)
  if ne<=e or (300<=nw<=500 and random.random()<math.exp((e-ne)/temp)):
   if ng==gs[j]:continue
   shifts[j]=ns;maps[j]=nm;gs[j]=ng;f=nf;w=nw;e=ne;accept+=1;stats[w]+=1
   if w in T and w not in found:
    found[w]=(shifts.copy(),hex(f),[M.copy() for M in maps]);pickle.dump(found,open('workspace/agent4_seven_graph_incidence_hits.pkl','wb'));print('HIT',w,'geom',geom,'it',it,'sec',time.time()-start,flush=True)
  if len(found)==4:break
 if geom%10==0:print('geom',geom,'accept',accept,'found',found.keys(),'sec',time.time()-start,flush=True)
 if len(found)==4:break
print('DONE',accept,found.keys(),'nearstats',sorted((w,c) for w,c in stats.items() if w<360),time.time()-start)
open('workspace/agent4_seven_graph_incidence_walk.py','w').write(open(__file__).read())
