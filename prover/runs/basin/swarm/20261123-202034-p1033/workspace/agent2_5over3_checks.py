import itertools,json,math,random
from pathlib import Path

def build(h):
 n=h*(h+1);V=range(n)
 G=[(a,b) for block in range(h) for a,b in itertools.combinations(range(block*(h+1),(block+1)*(h+1)),2)]
 E=list(itertools.combinations(V,2));idx={e:j for j,e in enumerate(E)}
 stars=[set(idx[tuple(sorted((a,b)))] for b in V if b!=a) for a in V]
 petals=[]
 for i,(a,b) in enumerate(G):
  own=idx[(a,b)]
  for center in (a,b):
   for ps in itertools.combinations(sorted(stars[center]-{own}),n-h-1):
    P=set(ps);O={c for c in V if c!=center and idx[tuple(sorted((center,c)))] not in P}
    S={j for j,e in enumerate(G) if set(e)&O}-{i}
    assert len(O)==h and len(S)<=h*h-1
    petals.append((i,center,P,S,sum(1<<x for x in P)))
 for u,p in enumerate(petals):
  for q in petals[:u]:
   i,a,P,S,pm=p;j,b,Q,T,qm=q
   if i!=j and not(pm&qm):assert j in S or i in T
 return n,G,E,idx,petals
results=[]
for h in (2,3):
 n,G,E,idx,ps=build(h);t=len(G);m=len(E)
 bycolor=[[p[4] for p in ps if p[0]==i] for i in range(t)]
 rng=random.Random(7)
 masks=range(1<<m) if h==2 else [sum(1<<v for v in rng.sample(range(m),rng.randrange(m+1))) for _ in range(10000)]
 checked=0
 for C in masks:
  degree=[0]*n
  for bit,(a,b) in enumerate(E):
   if C>>bit&1:degree[a]+=1;degree[b]+=1
  cover=[]
  for i,(a,b) in enumerate(G):
   actual=all(C&p for p in bycolor[i]);formula=min(degree[a],degree[b])>=h+int(bool(C>>idx[(a,b)]&1))
   assert actual==formula
   if actual:cover.append(i)
  assert len(cover)<=C.bit_count()
  checked+=1
 results.append({'h':h,'n':n,'colors_t':t,'actual_points':m,'petal_types':len(ps),'petal_pairs_checked':len(ps)*(len(ps)-1)//2,'cover_pointsets_checked':checked,'all_cover_pointsets':h==2,'max_deficit_bound':n-h-1+h*h-1,'objective_bound':t*(n-h-1+h*h-1)})
Path('workspace/agent2_5over3_checks.json').write_text(json.dumps(results,indent=2))
Path('workspace/agent2_5over3_checks.py').write_text(Path('scratchpad.py').read_text())
print(json.dumps(results,indent=2))
