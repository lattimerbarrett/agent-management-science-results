code = r'''from itertools import combinations, permutations, product
import numpy as np
import networkx as nx
from scipy.sparse import csr_matrix

def odd_traces(G):
    A=nx.to_scipy_sparse_array(G, format='csr', dtype=np.int64)
    A2=A@A; A3=A2@A
    return int(A.multiply(A2).sum()), int(A2.multiply(A3).sum())

def target_edge(x,y):
    a,A=x; b,B=y
    return b in A and a in B and not A&B

def check_upper():
    for k in range(1,6):
        V=[(a,frozenset(j for j in range(k) if mask>>j&1))
           for a in range(k) for mask in range(1<<k) if not(mask>>a&1)]
        H=nx.Graph(); H.add_nodes_from(range(len(V)))
        H.add_edges_from((i,j) for i,j in combinations(range(len(V)),2)
                         if target_edge(V[i],V[j]))
        assert sum(nx.triangles(H).values())==0
    checked=0
    for G in nx.graph_atlas_g():
        if len(G)==0 or odd_traces(G)!=(0,0): continue
        A=nx.to_numpy_array(G,dtype=np.int64)
        B=(A+A@A@A)>0
        F=nx.from_numpy_array(B)
        assert not nx.number_of_selfloops(F)
        col=nx.coloring.greedy_color(F)
        image={v:(col[v],frozenset(col[w] for w in G[v])) for v in G}
        assert all(target_edge(image[u],image[v]) for u,v in G.edges())
        checked+=1
    legal=0
    for k in range(1,6):
        pairs=list(combinations(range(k),2))
        for mask in range(1<<len(pairs)):
            adj=[0]*k
            for j,(u,v) in enumerate(pairs):
                if mask>>j&1: adj[u]|=1<<v; adj[v]|=1<<u
            def nb(S):
                ans=0
                for i in range(k):
                    if S>>i&1: ans|=adj[i]
                return ans
            for S,T,U in product(range(1,1<<k),repeat=3):
                if S&T or S&U or T&U: continue
                P,Q,R=nb(S),nb(T),nb(U)
                if P&Q or P&R or Q&R or (S|T|U)&nb(S|T|U): continue
                six=(S,T,U,P,Q,R)
                assert all(not(x&y) for x,y in combinations(six,2))
                assert sum(x.bit_count() for x in six)<=k
                legal+=1
    print('upper: atlas graphs',checked,'; six-set configurations',legal)

def shift(N,k):
    V=list(combinations(range(N),k)); ids={v:i for i,v in enumerate(V)}
    E=[(ids[t[:-1]],ids[t[1:]]) for t in combinations(range(N),k+1)]
    L=[set() for _ in V]
    perms=list(permutations(range(N)))
    for p,pi in enumerate(perms):
        rank={x:i for i,x in enumerate(pi)}
        for v,t in enumerate(V):
            if min(range(k),key=lambda i:rank[t[i]])%2==1: L[v].add(p)
    m=len(perms); r=m*(k-1)//(2*k)
    assert all(len(s)==r for s in L)
    assert all(not L[u]&L[v] for u,v in E)
    # Test each step of extension-color reduction, starting with singleton colors.
    colors={v:i for i,v in enumerate(V)}
    for j in range(k,1,-1):
        new={t:frozenset(colors[t+(x,)] for x in range(t[-1]+1,N))
             for t in combinations(range(N),j-1)}
        assert all(new[t[:-1]]!=new[t[1:]] for t in combinations(range(N),j))
        colors=new
    assert len(set(colors.values()))==N
    return L,E,m,r

def check_lower(N,k,q=1):
    L,E,m,r=shift(N,k)
    typ=[0]*len(L); D=nx.Graph(); D.add_nodes_from(range(len(L)))
    for u,v in E:
        a=len(L); b=a+1
        L.extend([L[v],L[u]]); typ.extend([1,2])
        D.add_edges_from([(u,a),(a,b),(b,v)])
    s=len(D)
    for a in D:
        for b in D[a]:
            for c in D[b]:
                for d in D[c]:
                    if typ[a]==typ[d]: assert not L[a]&L[d]
    G=D.copy(); nxt=s
    for i in range(3):
        W=[list(range(nxt+j*q,nxt+(j+1)*q)) for j in range(m)]
        nxt+=m*q; P=list(range(nxt,nxt+r*q)); nxt+=r*q
        G.add_nodes_from(x for cell in W for x in cell); G.add_nodes_from(P)
        G.add_edges_from((w,p) for cell in W for w in cell for p in P)
        G.add_edges_from((x,w) for x in D if typ[x]==i for j in L[x] for w in W[j])
    assert len(G)==s+3*(m+r)*q
    assert min(dict(G.degree()).values())>=r*q
    assert odd_traces(G)==(0,0)
    print('lower:',(N,k),'n=',len(G),'minimum degree=',min(dict(G.degree()).values()),
          'odd traces=',odd_traces(G))

if __name__=='__main__':
    check_upper()
    check_lower(4,3)
    check_lower(5,3)
'''
open('workspace/complete_checks.py','w').write(code)
exec(compile(code,'workspace/complete_checks.py','exec'))