import itertools,json,pathlib,time,collections,sys
sys.path.insert(0,'workspace')
from agent3_graph_lifts import veronese
vs=veronese(8,2)
raw=json.loads(pathlib.Path('workspace/agent4_boundary256_orbits.json').read_text())
def span(B):
 z=[0]
 for b in B:z += [v^b for v in z]
 return z
flats=[]
for piv in itertools.combinations(range(7),3):
 non=[j for j in range(7) if j not in piv]
 free=[(i,j) for i,p in enumerate(piv) for j in non if j>p]
 for z in range(1<<len(free)):
  B=[1<<p for p in piv]
  for h,(i,j) in enumerate(free):
   if (z>>h)&1:B[i]^=1<<j
  H=span(B)
  for off in span([1<<j for j in non]):
   K=[x^off for x in H]
   flats.append(frozenset(K+[x^128 for x in K]))
assert len(flats)==188976 and len(set(flats))==188976
out=[];kept=[];t0=time.time()
for obj in raw:
 if not obj['solvable']:continue
 S={(p&63)|((p>>9)<<6) for p in obj['support']};assert len(S)==32
 hist=collections.Counter();n=0;best=0
 for H in flats:
  if len(S&H)!=5:continue
  n+=1;T=S^H;basis={}
  for p in T:
   z=vs[p]
   while z:
    i=z.bit_length()-1
    if i in basis:z^=basis[i]
    else:basis[i]=z;break
  k=38-len(basis);hist[k]+=1
  if k>best:
   best=k
   if k>=13:kept.append({'type':obj['type'],'K':k,'support':sorted(T)})
 out.append({'type':obj['type'],'flats':len(flats),'T38_count':n,'K_histogram':dict(hist),'bestK':best})
 print(out[-1],flush=True)
print('elapsed',time.time()-t0)
pathlib.Path('workspace/agent3_newboundary_T38.json').write_text(json.dumps({'results':out,'seeds':kept},indent=2))
pathlib.Path('workspace/agent3_newboundary_T38.py').write_text(pathlib.Path(__file__).read_text())
