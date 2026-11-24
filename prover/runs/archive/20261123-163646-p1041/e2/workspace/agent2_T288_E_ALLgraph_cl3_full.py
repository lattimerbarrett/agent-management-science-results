import json,sys,pathlib,collections,time,itertools
sys.path.insert(0,'workspace');from agent3_lift_closure import veronese,closure

def kernel(S,vs):
 B={};out=[]
 for i,p in enumerate(S):
  v=vs[p];c=1<<i
  while v:
   k=v.bit_length()-1
   if k not in B:B[k]=(v,c);break
   v^=B[k][0];c^=B[k][1]
  if not v:out.append(c)
 return out

def insert(B,v):
 while v:
  k=v.bit_length()-1
  if k in B:v^=B[k]
  else:B[k]=v;return v
 return 0
d3=veronese(11,3);d5=veronese(11,5);uu3=veronese(12,3);uu5=veronese(12,5);hist=collections.Counter();lhist=collections.Counter();hits=[];t=time.time();count=0
def process(S,typ):
 global count
 count+=1
 K3=kernel(S,d3);K5=kernel(S,d5);ext,rk=closure(set(S),d3);odd=sum((a&b).bit_count()%2 for a in K3 for b in K5);hist[typ,len(K3),len(K5),len(ext),bool(odd)]+=1
 if ext or odd:hits.append({'seed':count,'support':S,'extra':[p for p,c in ext],'odd':odd})
 if len(K5)>12:
  B={}
  for j in range(-1,11):insert(B,sum(1<<i for i,p in enumerate(S) if j==-1 or p>>j&1))
  X=[]
  for x in K5:
   z=insert(B,x)
   if z:X.append(z)
  assert len(X)==1
  U=[p|(((X[0]>>i)&1)<<11) for i,p in enumerate(S)];KU=kernel(U,uu5);ue,rk=closure(set(U),uu3);lhist[len(KU),len(ue)]+=1
  if ue:hits.append({'lift_of':count,'support':U,'extra':[p for p,c in ue]})
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
  process(F,obj['type'])
print('count',count,'hist',hist,'lhist',lhist,'hits',len(hits),'sec',time.time()-t)
json.dump({'count':count,'hist':{str(k):v for k,v in hist.items()},'lhist':{str(k):v for k,v in lhist.items()},'hits':hits},open('workspace/agent2_T288_E_ALLgraph_cl3.json','w'));None
