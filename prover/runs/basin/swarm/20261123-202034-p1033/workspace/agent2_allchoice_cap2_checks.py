from itertools import combinations,product
from pathlib import Path
import json,time
start=time.time()
rows=[]
for n in range(1,7):
    E=list(combinations(range(n),2));checked=0;high=0;k4=0
    for mask in range(1<<len(E)):
        edges=[set(E[j]) for j in range(len(E)) if mask>>j&1]
        if not edges:continue
        tau=next(r for r in range(n+1) if any(all(set(C)&e for e in edges) for C in combinations(range(n),r)))
        checked+=1
        if tau<3:continue
        high+=1
        seen={0};front=[0]
        while front:
            i=front.pop()
            for j,e in enumerate(edges):
                if j not in seen and not edges[i]&e:seen.add(j);front.append(j)
        if len(seen)!=len(edges):
            V=set().union(*edges)
            assert len(V)==4 and len(edges)==6
            assert {frozenset(e) for e in edges}=={frozenset(e) for e in combinations(V,2)}
            k4+=1
    rows.append(dict(vertices=n,nonempty_graphs_checked=checked,vertex_cover_at_least_3=high,disconnected_edge_disjointness_cases=k4))
# Exhaust all cap-one pattern families on three owners and three actual values.
t=3;actual=3;types=[]
for i in range(t):types.append([(None,j) for j in range(t) if j!=i]+[(x,None) for x in range(actual)])
valid=0;intersecting=0;configs=0
for masks in product(range(1,1<<(actual+t-1)),repeat=t):
    fam=[[p for j,p in enumerate(types[i]) if masks[i]>>j&1] for i in range(t)]
    configs+=1
    if not all((x is not None and x==y) or a==j or b==i for i in range(t) for j in range(i) for x,a in fam[i] for y,b in fam[j]):continue
    intersecting+=1
    # Expand cores of size two; actual ground follows the six core points.
    X=[{2*i,2*i+1} for i in range(t)];H=[]
    for i in range(t):
        for x,j in fam[i]:
            if x is None:H.extend([X[i]|{z} for z in X[j]])
            else:H.append(X[i]|{6+x})
    if any(all(set(C)&F for F in H) for C in combinations(range(6+actual),2)):continue
    valid+=1
    assert all(x is None and j is not None for ff in fam for x,j in ff)
    assert all(len(ff)==1 for ff in fam)
assert valid==2
# Sharp t=5 cap-two regular tournament: explicit full members and all 4-covers.
t=5;X=[set(range(3*i,3*i+3)) for i in range(t)];H=[]
for i in range(t):
    out=[(i+1)%t,(i+2)%t]
    H.extend([X[i]|set(P) for P in product(*(X[j] for j in out))])
assert len(H)==45 and all(len(F)==5 for F in H)
assert all(F&G for F,G in combinations(H,2))
covers4=0
for C in combinations(range(15),4):
    covers4+=1;assert not all(set(C)&F for F in H)
assert all(set(C)&F for C in product(*(sorted(x) for x in X)) for F in H)
result=dict(graph_lemma=rows,cap_one_three_class_all_pattern_configurations=configs,
            intersecting_cap_one_configurations=intersecting,cover_number_three_configurations=valid,
            sharp_cap_two_example=dict(classes=5,members=45,member_pairs=990,all_four_covers_tested=covers4,all_canonical_covers=3**5),
            runtime=time.time()-start)
print(json.dumps(result,indent=2))
Path('workspace/agent2_allchoice_cap2_checks.json').write_text(json.dumps(result,indent=2))
