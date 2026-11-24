import itertools,time,collections
mons=[sum(1<<i for i in I) for k in range(4) for I in itertools.combinations(range(8),k)]
cols=[sum(int(x&m==m)<<j for j,m in enumerate(mons)) for x in range(256)]
def span(bs,sh=0):
 out=[sh]
 for b in bs:out +=[x^b for x in out]
 return out
def check(nl,wdim,supp,allowed,expected):
 stats=collections.Counter();count=0;t=time.time()
 for pivs in itertools.combinations(range(nl),wdim):
  free=[(i,j) for i in range(wdim) for j in range(pivs[i]+1,nl) if j not in pivs]
  for bits in range(1<<len(free)):
   bs=[1<<p for p in pivs]
   for k,(i,j) in enumerate(free):
    if bits>>k&1:bs[i]^=1<<j
   V=span(bs);covered=set()
   for sh in range(1<<nl):
    if sh in covered:continue
    W={x^sh for x in V};covered|=W;count+=1;I=len(W&supp)
    if I not in allowed:continue
    A={x^y for x in W for y in span([1<<i for i in range(nl,8)])};U=A|supp;bas={}
    for x in U:
     v=cols[x]
     while v:
      p=v.bit_length()-1
      if p not in bas:bas[p]=v;break
      v^=bas[p]
    kd=len(U)-len(bas);order=sorted(bas,reverse=True);classes=collections.Counter()
    for x in range(256):
     if x in U:continue
     v=cols[x]
     for p in order:
      if v>>p&1:v^=bas[p]
     classes[v]+=1
    stats[(I,kd,classes[0],max(classes.values()))]+=1
 print(nl,wdim,'count',count,'stats',dict(stats),'seconds',time.time()-t,flush=True)
 assert dict(stats)==expected
if __name__=='__main__':
 f24={x for x in range(64) if ((x&3)==3)^((x&12)==12)}
 check(6,2,f24,[1,3],{(1,2,0,1):3840,(3,2,0,1):1280})
 f28={x for x in range(128) if ((x&7)==7)^((x&56)==56)}
 check(7,3,f28,[5,7],{(7,2,1,1):32,(5,2,0,2):1568})
