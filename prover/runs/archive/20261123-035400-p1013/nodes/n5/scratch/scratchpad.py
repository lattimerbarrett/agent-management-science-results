import networkx as nx

def k_colorable(G,k):
    colors={}
    def search():
        if len(colors)==len(G): return True
        v=max((v for v in G if v not in colors), key=lambda v:(len({colors[w] for w in G[v] if w in colors}),G.degree(v)))
        bad={colors[w] for w in G[v] if w in colors}
        used=max(colors.values(),default=-1)+1
        for c in range(min(k,used+1)):
            if c not in bad:
                colors[v]=c
                if search(): return True
                del colors[v]
        return False
    return search()

def turan(n,r):
    q,s=divmod(n,r)
    return (n*n-s*(q+1)**2-(r-s)*q*q)//2

for r in range(2,7):
    H=nx.Graph()
    for P in [list(range(r+1)),[0]+list(range(r+1,2*r+1))]:
        H.add_edges_from((u,v) for i,u in enumerate(P) for v in P[i+1:])
    assert not k_colorable(H,r) and k_colorable(H,r+1)
    critical=[]
    for edge in list(H.edges()):
        J=H.copy();J.remove_edge(*edge)
        if k_colorable(J,r):critical.append(edge)
    assert all(turan(n-1,r)+n-1-turan(n,r)==(n+r-1)//r-1 for n in range(1,100))
    print(f'r={r}: two K_(r+1)s sharing a vertex have {len(critical)} color-critical edges; universal-vertex surplus formula verified.')