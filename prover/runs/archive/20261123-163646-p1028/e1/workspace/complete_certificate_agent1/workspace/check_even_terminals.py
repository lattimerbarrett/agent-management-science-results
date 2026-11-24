import itertools,json,networkx as nx,sympy as S
out={}
for n in [5,7]:
 valid=0;mx=S.Rational(0);best=None
 poss=list(itertools.combinations(range(1,n),2))
 for es in itertools.combinations(poss,(3*n-1)//2-2):
  edges=[(0,1),(0,2)]+list(es);deg=[0]*n
  for u,v in edges:deg[u]+=1;deg[v]+=1
  if deg!=[2]+[3]*(n-1):continue
  G=nx.Graph(edges)
  if not nx.is_connected(G) or list(nx.bridges(G)):continue
  valid+=1;L=S.zeros(n)
  for u,v in edges:L[u,u]+=1;L[v,v]+=1;L[u,v]-=1;L[v,u]-=1
  rs=L[1:,1:].inv().diagonal();r=max(rs)
  if r>mx:mx=r;best=edges
 assert valid=={5:1,7:54}[n]
 assert mx=={5:S.Rational(7,8),7:S.Rational(11,8)}[n]
 out[n]=best
 print('terminal order',n,'all labelings',valid,'exact max',mx)
def cubic_extremizer(n):
 sizes=[5]+[4]*((n-10)//4 if n%4==2 else (n-12)//4)+[5 if n%4==2 else 7]
 G=nx.Graph();off=0;ports=[]
 for i,size in enumerate(sizes):
  if i==0:edges=out[5];left=right=0
  elif i==len(sizes)-1:edges=out[size];left=right=0
  else:edges=[(0,2),(0,3),(1,2),(1,3),(2,3)];left=0;right=1
  G.add_edges_from((u+off,v+off)for u,v in edges);ports.append((off+left,off+right));off+=size
 for i in range(len(ports)-1):G.add_edge(ports[i][1],ports[i+1][0])
 return G,3,n-sizes[-1]+(3 if sizes[-1]==5 else 5)
for n in range(10,42,2):
 G,s,t=cubic_extremizer(n)
 assert len(G)==n and nx.is_connected(G) and set(dict(G.degree()).values())=={3}
 L=S.zeros(n)
 for u,v in G.edges():L[u,u]+=1;L[v,v]+=1;L[u,v]-=1;L[v,u]-=1
 keep=[i for i in range(n)if i!=t];e=S.zeros(n-1,1);e[keep.index(s)]=1
 sol=L.extract(keep,keep).inv()*e
 assert sol[keep.index(s)]==S.Rational(2*n-(9 if n%4==2 else 11),4)
print('All full cubic constructions n=10,...,40 passed exact resistance checks.')
