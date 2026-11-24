import json,itertools,time
open('workspace/a1_cyclic_sparse_check.py','w').write(open(__file__).read())
D=json.load(open('workspace/a1_cyclic_matrix.json'));L=D['L'];H=D['H'];rows=D['rows'];wt={int(j):w for j,w in D['weights'].items()};fixed=[j for j,w in wt.items() if w==1];order=L+H;oi={j:i for i,j in enumerate(order)}
P=[];cases=[]
for goal,fixedones in [(322,[]),(326,fixed),(330,[fixed[0]])]:
 piv={};rhs={}
 for row in rows:
  rr=sum(1<<oi[j] for j in order if row>>j&1);v=sum((row>>j)&1 for j in fixedones)%2
  while rr:
   p=(rr&-rr).bit_length()-1
   if p in piv:rr ^=piv[p];v ^=rhs[p]
   else:piv[p]=rr;rhs[p]=v;break
  if not rr:assert v==0
 hp=sorted(p for p in piv if p>=len(L));hs=sum(rhs[p]<<i for i,p in enumerate(hp))
 if not P:P=[piv[p]>>len(L) for p in hp]
 cases.append((goal,fixedones,piv,rhs,hs))
 print('case',goal,'Hrhs',hs,flush=True)
cols=[sum(((r>>j)&1)<<i for i,r in enumerate(P)) for j in range(len(H))]
free=[i for i in range(len(L)) if i not in cases[0][2]];print('free',free,flush=True)
found={};seen=set();cnt=0
# check only highpattern's 8 uniquely possible lowcompletions
# each case has fixeddegree constraints with differing RHS

def check(hpos,hs):
 global cnt
 mask=sum(1<<i for i in hpos)
 key=(mask,hs)
 if key in seen:return
 seen.add(key);cnt+=1
 for goal,ff,piv,rhs,target in cases:
  if hs!=target or goal in found:continue
  for f in range(1<<len(free)):
   x=mask<<len(L)
   for j,i in enumerate(free):
    if f>>j&1:x |=1<<i
   for p in sorted((p for p in piv if p<len(L)),reverse=True):
    if (piv[p]&x).bit_count()%2 !=rhs[p]:x |=1<<p
   W=49*len(hpos)+7*(x&((1<<len(L))-1)).bit_count()+len(ff)
   if W==goal:
    supportorbs=ff+[j for i,j in enumerate(order) if x>>i&1]
    found[goal]=supportorbs
    print('FOUND',goal,'Hweight',len(hpos),'candidates',cnt,flush=True)
    json.dump(found,open('workspace/a1_cyclic_orbit_seeds.json','w'))

pair={}
for a,b in itertools.combinations(range(len(H)),2):
 s=cols[a]^cols[b]
 pair.setdefault(s,[]).append((a,b))
for s,ps in pair.items():
 for case in cases:
  hs=case[-1]
  if s^hs in pair:
   for a in ps:
    for b in pair[s^hs]:check(set(a)^set(b),hs)
print('pairs done candidates',cnt,'syndromes',len(pair),flush=True)
triples={};start=time.time()
for a in range(len(H)):
 for b in range(a+1,len(H)):
  ss=cols[a]^cols[b]
  for c in range(b+1,len(H)):
   s=ss^cols[c];pack=a|(b<<9)|(c<<18)
   for case in cases:
    hs=case[-1]
    if s^hs in pair:
     for p in pair[s^hs]:check({a,b,c}^set(p),hs)
    prev=triples.get(s^hs)
    if prev is not None:
     for q in (prev if isinstance(prev,list) else [prev]):
      check({a,b,c}^{q&511,(q>>9)&511,q>>18},hs)
   prev=triples.get(s)
   if prev is None:triples[s]=pack
   elif isinstance(prev,list):prev.append(pack)
   else:triples[s]=[prev,pack]
 if a%20==0:print('a',a,'dict',len(triples),'cand',cnt,'time',time.time()-start,flush=True)
 if len(found)==3:break
print('done',list(found),'candidates',cnt,'time',time.time()-start)
