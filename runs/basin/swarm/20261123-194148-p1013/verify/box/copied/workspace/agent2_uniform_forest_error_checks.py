import networkx as nx,itertools,math,json,time
from pathlib import Path
C=lambda a,b:math.comb(a,b) if 0<=b<=a else 0
cnt=0;ng=0;st=time.time()
for G in nx.graph_atlas_g():
 if len(G)>6:continue
 ng+=1;es=list(G.edges());M=len(es);D=max(dict(G.degree()).values(),default=0)
 adjpairs=[frozenset((i,j)) for i in range(M) for j in range(i+1,M) if set(es[i])&set(es[j])]
 w=len(adjpairs);N3=N4=0
 for a,b in itertools.combinations(adjpairs,2):
  if len(a|b)==3:N3+=1
  else:N4+=1
 assert N3<=M*C(max(0,2*D-2),2)
 assert N4<=C(w,2)
 S=[0]*(M+1)
 for mask in range(1<<M):
  ids=[i for i in range(M) if mask>>i&1];j=len(ids);degs={};parent=list(range(len(G)));forest=True
  def find(x):
   while parent[x]!=x:x=parent[x]
   return x
  for i in ids:
   a,b=es[i];degs[a]=degs.get(a,0)+1;degs[b]=degs.get(b,0)+1
   aa,bb=find(a),find(b)
   if aa==bb:forest=False
   else:parent[aa]=bb
  wa=sum(C(d,2) for d in degs.values())
  linear=forest and max(degs.values(),default=0)<=2
  W=(1<<(j-wa)) if linear else 0
  ideal=(1<<j)-(1<<(j-1))*wa if j else 1
  assert abs(W-ideal)<=(1<<j)*C(wa,2)
  S[j]+=W;cnt+=1
 for j in range(M+1):
  ideal=(1<<j)*C(M,j)-(1<<(j-1))*w*C(M-2,j-2) if j else 1
  bd=(1<<j)*(N3*C(M-3,j-3)+N4*C(M-4,j-4))
  assert abs(S[j]-ideal)<=bd
out={'graphs':ng,'edge_subsets':cnt,'max_vertices':6,'seconds':time.time()-st}
print(out)
Path('workspace/agent2_uniform_forest_error_checks.json').write_text(json.dumps(out,indent=2))
Path('workspace/agent2_uniform_forest_error_checks.py').write_text(Path(__file__).read_text())
