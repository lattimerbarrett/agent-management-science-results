import itertools,json,pathlib,time,sys,collections
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese,closure

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
 while v:
  k=v.bit_length()-1
  if k not in B:
   rem^=1<<k;v^=1<<k;continue
  v^=B[k][0];c^=B[k][1]
 return rem,c

def rank4(a,b,c,d):
 return len(set([0,a,b,a^b,c,a^c,b^c,a^b^c,d,a^d,b^d,a^b^d,c^d,a^c^d,b^c^d,a^b^c^d]))==16

def q(x):return ((x>>0&1)&(x>>1&1))^((x>>2&1)&(x>>3&1))^((x>>4&1)&(x>>5&1))
vs=veronese(9,5);T=[p for p in range(512) if q(p)];BT=basis([vs[p] for p in T]);V10=veronese(10,5)
start=time.time();seeds=[];stats=[]
for j,(UB,EB) in enumerate([([1,4],[16,32,64,128,256]),([1,64],[4,8,16,32,128,256]),([64,128],[1,2,4,8,16,32,256])]):
 U=span(UB);E=span(EB);Z=[x for x in E if q(x)==0];ZZ=set(Z);nz=Z[1:];R={};C={}
 for p in Z:
  vv=0
  for u in U:vv^=vs[p^u]
  R[p],C[p]=red(vv,BT)
 total=0;indep=0;valid=0;unique={};khist=collections.Counter();sample=[]
 for a,b,c,d in itertools.combinations(nz,4):
  total+=1;s=a^b^c^d
  if s not in ZZ or not rank4(a,b,c,d):continue
  indep+=1
  if R[0]^R[a]^R[b]^R[c]^R[d]^R[s]:continue
  Q=tuple(sorted([0,a,b,c,d,s]));valid+=1
  if Q in unique:continue
  unique[Q]=True
  P=[p^u for p in Q for u in U];comb=0
  for p in Q:comb^=C[p]
  H=[p for ii,p in enumerate(T) if comb>>ii&1]+P
  S=sorted(set(H)^set(p|512 for p in H)^set(p|512 for p in T));assert len(S)==272
  if True:
   K=272-len(basis([V10[p] for p in S]));khist[K]+=1
   X,r=closure(S,veronese(10,3));assert not X
   assert K==11
   if len(sample)<20:sample.append({'j':j,'Q':Q,'P':P,'support':S,'K5':K})
 stats.append({'j':j,'qzero':len(Z),'quadruples':total,'independent_with_sum_zero':indep,'valid_multiplicity':valid,'unique_valid_caps':len(unique),'sample_K5':dict(khist)})
 print(stats[-1],time.time()-start,flush=True);seeds+=sample
json.dump({'stats':stats,'seeds':seeds},open('workspace/agent1_T272_q224_P24.json','w'));pathlib.Path('workspace/agent1_T272_q224_P24.py').write_text(pathlib.Path(__file__).read_text())
