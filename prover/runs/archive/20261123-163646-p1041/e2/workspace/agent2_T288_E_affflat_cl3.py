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
raw=json.load(open('workspace/agent3_T280_P12_allorbits.json'))['base_orbits'];cases=json.load(open('workspace/agent3_T288_E256_P16_affflats.json'))['results'];vv=veronese(10,5);v6=veronese(11,6)
for obj in raw:
 S=sorted(x+(r<<7) for x in obj['base'] for r in range(8));BB={}
 for j,p in enumerate(S):
  z=vv[p];c=1<<j
  while z:
   h=z.bit_length()-1
   if h in BB:z^=BB[h][0];c^=BB[h][1]
   else:BB[h]=(z,c);break
 for case in cases:
  if case['type']!=obj['type']:continue
  P=[x+(u<<7) for x in case['Q'] for u in range(1<<(4-case['d']))]
  z=0
  for p in P:z^=vv[p]
  c=0
  while z:
   h=z.bit_length()-1;assert h in BB;z^=BB[h][0];c^=BB[h][1]
  H=set(P)|{p for i,p in enumerate(S) if c>>i&1};F=sorted(H|{p|1024 for p in set(S)^H});assert len(F)==288
  syn=0
  for p in F:syn^=v6[p]
  assert syn==0
  process(F,obj['type'])
print('count',count,'hist',hist,'lhist',lhist,'hits',len(hits),'sec',time.time()-t)
json.dump({'count':count,'hist':{str(k):v for k,v in hist.items()},'lhist':{str(k):v for k,v in lhist.items()},'hits':hits},open('workspace/agent2_T288_E_affflat_cl3.json','w'))
