from itertools import product,combinations
from fractions import Fraction as Q
from pathlib import Path
import json
M=Q(1,9);T=6
vertices=['A1','A2','A3','B1','B2','B3','C1','C2','C3']
disjoint_global={frozenset(['A'+str(i),'C'+str(i)]) for i in range(1,4)}|{frozenset(['B1','B2']),frozenset(['B2','B3'])}
sets={v:{('private',v)} for v in vertices}
for u,v in combinations(vertices,2):
 if frozenset([u,v]) not in disjoint_global:
  p=('pair',u,v);sets[u].add(p);sets[v].add(p)
for u,v in combinations(vertices,2):assert bool(sets[u]&sets[v])==(frozenset([u,v]) not in disjoint_global)
print('actual set rank',max(map(len,sets.values())),'all 36 pair relations checked')
rows=[];global_points=set()
for bits in product([0,1],repeat=3): # 0=A 1=B
 names=[('B' if bits[i] else 'A')+str(i+1) for i in range(3)]+['C1','C2','C3']
 disjoint={frozenset(['A'+str(i),'C'+str(i)]) for i in range(1,4)}|{frozenset(['B1','B2']),frozenset(['B2','B3'])}
 edges=[(i,j) for i,j in combinations(range(T),2) if frozenset([names[i],names[j]]) in disjoint]
 def val(w):
  R=sum(w);return sum(w[i]*w[j] for i,j in edges)+M*R*(T-R)
 best=Q(-1);points=set()
 for free in range(T):
  fixed=[i for i in range(T) if i!=free]
  for b in product([0,1],repeat=5):
   w=[Q(0)]*T
   for i,x in zip(fixed,b):w[i]=Q(x)
   R=sum(w);degree=sum(w[j if i==free else i] for i,j in edges if free in (i,j))
   u=(degree+M*(T-2*R))/(2*M)
   for x in [Q(0),Q(1),max(Q(0),min(Q(1),u))]:
    w[free]=x;v=val(w)
    if v>best:best=v;points={tuple(w)}
    elif v==best:points.add(tuple(w))
 if best==3:
  for w in points:global_points.add((bits,w))
 rows.append(dict(choice=bits,edges=edges,maximum=str(best),maximizers=[[str(x) for x in w] for w in sorted(points)]))
 assert best<=3
assert len(global_points)==2
assert ((0,0,0),tuple(map(Q,[1]*6))) in global_points
assert ((1,1,1),tuple(map(Q,[1,1,1,0,0,0]))) in global_points
out=dict(M=str(M),global_maximum=3,rows=rows)
Path('workspace/agent3_common_profile_alignment_counter.json').write_text(json.dumps(out,indent=2))
Path('workspace/agent3_common_profile_alignment_counter.py').write_text(Path('scratchpad.py').read_text())
for r in rows:print(r['choice'],r['maximum'],r['maximizers'])
proof='''COMMON-PROFILE ALIGNMENT COUNTEREXAMPLE (without balanced Hall).\nSix colors. Colors i=1,2,3 have two actual choices A_i,B_i; colors 4,5,6 have C_1,C_2,C_3. Every color also has a common dummy. Only actual-disjoint pairs are A_i,C_i (i=1,2,3), B_1,B_2, and B_2,B_3. In particular choices within one color intersect. Objective is Qactual + (1/9)R(6-R).\nThis is realizable by finite nonempty actual sets: put one new point in both vertex-sets for every NONEDGE of this nine-vertex disjointness graph; optionally add a private point in each set. Thus actual intersections are exactly prescribed.\nFor fixed real mass in each color, objective is multilinear in the A/B choice distributions. Its maximum is therefore achieved by choosing A or B purely in each of the first three colors. Fix such a choice, leaving six real masses w_i in [0,1]. At any global maximizer, two fractional coordinates joined by an actual-disjointness edge cannot coexist: the 2x2 Hessian of Q has diagonal -2M and offdiagonal 1-2M, hence positive eigenvalue 1-4M>0. Fractional coordinates are consequently independent in the disjointness graph. Conditional on all other coordinates, their objective is linear minus M times the square of their sum. At an interior stationary maximum their linear coefficients are equal, so mass can be redistributed at fixed sum until at most one coordinate is fractional, preserving value. Hence some maximum lies on a cube edge. The exact Fraction computation checks all 8 choice profiles, every cube edge, its two endpoints, and its stationary point.\nResults: all-A has maximum 3, uniquely all six real masses 1; all-B has maximum 3, uniquely masses (1,1,1,0,0,0). Every other choice profile has maximum at most 26/9<3. These are the ONLY global maximizers: any further fractional-coordinate maximum redistributes at fixed sum to an edge optimum, which must be one of the listed two and is already an extreme cube point; any mixed A/B choice expands multilinearly into choice profiles and would put positive mass on a strictly-suboptimal profile.\nThus the two global optima have real totals 6 and 3 and common real colors 1,2,3, but their actual choices are respectively ALL A and ALL B. No common-profile alignment is possible. This does not satisfy balanced Hall (actual sets may have rank much larger than 6), so does not refute an alignment lemma requiring Hall and t much larger than rank. It does refute alignment as a formal consequence of QP optimality/common-real-color overlap alone.\n'''
Path('workspace/agent3_common_profile_alignment_counter.txt').write_text(proof)