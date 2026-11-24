from pathlib import Path
import itertools,json,math,networkx as nx
W=[310,322,326,330,334]
low=[0,128,192,224,240,248,252,254,256,272]
span={192:9,224:10,240:11,248:12,252:13,254:14,256:11,272:11}
R={}
for w in W:
    deg4=[t for t in low if w-128<=t<=w-128+8]
    assert not deg4
    cand=[]
    for t in low:
        if (t-w+128)%2:continue
        I=(t-w+128)//2
        if I<0 or not any(abs(I-r)<=3 for r in [0,1,2,4,8,16,32]):continue
        if I>35:continue
        join=7+span[t]-(I-1).bit_length()
        reason='two_minflats' if t in [252,254] else ('boundary_dichotomy' if t==256 else 'span_bound')
        assert reason=='two_minflats' or join<=14
        cand.append({'Tweight':t,'intersection':I,'join_bound':join,'reason':reason})
    R[w]={'degree4_candidates':deg4,'degree3_candidates':cand}
# E upper bound and E5-collapse
for w in W:
    deficit=(640-w)//2
    assert deficit>320-31*6
    assert deficit>5*32+5-16
# Nonedge count for a union of cliques on five vertices cannot equal5.
def partitions(n,lo=1):
    if not n:yield []
    for i in range(lo,n+1):
        for tail in partitions(n-i,i):yield [i]+tail
counts=sorted(set(sum(p*(p-1)//2 for p in ps) for ps in partitions(5)))
assert 5 not in counts
# Exhaustively classify the surviving simple Q-edge graphs.
reps=[];allpairs=list(itertools.combinations(range(5),2));number=0
for bits in range(1<<10):
    G=nx.Graph();G.add_nodes_from(range(5));G.add_edges_from(e for i,e in enumerate(allpairs) if bits>>i&1)
    E=G.number_of_edges()
    if not 2<=E<=4 or max(dict(G.degree()).values())>2:continue
    comps=sorted((C.number_of_nodes(),C.number_of_edges()) for C in (G.subgraph(c) for c in nx.connected_components(G)))
    if E==3 and ((3,3) in comps or (4,3) in comps):continue
    number+=1
    if not any(nx.is_isomorphic(G,H) for H in reps):reps.append(G)
assert len(reps)==6
out={'critical_weights':R,'clique_partition_edge_counts':counts,'surviving_labeled_graphs':number,'unlabeled_Qgraphs':[sorted(map(list,G.edges())) for G in reps]}
Path('workspace/agent4_fiveflat_Q_degree_checks.json').write_text(json.dumps(out,indent=2))
Path('workspace/agent4_fiveflat_Q_degree_checks.py').write_text(Path('scratchpad.py').read_text().split('