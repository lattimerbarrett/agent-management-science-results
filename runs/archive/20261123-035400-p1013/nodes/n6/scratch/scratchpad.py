import networkx as nx,itertools,math,time,pickle
import scipy.special as sp
import numpy as np
Hs=[]
for H in nx.graph_atlas_g():
 n=len(H)
 if n<3 or nx.is_bipartite(H) or min(dict(H.degree()).values())==0:continue
 fs=[]; partitions=[]
 for mask in range(1<<n):
  col=[(mask>>i)&1 for i in range(n)]
  same=[(u,v) for u,v in H.edges() if col[u]==col[v]]
  R=set(v for edge in same for v in edge)
  partitions.append((col,R))
  A=[i for i in range(n) if mask>>i&1]
  if H.subgraph(A).number_of_edges():continue
  F=H.subgraph([i for i in range(n) if i not in A]); F=F.subgraph([i for i,d in F.degree() if d])
  fs.append(F)
 if not any(max(dict(F.degree()).values(),default=0)<=1 for F in fs):continue
 if not any(len(F)>=2 and nx.is_tree(F) and max(dict(F.degree()).values())==len(F)-1 for F in fs):continue
 Hs.append((H,partitions))
print('H count',len(Hs),flush=True)
x=float(sp.iv(2,2)/sp.iv(1,2))
for k in [5,6]:
 for aa in range(1,k//2+1):
  bb=k-aa;pairs=list(itertools.combinations(range(k),2)); idx={p:i for i,p in enumerate(pairs)}
  masks=np.arange(1<<len(pairs),dtype=np.int64)
  ea=np.zeros(len(masks),dtype=np.int8);eb=ea.copy();miss=ea.copy()
  for bit,(i,j) in enumerate(pairs):
   bitvals=(masks>>bit)&1
   if j<aa:ea+=bitvals.astype(np.int8)
   elif i>=aa:eb+=bitvals.astype(np.int8)
   else:miss+=(1-bitvals).astype(np.int8)
  edges=ea+eb-miss;weight=np.maximum((1+x)*ea+x*eb,(1+x)*eb+x*ea)-miss
  for hi,(H,parts) in enumerate(Hs):
   reqs=set()
   for col,R in parts:
    RA=[v for v in R if col[v]==0];RB=[v for v in R if col[v]==1]
    if len(RA)>aa or len(RB)>bb:continue
    ER=[(u,v) for u,v in H.edges() if u in R and v in R]
    for pa in itertools.permutations(range(aa),len(RA)):
     for pb in itertools.permutations(range(aa,k),len(RB)):
      mp=dict(zip(RA+RB,pa+pb));req=0
      for u,v in ER:
       p,q=sorted((mp[u],mp[v]));req|=1<<idx[p,q]
      reqs.add(req)
   minimal=[]
   for req in sorted(reqs,key=int.bit_count):
    if not any(req&v==v for v in minimal):minimal.append(req)
   good=np.ones(len(masks),dtype=bool)
   for req in minimal:good&=(masks&req)!=req
   if not good.any():continue
   me=edges[good].max();mw=weight[good].max();edgew=weight[good&(edges==me)].max()
   if mw>edgew+1e-7:
    print('FOUND k,a=',k,aa,'H',list(H.edges()),'me',me,'ew',edgew,'mw',mw,flush=True)
    ids=np.where(good&((weight>mw-1e-7)|((edges==me)&(weight>edgew-1e-7))))[0]
    for i in ids[:20]:print(' ',int(masks[i]),int(edges[i]),float(weight[i]),'ea eb miss',ea[i],eb[i],miss[i],flush=True)
    with open('candidate.pkl','wb') as f:pickle.dump((H,k,aa,masks[good],edges[good],weight[good]),f)
    raise SystemExit
  print('done',k,aa,flush=True)
print('none')