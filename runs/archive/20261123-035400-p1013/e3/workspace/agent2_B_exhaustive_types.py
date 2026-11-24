import networkx as nx,itertools,json,time

def good(G):
 if max(dict(G.degree()).values(),default=0)>3:return False
 ts=[set(t) for t in itertools.combinations(G,3) if G.subgraph(t).number_of_edges()>=2]
 return not any(a.isdisjoint(b) for a,b in itertools.combinations(ts,2))
levels={1:[nx.empty_graph(1)]}
for n in range(2,8):
 out=[]
 for F in levels[n-1]:
  eligible=[v for v in F if F.degree(v)<3]
  for k in range(1,min(3,len(eligible))+1):
   for nei in itertools.combinations(eligible,k):
    G=F.copy();G.add_node(n-1);G.add_edges_from((n-1,v) for v in nei)
    if not good(G):continue
    if not any(nx.is_isomorphic(G,T) for T in out):out.append(G)
 levels[n]=out
print('EXHAUSTIVE connected2P3free Δ3 counts',[(n,len(g)) for n,g in levels.items()])
cert=json.load(open('workspace/agent2_B_upper_explicit_certificates.json'))
fs=[nx.from_graph6_bytes(c['F_graph6'].encode()) for c in cert if c['F_graph6']!='?']
assert len(fs)==sum(len(levels[n]) for n in range(3,8))==21
assert all(any(nx.is_isomorphic(G,F) for F in fs) for n in range(3,8) for G in levels[n])
print('PASS: all21 independentlygeneratedtypes coveredby explicitHembeddingcertificates')
