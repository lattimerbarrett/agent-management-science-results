import networkx as nx

FORBIDDEN=[nx.path_graph(5),nx.cycle_graph(4),nx.disjoint_union(nx.path_graph(4),nx.path_graph(2))]

def contains(G,H):
    return nx.algorithms.isomorphism.GraphMatcher(G,H).subgraph_is_monomorphic()

def pineapple(C):
    n=len(C)
    if n<3 or C.number_of_edges()!=n:return False
    for a in C:
        D=C.copy();D.remove_node(a)
        if sum(d==1 for _,d in D.degree())==2 and all(d<=1 for _,d in D.degree()) and D.number_of_edges()==1 and C.degree(a)==n-1:
            return True
    return False

def described(G):
    big=False
    for nodes in nx.connected_components(G):
        C=G.subgraph(nodes).copy();n=len(C)
        if nx.is_tree(C):
            if nx.diameter(C)>3:return False
        elif not pineapple(C):return False
        if contains(C,nx.path_graph(4)):big=True
    if big and sum(len(nodes)>1 for nodes in nx.connected_components(G))!=1:return False
    return True

if __name__=='__main__':
    count=0
    for G in nx.graph_atlas_g():
        allowed=not any(contains(G,H) for H in FORBIDDEN)
        assert allowed==described(G),(G.number_of_nodes(),list(G.edges()))
        if allowed:
            assert G.number_of_edges()<=len(G)
            if G.number_of_edges()==len(G) and len(G):
                assert all(len(c)==3 for c in nx.connected_components(G)) or pineapple(G)
        count+=1
    print('All',count,'graphs in the atlas (n<=7) verified.')
