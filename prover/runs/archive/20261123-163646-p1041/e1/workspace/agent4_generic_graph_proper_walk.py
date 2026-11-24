import random,time,pickle,collections,math
start=time.time();random.seed(435350);N=1<<14;ALL=(1<<N)-1
T=[322,326,330,334];found={};accept=0;stats=collections.Counter();best=1000;saved={}
BOUND={2:192,3:224,4:240,5:248,6:252}
SUB=[[s for s in range(1,127) if s>>j&1 and s.bit_count()>1] for j in range(7)]
SUB=[sorted(ss,key=lambda s:s.bit_count()) for ss in SUB]
def linmap(cols):
 M=[0]*128
 for x in range(1,128):
  lo=x&-x;M[x]=M[x^lo]^cols[lo.bit_length()-1]
 return M
for geom in range(50):
 maps=[linmap([random.randrange(128) for _ in range(7)]) for j in range(7)]
 gs=[sum(1<<(x+(y<<7)) for x,y in enumerate(M)) for M in maps];sw=[0]*128;shifts=[0]*7
 for s in range(1,128):
  lo=s&-s;sw[s]=sw[s^lo]^gs[lo.bit_length()-1]
 assert all(sw[s].bit_count()>=BOUND[s.bit_count()] for s in range(1,127) if s.bit_count()>1)
 f=sw[127];w=f.bit_count()
 if w%4!=2:continue
 en=lambda w:min(abs(w-t) for t in T)+(0 if w%4==2 else 5);e=en(w)
 for it in range(5000):
  j=random.randrange(7);M=maps[j];sh=shifts[j];q=random.random()
  if q<.1:nm=M;ns=sh^(1<<random.randrange(7))
  else:
   ns=sh
   if q<.9:
    k=random.randrange(6);k+=k>=j;D=[x^y for x,y in zip(M,maps[k])];x0=random.randrange(1,128);v=D[x0]
    if not v:continue
    be=random.randrange(1,128)
    if not (be&v).bit_count()%2:continue
    al=sum(1<<i for i in range(7) if (be&D[1<<i]).bit_count()%2)
   else:v=random.randrange(1,128);al=random.randrange(1,128)
   nm=[y^(v if (x&al).bit_count()%2 else 0) for x,y in enumerate(M)]
  ng=sum(1<<(x+((y^ns)<<7)) for x,y in enumerate(nm));delta=gs[j]^ng
  if not delta:continue
  nf=f^delta;nw=nf.bit_count()
  if nw%4!=2:continue
  ne=en(nw);temp=.5
  if ne>e and random.random()>=math.exp((e-ne)/temp):continue
  good=True
  for s in SUB[j]:
   ww=(sw[s]^delta).bit_count()
   if ww in T and ww not in found:
    fs=[(gs[k]^(delta if k==j else 0)) for k in range(7) if s>>k&1];ff=0
    for gg in fs:ff^=gg
    assert ff.bit_count()==ww
    found[ww]=(hex(ff),[hex(gg) for gg in fs]);pickle.dump(found,open('workspace/agent4_generic_graph_proper_hits.pkl','wb'));print('SUBHIT',ww,flush=True)
   if ww<BOUND[s.bit_count()]:good=False;break
  if not good:continue
  for s in range(1,128):
   if s>>j&1:sw[s]^=delta
  shifts[j]=ns;maps[j]=nm;gs[j]=ng;f=nf;w=nw;e=ne;accept+=1;stats[w]+=1
  if w<best:best=w
  if w<=398 and w not in saved:saved[w]=(hex(f),[hex(g) for g in gs]);pickle.dump(saved,open('workspace/agent4_generic_graph_proper_small.pkl','wb'))
  if w in T and w not in found:
   found[w]=(hex(f),[hex(g) for g in gs]);pickle.dump(found,open('workspace/agent4_generic_graph_proper_hits.pkl','wb'));print('HIT',w,'geom',geom,'it',it,'sec',time.time()-start,flush=True)
  if len(found)==4:break
 if geom%5==0:print('geom',geom,'best',best,'last',w,'accept',accept,'found',found.keys(),'sec',time.time()-start,flush=True)
 if len(found)==4:break
print('DONE',accept,found.keys(),'nearstats',sorted((w,c) for w,c in stats.items() if w<400),time.time()-start)
open('workspace/agent4_generic_graph_proper_walk.py','w').write(open(__file__).read())
