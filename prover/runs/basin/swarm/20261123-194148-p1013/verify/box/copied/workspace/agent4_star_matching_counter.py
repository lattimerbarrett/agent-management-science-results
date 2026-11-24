import networkx as nx,json
for k in [3,4]:
 # 0=w,1,2=u's,3,4=v's; A_i 5..,B_i5+k..
 H=nx.Graph();H.add_nodes_from(range(2*k+5));H.add_edges_from([(0,i) for i in range(1,5)])
 for i in range(k):
  a=5+i;b=5+k+i;H.add_edges_from([(1,a),(2,a),(3,b),(4,b),(a,b)])
 n=len(H);best=100;side=[]
 for mask in range(1<<n):
  X=[i for i in H if mask>>i&1];Y=[i for i in H if not mask>>i&1];R=H.subgraph(X);S=H.subgraph(Y)
  if S.number_of_edges()==0 and max(dict(R.degree()).values(),default=0)<=1:
   best=min(best,R.number_of_edges())
 print('k',k,'n',n,'min onepartmatching',best);assert best==k
open('workspace/agent4_star_matching_counter.py','w').write(open(__file__).read())
