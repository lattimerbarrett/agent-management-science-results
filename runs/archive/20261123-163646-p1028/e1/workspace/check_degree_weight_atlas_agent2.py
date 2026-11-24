import networkx as nx,sympy as S,itertools,json
count=0; margin=None; example=None
for G in nx.graph_atlas_g():
 n=len(G)
 if n<3 or not nx.is_connected(G) or min(dict(G.degree()).values())<2:continue
 L=S.zeros(n)
 for u,v in G.edges():L[u,u]+=1;L[v,v]+=1;L[u,v]-=1;L[v,u]-=1
 inv=L[1:,1:].inv();dg=dict(G.degree());total=sum(S.Rational(1,dg[v]-1) for v in G)
 for u,v in itertools.combinations(range(n),2):
  R= inv[v-1,v-1] if u==0 else inv[u-1,u-1]+inv[v-1,v-1]-2*inv[u-1,v-1]
  B=total-1-S.Rational(1,dg[u]-1)-S.Rational(1,dg[v]-1)+S.Rational(1,dg[u])+S.Rational(1,dg[v])
  count+=1
  if margin is None or B-R<margin:margin=B-R;example=(list(G.edges()),u,v,str(R),str(B))
  if R>B:
   print('COUNTER',list(G.edges()),u,v,R,B);raise SystemExit
print('pairs',count,'minimum margin',margin,'example',example)
with open('workspace/check_degree_weight_atlas_agent2.py','w') as f:f.write(open(__file__).read())
