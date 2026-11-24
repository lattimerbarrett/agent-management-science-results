import time

def comps(caps,total,prefix=()):
 if len(caps)==1:
  if 0<=total<=caps[0]:yield prefix+(total,)
 else:
  for i in range(max(0,total-sum(caps[1:])),min(caps[0],total)+1):yield from comps(caps[1:],total-i,prefix+(i,))
for d in [7,8,9]:
 m=2*d;S=set();start=time.time()
 for ov in range(d+1):
  caps=[ov,d-ov,d-ov,ov];pat=[3,1,2,0]
  for cs in comps(caps,d):
   ns=[];ps=[]
   for n,c,p in zip(caps,cs,pat):ns.extend([c,n-c]);ps.extend([p|4,p])
   for ds in comps(ns,d):
    ii=[0]*16
    for n,z,p in zip(ns,ds,ps):
     for pp,nn in [(p|8,z),(p,n-z)]:
      if nn:
       for mask in range(1,16):
        if pp&mask==mask:ii[mask]+=nn
    w=sum((-2)**(mask.bit_count()-1)*(1<<ii[mask]) for mask in range(1,16));S.add(w)
 lo=5*2**(d-1);hi=21*2**(d-3)
 print(d,lo,hi, sorted(w for w in S if lo<=w<hi),time.time()-start,flush=True)
