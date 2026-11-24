"""Explicit lower-bound construction and exact finite-instance checks."""
import itertools
import numpy as np
from scipy.sparse import csr_matrix

def kneser(m,r):
    sets=list(map(frozenset,itertools.combinations(range(m),r)))
    edges=[(u,v) for u in range(len(sets)) for v in range(u+1,len(sets)) if sets[u].isdisjoint(sets[v])]
    return sets,edges

def construct(m,r,q=1):
    """W_i has m*q vertices, P_i has r*q; skeleton 3-subdivides KG(m,r)."""
    sets,edges=kneser(m,r)
    return construct_from_labels(sets,edges,m,r,q)

def construct_from_labels(sets,edges,m,r,q=1):
    assert all(len(s)==r for s in sets)
    assert all(set(sets[u]).isdisjoint(sets[v]) for u,v in edges)
    types=[0]*len(sets)
    labels=list(sets)
    skeleton=[]
    for u,v in edges:
        a=len(types); b=a+1
        types.extend([1,2]); labels.extend([sets[v],sets[u]])
        skeleton.extend([(u,a),(a,b),(b,v)])
    core_n=len(types)
    adj=[set() for _ in range(core_n)]
    def vertex():
        adj.append(set()); return len(adj)-1
    def add(u,v):
        assert u!=v
        adj[u].add(v); adj[v].add(u)
    for u,v in skeleton: add(u,v)
    for i in range(3):
        W=[[vertex() for _ in range(q)] for j in range(m)]
        P=[vertex() for _ in range(r*q)]
        for cell in W:
            for w in cell:
                for p in P: add(w,p)
        for x in range(core_n):
            if types[x]==i:
                for j in labels[x]:
                    for w in W[j]: add(x,w)
    return adj, dict(m=m,r=r,q=q,core_n=core_n,types=types,labels=labels,skeleton=skeleton,branch_n=len(sets),F_edges=edges)

def check_symbolic_core(data):
    n=data['core_n']; adj=[set() for _ in range(n)]
    for u,v in data['skeleton']: adj[u].add(v);adj[v].add(u)
    count=0
    for a in range(n):
        for b in adj[a]:
            for c in adj[b]:
                for d in adj[c]:
                    if data['types'][a]==data['types'][d]:
                        assert data['labels'][a].isdisjoint(data['labels'][d])
                        count+=1
    for u,v in data['F_edges']:
        assert any(v in adj[b] for a in adj[u] for b in adj[a])
    return count

def check_no_C3_C5(adj):
    n=len(adj)
    rows=[];cols=[]
    for u in range(n):
        for v in adj[u]: rows.append(u);cols.append(v)
    A=csr_matrix((np.ones(len(rows),dtype=np.int64),(rows,cols)),shape=(n,n))
    A2=A@A; A3=A2@A
    # trace(A^3) and trace(A^5) count all closed odd walks, not just induced cycles.
    t3=int(A.multiply(A2).sum())
    t5=int(A2.multiply(A3).sum())
    assert t3==0 and t5==0,(t3,t5)
    return t3,t5

def verify(m,r,q):
    adj,data=construct(m,r,q)
    assert min(map(len,adj))>=r*q
    assert len(adj)==data['core_n']+3*(m+r)*q
    count=check_symbolic_core(data)
    traces=check_no_C3_C5(adj)
    return dict(m=m,r=r,q=q,n=len(adj),minimum_degree=min(map(len,adj)),ratio=min(map(len,adj))/len(adj),limit=r/(3*(m+r)),same_type_3walks=count,odd_traces=traces)

def shift_representation(N,k):
    assert k%2==1 and 1<k<=N
    vertices=list(itertools.combinations(range(N),k))
    ids={v:i for i,v in enumerate(vertices)}
    edges=[(ids[t[:-1]],ids[t[1:]]) for t in itertools.combinations(range(N),k+1)]
    labels=[set() for _ in vertices]
    for p,permutation in enumerate(itertools.permutations(range(N))):
        rank={v:i for i,v in enumerate(permutation)}
        for i,v in enumerate(vertices):
            minpos=min(range(k),key=lambda j:rank[v[j]])
            if minpos%2==1: labels[i].add(p)
    m=p+1; r=m*(k-1)//(2*k)
    assert all(len(label)==r for label in labels)
    assert all(labels[u].isdisjoint(labels[v]) for u,v in edges)
    return labels,edges,m,r

def extension_coloring(N,k,colors):
    """Verify the elementary chromatic reduction for any supplied proper coloring."""
    vs=list(itertools.combinations(range(N),k))
    assert set(colors)==set(vs)
    for t in itertools.combinations(range(N),k+1):
        assert colors[t[:-1]]!=colors[t[1:]]
    reduced={t:frozenset(colors[t+(x,)] for x in range(t[-1]+1,N))
             for t in itertools.combinations(range(N),k-1)}
    for t in itertools.combinations(range(N),k):
        assert reduced[t[:-1]]!=reduced[t[1:]]
    return reduced
