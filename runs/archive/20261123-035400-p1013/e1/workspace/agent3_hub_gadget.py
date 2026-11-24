"""Finite certificates for the H9 hub-gadget argument. Run with Python 3."""
import itertools
import networkx as nx
H=nx.wheel_graph(5)
H.add_edges_from([(1,5),(1,6),(5,6),(3,7),(3,8),(7,8)])

def certificate(deleted,A,B,internal,required_good):
    assert set(A).isdisjoint(B)
    assert set(A)|set(B)==set(H)-{deleted}
    E={frozenset(e) for e in H.edges if (e[0] in A)==(e[1] in A) and deleted not in e}
    assert E=={frozenset(e) for e in internal},(E,internal)
    endpoints=set().union(*E)
    assert {w for w in endpoints if H.has_edge(deleted,w)}==set(required_good)
    return endpoints

# Same-side two disjoint edges require no adjacency to hub.
certificate(0,{2,4,5,6,7,8},{1,3},[(5,6),(7,8)],set())
# A P3 requires adjacency to only one leaf (0), not center (3).
certificate(1,{0,3,5,7},{2,4,6,8},[(0,3),(3,7)],{0})
# Opposite-side edges require only one endpoint adjacent to hub.
certificate(0,{1,3,5},{2,4,6,7,8},[(1,5),(7,8)],{1})
assert not any(H.has_edge(a,b) for a in (1,5) for b in (7,8))

# Exhaustive check of abstract gadget inequality for all side graphs <=5 vertices.
# General proof: matching-number <=1 means star or triangle, and any P3
# must have both leaves bad. The enumeration checks exactly those conditions.
states=set()
for n in range(6):
    E=list(itertools.combinations(range(n),2))
    for mask in range(1<<len(E)):
        J=nx.Graph();J.add_nodes_from(range(n));J.add_edges_from(e for k,e in enumerate(E) if mask>>k&1)
        if len(nx.max_weight_matching(J,maxcardinality=True))>1:continue
        for goodbits in range(1<<n):
            good={v for v in J if goodbits>>v&1}
            if any((a in good or b in good) for v in J for a,b in itertools.combinations(J[v],2)):continue
            e=J.number_of_edges();bad=n-len(good)
            touches=any(a in good or b in good for a,b in J.edges)
            states.add((e,bad,touches))
checks=0
for e,b,t in states:
    for f,c,u in states:
        # Split certificate forbids an edge on each side when either touches good.
        if e and f and (t or u):continue
        surplus=e+f-b-c
        assert surplus<=1
        if surplus==1:
            assert b+c==0 and e+f==1
        checks+=1
print('All H9 embedding certificates verified.')
print('Abstract two-side gadget checks:',checks)
