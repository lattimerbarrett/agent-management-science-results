from itertools import combinations,product
from fractions import Fraction
from pathlib import Path
import json
n=4
pairs=list(combinations(range(n),2));actual={p:4+j for j,p in enumerate(pairs)}
stars=[set(actual[e] for e in pairs if i in e) for i in range(n)]
patterns=[];full=[]
for i in range(n):
 cl=[]
 for j in range(n):
  if j!=i:
   a=stars[i]-{actual[tuple(sorted((i,j)))]};cl.append((a,{j},False));full.append({i,j}|a)
 cl.append((stars[i],set(),True));full.append({i}|stars[i]);patterns.append(cl)
assert len({frozenset(e) for e in full})==16
assert all(len(e)==4 for e in full)
assert all(e&f for j,e in enumerate(full) for f in full[:j])
assert all(not all(set(c)&e for e in full) for c in combinations(range(10),3))
assert all(a&b for cl in patterns for a,_,_ in cl for b,_,_ in cl)
byR={};witness={}
for choices in product(range(4),repeat=4):
 chosen=[patterns[i][choices[i]] for i in range(4)]
 R=sum(seed for a,t,seed in chosen)
 Q=sum(not(a&b) for j,(a,t,s) in enumerate(chosen) for b,u,v in chosen[:j])
 if Q>byR.get(R,-1):byR[R]=Q;witness[R]=choices
# All exact positive-alpha breakpoints of possible upper-envelope lines.
points={Fraction(0)}
for r,s in combinations(byR,2):
 a=Fraction(byR[r]-byR[s],s-r)
 if a>=0:points.add(a)
points=sorted(points);checks=[]
for a in points+[points[-1]+1]:
 vals={r:Fraction(q)+a*r for r,q in byR.items()};best=max(vals.values());opt=[r for r,v in vals.items() if v==best]
 checks.append(dict(alpha=str(a),optimal_seed_counts=opt,objective=str(best)))
result=dict(t=4,k=4,n_ground=10,members=16,intersection_pairs=120,three_covers_tested=120,within_color_pairs_all_intersect=True,pure_profiles_checked=4**4,Q_max_by_seed_count=byR,exact_envelope_checks=checks)
print(json.dumps(result,indent=2))
Path('workspace/agent3_seed_bonus_pure_check.json').write_text(json.dumps(result,indent=2))
Path('workspace/agent3_seed_bonus_pure_check.py').write_text(Path('scratchpad.py').read_text())
Path('workspace/agent3_seed_bonus_pure_proof.txt').write_text('''LIMITATION OF LINEAR ACTUAL-SEED BONUS FOR THE QP ROOT METHOD
Consider duplicate-center upper construction n>4m-1. All actual base petals at center a are (n-2m)-subsets of its (n-1)-point star. Any two intersect in at least n-4m+1>0 actual points. The rank-t seed actual petal is the FULL star and hence intersects every old actual petal in its class. Thus the actual Kneser adjacency block WITHIN EVERY COLOR is identically zero, including seed/old pairs.
Consequently Q(mu)+alpha*seedmass(mu) is multilinear on the product of color probability simplices: fixing all other colors, it is linear in the probabilities of the remaining color. A maximizer exists at a product of vertices, by successively replacing each color distribution by a pure best response without lowering the objective. This holds for EVERY alpha>=0 (indeed every real alpha). Hence one can choose an ALL-PURE global optimizer throughout the entire homotopy. The positive within-color support-difference space can be zero at every parameter. Hessian/ADE arguments alone therefore do not bypass the pure-color obstruction merely by replacing common dummies with linear-bonus actual rank-t seeds.
This does not refute the usefulness of endpoint mincover duality, nor a further boundary/combinatorial argument. It only shows that nontrivial mixed norm-2 roots are NOT forced by the proposed homotopy, even in the construction believed asymptotically extremal for the 5/3 bound.
An exact n=4,m=1 instance is checked in the Python: core singleton i for i=0,1,2,3; six actual points are K4 edges. Class i has three old patterns star(i) minus ij, targeting core j, plus the target-free full-star seed. All 16 full members have rank4, every pair intersects, every three-point cover fails. Every within-color actual petal pair intersects. ALL4^4 pure profiles are enumerated, and exact rational envelope of Q+alpha*seedcount is recorded.
''')
