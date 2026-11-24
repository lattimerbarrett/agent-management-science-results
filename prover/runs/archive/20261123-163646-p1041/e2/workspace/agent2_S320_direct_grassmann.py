import itertools,random,time,json,pathlib,collections
rng=random.Random(202603);N=320;ONE=(1<<N)-1

def insert(B,v):
 while v:
  j=v.bit_length()-1
  if j in B:v^=B[j]
  else:B[j]=v;return v
 return 0

def prodrows(R,d):
 out=[ONE]
 for k in range(1,min(d,len(R))+1):
  for I in itertools.combinations(range(len(R)),k):
   p=ONE
   for i in I:p&=R[i]
   out.append(p)
 return out

def solve(eqs):
 B={}
 for v,b in eqs:
  while v:
   j=v.bit_length()-1
   if j in B:v^=B[j][0];b^=B[j][1]
   else:B[j]=(v,b);break
  if not v and b:return None
 piv=sorted(B);free=[j for j in range(N) if j not in B]
 def finish(x,inh):
  for j in piv:
   if ((B[j][0]&x).bit_count()&1) ^ (B[j][1] if inh else 0):x^=1<<j
  return x
 return finish(0,True),[finish(1<<j,False) for j in free]

def ran(K):
 z=0
 for x in K:
  if rng.getrandbits(1):z^=x
 return z

def pts(R):
 return [sum((r>>i&1)<<j for j,r in enumerate(R)) for i in range(N)]

def groups(R):
 D=collections.defaultdict(list)
 for i,p in enumerate(pts(R)):D[p].append(i)
 return list(D.values())

def periods(S):
 SS=set(S);a=S[0];out=[]
 for p in S[1:]:
  v=a^p
  if all(x^v in SS for x in S):out.append(v)
 return out
U=[0]
for j in [0,2,4,5,9,10,11]:U +=[x^(1<<j) for x in U]
S=sorted(set(U)|{x for x in range(512) if ((x&1)*(x>>1&1))^((x>>2&1)*(x>>3&1))});assert len(S)==N
R=[sum(1<<i for i,p in enumerate(S) if p>>j&1) for j in range(12)];assert all(p.bit_count()%2==0 for p in prodrows(R,6));start=time.time();mut=acc=0;hist=collections.Counter();khist=collections.Counter();hits=[];minK=999
while time.time()-start<120:
 mut+=1
 # Randomize basis of the same old rowspace, keeping the all-one row explicit.
 RR=R[:]
 for _ in range(30):
  i,j=rng.sample(range(12),2);RR[i]^=RR[j]
 rng.shuffle(RR);base=RR[:10];old1,old2=RR[10:];sol=solve((p,0) for p in prodrows(base,5));assert sol is not None;K=sol[1];hist[len(K)]+=1
 if len(K)<12:raise RuntimeError('lostoldspace')
 BB={}
 for x in [ONE]+base:insert(BB,x)
 candidate=None
 for tries in range(8):
  a=ran(K)
  if not insert(dict(BB),a):continue
  gg=groups(base+[a])
  if any(len(g)>2 for g in gg):continue
  eq=[(p,0) for p in prodrows(base+[a],5)]+[((1<<g[0])|(1<<g[1]),1) for g in gg if len(g)==2];so=solve(eq)
  if so is None:continue
  b=so[0]^ran(so[1]);BBB=dict(BB);insert(BBB,a)
  if not insert(BBB,b):continue
  candidate=base+[a,b];break
 if candidate is None:continue
 R=candidate;acc+=1;assert len(set(pts(R)))==320
 if acc%10:continue
 PK=solve((p,0) for p in prodrows(R,5))[1];khist[len(PK)]+=1
 if len(PK)>=15:
  odd=sum((a&b).bit_count()%2 for i,a in enumerate(PK) for b in PK[i+1:])
  if odd:
   S=pts(R);assert all(p.bit_count()%2==0 for p in prodrows(R,6));hit={'support':S,'K5':PK,'mixed_odd':odd,'periods':periods(S)};hits.append(hit);print('MAINGRAMHIT',len(PK),odd,'periods',len(hit['periods']),flush=True);break
 if acc%100==0:print('progress',mut,acc,'K5',khist,'sec',time.time()-start,flush=True)
print('DONE',mut,acc,'firstkernels',hist,'fullK5',khist,'hits',len(hits),'sec',time.time()-start)
json.dump({'mutations':mut,'accepted':acc,'firstKernelDims':dict(hist),'fullK5dims':dict(khist),'hits':hits},open('workspace/agent2_S320_direct_grassmann.json','w'));pathlib.Path('workspace/agent2_S320_direct_grassmann.py').write_text(pathlib.Path(__file__).read_text())
