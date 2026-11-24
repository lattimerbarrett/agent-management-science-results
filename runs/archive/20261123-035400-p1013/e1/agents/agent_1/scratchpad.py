from pathlib import Path
source=Path('workspace/agent4_cyclechecks.py').read_text().split('\nH=nx.Graph();')[0]
extra=r'''
# The forbidden graph and finite embedding certificates.
H=nx.Graph([(0,1),(0,2),(0,3),(0,4),(1,2),(2,3),(3,4),(4,1),
            (1,5),(5,6),(6,1),(3,7),(7,8),(8,3)])
assert nx.is_bipartite(H.subgraph([2,4,6,8]))
assert H.subgraph([2,4,6,8]).number_of_edges()==0
assert nx.is_isomorphic(H.subgraph([0,1,3,5,7]),nx.path_graph(5))
assert H.subgraph([1,3]).number_of_edges()==0
assert nx.is_isomorphic(H.subgraph([0,2,4,5,6,7,8]),
                       nx.disjoint_union_all([nx.path_graph(3),nx.path_graph(2),nx.path_graph(2)]))
colors={0:2,1:0,2:1,3:0,4:1,5:1,6:2,7:1,8:2}
assert all(colors[x]!=colors[y] for x,y in H.edges())
assert sum(1 for t in itertools.combinations(H,3) if H.subgraph(t).number_of_edges()==3)>0
for v in H:
    nodes=[u for u in H if u!=v]
    defect=min(sum(bits[nodes.index(x)]==bits[nodes.index(y)]
                   for x,y in H.edges() if v not in (x,y))
               for bits in itertools.product(range(2),repeat=8))
    assert defect>=2
# For rooted hub gadget certificates, 2 denotes the hub image.
# Each entry: label-color map, core internal edges, exceptional core labels,
# hub neighbors among exceptional labels that must be good.
certs=[
 ({0:2,1:1,2:0,3:1,4:0,5:0,6:0,7:0,8:0},
  {(5,6),(7,8)}, {5,6,7,8}, set()),
 ({0:0,1:2,2:1,3:0,4:1,5:0,6:1,7:0,8:1},
  {(0,3),(3,7)}, {0,3,7}, {0}),
 ({0:2,1:0,2:1,3:0,4:1,5:0,6:1,7:1,8:1},
  {(1,5),(7,8)}, {1,5,7,8}, {1}),
]
for col,edges,exc,required in certs:
    root=next(v for v in col if col[v]==2)
    actual={tuple(sorted((x,y))) for x,y in H.edges()
            if root not in (x,y) and col[x]==col[y]}
    assert actual==edges
    assert {v for v in exc if H.has_edge(root,v)}==required
    # No cross-edge between distinct exceptional labels is required.
    assert not any(x in exc and y in exc and col[x]!=col[y] for x,y in H.edges())
print('Forbidden-graph partitions, colorings, bipartization defects, and all hub certificates verified.')
'''
Path('workspace/agent1_verify.py').write_text(source+extra)
exec(compile(source+extra,'agent1_verify.py','exec'))
