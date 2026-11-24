import itertools as it
from fractions import Fraction
import networkx as nx
from z3 import Solver, Int, Distinct, sat


def odd3(G):
    J=nx.Graph(); J.add_nodes_from(G)
    for x in G:
        for a in G[x]:
            for b in G[a]:
                for y in G[b]:
                    assert x!=y, 'triangle / closed 3-walk'
                    J.add_edge(x,y)
    return J

def no_cycle(G,l):
    for s in G:
        def dfs(path):
            if len(path)==l:
                return s not in G[path[-1]]
            for v in G[path[-1]]:
                if v not in path and not dfs(path+[v]): return False
            return True
        if not dfs([s]): return False
    return True

def colorable(G,q):
    z={v:Int('x'+str(i)) for i,v in enumerate(G)}
    so=Solver(); so.add(*[a>=0 for a in z.values()],*[a<q for a in z.values()])
    so.add(*[z[u]!=z[v] for u,v in G.edges()])
    return so.check()==sat

def lower(m,k,t=1):
    sets=list(it.combinations(range(m),k))
    F=nx.Graph(); F.add_nodes_from(range(len(sets)))
    for i,j in it.combinations(range(len(sets)),2):
        if set(sets[i]).isdisjoint(sets[j]): F.add_edge(i,j)
    G=nx.Graph(); typ={}; lab={}
    for i,S in enumerate(sets):
        v=('v',i); G.add_node(v); typ[v]=0;lab[v]=S
    for i,j in F.edges():
        a=('a',i,j);b=('b',i,j)
        G.add_edges_from([(('v',i),a),(a,b),(b,('v',j))])
        typ[a]=1;typ[b]=2;lab[a]=sets[i];lab[b]=sets[j]
    core=list(G)
    for h in range(3):
        R=[('R',h,i,s) for i in range(m) for s in range(t)]
        B=[('B',h,s) for s in range(k*t)]
        G.add_nodes_from(R+B)
        G.add_edges_from(it.product(R,B))
    for v in core:
        G.add_edges_from((v,('R',typ[v],i,s)) for i in lab[v] for s in range(t))
    return G,F

def universal_image(G,col):
    sig={v:(col[v],frozenset(col[w] for w in G[v])) for v in G}
    H=nx.Graph();H.add_nodes_from(sig.values())
    for x,y in it.combinations(H,2):
        i,S=x;j,T=y
        if i in T and j in S and S.isdisjoint(T):H.add_edge(x,y)
    assert all(H.has_edge(sig[u],sig[v]) for u,v in G.edges())
    assert sum(nx.triangles(H).values())==0
    return H

def density(G,A,B):
    return Fraction(sum(G.has_edge(a,b) for a in A for b in B),len(A)*len(B))

def subsets(A):
    A=list(A)
    for mask in range(1,1<<len(A)):
        yield frozenset(A[i] for i in range(len(A)) if mask>>i&1)

def irregular_witness(G,A,B,eps):
    base=density(G,A,B)
    for X in subsets(A):
        if len(X)<eps*len(A):continue
        for Y in subsets(B):
            if len(Y)>=eps*len(B) and abs(density(G,X,Y)-base)>eps:
                return X,Y
    return None

def energy(G,parts):
    n=len(G)
    return sum(Fraction(len(A)*len(B),n*n)*density(G,A,B)**2
               for A in parts for B in parts)

def weighted_regularity(G,parts,eps):
    steps=0
    while True:
        cuts=[[] for A in parts]; badmass=0
        for i,j in it.combinations(range(len(parts)),2):
            w=irregular_witness(G,parts[i],parts[j],eps)
            if w:
                cuts[i].append(w[0]);cuts[j].append(w[1])
                badmass+=2*len(parts[i])*len(parts[j])
        if badmass<=eps*len(G)**2:return parts,steps
        old=energy(G,parts); new=[]
        for A,C in zip(parts,cuts):
            atoms=[frozenset(A)]
            for X in C:
                atoms=[Z for Y in atoms for Z in (Y&X,Y-X) if Z]
            new+=atoms
        parts=new; steps+=1
        assert energy(G,parts)-old>eps**5
        assert steps<1/eps**5+1

def check_signature_coloring(G,parts,R,c,rho):
    n=len(G);alpha=rho;beta=c-2*rho;gamma=c-rho
    S={v:frozenset(i for i,A in enumerate(parts)
                   if len(set(G[v])&set(A))>=alpha*len(A)) for v in G}
    weight=lambda P:sum(len(parts[i]) for i in P)
    NR=lambda P:set().union(*(set(R[i]) for i in P))
    assert min(weight(R[i]) for i in R)>=gamma*n
    assert n-sum(map(len,parts))<=rho*n
    for u,v in G.edges():assert NR(S[u]).isdisjoint(NR(S[v]))
    for u in G:
        for v in G:
            if u==v or set(G[u])&set(G[v]):
                assert not any(R.has_edge(i,j) for i in S[u] for j in S[v])
    J=odd3(G)
    W={v for v in G if weight(S[v])<2*beta*n}
    assert all(S[u]!=S[v] for u,v in J.edges() if u in W and v in W)
    sig={v:(S[v],frozenset(S[w] for w in G[v] if w in W),
                   frozenset(S[w] for w in G[v])) for v in G}
    assert all(sig[u]!=sig[v] for u,v in J.edges())
    colors={s:i for i,s in enumerate(set(sig.values()))}
    universal_image(G,{v:colors[sig[v]] for v in G})
    p=2**len(parts)
    assert len(colors)<=p*2**(2*p)


def check_support_counting():
    count=0
    for R in nx.graph_atlas_g():
        n=len(R)
        if not (1<=n<=6) or min(dict(R.degree()).values())==0:continue
        full=(1<<n)-1
        adj=[sum(1<<j for j in R[i]) for i in range(n)]
        neigh={S:0 for S in range(1<<n)}
        for S in range(1<<n):
            for i in range(n):
                if S>>i&1:neigh[S]|=adj[i]
        ind=[S for S in range(1,1<<n) if not S&neigh[S]]
        for P,Q,T in it.product(ind,repeat=3):
            NP,NQ,NT=neigh[P],neigh[Q],neigh[T]
            if NP&NQ or NP&NT or NQ&NT:continue
            U=P|Q|T
            if U&neigh[U]:continue
            regions=[P,Q,T,NP,NQ,NT]
            assert all(not (A&B) for A,B in it.combinations(regions,2))
            assert sum(A.bit_count() for A in regions)<=n
            count+=1
    R=nx.disjoint_union_all([nx.star_graph(2) for _ in range(3)])
    Ps=[{1,2},{4,5},{7,8}]
    Ns=[set().union(*(set(R[v]) for v in P)) for P in Ps]
    assert sum(map(len,Ps+Ns))==len(R)==9
    print('support counting checked:',count,'configurations; equality template has 9 vertices')

def check_large_parameter_arithmetic(c,h):
    k=int(3*c*(h-1)/(1-9*c))+1
    m=2*k+h-1
    import math
    v=math.comb(m,k); e=v*math.comb(m-k,k)//2
    core=v+2*e
    gap=k-3*c*(m+k)
    t=int(c*core/gap)+1
    assert gap>0 and k*t>c*(3*(m+k)*t+core)
    assert m-2*k+2==h+1
    print('large lower-bound parameters checked:', 'c='+str(c),'h='+str(h),'k='+str(k),
          't has',len(str(t)),'decimal digits')

if __name__=='__main__':
    for m,k in [(3,1),(5,2),(6,2),(7,3)]:
        G,F=lower(m,k)
        assert len(G)==len(F)+2*F.number_of_edges()+3*(m+k)
        assert min(dict(G.degree()).values())>=k
        assert no_cycle(G,3) and no_cycle(G,5)
        J=odd3(G)
        assert all(J.has_edge(('v',i),('v',j)) for i,j in F.edges())
        chi=m-2*k+2
        assert colorable(F,chi) and not colorable(F,chi-1)
        print('lower checked:',m,k,'core chromatic',chi,'G order',len(G),'degree',min(dict(G.degree()).values()))
    cnt=0
    for G in nx.graph_atlas_g():
        if G and no_cycle(G,3) and no_cycle(G,5):
            J=odd3(G)
            col=nx.coloring.greedy_color(J,strategy='largest_first')
            universal_image(G,col);cnt+=1
    print('universal image checked on',cnt,'atlas graphs')
    for c in [Fraction(1,9)+Fraction(1,10000),Fraction(1,8),Fraction(1,5),Fraction(1,2)]:
        rho=min((9*c-1)/30,Fraction(1,100))
        assert rho>0 and 9*c-15*rho>1 and c-2*rho>0
    print('rational slack checked')
    check_support_counting()
    G=nx.complete_bipartite_graph(4,4)
    check_signature_coloring(G,[set(range(4)),set(range(4,8))],nx.path_graph(2),Fraction(1,2),Fraction(1,100))
    G=nx.cycle_graph(7)
    check_signature_coloring(G,[{i} for i in G],G,Fraction(1,4),Fraction(1,100))
    print('upper signature construction checked on K4,4 and C7')
    G=nx.gnp_random_graph(12,Fraction(1,3),seed=19)
    parts,steps=weighted_regularity(G,[frozenset(range(i,i+3)) for i in range(0,12,3)],Fraction(1,5))
    print('weighted regularity exact-rational energy increments checked:',steps,'steps,',len(parts),'parts')
    for c,h in [(Fraction(1,10),4),(Fraction(1,9)-Fraction(1,1000),10)]:
        check_large_parameter_arithmetic(c,h)
