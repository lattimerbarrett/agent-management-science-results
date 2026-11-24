import itertools,time
n=13;N=1<<n;F=N-1

def span(vs):
 s={0}
 for v in vs:s|={x^v for x in s}
 return s

def rankbasis(rows):
 P={}
 for v in rows:
  while v:
   p=v.bit_length()-1
   if p in P:v^=P[p]
   else:P[p]=v;break
 return P

def footprint(Union):
 mons=sorted(range(N),key=lambda x:(x.bit_count(),x));ix={x:i for i,x in enumerate(mons)}
 rows=[]
 for x in Union:
  a=F^x;free=F^a;t=free;v=0
  while True:
   v^=1<<ix[a|t]
   if not t:break
   t=(t-1)&free
  rows.append(v)
 P=rankbasis(rows);assert len(P)==len(Union)
 nonstandard={mons[p] for p in P}
 D=set(range(N))-nonstandard
 assert all((m|(1<<i)) in nonstandard for m in nonstandard for i in range(n))
 best=N
 for s in D:
  if s.bit_count()>7:continue
  free=F^s;t=free;c=0
  while True:
   c+=int((s|t) in D)
   if not t:break
   t=(t-1)&free
  best=min(best,c)
 return best

def shortpuncture(Union,gset,flats):
 Union=sorted(Union);ix={x:i for i,x in enumerate(Union)}
 rows=[]
 for m in range(N):
  if m.bit_count()<=5: rows.append(sum(1<<i for i,x in enumerate(Union) if x&m==m))
 P=rankbasis(rows);free=[i for i in range(len(Union)) if i not in P];null=[]
 for j in free:
  v=1<<j
  for p in sorted(P):
   if (P[p]&v).bit_count()%2:v^=1<<p
  assert all((r&v).bit_count()%2==0 for r in rows)
  null.append(v)
 # Every shortened word is a sum of affine functions localized on the
 # three flats. Their complete localized space has dimension24, exactly
 # the computed shortened dimension; verify containment by dual moments.
 local=[]
 for B in flats:
  local.append(sum(1<<i for i,x in enumerate(Union) if x in B))
  for j in range(n):local.append(sum(1<<i for i,x in enumerate(Union) if x in B and x>>j&1))
 assert len(null)==24 and len(rankbasis(local))==24
 assert all((a&b).bit_count()%2==0 for a in local for b in rows)
 outidx=[ix[x] for x in Union if x not in gset]
 Q=rankbasis(sum(((v>>i)&1)<<j for j,i in enumerate(outidx)) for v in null)
 print('short dimension',len(null),'puncture length',len(outidx),'rank',len(Q),flush=True)
 assert len(Q)<=25
 vals=set();v=0;prev=0;basis=list(Q.values())
 for i in range(1<<len(basis)):
  gray=i^(i>>1)
  if i:v^=basis[(gray^prev).bit_length()-1]
  prev=gray;vals.add(v.bit_count())
 return sorted(vals)

U=span([1<<i for i in range(7)])
V=span([1<<i for i in [0,1,2,3,4,7,8]])
W=span([1<<i for i in [5,7,9,10,11,12]]+[(1<<6)^(1<<8)])
Waff={x^(1<<6) for x in span([1<<i for i in [5,7,8,9,10,11,12]])}
W312=span([1<<i for i in [5,6,7,9,10,11,12]])
Wcycle={x^(1<<6) for x in W}
for name,X in [('g312',W312),('g312cycle',Wcycle),('g316linear',W),('g316affine',Waff)]:
 Union=U|V|X;g=U^V^X
 print(name,'weight',len(g),'pairs',[len(U&V),len(U&X),len(V&X),len(U&V&X)],'union',len(Union),flush=True)
 bound=footprint(Union)
 assert bound==15
 vals=shortpuncture(Union,g,[U,V,X])
 for target in [322,326,330,334]:
  p=(target-len(g))//2
  assert p<bound and p not in vals,(name,target,p)
 print('footprint',bound,'weights',vals,flush=True)

