from itertools import combinations,product
from pathlib import Path
import json,time,random

def tournament(t):
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
 return X,H,owner,n

def minimal_transversals(blocks):
 fam={0}
 for b in blocks:
  cand=set()
  for c in fam:
   if b&c:cand.add(c)
   else:
    q=b
    while q:
     p=q&-q;cand.add(c|p);q-=p
  fam=[]
  for c in sorted(cand,key=int.bit_count):
   if not any(f&c==f for f in fam):fam.append(c)
 return list(fam)

results=[];rng=random.Random(20)
for t in (3,4,5):
 st=time.time();X,H,owner,n=tournament(t)
 # Actual points: own copies 0..n-1, foreign copies n..2n-1.
 # (Tournament has no external points.)
 Q=[];R=[];Hm=[]
 for f,i in zip(H,owner):
  xx=sorted(X[i]);assert len(xx)>=2
  pet=f-X[i]
  Q.append(sum(1<<p for p in X[i]-{xx[0]})+sum(1<<(n+p) for p in pet))
  R.append(sum(1<<p for p in X[i]-{xx[1]})+sum(1<<(n+p) for p in pet))
  Hm.append(sum(1<<p for p in f))
 # Exact/random union checks.
 tests=[s for r in range(1,min(4,len(H))+1) for s in combinations(range(len(H)),r)]
 tests.extend(tuple(rng.sample(range(len(H)),rng.randint(1,len(H)))) for _ in range(2000))
 for ids in tests:
  U=0;W=0
  for j in ids:U|=Hm[j];W|=Q[j]
  assert U.bit_count()<=W.bit_count()+1
  # EVERY R edge has an own point outside any Q union.
  assert all(r&~W for r in R)
 A=[];B=[]
 for x in range(n):
  A.append(minimal_transversals([q for q,h in zip(Q,Hm) if h>>x&1]))
  B.append(minimal_transversals([r for r,h in zip(R,Hm) if not h>>x&1]))
 families=[a+[(1<<(2*n))|p for p in b] for a,b in zip(A,B)]
 assert all(all(c&q for q,h in zip(Q,Hm) if h>>x&1) for x,cl in enumerate(A) for c in cl)
 assert all(all(c&r for r,h in zip(R,Hm) if not h>>x&1) for x,cl in enumerate(B) for c in cl)
 data=dict(t=t,old_cores=[list(a) for a in X],old_edges=Hm,Q=Q,R=R,actual_ground=2*n+1,external_v=2*n,families=families,types=[['A']*len(a)+['B']*len(b) for a,b in zip(A,B)])
 Path('workspace/agent3_compressed_reverse_t%d.json'%t).write_text(json.dumps(data))
 # Full Hall and exact formula at t3, exhaustive all actual sets.
 hall=0
 if t==3:
  for c in range(1<<(2*n+1)):
   activated=sum(1<<x for x,cl in enumerate(families) if all(c&p for p in cl))
   assert activated.bit_count()<=c.bit_count();hall+=1
   S=[j for j,q in enumerate(Q) if q&c==q];TT=[j for j,r in enumerate(R) if r&c==r]
   U=0
   for j in S:U|=Hm[j]
   if c>>(2*n)&1:expected=U
   elif TT:
    inter=(1<<n)-1
    for j in TT:inter&=Hm[j]
    expected=U&~inter
   else:expected=0
   assert activated==expected
 results.append(dict(t=t,old_n=n,old_edges=len(H),new_edges=sum(map(len,families)),family_sizes=list(map(len,families)),max_A_rank=max(p.bit_count() for cl in A for p in cl),max_B_rank=max(1+p.bit_count() for cl in B for p in cl),union_subcollections_checked=len(tests),hall_point_sets_checked=hall,seconds=time.time()-st))
 print(results[-1],flush=True)
Path('workspace/agent3_compressed_reverse_checks.json').write_text(json.dumps(results,indent=2))
Path('workspace/agent3_compressed_reverse_checks.py').write_text(Path('scratchpad.py').read_text())
Path('workspace/agent3_compressed_reverse_proof.txt').write_text('''COMPRESSED PURE-HALL REVERSE GADGET; DOES NOT COMPLETE ORIGINAL INTERSECTION
Assume original intersecting family B partitioned by disjoint cores Xi, all |Xi|>=2, and strict-owner property: whenever cross-class F,G have disjoint EXTERNAL parts (outside union Xi), then F meets the other OWNER core or G meets the other OWNER core. Tournaments and duplicate-center star constructions have this property.
Create own copies p^own and foreign copies p^out for each old core point p, and a separate copy e_i of every old external point e for every source class i. Fix distinct ri,si in Xi. For F owned by i, let Q_F consist of own Xi except ri, global out copies of F's owned-core petal points, and source-i copies of its external petal points. Define R_F identically except omit si instead of ri. Both have size |F|-1.
UNION BOUND. For a nonempty edge collection, group by r used owner classes. Let A_i be union of external parts in class i, and let c be number of components of their intersection graph. External duplication credit delta=sum|A_i|-|union A_i|>=r-c. Across any two components all external parts are disjoint; strict-owner property therefore creates a core-owner visit in at least one direction. The component visit digraph is semicomplete, hence at most one component has indegree zero. If h_i counts distinct points of selected owner core Xi visited by foreign selected edges (including omitted ri), then sum h_i>=c-1. Exact counting of own/out copies yields |union Q_F|=|union F|-r+delta+sum h_i >= |union F|-1.
TWO-ANCHOR REPAIR. For ANY collection of Q-blocks, EVERY R_G has an OWN point outside its union: if G's owner j occurs in the Q collection, rj is omitted by every own-Qj block but is in own-Rj; if j does not occur, any own point in Rj is fresh. Residual foreign copies can never supply an own point.
For every old point x take A_x=blocker{Q_F:x in F}, and B_x={v} plus blocker{R_F:x notin F}; all blockers mean inclusion-minimal transversals, empty block family has blocker {empty}. A cover C with v activates the union U of Q-exhausted original edges; |U|<=|Qunion|+1<=|C|. Without v, if any color is activated then some R-block is exhausted, forcing an extra own point outside Qunion; hence |C|>=|Qunion|+1>=|U|, and activated colors are a subset of U. Thus full petal Hall holds. After avoiding v only A_x remain; minimal bad coalitions are exactly original edges, by the same union-bound proof as the original reverse gadget.
STAR RANK BOUND. In original n-center,m-copy construction with T=nm classes and core size c, each conditional Q/R-blocker contains at most one own-Qi point per class (<=T), at most all source-copied external actual points (<=T(n-1)), and at most ONE fully exhausted foreign core-choice pool per CENTER (<=nc). Target choices are independent. A partial choice pool cannot help cover all choices and is redundant in an inclusion-minimal transversal; conditioning on x only fixes or excludes ONE point and replaces at most one pool by a singleton or a c-1 pool. Once one pool at a center is exhausted, another at that center is redundant since every target includes choices from ALL m cores there. Hence reverse rank <=T+T(n-1)+nc+1=O(Tn)=O(original total deficit) for n~m^2.
DECISIVE OBSTRUCTION. This is only a Hall gadget. For every nonanchor original owned point x in Xi, A_x has the self petal {owncopy(x), foreigncopy(x)} after deleting unused members if necessary. It is inclusion-minimal: own copy hits all owner-i incident blocks, foreign copy hits all foreign-owner blocks containing x; each has a private block witness when needed. Distinct x yield pairwise disjoint self petals. There are about sum|Xi|~T^2 such colors, forcing any target-only original-intersection completion to pay Omega(T^2) targets per petal by the rainbow matching tournament count. Thus rank compression and two-anchor repair do NOT produce a phi upper construction. This branch is closed unless the A_x families themselves change.
''')
