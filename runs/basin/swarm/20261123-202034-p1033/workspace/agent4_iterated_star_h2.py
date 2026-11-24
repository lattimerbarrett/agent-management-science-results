import itertools,z3,time,json
start=time.time();h=2;n=8
G=[]
for block in range(h):
 L=list(range(4*block,4*block+2));R=list(range(4*block+2,4*block+4));G += [(a,b) for a in L for b in R]
actual=list(itertools.combinations(range(n),2));eid={e:j for j,e in enumerate(actual)};t=len(G)
families=[]
for a,b in G:
 fam=[]
 for c,other in [(a,b),(b,a)]:
  star=[eid[tuple(sorted((c,x)))] for x in range(n) if x not in (c,other)]
  fam += [tuple(P) for P in itertools.combinations(star,5)]
 families.append(fam)
def analyze(deleted,colors):
 pruned={i:[P for P in families[i] if not set(P)&deleted] for i in colors}
 vs=[z3.Bool('x%d'%i) for i in range(36)];bad=[]
 for mask in range(1,1<<len(colors)):
  I=[colors[j] for j in range(len(colors)) if mask>>j&1]
  s=z3.Solver();s.add(z3.PbLe([(x,1) for x in vs],len(I)-1))
  for i in I:
   for P in pruned[i]:s.add(z3.Or(vs[28+i],*[vs[p] for p in P]))
  if s.check()==z3.sat:bad.append(mask)
 minimal=[b for b in bad if not any(c!=b and c&b==c for c in bad)]
 for k in range(len(colors)+1):
  hits=[T for T in itertools.combinations(range(len(colors)),k) if all(any(b>>i&1 for i in T) for b in minimal)]
  if hits:break
 return dict(deleted=[actual[v] for v in sorted(deleted)],colors=colors,minimal_bad=[[colors[i] for i in range(len(colors)) if b>>i&1] for b in minimal],lambda_v=k,min_hitting_sets=[[colors[i] for i in T] for T in hits])
results=[]
for vpair in [(0,1),(0,4)]:
 v=eid[vpair]
 for discard in [0,4]:
  colors=[i for i in range(8) if i!=discard]
  base=analyze({v},colors);assert base['lambda_v']==0
  for w in range(28):
   if w==v:continue
   item=analyze({v,w},colors);item['first_discard']=discard;results.append(item)
   if item['lambda_v']>1:print(item,flush=True)
print('max lambda',max(x['lambda_v'] for x in results),'runtime',time.time()-start)
with open('workspace/agent4_iterated_star_h2.json','w') as f:json.dump(results,f,indent=2)
with open('workspace/agent4_iterated_star_h2.py','w') as f:f.write(open(__file__).read())
