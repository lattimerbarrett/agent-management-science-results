import itertools,json,pathlib,time,sys,collections
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese,closure

def span(B):
 z=[0]
 for b in B:z +=[x^b for x in z]
 return z

def spaces(n,d):
 for piv in itertools.combinations(range(n),d):
  non=[j for j in range(n) if j not in piv];free=[(i,j) for i,p in enumerate(piv) for j in non if j>p]
  for z in range(1<<len(free)):
   B=[1<<p for p in piv]
   for h,(i,j) in enumerate(free):
    if z>>h&1:B[i]^=1<<j
   yield B,span(B)

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

def q(x):return ((x>>0&1)&(x>>1&1))^((x>>2&1)&(x>>3&1))^((x>>4&1)&(x>>5&1))
vs=veronese(9,5);T=[p for p in range(512) if q(p)];BT=basis([vs[p] for p in T]);V10=veronese(10,5)
start=time.time();seeds=[];stats=[]
for typ,U,EB,ABS in [('active',[0,1],[4,8,16,32,64,128,256],[[4,16,64],[4,64,128],[64,128,256]]),('radical',[0,64],[1,2,4,8,16,32,128,256],[[1,4,16],[1,4,128],[1,128,256]])]:
 E=span(EB);R={};C={}
 for p in E:
  vv=0
  for u in U:vv^=vs[p^u]
  R[p],C[p]=red(vv,BT)
 for k,AB in enumerate(ABS):
  A=span(AB);AA=set(A);sig=0
  for a in A[1:]:sig^=R[a]
  total=0;singular=0;disjoint=0;valid=0;khist=collections.Counter();clhist=collections.Counter();sample=[]
  for BB,B in spaces(len(EB),3):
   total+=1;B=[E[p] for p in B]
   if any(q(p) for p in B):continue
   singular+=1
   if len(AA.intersection(B))!=1:continue
   disjoint+=1;ss=0
   for b in B[1:]:ss^=R[b]
   if ss!=sig:continue
   valid+=1;P=[p^u for p in A[1:]+B[1:] for u in U];assert len(set(P))==28
   z=0
   for p in P:z^=vs[p]
   rem,c=red(z,BT);assert not rem
   H=[p for ii,p in enumerate(T) if c>>ii&1]+P
   S=sorted(set(H)^set(p|512 for p in H)^set(p|512 for p in T));assert len(S)==280
   K=280-len(basis([V10[p] for p in S]));khist[K]+=1
   X,r=closure(S,V10);clhist[len(X)]+=1
   if len(sample)<10 or X:sample.append({'Utype':typ,'Aorbit':k,'P':P,'support':S,'K5':K,'cl5extra':len(X)})
  stat={'Utype':typ,'Aorbit':k,'total':total,'singular':singular,'disjoint':disjoint,'valid':valid,'K5_hist':dict(khist),'cl5extra_hist':dict(clhist)};stats.append(stat);seeds+=sample
  print(stat,'time',time.time()-start,flush=True)
json.dump({'stats':stats,'seeds':seeds},open('workspace/agent1_T280_q224_P28.json','w'));pathlib.Path('workspace/agent1_T280_q224_P28.py').write_text(pathlib.Path(__file__).read_text())
