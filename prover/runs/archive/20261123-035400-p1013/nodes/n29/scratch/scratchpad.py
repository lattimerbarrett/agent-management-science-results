import networkx as nx
from math import exp
H=nx.wheel_graph(5)
H.add_edges_from([(1,5),(5,6),(6,1),(3,7),(7,8),(8,3)])

def defective_coloring(G,r):
    order=sorted(G,key=lambda x:G.degree(x),reverse=True)
    color={}; groups=[[] for _ in range(r)]
    def visit(i,used):
        if i==len(order):return dict(color)
        v=order[i]
        for c in range(min(r,used+1)):
            neighbors=[u for u in groups[c] if G.has_edge(u,v)]
            if len(neighbors)>1:continue
            if neighbors and any(G.has_edge(neighbors[0],w) for w in groups[c]):continue
            color[v]=c;groups[c].append(v)
            ans=visit(i+1,max(used,c+1))
            if ans is not None:return ans
            groups[c].pop();del color[v]
        return None
    return visit(0,0)

for r in range(3,7):
    J=H.copy()
    for i in range(r-2):
        pair=[9+2*i,10+2*i]
        old=list(J)
        J.add_nodes_from(pair)
        J.add_edges_from((u,v) for u in pair for v in old)
    ans=defective_coloring(J,r)
    p=(r-1)/r
    print('r=',r,'naive join has matching-defective coloring:',ans,flush=True)
    print('universal-vertex cycle factor:',p**-2,
          'two-matching factor:',exp(2/(r-1)),
          'all-matching excess coefficient:',.5,
          'target coefficient:',1/r,flush=True)
