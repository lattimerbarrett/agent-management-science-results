import networkx as nx,itertools,pickle,random,time
import numpy as np
from scipy.special import iv
random.seed(2026)
def trim(G,large=False):
 verts=[]
 for C in nx.connected_components(G):
  if len(C)>=(3 if large else 2):verts.extend(C)
 return nx.convert_node_labels_to_integers(G.subgraph(verts))
def key(G):return nx.weisfeiler_lehman_graph_hash(G)
Fs={key(trim(G)):trim(G) for G in nx.graph_atlas_g()};Fs=list(Fs.values())
cache={}
def sub(A,B):
 k=key(A),key(B)
 if k not in cache:
  cache[k]=len(A)<=len(B) and A.number_of_edges()<=B.number_of_edges() and max(dict(A.degree()).values(),default=0)<=max(dict(B.degree()).values(),default=0) and nx.algorithms.isomorphism.GraphMatcher(B,A).subgraph_is_monomorphic()
 return cache[k]
P3s=nx.disjoint_union_all([nx.path_graph(3)]*3)
seen=set(); tested=0
for trial in range(10000):
 n=random.choice([8,9,10]);a=n//2
 H=nx.Graph();H.add_nodes_from(range(n))
 H.add_edges_from([(i,i+1) for i in range(0,a-1,2)]+[(i,i+1) for i in range(a,n-1,2)])
 prob=random.uniform(.3,.8)
 H.add_edges_from((i,j) for i in range(a) for j in range(a,n) if random.random()<prob)
 if min(dict(H.degree()).values())==0 or nx.is_bipartite(H):continue
 if not any(nx.is_bipartite(nx.subgraph(H,[u for u in H if u!=v])) for v in H):continue
 kh=key(H)
 if kh in seen:continue
 seen.add(kh)
 pats={}; mono_matching=False; p3host=False
 for mask in range(1<<n):
  AA=H.subgraph([i for i in range(n) if mask>>i&1]);BB=H.subgraph([i for i in range(n) if not(mask>>i&1)])
  if BB.number_of_edges()==0 and max(dict(AA.degree()).values(),default=0)<=1:
   mono_matching=True;break
  A=trim(AA,True);B=trim(BB)
  if not len(B) and sub(A,P3s):p3host=True
  if len(A)>7 or len(B)>7:continue
  pats[key(A),key(B)]=(A,B)
 if mono_matching or not p3host:continue
 P=list(pats.values()); tested+=1
 Acore=[G for G in Fs if not any(len(B)==0 and sub(A,G) for A,B in P)]
 Bcore=[G for G in Fs if not any(len(A)==0 and sub(B,G) for A,B in P)]
 good=[]
 for G in Acore:
  for J in Bcore:
   if any(sub(A,G) and sub(B,J) for A,B in P):continue
   good.append((G.number_of_edges(),len(G),J.number_of_edges(),G,J))
 for parity in [0,1]:
  # Baseline matching in a class of this parity.
  vals=[(e-(v+1-parity)//2,b,G,J) for e,v,b,G,J in good]
  for wa,wb,label in [(1.,2.,'even order'),(1.,float(iv(2,2*2**.5)/iv(0,2*2**.5)*2),'odd order')]:
   me=max(x+b for x,b,_,_ in vals);mw=max(wa*x+wb*b for x,b,_,_ in vals)
   ew=max(wa*x+wb*b for x,b,_,_ in vals if x+b==me)
   if mw>ew+1e-8:
    print('FOUND trial',trial,'tested',tested,'parity',parity,label,'H',list(H.edges()),'edge max',me,'edge weight',ew,'cycle weight',mw,flush=True)
    for x,b,G,J in vals:
     if (x+b==me and abs(wa*x+wb*b-ew)<1e-8) or abs(wa*x+wb*b-mw)<1e-8:
      print(' ',x,b,list(G.edges()),list(J.edges()),flush=True)
    with open('matching_candidate.pkl','wb') as f:pickle.dump((H,good),f)
    raise SystemExit
 if tested%10==0:print('tested',tested,'trial',trial,flush=True)
print('none; tested',tested)
