import itertools,json,pathlib,time,sys,collections
sys.path.insert(0,'workspace');from agent3_graph_lifts import veronese,kernel

def span(B):
 z=[0]
 for b in B:z +=[x^b for x in z]
 return z

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
 c=0;rem=0
 for k in sorted(B,reverse=True):
  if v>>k&1:v^=B[k][0];c^=B[k][1]
 return v,c

def rank4(a,b,c,d):return len(set(span([a,b,c,d])))==16

def q(x):return sum((x>>(2*j)&1)*(x>>(2*j+1)&1) for j in range(4))&1
v=veronese(9,5);T=[p for p in range(512) if q(p)];BT=basis([v[p] for p in T]);assert len(T)==240 and 240-len(BT)==10
v3=veronese(10,3);v5=veronese(10,5);v6=veronese(10,6)
res=[];stats=[];hist=collections.Counter();start=time.time()
for j,(UB,EB) in enumerate([([1,4],[16,32,64,128,256]),([1,256],[4,8,16,32,64,128])]):
 U=span(UB);E=span(EB);Z=[x for x in E if not q(x)];ZZ=set(Z);nz=Z[1:];R={};C={}
 for p in Z:
  z=0
  for u in U:z^=v[p^u]
  R[p],C[p]=red(z,BT)
 seen=set();total=indep=valid=0
 for a,b,c,d in itertools.combinations(nz,4):
  total+=1;s=a^b^c^d
  if s not in ZZ or not rank4(a,b,c,d):continue
  indep+=1
  if R[0]^R[a]^R[b]^R[c]^R[d]^R[s]:continue
  valid+=1;Q=tuple(sorted([0,a,b,c,d,s]))
  if Q in seen:continue
  seen.add(Q);P=[p^u for p in Q for u in U];comb=0
  for p in Q:comb^=C[p]
  H=set(P)|{p for i,p in enumerate(T) if comb>>i&1}
  F=sorted(H|{x^512 for x in set(T)^H});assert len(F)==288
  sy=0
  for p in F:sy^=v6[p]
  assert sy==0
  K3=kernel(F,v3);K5=kernel(F,v5);odd=sum((a&b).bit_count()%2 for a in K3 for b in K5)
  hist[(len(K3),len(K5),bool(odd))]+=1
  res.append({'j':j,'Q':Q,'P':P,'support':F,'K3':len(K3),'K5':len(K5),'odd':odd})
 st={'j':j,'qzero':len(Z),'quadruples':total,'independent':indep,'valid_with_multiplicity':valid,'unique_caps':len(seen)};stats.append(st);print(st,flush=True)
print('TOTAL',len(res),'HIST',hist,'seconds',time.time()-start)
pathlib.Path('workspace/agent3_T288_cubic10_k24.json').write_text(json.dumps({'stats':stats,'histogram':{str(k):v for k,v in hist.items()},'results':res},indent=2))
pathlib.Path('workspace/agent3_T288_cubic10_k24.py').write_text(pathlib.Path(__file__).read_text())
