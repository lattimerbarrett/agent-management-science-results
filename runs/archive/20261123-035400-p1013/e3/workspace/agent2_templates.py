import networkx as nx,itertools,random

def branches(G,s,K):
 L=s*K;stars=paths=True;bigS=bigP=0
 for cc in nx.connected_components(G):
  h=G.subgraph(cc);n=len(h);e=h.number_of_edges();d=max(dict(h.degree()).values(),default=0)
  stars &= e==n-1 and (n<=2 or d==n-1) and n<=L
  paths &= e==n-1 and d<=2 and n<=L-1
  bigS+=n>s;bigP+=n if n>s else 0
 return stars and bigS<=1, paths and bigP<=L-1

def parts(n,lo):
 if n==0:yield ()
 for x in range(lo,n+1):
  for p in parts(n-x,x):yield (x,)+p

def path_forest(p):
 G=nx.Graph()
 for n in p:G=nx.disjoint_union(G,nx.path_graph(n))
 return G

def obstruction_families(s,K):
 L=s*K
 A=[nx.complete_graph(3),nx.path_graph(4),nx.star_graph(L),nx.disjoint_union(nx.star_graph(s),nx.star_graph(s))]
 B=[nx.star_graph(3),nx.path_graph(L)]+[nx.cycle_graph(i) for i in range(3,L)]
 B += [path_forest(p) for n in range(L,2*L) for p in parts(n,s+1)]
 return A,B

def contains(G,H):
 if len(H)>len(G) or H.number_of_edges()>G.number_of_edges():return False
 return nx.algorithms.isomorphism.GraphMatcher(G,H).subgraph_is_monomorphic()

def path_capacity_subgraph(host,pat):
 # Bin packing of vertex-disjoint paths into host path components (extra edges can be omitted).
 pat=sorted(pat,reverse=True);bins=list(host)
 def rec(i):
  if i==len(pat):return True
  seen=set()
  for j,b in enumerate(bins):
   if b>=pat[i] and b not in seen:
    seen.add(b);bins[j]-=pat[i]
    if rec(i+1):return True
    bins[j]+=pat[i]
  return False
 return rec(0)

if __name__=='__main__':
 tested=0;pf=0;random.seed(237)
 for s,K in [(3,2),(4,2),(6,2),(8,3)]:
  L=s*K;A,B=obstruction_families(s,K)
  for G in nx.graph_atlas_g():
   S,P=branches(G,s,K)
   assert S==all(not contains(G,h) for h in A),(s,K,'S',G.edges())
   assert P==all(not contains(G,h) for h in B),(s,K,'P',G.edges())
   tested+=1
  cap=[p for n in range(L,2*L) for p in parts(n,s+1)]
  for _ in range(1000):
   p=[random.randrange(1,2*L) for j in range(random.randrange(1,7))]
   allowed=all(x<L for x in p) and sum(x for x in p if x>s)<L
   avoids=all(x<L for x in p) and not any(path_capacity_subgraph(p,q) for q in cap)
   assert allowed==avoids,(s,K,p)
   pf+=1
 print('PASS: corrected hereditary templates;',tested,'atlas graphs;',pf,'random path forests')
