from itertools import combinations,product
from pathlib import Path
import json,time,random

def example(t):
 out=[[] for _ in range(t)]
 for i,j in combinations(range(t),2):
  n=t if t%2 else t+1
  a,b=(i,j) if (j-i)%n<=n//2 else (j,i);out[a].append(b)
 ind=[sum(i in out[j] for j in range(t)) for i in range(t)]
 X=[];n=0
 for v in ind:X.append(set(range(n,n+v+1)));n+=v+1
 H=[];owner=[]
 for i in range(t):
  for p in product(*(X[j] for j in out[i])):H.append(X[i]|set(p));owner.append(i)
 Qcore=[];N=0
 for x in X:Qcore.append(set(range(N,N+len(x)-1)));N+=len(x)-1
 copies={};Q=[]
 for f,i in zip(H,owner):
  q=set(Qcore[i])
  for p in f-X[i]:
   if (i,p) not in copies:copies[i,p]=N;N+=1
   q.add(copies[i,p])
  assert len(q)==t-1;Q.append(q)
 return X,H,owner,Q,N,n

def union_intersection(H,ids):
 fs=[H[i] for i in ids]
 U=set().union(*fs);J=set(fs[0])
 for f in fs:J&=f
 return U,J

rows=[];rng=random.Random(17)
for t,upto in ((3,6),(4,4),(5,3)):
 X,H,owner,Q,N,n=example(t);cnt=0
 inds=list(range(len(H)))
 tests=[s for r in range(1,upto+1) for s in combinations(inds,r)]
 tests.extend(tuple(rng.sample(inds,rng.randint(1,len(H)))) for _ in range(1000))
 for ids in tests:
  U,J=union_intersection(H,ids);W=set().union(*(Q[i] for i in ids))
  assert len(U)<=len(W)+1
  assert len(U-J)<=len(W)
  cnt+=1
 rows.append(dict(t=t,edges=len(H),factor_ground=N,disjoint_block_ground=len(H)*(t-1),subcollections_checked=cnt))
# Full reverse-gadget verification at t=3, including ALL point sets and bad coalitions.
X,H,owner,Q,N,n=example(3)
qm=[sum(1<<p for p in q) for q in Q];hm=[sum(1<<p for p in f) for f in H]

def blockers(ids):
 q=[qm[i] for i in ids];answer=[]
 for c in range(1<<N):
  if all(c&a for a in q) and all(not all((c^(1<<p))&a for a in q) for p in range(N) if c>>p&1):answer.append(c)
 return answer

families=[]
for x in range(n):
 A=blockers([i for i,f in enumerate(H) if x in f]);B=blockers([i for i,f in enumerate(H) if x not in f])
 families.append(set(A)|{(1<<N)|b for b in B})
allI=(1<<n)-1;bad=[False]*(1<<n)
for c in range(1<<(N+1)):
 activated=sum(1<<x for x in range(n) if all(c&p for p in families[x]))
 assert activated.bit_count()<=c.bit_count()
 # Exact activation formula based on exhausted Q blocks.
 ids=[i for i,q in enumerate(qm) if q&c==q]
 if ids:
  U,J=union_intersection(H,ids);expected=U if c>>N&1 else U-J
 else:expected=set()
 assert activated==sum(1<<x for x in expected)
 # After avoiding v, only type-A petals remain. C needs no v.
 if not c>>N&1:
  act=sum(1<<x for x in range(n) if all(c&p for p in families[x] if not p>>N&1))
  for I in range(1<<n):
   if (act&I).bit_count()>c.bit_count():bad[I]=True
for I in range(1<<n):assert bad[I]==any(f&I==f for f in hm)
rows.append(dict(case='full_reverse_t3',new_colors=n,ground=N+1,max_petal_rank=max(p.bit_count() for fam in families for p in fam),family_sizes=list(map(len,families)),point_sets_checked=1<<(N+1),coalitions_checked=1<<n,minimal_bad_coalitions=[I for I in range(1<<n) if bad[I] and all(not bad[I^(1<<x)] for x in range(n) if I>>x&1)],expected_inner_edges=hm))
print(json.dumps(rows,indent=2))
Path('workspace/agent3_factored_reverse_checks.json').write_text(json.dumps(rows,indent=2))
Path('workspace/agent3_factored_reverse_checks.py').write_text(Path('scratchpad.py').read_text())
Path('workspace/agent3_factored_reverse_proof.txt').write_text('''FACTORED REVERSE BAD-COALITION GADGET
Start with intersecting k-uniform B partitioned into classes B_i with disjoint nonempty cores X_i. For each i create Q_i of size |X_i|-1, plus a private-to-i COPY of every point occurring in its petals; points are shared across petal occurrences WITHIN class, but never across classes. For F in class i put Q_F=Q_i union copy_i(F\\X_i). Thus |Q_F|=k-1.
For any nonempty collection S of inner edges, group by used owners i. Let U_i=X_i union all their petals. Then |union Q_F|=sum_i(|U_i|-1). The sets U_i are pairwise intersecting, so delta=sum|U_i|-|union U_i|>=m-1. Hence |union F|<=|union Q_F|+1. Moreover |union F \\ intersection F|<=|union Q_F|: if delta>=m the claim is immediate; if delta=m-1, equality in connected union counting forces every U_i to share one point p and have otherwise mutually disjoint parts. For m>=2 each cross-owner F,Fprime can intersect only at p, so every F contains p; for m=1 every F contains X_i nonempty. Thus intersection F is nonempty in the only case union F might exceed union Q_F by one.
The equality characterization follows by adding U_i in any order: each new set overlaps the previous union at least one point, and equality in total overlap forces that overlap to have size exactly one; pairwise intersection then forces the same point for all earlier sets. Inductively all U_i have common p and disjoint remainders.
Now for each original point x introduce a new color (and an eventual private core point), with petals: (A) ALL inclusion-minimal transversals of {Q_F:x in F}; (B) {v} union ALL inclusion-minimal transversals of {Q_F:x notin F}. Empty subfamily has blocker {empty set}. A point set C covers blocker(K) iff it CONTAINS some edge of K (blocker involution). Therefore if S is the set of Q_F exhausted by C, its activated colors are union(S-original F) when v in C, and union F minus intersection F when v notin C. The inequalities above show number activated<=|C|, i.e. the full petal Hall condition.
After avoiding v only type A remains. A coalition I is bad iff it contains some original F: forward, if I contains no F, any exhausted collection leaves at least one point of union F outside I, so activated colors inside I <=|union F|-1<=|union Q_F|<=|C|. Conversely if F subset I, C=Q_F activates at least k points at cost k-1. Thus minimal bad coalitions are exactly B. Rank is at most 1+sum over owners i of the largest inclusion-minimal transversal size of the relevant conditional petal subfamily, or the shared Q_i singleton option. This can be far smaller than number of inner edges, but no O(original total deficit) bound has been proved.
This gadget only establishes petal Hall, not the ORIGINAL full-family intersection condition.
''')
