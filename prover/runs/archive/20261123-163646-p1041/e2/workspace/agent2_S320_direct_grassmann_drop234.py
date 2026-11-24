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
seen=set();profiles=collections.Counter();examples=[]
def canon(R):
 B={}
 for r in [ONE]+R:insert(B,r)
 for j in sorted(B):
  for k in sorted(B):
   if k>j and B[k]>>j&1:B[k]^=B[j]
 return tuple(B[k] for k in sorted(B))
while time.time()-start<120:
 mut+=1;RR=R[:]
 for _ in range(40):
  i,j=rng.sample(range(12),2);RR[i]^=RR[j]
 rng.shuffle(RR);drop=rng.choice([2,3,4]);base=RR[:-drop];candidate=base[:];valid=True
 for stage in range(drop):
  last=stage==drop-1;eq=[(p,0) for p in prodrows(candidate,5)]
  if last:
   gg=groups(candidate)
   if any(len(g)>2 for g in gg):valid=False;break
   eq += [((1<<g[0])|(1<<g[1]),1) for g in gg if len(g)==2]
  sol=solve(eq)
  if sol is None:valid=False;break
  row=None;BB={}
  for x in [ONE]+candidate:insert(BB,x)
  for tries in range(12):
   a=sol[0]^ran(sol[1])
   if not insert(dict(BB),a):continue
   if not last and any(len(g)>(1<<(drop-stage-1)) for g in groups(candidate+[a])):continue
   row=a;break
  if row is None:valid=False;break
  candidate.append(row)
 if not valid:continue
 key=canon(candidate)
 if key in seen:continue
 seen.add(key)
 PK=solve((p,0) for p in prodrows(candidate,5))[1];khist[len(PK)]+=1
 if len(PK)<15:continue
 R=candidate;acc+=1;S=pts(R);assert len(set(S))==320
 odd=sum((a&b).bit_count()%2 for i,a in enumerate(PK) for b in PK[i+1:])
 if odd:
  assert all(p.bit_count()%2==0 for p in prodrows(R,6));hits.append({'support':S,'K5':PK,'odd':odd});print('HIT',len(PK),odd,flush=True);break
 if acc%10==0:
  k6=len(solve((p,0) for p in prodrows(R,6))[1]);per=periods(S);prof=(len(PK),k6,len(per));profiles[prof]+=1
  if profiles[prof]==1:examples.append({'support':S,'K5':len(PK),'K6':k6,'periods':per});print('NEWPROFILE',prof,'mut',mut,'accepted',acc,flush=True)
print('DONE',mut,acc,'uniquerowspaces',len(seen),'fullK5',khist,'profiles',profiles,'hits',len(hits),'sec',time.time()-start)
json.dump({'mutations':mut,'accepted':acc,'unique':len(seen),'fullK5dims':dict(khist),'profiles':{str(k):v for k,v in profiles.items()},'examples':examples,'hits':hits},open('workspace/agent2_S320_direct_grassmann_drop234.json','w'))
