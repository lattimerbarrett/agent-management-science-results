import itertools,time,json
from collections import Counter
start=time.time();targets={136,144,154,158};out={w:Counter() for w in targets};cases=0
triples=[sum(1<<i for i in I) for I in itertools.combinations(range(12),3)];ix3={m:i for i,m in enumerate(triples)}
sept=[sum(1<<i for i in I) for I in itertools.combinations(range(12),7)];ix7={m:i for i,m in enumerate(sept)}
def rank(rows):
 piv={}
 for v in rows:
  while v:
   j=v.bit_length()-1
   if j in piv:v^=piv[j]
   else:piv[j]=v;break
 return len(piv)
def span(bs):
 S={0}
 for v in bs:S|={q^v for q in S}
 return S
def norm(L):
 rows=list(L);piv=[];r=0
 for j in range(11,-1,-1):
  k=next((k for k in range(r,len(rows)) if rows[k]>>j&1),None)
  if k is None:continue
  rows[r],rows[k]=rows[k],rows[r]
  for k in range(len(rows)):
   if k!=r and rows[k]>>j&1:rows[k]^=rows[r]
  piv.append(j);r+=1
 ans=[]
 for j in range(12):
  if j not in piv:ans.append((1<<j)|sum(1<<p for p,row in zip(piv,rows) if row>>j&1))
 assert len(ans)==6
 return ans
def wedge(B):
 P={0}
 for v in B:
  N=set()
  for m in P:
   rest=v&~m
   while rest:
    bit=rest&-rest;rest-=bit;mm=m|bit
    if mm in N:N.remove(mm)
    else:N.add(mm)
  P=N
 return P
def flattenrank(P):
 rows=[0]*220
 for m in P:
  J=[i for i in range(12) if m>>i&1]
  for I in itertools.combinations(J,3):
   a=sum(1<<i for i in I);b=m^a;rows[ix3[a]]^=1<<ix3[b]
 return rank(rows)
def annihilator(P):
 rows=[]
 for j in range(12):
  row=0
  for m in P:
   if not(m>>j&1):row^=1<<ix7[m|1<<j]
  rows.append(row)
 return 12-rank(rows)
for t,a,b,c,d in itertools.product(range(8),repeat=5):
 x=7-t-a-b-d;y=7-t-a-c-d;z=7-t-b-c-d
 if min(x,y,z)<0:continue
 pos0=t+a+b+c+2*d+x+y+z
 if pos0>13:continue
 dims=[t,a,b,c,x,y,z];A=[];B=[];C=[];first=[];pos=0
 for k,Ls in zip(dims,[[A,B,C],[A,B],[A,C],[B,C],[A],[B],[C]]):
  first.append(1<<pos if k else 0)
  for _ in range(k):
   for L in Ls:L.append(1<<pos)
   pos+=1
 ef=1<<pos if d else 0;ff=1<<(pos+1) if d else 0;fs=1<<(pos+3) if d>=2 else 0
 for _ in range(d):A.append(1<<pos);B.append(1<<(pos+1));C.append(3<<pos);pos+=2
 assert pos==pos0 and len(A)==len(B)==len(C)==7
 ells=[]
 if t:ells.append(first[0])
 diag=[0]+([ef,ff,ef|ff] if d else[])+([ef|fs] if d>=2 else[])
 for ea,eb,ec in itertools.product([0,1],repeat=3):
  if(ea and not a)or(eb and not b)or(ec and not c):continue
  w=192-ea*(1<<(t+a))-eb*(1<<(t+b))-ec*(1<<(t+c))
  if w not in targets:continue
  for ex,ey,ez in itertools.product([0,1],repeat=3):
   if(ex and not x)or(ey and not y)or(ez and not z):continue
   base=sum(v*f for v,f in zip([ea,eb,ec,ex,ey,ez],first[1:]));ells.extend(base|dd for dd in diag)
 for ell in set(ells):
  if not ell:continue
  if any(not any((v&ell).bit_count()%2 for v in L) for L in[A,B,C]):continue
  p=(ell&-ell).bit_length()-1
  def drop(v):return(v&((1<<p)-1))|((v>>(p+1))<<p)
  top=set();S=set()
  for L in[A,B,C]:
   o=next(v for v in L if(v&ell).bit_count()%2)
   L0=[v^(o if(v&ell).bit_count()%2 else 0) for v in L if v!=o]
   LL=[drop(v) for v in L0];oo=drop(o)
   SS={v^oo for v in span(LL)};assert len(SS)==64;S^=SS
   top^=wedge(norm(LL))
  w=len(S)
  if w not in targets:continue
  affine=rank([v^(next(iter(S))) for v in S]);ann=annihilator(top);fr=flattenrank(top)
  if w in(136,144):assert affine<=11 and ann>0,(w,affine,ann)
  else:assert fr==52,(w,fr,(t,a,b,c,d,x,y,z),ell)
  out[w][(affine,ann,fr)]+=1;cases+=1
print('CASES',cases,'time',time.time()-start)
for w,D in sorted(out.items()):print(w,dict(D))
json.dump({str(w):{str(k):v for k,v in D.items()} for w,D in out.items()},open('workspace/agent2_c6_threeflat_invariants.json','w'),indent=2)
open('workspace/agent2_c6_threeflat_invariants.py','w').write(open(__file__).read())
