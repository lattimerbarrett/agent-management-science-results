import networkx as nx,itertools as it,math,json
from functools import lru_cache
import mpmath as mp
atlas=nx.graph_atlas_g()

def chromatic3(G):
 if nx.is_bipartite(G):return False
 nodes=sorted(G,key=lambda v:-G.degree(v));cols={}
 def rec(i):
  if i==len(nodes):return True
  v=nodes[i]
  for c in range(3):
   if all(cols.get(w)!=c for w in G[v]):
    cols[v]=c
    if rec(i+1):return True
    del cols[v]
  return False
 return rec(0)

def noisol(G):return nx.convert_node_labels_to_integers(G.subgraph([v for v in G if G.degree(v)]))
def key(G):return nx.weisfeiler_lehman_graph_hash(G),len(G),G.number_of_edges(),tuple(sorted(dict(G.degree()).values()))

# distinct small internal graph isomorphism types
Fs=[G.copy() for G in atlas if (len(G)==0 or min(dict(G.degree()).values())>0) and (len(G)==0 or max(dict(G.degree()).values())<=2) and len(nx.max_weight_matching(G,maxcardinality=True))<=2]
Fs.sort(key=lambda G:(G.number_of_edges(),len(G)))
print('internal types',len(Fs),flush=True)
contains={}
def sub(H,F):
 if len(H)==0:return True
 if len(H)>len(F) or H.number_of_edges()>F.number_of_edges():return False
 return nx.algorithms.isomorphism.GraphMatcher(F,H).subgraph_is_monomorphic()

wa=float(mp.besseli(0,2));wb=float(mp.besseli(2,2))
for ind,H in enumerate(atlas):
 if len(H)<3 or not chromatic3(H):continue
 h=len(H);decs=[];star=False;matching=False
 for mask in range(1<<h):
  A=[i for i in range(h) if mask>>i&1];B=[i for i in range(h) if not mask>>i&1]
  X=noisol(H.subgraph(A));Y=noisol(H.subgraph(B));decs.append((X,Y))
  if len(Y)==0:
   if len(X)>0 and max(dict(X.degree()).values())<=1:matching=True
   if len(X)>0 and X.number_of_edges()<=3 and max(dict(X.degree()).values())==X.number_of_edges():star=True
 if not(star and matching):continue
 allowed=[]
 for i,F in enumerate(Fs):
  for j,J in enumerate(Fs):
   if not any(sub(X,F) and sub(Y,J) for X,Y in decs):allowed.append((F.number_of_edges(),J.number_of_edges(),i,j))
 if not allowed:continue
 em=max(a+b for a,b,_,_ in allowed)
 wm=max(wa*a+wb*b for a,b,_,_ in allowed if a+b==em)
 wc,aa=max((wa*a+wb*b,(a,b,i,j)) for a,b,i,j in allowed)
 if wc>wm+1e-8:
  print('FOUND H',ind,'h',h,'edges',list(H.edges()),'edge max',em,'weights',wm,wc,'cycbest',aa,flush=True)
  print('edgeconfigs',[(a,b,i,j) for a,b,i,j in allowed if a+b==em])
  json.dump({'H':list(H.edges()),'Hn':h,'A':list(Fs[aa[2]].edges()),'B':list(Fs[aa[3]].edges())},open('constant_counter.json','w'))
  break
else:print('No atlas counterexample',flush=True)
