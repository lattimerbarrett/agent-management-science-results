from pathlib import Path
code=r'''"""Self-contained finite verifications accompanying the proof.
Python 3 + NumPy.  No network, data files, or graph-theory packages.
The proof, not these finite tests, establishes the general statements.
"""
from itertools import combinations, permutations, product
from math import factorial
import numpy as np

def shift_instance(N,k):
    assert k>=3 and k%2
    vertices=list(combinations(range(N),k)); index={v:i for i,v in enumerate(vertices)}
    edges=[(index[t[:-1]],index[t[1:]]) for t in combinations(range(N),k+1)]
    cover=[set() for _ in vertices]
    for j,pi in enumerate(permutations(range(N))):
        rank={v:i for i,v in enumerate(pi)}
        for i,v in enumerate(vertices):
            if (max(range(k),key=lambda s:rank[v[s]])+1)%2==0:cover[i].add(j)
    m=factorial(N);p=m*(k-1)//(2*k)
    assert all(len(s)==p for s in cover)
    assert all(not(cover[u]&cover[v]) for u,v in edges)
    # Core, with nearest-endpoint labels.
    labels=[(0,i) for i in range(len(vertices))];core_edges=[]
    for u,v in edges:
        a=len(labels);labels.extend([(1,u),(2,v)])
        core_edges.extend([(u,a),(a,a+1),(a+1,v)])
    z=len(labels);n=z+3*(m+p);adj=[set() for _ in range(n)]
    def add(u,v):adj[u].add(v);adj[v].add(u)
    for u,v in core_edges:add(u,v)
    for t in range(3):
        base=z+t*(m+p)
        for i in range(m):
            for j in range(p):add(base+i,base+m+j)
    for u,(t,label) in enumerate(labels):
        for i in cover[label]:add(u,z+t*(m+p)+i)
    assert min(map(len,adj))>=p
    A=np.zeros((n,n),dtype=np.int64)
    for u in range(n):A[u,list(adj[u])]=1
    B=A@A; C=B@A
    assert np.trace(C)==0                   # no triangle
    assert np.sum(B*C.T)==0                 # tr(A^5)=0, no 5-cycle
    # Verify extension-color-set descent, starting with distinct colors.
    colors={v:i for i,v in enumerate(vertices)}
    for j in range(k-1,0,-1):
        colors={t:frozenset(colors[t+(y,)] for y in range(t[-1]+1,N))
                for t in combinations(range(N),j)}
        assert all(colors[t[:-1]]!=colors[t[1:]]
                   for t in combinations(range(N),j+1))
    assert len(set(colors.values()))==N
    return n,sum(map(len,adj))//2,min(map(len,adj))

def support_check(k=6):
    # Exhaust all reduced graphs on k vertices, then all triples of supports
    # with independent union (allowing overlap initially).
    pairs=list(combinations(range(k),2));graphs=cases=0
    for mask in range(1<<len(pairs)):
        a=[0]*k
        for j,(u,v) in enumerate(pairs):
            if mask>>j&1:a[u]|=1<<v;a[v]|=1<<u
        if not all(a):continue
        graphs+=1;nb=[0]*(1<<k)
        for s in range(1,1<<k):
            bit=s&-s;nb[s]=nb[s^bit]|a[bit.bit_length()-1]
        for U in range(1,1<<k):
            if U&nb[U]:continue
            verts=[v for v in range(k) if U>>v&1]
            for memberships in product(range(1,8),repeat=len(verts)):
                S=[0,0,0]
                for v,mem in zip(verts,memberships):
                    for i in range(3):
                        if mem>>i&1:S[i]|=1<<v
                if not all(S):continue
                T=[nb[s] for s in S]
                if any(T[i]&T[j] for i,j in combinations(range(3),2)):continue
                six=S+T
                assert all(six)
                assert all(not(six[i]&six[j]) for i,j in combinations(range(6),2))
                assert sum(s.bit_count() for s in six)<=k
                cases+=1
    return graphs,cases

def universal_target(q):
    verts=[(i,s) for i in range(q) for s in range(1<<q) if not(s>>i&1)]
    edges=set()
    for a,b in combinations(range(len(verts)),2):
        i,s=verts[a];j,t=verts[b]
        if t>>i&1 and s>>j&1 and not(s&t):edges.add((a,b))
    assert all(not(all(tuple(sorted(e)) in edges for e in combinations(t,2)))
               for t in combinations(range(len(verts)),3))
    return len(verts),len(edges)

if __name__=='__main__':
    for N,k in [(4,3),(5,3)]:print('shift',N,k,shift_instance(N,k))
    for q in range(1,5):print('target',q,universal_target(q))
    print('six-set reduced graphs/cases',support_check())
'''
Path('workspace/agent4_final_verify.py').write_text(code)
exec(compile(code,'workspace/agent4_final_verify.py','exec'))