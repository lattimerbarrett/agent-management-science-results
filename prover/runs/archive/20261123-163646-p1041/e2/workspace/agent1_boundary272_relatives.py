import itertools,json,pathlib,time,collections,sys
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese,closure

def span(B):
 z=[0]
 for b in B:z +=[x^b for x in z]
 return z

def flats(n,d):
 for piv in itertools.combinations(range(n),d):
  non=[j for j in range(n) if j not in piv]
  free=[(i,j) for i,p in enumerate(piv) for j in non if j>p]
  for z in range(1<<len(free)):
   B=[1<<p for p in piv]
   for h,(i,j) in enumerate(free):
    if z>>h&1:B[i]^=1<<j
   H=span(B)
   for off in span([1<<j for j in non]):yield [x^off for x in H]

def basis(columns):
 B={}
 for j,v in enumerate(columns):
  c=1<<j
  while v:
   k=v.bit_length()-1
   if k in B:v^=B[k][0];c^=B[k][1]
   else:B[k]=(v,c);break
 return B

def red(v,B):
 c=0
 while v:
  k=v.bit_length()-1
  if k not in B:return v,c
  v^=B[k][0];c^=B[k][1]
 return v,c

def mobius(a):
 a=a[:];n=len(a).bit_length()-1
 for i in range(n):
  for m in range(len(a)):
   if m>>i&1:a[m]^=a[m^(1<<i)]
 return a

raw=json.load(open('workspace/agent4_boundary256_orbits.json'));out=[];t0=time.time();seeds=[]
for obj in raw:
 if not obj['solvable']:continue
 S=sorted({(p&63)|((p>>3)&64) for p in obj['support']});SS=set(S)
 S256=sorted(p|(r<<7) for p in S for r in range(8));vs10=veronese(10,5);B256=basis([vs10[p] for p in S256])
 counts={};khist=collections.Counter();local=[]
 for d in range(4):
  vs=veronese(7,d+2);B=basis([vs[p] for p in S]);nr=0;tot=0
  for Q in flats(7,d):
   tot+=1
   if SS.intersection(Q):continue
   z=0
   for p in Q:z^=vs[p]
   if red(z,B)[0]:continue
   nr+=1
   P=[p|(r<<7) for p in Q for r in range(1<<(3-d))]
   z=0
   for p in P:z^=vs10[p]
   rem,c=red(z,B256);assert rem==0
   H=[p for j,p in enumerate(S256) if c>>j&1]+P
   T=sorted(set(H)^set(p|1024 for p in S256))
   # f(x,t)=h(x)+t*g(x): h on BOTH slices, tg only on upper.
   T=sorted(set(H)^set(p|1024 for p in H)^set(p|1024 for p in S256))
   assert len(T)==272
   if nr==1:
    a=[0]*2048
    for p in T:a[p]=1
    anf=mobius(a);assert max(p.bit_count() for p,v in enumerate(anf) if v)<=4
   K=272-len(basis([veronese(11,5)[p] for p in T]));khist[K]+=1
   if len(local)<40 or K>=16:
    local.append({'d':d,'Q':Q,'K5':K,'support':T})
  counts[d]={'total':tot,'valid':nr}
  print(obj['type'],d,counts[d],dict(khist),'time',time.time()-t0,flush=True)
 out.append({'type':obj['type'],'counts':counts,'K5_hist':dict(khist)});seeds +=[dict(a,type=obj['type']) for a in local]
json.dump({'summary':out,'seeds':seeds},open('workspace/agent1_boundary272_relatives.json','w'))
pathlib.Path('workspace/agent1_boundary272_relatives.py').write_text(pathlib.Path(__file__).read_text());print('DONE',len(seeds))
