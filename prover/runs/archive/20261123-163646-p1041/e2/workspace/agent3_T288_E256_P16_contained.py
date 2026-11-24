import json,pathlib,sys,collections,itertools,time
sys.path.insert(0,'workspace');from agent3_graph_lifts import veronese,kernel
raw=json.loads(pathlib.Path('workspace/agent3_T280_P12_allorbits.json').read_text())['base_orbits']
v5=veronese(10,5);u5=veronese(11,5);u4=veronese(11,4);u6=veronese(11,6)
allres=[];hist=collections.Counter();bad=[];start=time.time()
for obj in raw:
 B=obj['base'];E=obj['extra'];S=sorted(x+(r<<7) for x in B for r in range(8));D={}
 for j,p in enumerate(S):
  z=v5[p];c=1<<j
  while z:
   h=z.bit_length()-1
   if h in D:z^=D[h][0];c^=D[h][1]
   else:D[h]=(z,c);break
 A4=[];basis=obj['relative_codes']['3']['basis'];z=0
 for i in range(1<<len(basis)):
  if i:z^=basis[(i&-i).bit_length()-1]
  if z.bit_count()==4:A4.append([E[j] for j in range(16) if z>>j&1])
 assert len(A4)==8
 ps=[]
 for p,q in itertools.combinations(E,2):ps.append(sorted([p+(r<<7) for r in range(8)]+[q+(r<<7) for r in range(8)]))
 for A in A4:
  for norm in range(1,8):
   for bs in range(16):ps.append(sorted(p+(r<<7) for j,p in enumerate(A) for r in range(8) if ((norm&r).bit_count()&1)==(bs>>j&1)))
 assert len(ps)==1016 and len({tuple(p) for p in ps})==1016
 for P in ps:
  z=0
  for p in P:z^=v5[p]
  c=0
  while z:
   h=z.bit_length()-1;assert h in D
   z^=D[h][0];c^=D[h][1]
  H=set(P)|{S[j] for j in range(256) if c>>j&1}
  F=sorted(H|{x^1024 for x in set(S)^H});assert len(F)==288
  syn=0
  for p in F:syn^=u6[p]
  assert syn==0
  K5=kernel(F,u5);K4=kernel(F,u4);odd=sum((a&b).bit_count()%2 for a in K4 for b in K5)
  AA={}
  for p in F:
   z=p^F[0]
   while z:
    h=z.bit_length()-1
    if h in AA:z^=AA[h]
    else:AA[h]=z;break
  hist[(len(AA),len(K5),len(K4),bool(odd))]+=1
  rr={'type':obj['type'],'P':P,'affrank':len(AA),'K5':len(K5),'K4':len(K4),'odd':odd}
  if odd:bad.append(dict(rr,support=F))
  allres.append(rr)
 print(obj['type'],'done',len(allres),'secs',time.time()-start,flush=True)
print('HIST',hist,'bad',len(bad))
pathlib.Path('workspace/agent3_T288_E256_P16_contained.json').write_text(json.dumps({'histogram':{str(k):v for k,v in hist.items()},'results':allres,'badseeds':bad},indent=2))
pathlib.Path('workspace/agent3_T288_E256_P16_contained.py').write_text(pathlib.Path(__file__).read_text())
