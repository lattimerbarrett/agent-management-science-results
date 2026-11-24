import random,time,pickle,collections,math
start=time.time();random.seed(413388);N=1<<14;ALL=(1<<N)-1
Y=[sum(1<<x for x in range(N) if x>>(7+i)&1) for i in range(7)]
A=[((x&1)^((x>>1)&1))|(((x>>1)&1)<<1) for x in range(128)]
BASE=[[0]*128,A,[x^A[x] for x in range(128)]]
T=[322,326,330,334];found={};accept=0;stats=collections.Counter()
def translate(p,i):
 s=1<<(7+i);return ((p&(ALL^Y[i]))<<s)|((p&Y[i])>>s)
for geom in range(2000):
 u=random.randrange(1,128);a,b=random.sample(range(1,128),2);R=random.choice(BASE)
 maps=BASE.copy()+[[R[x]^(u if (x&m).bit_count()%2 else 0) for x in range(128)] for m in [0,a,b,a^b]]
 gs=[]
 for M in maps:
  g0=sum(1<<(x+(y<<7)) for x,y in enumerate(M));g=[g0]*128
  for sh in range(1,128):
   lo=sh&-sh;i=lo.bit_length()-1;g[sh]=translate(g[sh^lo],i)
  gs.append(g)
 f=0;shifts=[0]*7
 for g in gs:f^=g[0]
 assert f.bit_count()==318
 w=318
 def en(w):return min(abs(w-t) for t in T)+(0 if w%4==2 else 8)
 e=en(w)
 for it in range(5000):
  j=random.randrange(7);sh=shifts[j]^(1<<random.randrange(7));nf=f^gs[j][shifts[j]]^gs[j][sh];nw=nf.bit_count();ne=en(nw)
  if ne<=e or (300<=nw<=420 and random.random()<math.exp((e-ne)/5)):
   shifts[j]=sh;f=nf;w=nw;e=ne;accept+=1;stats[w]+=1
   if w in T and w not in found:
    found[w]=(u,a,b,BASE.index(R),shifts.copy(),hex(f),maps);pickle.dump(found,open('workspace/agent4_seven_graph_translation_hits.pkl','wb'));print('HIT',w,'geom',geom,'it',it,'sec',time.time()-start,flush=True)
  if len(found)==4:break
 if geom%200==0:print('geom',geom,'accept',accept,'found',found.keys(),'sec',time.time()-start,flush=True)
 if len(found)==4:break
print('DONE',accept,found.keys(),'nearstats',sorted((w,c) for w,c in stats.items() if w<360),time.time()-start)
open('workspace/agent4_seven_graph_translation_walk.py','w').write(open(__file__).read())
