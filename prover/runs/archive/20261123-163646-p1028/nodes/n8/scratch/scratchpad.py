import networkx as nx
import sympy as sp
import pickle

atlas=nx.graph_atlas_g()
blocks=[]
for G in atlas:
    k=len(G)
    if k<2 or not nx.is_connected(G):continue
    if k!=2 and not nx.is_biconnected(G):continue
    L=sp.zeros(k)
    for u,v in G.edges():
        L[u,u]+=1;L[v,v]+=1;L[u,v]-=1;L[v,u]-=1
    Q=(L+sp.ones(k,k)/k).inv()
    R=[[Q[u,u]+Q[v,v]-2*Q[u,v] for v in range(k)] for u in range(k)]
    blocks.append((k,[G.degree(v) for v in range(k)],R))
print('blocks through order 7:',len(blocks),flush=True)

def addsets(A,B,limit):
    return {a+b for a in A for b in B if a+b<=limit}

def rooted_sets(n,d,bs):
    limit=n-1
    F=[set() for _ in range(d+1)];F[0]={0}
    while True:
        C=[set() for _ in range(d+1)]
        for k,ds,R in bs:
            for u in range(k):
                costs={k-1}
                for v in range(k):
                    if v!=u:costs=addsets(costs,F[d-ds[v]],limit)
                C[ds[u]]|=costs
        new=[set() for _ in range(d+1)];new[0]={0}
        for r in range(1,d+1):
            for s in range(1,r+1):new[r]|=addsets(C[s],new[r-s],limit)
        if new==F:return F
        F=new

def block_opt(n,d):
    bs=[B for B in blocks if B[0]<=n and max(B[1])<=d]
    F=rooted_sets(n,d,bs)
    K={}
    for k,ds,R in bs:
        for u in range(k):
            for v in range(k):
                if u==v:continue
                costs={k-2}
                for w in range(k):
                    if w!=u and w!=v:costs=addsets(costs,F[d-ds[w]],n-2)
                for cost in costs:
                    key=(ds[u],ds[v],cost)
                    K[key]=max(K.get(key,-1),R[u][v])
    # DP size counts all vertices except the two current endpoints.
    dp=[{} for _ in range(n-1)]
    for (s,t,k),r in K.items():
        for a in F[d-s]:
            if a+k<=n-2:dp[a+k][t]=max(dp[a+k].get(t,-1),r)
    for used in range(n-1):
        for t,r in list(dp[used].items()):
            for (s,t2,k),r2 in K.items():
                if t+s>d:continue
                for a in F[d-t-s]:
                    new=used+1+a+k
                    if new<=n-2:dp[new][t2]=max(dp[new].get(t2,-1),r+r2)
    best=-1
    for used in range(n-1):
        for t,r in dp[used].items():
            if n-2-used in F[d-t]:best=max(best,r)
    return n*d*best if best!=-1 else None

def brute(n,d):
    best=None
    for G in atlas:
        if len(G)!=n or not nx.is_connected(G) or set(dict(G.degree()).values())!={d}:continue
        L=sp.zeros(n)
        for u,v in G.edges():
            L[u,u]+=1;L[v,v]+=1;L[u,v]-=1;L[v,u]-=1
        Q=(L+sp.ones(n,n)/n).inv()
        val=n*d*max(Q[u,u]+Q[v,v]-2*Q[u,v] for u in range(n) for v in range(n))
        if best is None or val>best:best=val
    return best

for n in range(3,8):
    for d in range(2,n):
        if n*d%2:continue
        a=block_opt(n,d);b=brute(n,d)
        print('exact test',n,d,a,b,'PASS' if a==b else 'FAIL',flush=True)
        assert a==b
for n in [10,12,14,15,16,17,18,19,20,21]:
    d=3 if n%2==0 else 4
    print('blocks <=7 lower bound:',n,d,block_opt(n,d),flush=True)

# Independently check the exponential-generating-function block expansion.
from fractions import Fraction as Fr
from collections import defaultdict
from math import factorial

def gf_count(n,d):
    m=n-2
    zero=lambda:[Fr(0)]*(m+1)
    one=zero();one[0]=Fr(1)
    def plus(a,b):return [x+y for x,y in zip(a,b)]
    def times(a,b):return [sum((a[j]*b[i-j] for j in range(i+1)),Fr(0)) for i in range(m+1)]
    def scale(a,c):return [c*x for x in a]
    def shift(a,k):return [Fr(0)]*k+a[:m+1-k] if k<=m else zero()
    groups1=defaultdict(Fr);groups2=defaultdict(Fr)
    for G in atlas:
        k=len(G)
        if k<2 or k>n or max(dict(G.degree()).values())>d:continue
        if not nx.is_connected(G) or (k!=2 and not nx.is_biconnected(G)):continue
        aut=sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(G,G).isomorphisms_iter())
        ds=[G.degree(v) for v in range(k)]
        for u in range(k):
            rest=tuple(sorted(d-ds[v] for v in range(k) if v!=u))
            groups1[k,ds[u],rest]+=Fr(1,aut)
            for v in range(k):
                if u==v:continue
                rest=tuple(sorted(d-ds[w] for w in range(k) if w not in [u,v]))
                groups2[k,ds[u],ds[v],rest]+=Fr(1,aut)
    F=[zero() for _ in range(d+1)];F[0]=one
    for it in range(n):
        U=[zero() for _ in range(d+1)]
        for (k,s,rest),coef in groups1.items():
            p=one
            for r in rest:p=times(p,F[r])
            U[s]=plus(U[s],scale(shift(p,k-1),coef))
        new=[zero() for _ in range(d+1)];new[0]=one
        for r in range(1,d+1):
            for s in range(1,r+1):new[r]=plus(new[r],scale(times(U[s],new[r-s]),Fr(s,r)))
        F=new
    K=[[zero() for _ in range(d+1)] for _ in range(d+1)]
    for (k,s,t,rest),coef in groups2.items():
        p=one
        for r in rest:p=times(p,F[r])
        K[s][t]=plus(K[s][t],scale(shift(p,k-2),coef))
    # row vector f^T K, then sum f^T K (J K)^ell f.
    row=[zero() for _ in range(d+1)]
    for s in range(1,d+1):
        for t in range(1,d+1):row[t]=plus(row[t],times(F[d-s],K[s][t]))
    total=zero()
    for ell in range(n-1):
        for t in range(1,d+1):total=plus(total,times(row[t],F[d-t]))
        middle=[zero() for _ in range(d+1)]
        for t in range(1,d+1):
            for s in range(1,d-t+1):middle[s]=plus(middle[s],shift(times(row[t],F[d-t-s]),1))
        row=[zero() for _ in range(d+1)]
        for s in range(1,d+1):
            for t in range(1,d+1):row[t]=plus(row[t],times(middle[s],K[s][t]))
    predicted=total[m]*factorial(m)
    actual=0
    for G in atlas:
        if len(G)!=n or not nx.is_connected(G) or set(dict(G.degree()).values())!={d}:continue
        aut=sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(G,G).isomorphisms_iter())
        actual+=factorial(n)//aut
    print('GF labelled count test',n,d,predicted,actual,flush=True)
    assert predicted==actual
for n,d in [(4,2),(4,3),(5,2),(5,4),(6,2),(6,3),(6,4),(6,5),(7,2),(7,4),(7,6)]:gf_count(n,d)
