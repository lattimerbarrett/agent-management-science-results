import itertools,json
n=14;FULL=(1<<14)-1;A=127;B=A<<7
def rot(x):return ((x<<1)&FULL&~128)|((x>>6)&1)|((x>>6)&128)
inds={k:{sum(1<<i for i in C):j for j,C in enumerate(itertools.combinations(range(n),k))} for k in [1,2,3,4,5,6]}
def rankcat(terms,k):
 rows={}
 for t in terms:
  on=[i for i in range(n) if t>>i&1]
  for C in itertools.combinations(on,k):
   s=sum(1<<i for i in C);rows[s]=rows.get(s,0)^(1<<inds[7-k][t^s])
 basis={}
 for v in rows.values():
  while v:
   p=v.bit_length()-1
   if p not in basis:basis[p]=v;break
   v^=basis[p]
 return len(basis)
for k in range(1,7):
 c=(1<<k)-1|(((1<<(7-k))-1)<<7)
 rr=[rankcat([A,B,c],j) for j in [1,2,3]]
 print('single',k,rr,2*(1+sum(rr)))
for k in range(1,4):
 groups=[list(range(k)),list(range(k,7)),list(range(7,14-k)),list(range(14-k,14))]
 c=sum(1<<i for i in groups[0]+groups[2])
 for counts in itertools.product(*(range(len(g)+1) for g in groups)):
  if sum(counts)!=7:continue
  d=sum(1<<v for g,z in zip(groups,counts) for v in g[:z])
  tt={A,B,c,d}
  if len(tt)!=4:continue
  rr=[rankcat(tt,j) for j in [1,2,3]]
  if 2*(1+sum(rr))==310:
   print('FOUND4APOLAR310',sorted(tt));json.dump(sorted(tt),open('workspace/agent3_apolar310.json','w'));quit()
seen=set();freq={}
for C in itertools.combinations(range(n),7):
 mask=sum(1<<i for i in C)
 if mask in seen:continue
 orb=[];m=mask
 for _ in range(7):seen.add(m);orb.append(m);m=rot(m)
 terms=set(orb)^{A,B}
 r1,r2,r3=[rankcat(terms,k) for k in [1,2,3]]
 d=2*(1+r1+r2+r3);freq[d]=freq.get(d,0)+1
 if d==310:
  print('FOUNDAPOLAR310',sorted(terms));json.dump(sorted(terms),open('workspace/agent3_apolar310.json','w'));quit()
print('freq',freq)