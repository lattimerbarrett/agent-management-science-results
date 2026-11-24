import itertools,json,pathlib,time,sys,collections
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese,closure

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
 while v:
  k=v.bit_length()-1
  if k not in B:rem^=1<<k;v^=1<<k;continue
  v^=B[k][0];c^=B[k][1]
 return rem,c

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

def Pcases(E0,quads):
 for a,b in itertools.combinations(E0,2):yield [(x|(r<<7)) for x in [a,b] for r in range(8)],('pair',a,b)
 for Q in quads:
  for n in range(1,8):
   for off in range(16):
    yield [x|(r<<7) for j,x in enumerate(Q) for r in range(8) if ((r&n).bit_count()%2)==((off>>j)&1)],('four',Q,n,off)

raw=json.load(open('workspace/agent4_boundary256_orbits.json'));stats=[];seeds=[];start=time.time();v7=veronese(7,3);v10=veronese(10,5);v114=veronese(11,4);v115=veronese(11,5)
for obj in raw:
 if not obj['solvable']:continue
 S=sorted({(p&63)|((p>>3)&64) for p in obj['support']});X,r=closure(set(S),veronese(7,2));E0=sorted(p for p,c in X);assert len(E0)==16
 B=basis([v7[p] for p in S]);Q4=[]
 for Q in itertools.combinations(E0,4):
  z=0
  for p in Q:z^=v7[p]
  if not red(z,B)[0]:Q4.append(Q)
 assert len(Q4)==8
 T=sorted(p|(r<<7) for p in S for r in range(8));BT=basis([v10[p] for p in T]);hist=collections.Counter();cnt=0
 for P,desc in Pcases(E0,Q4):
  assert len(P)==16;vv=0
  for p in P:vv^=v10[p]
  rem,c=red(vv,BT);assert not rem
  H=[p for ii,p in enumerate(T) if c>>ii&1]+P
  W=sorted(set(H)^set(p|1024 for p in H)^set(p|1024 for p in T));assert len(W)==288
  K4=kernel(W,v114);K5=kernel(W,v115);nz=sum((a&b).bit_count()%2 for a in K4 for b in K5)
  ext,r=closure(set(W),v114);hist[(len(K4),len(K5),bool(nz),len(ext))]+=1
  if cnt<3 or nz or ext:seeds.append({'type':obj['type'],'desc':desc,'support':W,'K4':len(K4),'K5':len(K5),'cross_nonzero':nz,'cl4extra':len(ext)})
  cnt+=1
 assert cnt==1016
 st={'type':obj['type'],'cases':cnt,'hist':{str(k):v for k,v in hist.items()}};stats.append(st);print(st,'time',time.time()-start,flush=True)
json.dump({'stats':stats,'seeds':seeds},open('workspace/agent1_T288_E256_P16.json','w'));pathlib.Path('workspace/agent1_T288_E256_P16.py').write_text(pathlib.Path(__file__).read_text())
