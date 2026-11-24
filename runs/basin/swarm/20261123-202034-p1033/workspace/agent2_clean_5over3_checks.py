import itertools,math,json,random,time
from pathlib import Path
start=time.time();h=2;n=2*h*h;t=h**3;r=n-h-1;ell=h*h-1;D=r+ell;k=t+D
G=[(b*2*h+a,b*2*h+h+c) for b in range(h) for a in range(h) for c in range(h)]
E=list(itertools.combinations(range(n),2));idx={e:i for i,e in enumerate(E)}
stars=[{idx[tuple(sorted((a,b)))] for b in range(n) if a!=b} for a in range(n)]
petals=[]
for i,(a,b) in enumerate(G):
 for center in (a,b):
  for pt in itertools.combinations(sorted(stars[center]-{idx[(a,b)]}),r):
   P=set(pt);O={c for c in range(n) if c!=center and idx[tuple(sorted((center,c)))] not in P}
   S={j for j,e in enumerate(G) if set(e)&O}-{i}
   assert len(O)==h and len(S)<=ell
   S.update(j for j in range(t) if j!=i and j not in S and len(S)<ell)
   assert len(S)==ell
   petals.append((i,center,sum(1<<p for p in P),tuple(sorted(S))))
for u,(i,a,P,S) in enumerate(petals):
 for j,c,Q,T in petals[:u]:
  if i!=j and not P&Q:assert j in S or i in T
bycolor=[[P for i,a,P,S in petals if i==j] for j in range(t)]
# Exactly all actual-point subsets potentially occurring in a cover of size<t.
cover_checked=0
for q in range(t):
 for C in itertools.combinations(range(len(E)),q):
  mask=sum(1<<x for x in C);deg=[0]*n
  for x in C:
   a,b=E[x];deg[a]+=1;deg[b]+=1
  covered=0
  for i,(a,b) in enumerate(G):
   formula=min(deg[a],deg[b])-int(bool(mask>>idx[(a,b)]&1))>=h
   actual=all(mask&P for P in bycolor[i])
   assert formula==actual
   covered+=actual
  assert covered<=q
  cover_checked+=1
# Enumerate EVERY member of the final uniform family for h=2.
m=len(E);cores=[tuple(range(m+i*t,m+(i+1)*t)) for i in range(t)]
coremasks=[sum(1<<x for x in X) for X in cores]
family=[];lookup={}
for i,a,P,S in petals:
 for choice in itertools.product(*(cores[j] for j in S)):
  F=coremasks[i]|P|sum(1<<x for x in choice)
  assert F.bit_count()==k and all((F&coremasks[j]).bit_count()==int(j in S) for j in range(t) if j!=i)
  family.append(F);lookup[(i,P,S,choice)]=F
rng=random.Random(21)
for _ in range(10000):
 q=rng.randrange(t);C=set(rng.sample(range(m+t*t),q));cm=sum(1<<x for x in C)
 actualC={x for x in C if x<m};A={i for i,X in enumerate(cores) if set(X)&C}
 found=None
 for i,a,P,S in petals:
  if i in A or P&cm:continue
  choices=tuple(next(x for x in cores[j] if x not in C) for j in S)
  found=lookup[i,P,S,choices];break
 assert found is not None and not found&cm
result={'h':h,'n':n,'t':t,'r':r,'target_count':ell,'uniform_deficit':D,'uniform_k':k,'actual_points':m,'petal_types':len(petals),'base_pairs_checked':math.comb(len(petals),2),'all_actual_cover_pointsets_size_lt_t':cover_checked,'final_members_enumerated':len(family),'random_full_covers_falsified':10000,'seconds':time.time()-start}
Path('workspace/agent2_clean_5over3_checks.json').write_text(json.dumps(result,indent=2))
Path('workspace/agent2_clean_5over3_checks.py').write_text(Path('scratchpad.py').read_text())
print(json.dumps(result,indent=2))
