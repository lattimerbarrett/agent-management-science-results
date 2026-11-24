import networkx as nx, itertools, sympy as s, json
result={}
for b in [4,5]:
 E=list(itertools.combinations(range(b),2)); mx=s.S.Zero;cnt=0
 for missing in itertools.combinations(E,len(E)-(2*b-2)):
  G=nx.Graph();G.add_nodes_from(range(b));G.add_edges_from(e for e in E if e not in missing)
  if not nx.is_connected(G):continue
  defs=[4-G.degree(v) for v in range(b)]
  L=s.Matrix(nx.laplacian_matrix(G).toarray());Q=L[:-1,:-1].inv()
  for left in itertools.product(*[range(k+1) for k in defs]):
   if sum(left)!=2:continue
   right=[defs[i]-left[i] for i in range(b)]
   sigma=[left[i]-right[i] for i in range(b)]
   good=True
   for mask in range(1,2**b-1):
    S={v for v in range(b) if mask>>v&1}
    cut=sum((u in S)!=(v in S) for u,v in G.edges())
    a=abs(sum(sigma[v] for v in S))
    if a and cut<=a:good=False;break
   if not good:continue
   demand=s.Matrix([s.Rational(z,2) for z in sigma][:-1])
   en=(demand.T*Q*demand)[0]
   mx=max(mx,en);cnt+=1
 assert mx=={4:s.Rational(1,4),5:s.Rational(1,3)}[b]
 assert mx+s.Rational(1,2)<=s.Rational(3*b,16)
 result[b]={'count':cnt,'max_uniform_energy':str(mx)}
print(result)
