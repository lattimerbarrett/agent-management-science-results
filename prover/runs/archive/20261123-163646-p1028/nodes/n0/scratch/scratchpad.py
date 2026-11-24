import networkx as nx
import sympy as s

def res(G,u,v):
    ns=list(G); ns.remove(v)
    L=s.zeros(len(ns))
    for i,a in enumerate(ns):
        L[i,i]=G.degree(a)
        for j,b in enumerate(ns):
            if G.has_edge(a,b): L[i,j]=-1
    return L.inv()[ns.index(u),ns.index(u)]
for n in [5,6,7]:
 for typ in ['internal','end']:
    best=(-1,None)
    for G in nx.graph_atlas_g():
     if len(G)!=n or not nx.is_connected(G):continue
     ds=sorted(dict(G.degree()).values())
     if typ=='end' and ds==[2]+[4]*(n-1):
      u=next(v for v,d in G.degree() if d==2)
      for v in G:
       if v==u:continue
       r=res(G,u,v)
       if r>best[0]:best=(r,(G,u,v))
     if typ=='internal' and ds==[2,2]+[4]*(n-2):
      u,v=[v for v,d in G.degree() if d==2]
      r=res(G,u,v)
      if r>best[0]:best=(r,(G,u,v))
    if best[1]:print(n,typ,best[0],list(best[1][0].edges()),best[1][1:])
