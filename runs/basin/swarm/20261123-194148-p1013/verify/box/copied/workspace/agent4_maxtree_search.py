import networkx as nx, random, functools, time,json
random.seed(132)
def code(T):
 if len(T)==1:return '()'
 def rooted(v,p):return '('+''.join(sorted(rooted(w,v) for w in T[v] if w!=p))+')'
 return min(rooted(v,None) for v in nx.center(T))
trees={};byorder={}
for k in range(1,10):
 ts=[nx.empty_graph(1)] if k==1 else list(nx.nonisomorphic_trees(k))
 byorder[k]=[]
 for T in ts:
  c=code(T);trees[c]=T;byorder[k].append(c)
@functools.lru_cache(None)
def contains(tc,rc):
 T=trees[tc];R=trees[rc]
 return len(R)<=len(T) and nx.algorithms.isomorphism.GraphMatcher(T,R).subgraph_is_isomorphic()
def families(H):
 n=len(H);adj=[sum(1<<j for j in H[i]) for i in H];full=(1<<n)-1;fs=set();cyc=set()
 for B in range(1<<n):
  if any(adj[i]&B for i in range(n) if B>>i&1):continue
  A=[i for i in range(n) if not B>>i&1];R=H.subgraph(A)
  comps=[R.subgraph(vs) for vs in nx.connected_components(R)]
  if all(max(dict(T.degree()).values())<=2 for T in comps):
   for ell in [3,4]:
    if all((T.number_of_edges()==len(T)-1 and len(T)<=ell) or (T.number_of_edges()==len(T) and len(T)==ell) for T in comps):cyc.add(ell)
  if not nx.is_forest(R):continue
  cs=[]
  for vs in nx.connected_components(R):
   T=R.subgraph(vs);c=code(T);trees[c]=nx.convert_node_labels_to_integers(T);cs.append(c)
  fs.add(frozenset(cs))
 return fs,cyc
start=time.time(); checked=0
for it in range(30000):
 n=random.randrange(10,15);a=(n-1)//2;p=random.uniform(.25,.7)
 H=nx.Graph();H.add_nodes_from(range(n))
 H.add_edges_from((i,j) for i in range(a) for j in range(a,n-1) if random.random()<p)
 H.add_edges_from((i,n-1) for i in range(n-1) if random.random()<.8)
 if nx.is_bipartite(H):continue
 fs,cyc=families(H)
 if cyc!={3,4}:continue
 def allowed(tc):return not any(all(contains(tc,rc) for rc in F) for F in fs)
 if any(allowed(c) for c in byorder[9]):continue
 checked+=1
 for k in range(8,0,-1):
  al=[c for c in byorder[k] if allowed(c)]
  if al:
   ws={sum(d*(d-1)//2 for _,d in trees[c].degree()) for c in al}
   if len(ws)>1:
    print('FOUND',it,n,k,ws,list(H.edges()),[list(trees[c].edges()) for c in al])
    for ell in [3,4]:
     ok=False
     for mask in range(1<<n):
      B=[i for i in H if mask>>i&1]
      if H.subgraph(B).number_of_edges():continue
      R=H.subgraph([i for i in H if not mask>>i&1]);C=nx.cycle_graph(ell)
      if all(nx.algorithms.isomorphism.GraphMatcher(C,R.subgraph(comp)).subgraph_is_monomorphic() for comp in nx.connected_components(R)):
       print('cycle',ell,'witnessA',list(R));ok=True;break
     if not ok:print('cycle',ell,'FAIL')
    open('workspace/agent4_treephase_H13.json','w').write(json.dumps(dict(edges=list(H.edges()),maxorder=k,wedges=sorted(ws))))
    open('workspace/agent4_maxtree_search.py','w').write(open(__file__).read())
    raise SystemExit
   break
print('none',checked,'boundedmaxcases',time.time()-start,'seconds')
open('workspace/agent4_maxtree_search.py','w').write(open(__file__).read())
