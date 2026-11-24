from itertools import combinations
from pathlib import Path
import json,time
res=[]
for n in range(3,7):
 st=time.time();allE=[(1<<i)|(1<<j) for i,j in combinations(range(n),2)];covers=[(1<<i)|(1<<j) for i,j in combinations(range(n),2)]
 checked=0;qualifying=0;disconnected=0
 for mask in range(1<<len(allE)):
  E=[e for j,e in enumerate(allE) if mask>>j&1];checked+=1
  if not E or any(all(c&e for e in E) for c in covers):continue
  qualifying+=1
  reached={0};todo=[0]
  while todo:
   i=todo.pop()
   for j,e in enumerate(E):
    if j not in reached and not E[i]&e:reached.add(j);todo.append(j)
  if len(reached)==len(E):continue
  disconnected+=1
  U=0
  for e in E:U|=e
  assert U.bit_count()==4 and len(E)==6
  assert set(E)=={(1<<i)|(1<<j) for i,j in combinations([v for v in range(n) if U>>v&1],2)}
 res.append(dict(n=n,graphs_checked=checked,tau_at_least3=qualifying,disconnected_Kneser_graphs=disconnected,expected_K4s=len(list(combinations(range(n),4))),seconds=time.time()-st))
 assert disconnected==len(list(combinations(range(n),4)))
print(json.dumps(res,indent=2))
Path('workspace/agent3_rank2_kneser_components_checks.json').write_text(json.dumps(res,indent=2))
Path('workspace/agent3_rank2_kneser_components_checks.py').write_text(Path('scratchpad.py').read_text())
Path('workspace/agent3_rank2_kneser_components_proof.txt').write_text('''GRAPH CLASSIFICATION FOR AGENT2 CAP-2 THEOREM
Let G be a finite simple graph with vertex-cover number at least 3. Its Kneser graph has the edges of G as vertices and joins disjoint G-edges. If this Kneser graph is disconnected, G is exactly K4 plus isolated vertices.
Proof. No Kneser vertex is isolated: an edge meeting every G-edge would have its two endpoints cover G. Choose a disjoint pair ab,cd in one component, and a disjoint pair C,D in another component (the latter exists because no component is a singleton). Both C,D must meet each of ab,cd, so they are opposite crossing pairs; relabel c,d if needed to get C=ac,D=bd. Every G-edge in the first component must intersect both ac and bd, so lies inside {a,b,c,d}. Every G-edge outside that component must intersect both ab and cd, so also lies inside {a,b,c,d}. Since a proper subgraph of K4 has a vertex cover of size at most two (take the endpoints complementary to a missing edge), G must be all K4. Its Kneser graph has exactly three components, the opposite-edge pairs.
Actual code enumerates every labeled graph on n=3,4,5,6 vertices and verifies the classification; isolated ambient vertices are allowed.
USE IN NO-EMPTY-ACTUAL-PATTERN CASE. Actual size-2 patterns carry no targets, hence Kneser-adjacent edges have the same owner. If KG connected, all size-2 actual patterns have one owner h. Any foreign pattern must target h, since its rank<=2 actual part cannot cover G; no-empty assumption forces it to be actual singleton plus this target. Cross-foreign intersections force all these singleton points equal, so one actual point plus an h-core representative covers the whole family, forcing t<=2.
If G=K4 and uses s>=2 distinct owners (s<=3), a foreign owner not among these cannot have any pattern: an actual 2-set/no-target cannot cover K4; an actual singleton/one-target leaves at least one entire opposite-edge component untargeted, and a singleton cannot hit those two disjoint edges. Thus t<=3. If s=1, use the preceding one-owner argument. Therefore when t>=4 and no actual-empty patterns, the actual size-2 graph must have a cover U of at most two points.
The one-owner implication NEEDS the no-empty-actual-pattern assumption; otherwise three pure-target cyclic classes can be adjoined and still give t=4,d=2.
''')
