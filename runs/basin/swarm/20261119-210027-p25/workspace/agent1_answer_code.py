from itertools import combinations
from math import comb
import networkx as nx
import numpy as np
from scipy.sparse import csr_matrix

def shift(k,m):
    V=list(combinations(range(m),k)); ix={v:i for i,v in enumerate(V)}
    F=nx.Graph(); F.add_nodes_from(range(len(V)))
    for a in combinations(range(m),k+1): F.add_edge(ix[a[:-1]],ix[a[1:]])
    return F,V

def W3(F):
    W=nx.Graph(); W.add_nodes_from(F)
    for u in F:
        r=set(F[u])
        for a in F[u]:
            for b in F[a]: r.update(F[b])
        assert u not in r
        W.add_edges_from((u,v) for v in r)
    return W

def traces(G):
    A=csr_matrix(nx.to_scipy_sparse_array(G,dtype=np.int64))
    B=A@A; C=B@A
    return int(A.multiply(B).sum()),int(B.multiply(C).sum())

# Exact shift identities and the color-set reduction.
F,V=shift(7,11); W=W3(F)
coeff=np.zeros((len(V),11),dtype=int)
for i,a in enumerate(V):
    for j,x in enumerate(a): coeff[i,x]=(-1)**j
assert all(abs(coeff[u]+coeff[v]).sum()<=2 for u,v in F.edges())
assert all(abs(coeff[u]+coeff[v]).sum()<=6 for u,v in W.edges())
assert traces(F)==(0,0)
color=nx.coloring.greedy_color(F)
for k in range(7,1,-1):
    Q,U=shift(k-1,11); ix={v:i for i,v in enumerate(V)}
    sets=[frozenset(color[ix[a+(z,)]] for z in range(a[-1]+1,11)) for a in U]
    assert all(sets[u]!=sets[v] for u,v in Q.edges())
    ids={s:i for i,s in enumerate(set(sets))}
    color={i:ids[s] for i,s in enumerate(sets)}; V=U
assert len(set(color.values()))==11

# Build every sign support, then the entire finite lower-bound graph.
F,V=shift(7,8); M=256
S=[{z for z in range(M) if sum((-1)**j*(1 if z>>a&1 else -1)
      for j,a in enumerate(v))>3} for v in V]
assert set(map(len,S))=={16}
assert all(not S[u]&S[v] for u,v in W3(F).edges())
G=nx.Graph()
for i in range(3):
    G.add_edges_from((('u',i,z),('h',i,h)) for z in range(M) for h in range(16))
    G.add_edges_from((('v',i,a),('u',i,z)) for a in F for z in S[a])
for a,b in F.edges():
    G.add_edges_from((('v',i,a),('v',(i+1)%3,b)) for i in range(3))
assert traces(G)==(0,0)
assert min(dict(G.degree()).values())==16
print('Actual lift:',len(G),G.number_of_edges(),traces(G))

# Universal targets are triangle-free.
for t in range(1,6):
    T=[(i,s) for i in range(t) for s in range(1<<t) if not s>>i&1]
    H=nx.Graph(); H.add_nodes_from(T)
    for (i,s),(j,r) in combinations(T,2):
        if s>>j&1 and r>>i&1 and not s&r:H.add_edge((i,s),(j,r))
    assert sum(nx.triangles(H).values())==0

# Exhaust every reduced graph through order 6 and all admissible triples.
ng=nt=0
for n in range(1,7):
    E=list(combinations(range(n),2))
    for mask in range(1<<len(E)):
        N=[0]*n
        for j,(u,v) in enumerate(E):
            if mask>>j&1:N[u]|=1<<v;N[v]|=1<<u
        d=min(map(int.bit_count,N))
        if not d:continue
        ng+=1; P=[]
        for a in range(1,1<<n):
            na=0
            for u in range(n):
                if a>>u&1:na|=N[u]
            if not a&na:P.append((a,na))
        for (a,na),(b,nb),(c,nc) in combinations(P,3):
            blocks=[a,b,c,na,nb,nc]
            if any(x&y for x,y in combinations(blocks,2)):continue
            assert sum(map(int.bit_count,blocks))<=n
            assert a.bit_count()+b.bit_count()+c.bit_count()+3*d<=n
            nt+=1
print('Reduced graphs / six-block triples:',ng,nt)
for k in (7,31,127,511,2047):
    p=sum(comb(k,j) for j in range((k+5)//2,k+1))/(1<<k)
    print('k, support fraction, limiting density:',k,p,p/(3*(1+p)))
from pathlib import Path
Path('workspace/agent1_answer_code.py').write_text(Path('scratchpad.py').read_text())
