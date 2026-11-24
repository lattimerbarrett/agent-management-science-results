# Stand-alone finite check of the elementary shift-graph cyclic-lift lower construction.
import itertools, json
import networkx as nx
import numpy as np
from scipy.sparse import csr_matrix

k,m=6,8
words=list(itertools.combinations(range(m),k))
F=nx.Graph(); F.add_nodes_from(words)
for w in words:
    F.add_edges_from((w,w[1:]+(b,)) for b in range(w[-1]+1,m))
signs=list(itertools.product((-1,1),repeat=m))
def score(w,z): return sum((-1)**j*z[a] for j,a in enumerate(w))
S={w:{j for j,z in enumerate(signs) if score(w,z)>3} for w in words}
M=len(signs); counts={len(S[w]) for w in words}; assert len(counts)==1
L=counts.pop(); assert L>0
# All endpoints of odd walks of length one or three have disjoint supports.
for w in words:
    reach=set(F[w])
    for a in F[w]:
        for b in F[a]: reach.update(F[b])
    assert w not in reach
    assert all(S[w].isdisjoint(S[v]) for v in reach)
# Every edge has score_x + score_y of absolute value at most two.
assert all(abs(score(w,z)+score(v,z))<=2 for w,v in F.edges() for z in signs)
G=nx.Graph()
for i in range(3):
    G.add_nodes_from(('v',i,w) for w in words)
    G.add_edges_from((('U',i,j),('X',i,h)) for j in range(M) for h in range(L))
    G.add_edges_from((('v',i,w),('U',i,j)) for w in words for j in S[w])
for w,v in F.edges():
    G.add_edges_from((('v',i,w),('v',(i+1)%3,v)) for i in range(3))
A=nx.to_scipy_sparse_array(G,dtype=np.int64,format='csr'); A2=A@A; A3=A2@A
trace3=int(A.multiply(A2).sum()); trace5=int(A2.multiply(A3).sum())
assert trace3==trace5==0
assert min(dict(G.degree()).values())>=L
result=dict(k=k,m=m,base_vertices=len(F),base_edges=F.number_of_edges(),universe=M,support=L,vertices=len(G),edges=G.number_of_edges(),minimum_degree=min(dict(G.degree()).values()),trace_A3=trace3,trace_A5=trace5)
print(json.dumps(result,indent=2))
with open('workspace/agent4_lift_standalone.json','w') as f:json.dump(result,f,indent=2)
with open('workspace/agent4_lift_standalone.py','w') as f:f.write(open('scratchpad.py').read().split("with open('workspace/agent4_lift_standalone.py'")[0])
