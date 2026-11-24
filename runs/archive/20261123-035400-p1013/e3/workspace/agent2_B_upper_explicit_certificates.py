import networkx as nx,z3,json,itertools,time
code=open('workspace/agent2_AB_embed.py').read().replace('return S.check()==z3.sat',"st=S.check()\n if st!=z3.sat:return None\n m=S.model();return {v:m.eval(lab[v]).as_long() for v in H}")
exec(code)
H=nx.node_link_graph(json.load(open('workspace/agent2_glue_b_vs_clique.json')));HH=list(H);h=len(H)
def no2p3(F):
 ts=[set(t) for t in itertools.combinations(F,3) if F.subgraph(t).number_of_edges()>=2]
 return not any(a.isdisjoint(b) for a,b in itertools.combinations(ts,2))
patterns=[]
for F in nx.graph_atlas_g():
 if len(F)<3 or not nx.is_connected(F) or max(dict(F.degree()).values())>3 or not no2p3(F):continue
 f=max(0,8-F.number_of_edges());B=F.copy()
 for _ in range(f):B=nx.disjoint_union(B,nx.path_graph(2))
 patterns.append((F,f,B))
patterns.append((nx.empty_graph(),8,nx.disjoint_union_all([nx.path_graph(2)]*8)))
cert=[];t0=time.time()
for F,f,B in patterns:
 mp=embedAB(H,nx.empty_graph(),B);assert mp is not None,(F.edges(),f)
 aset={v for v in H if mp[v]==-1};used=set();real={};pair=0
 for u,v in H.subgraph(aset).edges():real[u]=2*pair;real[v]=2*pair+1;used|={u,v};pair+=1
 for u in aset-used:real[u]=2*pair;pair+=1
 b0=[v for v in H if mp[v]==0]
 for i,v in enumerate(b0):real[v]=2*h+len(B)+i
 for v in H:
  if mp[v]>=1:real[v]=2*h+mp[v]-1
 assert len(set(real.values()))==h
 def adj(x,y):
  if x<2*h and y<2*h:return x//2==y//2 and x!=y
  if (x<2*h)!=(y<2*h):return True
  x-=2*h;y-=2*h
  return x<len(B) and y<len(B) and B.has_edge(x,y)
 assert all(adj(real[u],real[v]) for u,v in H.edges())
 cert.append({'F_graph6':nx.to_graph6_bytes(F,header=False).decode().strip(),'f':f,'B_nodes':len(B),'B_edges':list(B.edges()),'map':[[list(v),real[v]] for v in H]})
print('CERTIFIED ALL',len(cert),'B edge>=8 obstructionpatterns, explicit47vertexinjectivemaps; seconds',time.time()-t0)
json.dump(cert,open('workspace/agent2_B_upper_explicit_certificates.json','w'))
