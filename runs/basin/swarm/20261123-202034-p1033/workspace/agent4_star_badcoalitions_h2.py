import itertools,z3,time,json
start=time.time();h=2;n=2*h*h
G=[]
for block in range(h):
 L=list(range(2*h*block,2*h*block+h));R=list(range(2*h*block+h,2*h*(block+1)))
 G += [(a,b) for a in L for b in R]
actual=list(itertools.combinations(range(n),2));eid={e:j for j,e in enumerate(actual)};t=len(G)
families=[]
for a,b in G:
 fam=[]
 for c,other in [(a,b),(b,a)]:
  star=[eid[tuple(sorted((c,x)))] for x in range(n) if x not in (c,other)]
  fam += [tuple(P) for P in itertools.combinations(star,n-h-1)]
 families.append(fam)
res=[]
for vpair in [(0,2),(0,1),(0,4)]:
 v=eid[vpair];pruned=[[P for P in fam if v not in P] for fam in families]
 vs=[z3.Bool('x%d'%i) for i in range(len(actual)+t)];bad=[]
 for mask in range(1,1<<t):
  I=[i for i in range(t) if mask>>i&1]
  s=z3.Solver()
  s.add(z3.PbLe([(x,1) for x in vs],len(I)-1))
  for i in I:
   for P in pruned[i]:s.add(z3.Or(vs[len(actual)+i],*[vs[p] for p in P]))
  if s.check()==z3.sat:bad.append(mask)
 minimal=[b for b in bad if not any(c!=b and c&b==c for c in bad)]
 assert all(a&b for a in minimal for b in minimal)
 hits=[]
 for k in range(t+1):
  hits=[T for T in itertools.combinations(range(t),k) if all(any(b>>i&1 for i in T) for b in minimal)]
  if hits:break
 item=dict(point=vpair,bad_count=len(bad),minimal_bad=[[i for i in range(t) if b>>i&1] for b in minimal],lambda_v=k,min_hitting_sets=hits)
 res.append(item);print(item,flush=True)
with open('workspace/agent4_star_badcoalitions_h2.json','w') as f:json.dump({'owners':G,'results':res},f,indent=2)
with open('workspace/agent4_star_badcoalitions_h2.py','w') as f:f.write(open(__file__).read())
print('elapsed',time.time()-start)
