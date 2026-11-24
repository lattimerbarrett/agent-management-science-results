import itertools as it, math, json
import numpy as np
import networkx as nx
from scipy.sparse import csr_matrix

def shift(k,m):
    V=list(it.combinations(range(m),k)); idx={x:i for i,x in enumerate(V)}
    F=nx.Graph();F.add_nodes_from(range(len(V)))
    for i,x in enumerate(V):
        for z in range(x[-1]+1,m):F.add_edge(i,idx[x[1:]+(z,)])
    return F,V

def odd3(F):
    W=nx.Graph();W.add_nodes_from(F)
    for u in F:
        reach=set(F[u])
        for a in F[u]:
            for b in F[a]:reach.update(F[b])
        assert u not in reach
        W.add_edges_from((u,v) for v in reach)
    return W

def traces(G):
    A=csr_matrix(nx.to_scipy_sparse_array(G,dtype=np.int64));A2=A@A;A3=A2@A
    return int(A.multiply(A2).sum()),int(A2.multiply(A3).sum())

# Shift graph, odd-walk score bound, and actual color-set recursion.
F,V=shift(7,11);W=odd3(F)
C=np.zeros((len(V),11),dtype=np.int64)
for i,x in enumerate(V):
    for j,z in enumerate(x):C[i,z]=(-1)**j
assert all(np.abs(C[a]+C[b]).sum()<=2 for a,b in F.edges())
assert all(np.abs(C[a]+C[b]).sum()<=6 for a,b in W.edges())
assert traces(F)==(0,0)
colors=nx.coloring.greedy_color(F)
for k in range(7,1,-1):
    lower,LV=shift(k-1,11); lookup={v:i for i,v in enumerate(V)}
    sets=[frozenset(colors[lookup[x+(z,)]] for z in range(x[-1]+1,11)) for x in LV]
    assert all(sets[a]!=sets[b] for a,b in lower.edges())
    names={s:i for i,s in enumerate(set(sets))}
    colors={i:names[s] for i,s in enumerate(sets)}; V=LV
assert len(set(colors.values()))==11

# Construct every support and the COMPLETE finite cyclic lift, not just a formula.
F,V=shift(7,8);M=1<<8
S=[]
for x in V:
    support=set()
    for z in range(M):
        score=sum((-1)**j*(1 if z>>a&1 else -1) for j,a in enumerate(x))
        if score>3:support.add(z)
    S.append(support)
assert set(map(len,S))=={16}
assert all(not S[a]&S[b] for a,b in odd3(F).edges())
G=nx.Graph()
for i in range(3):
    for u in range(M):
        for h in range(16):G.add_edge(('u',i,u),('h',i,h))
    for a in F:
        G.add_edges_from((('v',i,a),('u',i,u)) for u in S[a])
for a,b in F.edges():
    for i in range(3):G.add_edge(('v',i,a),('v',(i+1)%3,b))
assert traces(G)==(0,0)
assert min(dict(G.degree()).values())==16
assert len(G)==3*(len(F)+M+16)
for a,b in F.edges():
    assert all(G.has_edge(('v',i,a),('v',(i+1)%3,b)) for i in range(3))

# Check the universal triangle-free target for all t<=5.
for t in range(1,6):
    types=[(i,s) for i in range(t) for s in range(1<<t) if not(s>>i&1)]
    H=nx.Graph();H.add_nodes_from(types)
    for a,b in it.combinations(types,2):
        i,s=a;j,r=b
        if (s>>j&1) and (r>>i&1) and not(s&r):H.add_edge(a,b)
    assert sum(nx.triangles(H).values())==0

# Exhaust all reduced graphs through order 5 and all candidate hard profiles.
packing_graphs=0
for n in range(1,6):
    pairs=list(it.combinations(range(n),2))
    for bits in range(1<<len(pairs)):
        adj=[0]*n
        for j,(a,b) in enumerate(pairs):
            if bits>>j&1:adj[a]|=1<<b;adj[b]|=1<<a
        d=min(map(int.bit_count,adj))
        if d==0 or 9*d<=n:continue
        P=[]
        for a in range(1,1<<n):
            if a.bit_count()<2*d:continue
            na=0
            for i in range(n):
                if a>>i&1:na|=adj[i]
            if not(a&na):P.append((a,na))
        compatible=[set() for _ in P]
        for i,(a,na) in enumerate(P):
            for j in range(i):
                b,nb=P[j]
                if not(a&b or na&nb or a&nb or b&na):
                    compatible[i].add(j);compatible[j].add(i)
        assert all(not(compatible[i]&compatible[j]) for i in range(len(P)) for j in compatible[i])
        packing_graphs+=1

ratios=[]
for k in (7,31,127,511,2047):
    numerator=sum(math.comb(k,j) for j in range((k+3)//2+1,k+1))
    p=numerator/(1<<k)
    ratios.append((k,p,p/(3*(1+p))))
result={'shift':{'vertices':330,'edges':165,'W3_edges':W.number_of_edges()},'lift':{'vertices':len(G),'edges':G.number_of_edges(),'min_degree':16,'traces_3_5':traces(G)},'packing_graphs':packing_graphs,'score_ratios':ratios}
print(json.dumps(result,indent=2))
from pathlib import Path
Path('workspace/agent1_final_checks.py').write_text(Path('scratchpad.py').read_text())
Path('workspace/agent1_final_checks.json').write_text(json.dumps(result,indent=2))
