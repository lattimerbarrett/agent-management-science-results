import networkx as nx,z3,json,random,time
from pathlib import Path
F=nx.node_link_graph(json.load(open('workspace/agent2_base_min.json')));root=(0,29)
H=nx.Graph()
for side in [0,1]:
    def vv(v):return root if v==29 else (side,v)
    H.add_edges_from((vv(u),vv(v))for u,v in F.edges())

def embeds(G,ac,bc):
    S=z3.Solver();ls={v:z3.Int('l'+str(i))for i,v in enumerate(G)};na=len(ac);nb=len(bc)
    for v in G:S.add(ls[v]>=0,ls[v]<=na+nb+1)
    def apart(v):return ls[v]<=na
    for u,v in G.edges():S.add(z3.Or(apart(u)!=apart(v),z3.And(ls[u]==ls[v],ls[u]!=na+1)))
    for v in G:S.add(z3.Implies(ls[v]==0,z3.PbLe([(ls[w]==0,1)for w in G[v]],1)))
    for i,c in enumerate(ac,1):S.add(z3.PbLe([(ls[v]==i,1)for v in G],c))
    for i,c in enumerate(bc,na+2):S.add(z3.PbLe([(ls[v]==i,1)for v in G],c))
    st=S.check();assert st in[z3.sat,z3.unsat]
    return st==z3.sat

def good(G):return not embeds(G,[5],[2])and not embeds(G,[],[4,2])
assert good(H)
random.seed(718);best=H.copy();start=time.time();checks=0
for run in range(10):
    G=H.copy();change=True
    while change:
        change=False;edges=list(G.edges());random.shuffle(edges)
        for u,v in edges:
            C=G.copy();C.remove_edge(u,v);C.remove_nodes_from(list(nx.isolates(C)))
            checks+=1
            if good(C):G=C;change=True
        vs=[v for v in G if v!=root];random.shuffle(vs)
        for v in vs:
            C=G.copy();C.remove_node(v);C.remove_nodes_from(list(nx.isolates(C)))
            checks+=1
            if good(C):G=C;change=True
    print(run,len(G),G.number_of_edges(),'checks',checks,'sec',round(time.time()-start,2),flush=True)
    if (len(G),G.number_of_edges())<(len(best),best.number_of_edges()):
        best=G.copy();Path('workspace/agent4_H_counter_min.json').write_text(json.dumps(nx.node_link_data(best)));print('BEST',list(best.edges()),flush=True)
Path('workspace/agent4_H_counter_min.json').write_text(json.dumps(nx.node_link_data(best)))
