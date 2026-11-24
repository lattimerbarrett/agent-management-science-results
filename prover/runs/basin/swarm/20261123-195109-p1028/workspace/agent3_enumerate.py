import sys,time,itertools,json
from sage.all import Graph
import networkx as nx
import sympy as sp
from fractions import Fraction

def enumerate_deg(seq):
 n=len(seq);G=Graph(n);rem=list(seq);seen=set();full=[];calls=0
 def dfs():
  nonlocal calls
  calls+=1
  if any(x<0 for x in rem):return
  active=[v for v in range(n) if rem[v]]
  if not active:
   if G.is_connected():full.append(G.copy())
   return
  if sum(rem)%2 or not nx.is_graphical(rem):return
  colors=sorted(set(zip(seq,rem)))
  part=[[v for v in range(n) if (seq[v],rem[v])==c] for c in colors]
  C,cert=G.canonical_label(partition=part,certificate=True,algorithm='sage')
  ct=[None]*n
  for v,w in cert.items():ct[w]=(seq[v],rem[v])
  key=(C.graph6_string(),tuple(ct))
  if key in seen:return
  seen.add(key)
  v=max(active,key=lambda v:rem[v]);k=rem[v]
  opts=[u for u in active if u!=v and not G.has_edge(u,v)]
  if len(opts)<k:return
  rem[v]=0
  for ns in itertools.combinations(opts,k):
   for u in ns:G.add_edge(v,u);rem[u]-=1
   dfs()
   for u in ns:G.delete_edge(v,u);rem[u]+=1
  rem[v]=k
 dfs()
 # full duplicates removed independently (terminal states skipped canonical)
 uniq={}
 for H in full:
  colors=sorted(set(seq));part=[[v for v in range(n) if seq[v]==c] for c in colors]
  C=H.canonical_label(partition=part,algorithm='sage');uniq[C.graph6_string()]=H
 return list(uniq.values()),calls,len(seen)

def score(H,typ):
 n=H.order();L=sp.zeros(n-1)
 for i in range(1,n):
  L[i-1,i-1]=H.degree(i)
  for j in H.neighbors(i):
   if j:L[i-1,j-1]=-1
 Q=L.inv()
 return Q[0,0] if typ=='bead' else max(Q[i,i] for i in range(n-1))

if __name__=='__main__':
 out=[]
 for typ in ['cap','bead']:
  for n in range(6,11):
   t=time.time();seq=[2]+[4]*(n-1)
   if typ=='bead':seq[1]=2
   graphs,calls,seen=enumerate_deg(seq)
   vals=[score(G,typ) for G in graphs]
   m=max(vals);best=graphs[vals.index(m)]
   rec={'type':typ,'n':n,'numclasses':len(graphs),'max':str(m),'calls':calls,'states':seen,'time':time.time()-t,'edges':list(best.edges(labels=False))}
   out.append(rec);print(rec,flush=True);json.dump(out,open('workspace/agent3_exact.json','w'))
