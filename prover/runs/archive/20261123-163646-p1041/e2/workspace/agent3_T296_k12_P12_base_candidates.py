import json,pathlib,itertools,collections,time,sys
sys.path.insert(0,'workspace');from agent3_graph_lifts import veronese
B=json.loads(pathlib.Path('workspace/agent3_T288_mid_P8_bases.json').read_text())['bases'][0]['base'];BS=set(B);start=time.time()
vv=veronese(8,3);D={}
for p in B:
 z=vv[p]
 while z:
  h=z.bit_length()-1
  if h in D:z^=D[h]
  else:D[h]=z;break
R={}
for p in range(256):
 if p in BS:continue
 z=vv[p]
 for h in sorted(D,reverse=True):
  if z>>h&1:z^=D[h]
 assert z
 R[p]=z
rev={}
for p,z in R.items():rev.setdefault(z,[]).append(p)
tri=set()
for p,q in itertools.combinations(R,2):
 for r in rev.get(R[p]^R[q],[]):
  if p<q<r:tri.add((p,q,r))
print('triples',len(tri),flush=True)
P6=[];total=0;hist=collections.Counter()
for piv in itertools.combinations(range(8),5):
 non=[j for j in range(8) if j not in piv];free=[(i,j) for i,p in enumerate(piv) for j in non if j>p]
 for z in range(1<<len(free)):
  dirs=[1<<p for p in piv]
  for h,(i,j) in enumerate(free):
   if z>>h&1:dirs[i]^=1<<j
  H=[0]
  for b in dirs:H += [x^b for x in H]
  offs=[0]
  for j in non:offs += [x^(1<<j) for x in offs]
  for off in offs:
   F=[x^off for x in H];n=sum(p in BS for p in F);total+=1
   if n>=24:hist[n]+=1
   if n==26:P6.append(sorted(p for p in F if p not in BS))
print('5flats',total,'highhist',hist,'P6',len(P6),'secs',time.time()-start)
assert total==777240
pathlib.Path('workspace/agent3_T296_k12_P12_base_candidates.json').write_text(json.dumps({'base':B,'triples':sorted(tri),'P6':P6,'flat_count':total,'flat_intersection_high_hist':dict(hist)},indent=2))
pathlib.Path('workspace/agent3_T296_k12_P12_base_candidates.py').write_text(pathlib.Path(__file__).read_text())
