import itertools,time,networkx as nx,json,sympy as s

def graphs_degseq(ds):
 n=len(ds); adj=[set() for _ in ds]; rem=list(ds)
 def rec(i):
  if i==n:
   yield [(a,b) for a in range(n) for b in adj[a] if a<b];return
  d=rem[i]
  if d<0 or d>n-1-i:return
  groups={}
  for j in range(i+1,n):
   if rem[j]>0:groups.setdefault((rem[j],tuple(sorted(adj[j]))),[]).append(j)
  groups=list(groups.values())
  def choices(k,left,sel):
   if k==len(groups):
    if left==0:yield sel
    return
   group=groups[k]
   for r in range(min(left,len(group))+1):yield from choices(k+1,left-r,sel+group[:r])
  for nb in choices(0,d,[]):
   for j in nb:rem[j]-=1;adj[j].add(i);adj[i].add(j)
   ok=all(0<=rem[j]<=n-2-i for j in range(i+1,n)) and sum(rem[i+1:])%2==0
   if ok:
    seq=sorted(rem[i+1:],reverse=True)
    ok=all(sum(seq[:k])<=k*(k-1)+sum(min(k,x) for x in seq[k:]) for k in range(1,len(seq)+1))
   if ok:yield from rec(i+1)
   for j in nb:rem[j]+=1;adj[j].remove(i);adj[i].remove(j)
 yield from rec(0)

def exact_check(n,ports):
 ds=[2]*ports+[4]*(n-ports);count=0;connected=0;biconnected=0
 maxima={False:s.Integer(0),True:s.Integer(0)}; witnesses={}
 for edges in graphs_degseq(ds):
  count+=1;G=nx.Graph();G.add_nodes_from(range(n));G.add_edges_from(edges)
  if not nx.is_connected(G):continue
  connected+=1;bi=nx.is_biconnected(G);biconnected+=bi
  L=s.diag(*ds)
  for a,b in edges:L[a,b]=L[b,a]=-1
  Z=L[1:,1:].inv()
  r=max(Z.diagonal()) if ports==1 else Z[0,0]
  if r>maxima[False]:maxima[False]=r;witnesses[False]=edges
  if bi and r>maxima[True]:maxima[True]=r;witnesses[True]=edges
 return dict(n=n,ports=ports,count=count,connected=connected,biconnected=biconnected,
             maxima={str(k):str(v) for k,v in maxima.items()},witnesses={str(k):v for k,v in witnesses.items()})
if __name__=='__main__':
 results=[]
 for n in range(6,11):
  for ports in [1,2]:
   t=time.time();r=exact_check(n,ports);results.append(r);print(r,'secs',time.time()-t,flush=True)
 json.dump(results,open('workspace/local4_exact.json','w'),indent=2)
