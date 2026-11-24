import itertools
import networkx as nx
import numpy as np

def universal(t):
    nodes=[(a,S) for a in range(t) for S in range(1<<t) if not(S>>a&1)]
    H=nx.Graph(); H.add_nodes_from(nodes)
    for (a,S),(b,T) in itertools.combinations(nodes,2):
        if (S>>b&1) and (T>>a&1) and not(S&T):
            H.add_edge((a,S),(b,T))
    assert sum(nx.triangles(H).values())==0
    return H
Hs={t:universal(t) for t in range(1,8)}
print('universal triangle-free targets: (t, vertices, edges)')
for t,H in Hs.items(): print(t,len(H),H.number_of_edges())
count=0; hist={}
for G in nx.graph_atlas_g():
    n=len(G)
    if not n: continue
    A=nx.to_numpy_array(G,nodelist=range(n),dtype=np.int64)
    A3=A@A@A
    if np.trace(A3) or np.trace(A3@A@A): continue
    J=nx.from_numpy_array(((A+A3)>0).astype(int))
    assert nx.number_of_selfloops(J)==0
    colors=nx.coloring.greedy_color(J,strategy='largest_first')
    t=1+max(colors.values())
    f={v:(colors[v],sum(1<<a for a in {colors[w] for w in G[v]})) for v in G}
    assert all(f[v] in Hs[t] for v in G)
    assert all(Hs[t].has_edge(f[u],f[v]) for u,v in G.edges())
    count+=1;hist[t]=hist.get(t,0)+1
print('atlas graphs with no C3/C5 checked:',count)
print('wide-color counts:',hist)
from fractions import Fraction
from math import comb
from scipy.sparse import csr_matrix

def probability(k):
    assert k % 2 == 0
    return Fraction((1 << k) - comb(k,k//2) - 2*comb(k,k//2+1), 1 << (k+1))

print('Exact lower-bound parameters:')
for c in [Fraction(1,20), Fraction(1,10), Fraction(21,200), Fraction(11,100)]:
    k=4
    while probability(k) <= 3*c/(1-3*c): k*=2
    p=probability(k)
    assert p-3*c*(1+p)>0
    print('c=',float(c),'k=',k,'p=',float(p),'limiting degree=',float(p/(3*(1+p))))

def lower_example(m,k,multiplicity=1):
    F=nx.Graph()
    F.add_nodes_from(itertools.combinations(range(m),k))
    directed=[]
    for w in itertools.combinations(range(m),k+1):
        a,b=w[:-1],w[1:]
        F.add_edge(a,b); directed.append((a,b))
    Q=nx.Graph(); groups={}; labels={}
    for x in F:
        v=('x',x); Q.add_node(v); groups[v]=0; labels[v]=x
    for j,(a,b) in enumerate(directed):
        y,z=('y',j),('z',j)
        Q.add_edges_from([(('x',a),y),(y,z),(z,('x',b))])
        groups[y]=1;groups[z]=2;labels[y]=b;labels[z]=a
    assert all(groups[u]!=groups[v] for u,v in Q.edges())
    assert all(F.has_edge(labels[u],labels[v]) for u,v in Q.edges())
    G=Q.copy(); N=multiplicity*(1<<m); p=probability(k)
    vsize=p*N; assert vsize.denominator==1; vsize=int(vsize)
    for i in range(3):
        U=[('u',i,mask,r) for mask in range(1<<m) for r in range(multiplicity)]
        V=[('v',i,r) for r in range(vsize)]
        G.add_nodes_from(U+V)
        G.add_edges_from(itertools.product(U,V))
        for x in Q:
            if groups[x]!=i:continue
            for u in U:
                mask=u[2]
                score=sum((-1 if j%2==0 else 1)*(1 if mask>>a&1 else -1)
                          for j,a in enumerate(labels[x]))
                if score>3:G.add_edge(x,u)
    assert len(G)==len(Q)+3*(1+p)*N
    assert min(dict(G.degree()).values())>=p*N
    A=nx.to_scipy_sparse_array(G,dtype=np.int64,format='csr')
    A2=A@A; A3=A2@A
    assert int(A3.diagonal().sum())==0
    assert int(A3.multiply(A2.T).sum())==0
    # Check each of the score inequalities used in the proof.
    for mask in range(1<<m):
        h={x:sum((-1 if j%2==0 else 1)*(1 if mask>>a&1 else -1)
                 for j,a in enumerate(x)) for x in F}
        assert all(abs(h[a]+h[b])<=2 for a,b in F.edges())
        for a in F:
            for b in F[a]:
                for d in F[b]:
                    for e in F[d]:assert abs(h[a]+h[e])<=6
    print('Lower example:', 'm=',m,'k=',k,'copies=',multiplicity,
          'n=',len(G),'min_degree=',min(dict(G.degree()).values()),
          'C3 count=0, C5 count=0')
    return F,Q,G

lower_example(6,4,2)

# Exercise the non-bipartite three-type configuration in the upper proof.
F=nx.Graph();F.add_nodes_from(itertools.combinations(range(9),4))
for w in itertools.combinations(range(9),5):F.add_edge(w[:-1],w[1:])
print('Shift graph S(9,4):',len(F),'vertices,',F.number_of_edges(),
      'edges; bipartite =',nx.is_bipartite(F))
assert not nx.is_bipartite(F)

# Exhaust the color-set descent for every proper 3-coloring of S(5,2).
vertices=list(itertools.combinations(range(5),2))
E=[(w[:-1],w[1:]) for w in itertools.combinations(range(5),3)]
proper=0
for values in itertools.product(range(3),repeat=len(vertices)):
    q=dict(zip(vertices,values))
    if any(q[a]==q[b] for a,b in E):continue
    sets={a:frozenset(q[(a,b)] for b in range(a+1,5)) for a in range(5)}
    assert len(set(sets.values()))==5  # S(5,1)=K5
    proper+=1
print('Color-set descent: checked all',proper,'proper 3-colorings of S(5,2).')

# Verify all robust-path/type axioms in atlas graphs, using R=G, S_v=N(v).
axiom_graphs=0
for G in nx.graph_atlas_g():
    if not len(G) or min(dict(G.degree()).values())==0:continue
    A=nx.to_numpy_array(G,dtype=np.int64); A2=A@A; A3=A2@A
    if np.trace(A3) or np.trace(A3@A2):continue
    S={v:set(G[v]) for v in G}
    NS={v:set().union(*(S[w] for w in S[v])) for v in G}
    assert all(not G.subgraph(S[v]).number_of_edges() for v in G)
    for v,w in G.edges():
        assert S[v].isdisjoint(S[w])
        assert NS[v].isdisjoint(NS[w])
    for z in G:
        for v,w in itertools.combinations(G[z],2):
            assert all(not G.has_edge(a,b) for a in S[v] for b in S[w])
    axiom_graphs+=1
print('Type/short-walk axioms checked on',axiom_graphs,'atlas graphs without isolates.')

# Exact finite checks of the energy-increment inequality behind regularity.
# Refine a 3x3 binary matrix by an arbitrary witness rectangle A x B.
energy_checks=0
for bits in range(1<<9):
    mat=[[bits>>(3*i+j)&1 for j in range(3)] for i in range(3)]
    density=Fraction(sum(map(sum,mat)),9)
    for amask in range(1,8):
        AA=[i for i in range(3) if amask>>i&1]
        AC=[i for i in range(3) if not(amask>>i&1)]
        for bmask in range(1,8):
            BB=[j for j in range(3) if bmask>>j&1]
            BC=[j for j in range(3) if not(bmask>>j&1)]
            witness=Fraction(sum(mat[i][j] for i in AA for j in BB),len(AA)*len(BB))
            if abs(witness-density)<=Fraction(1,3):continue
            energy=Fraction(0)
            for C in [AA,AC]:
                for D in [BB,BC]:
                    if C and D:
                        edges=sum(mat[i][j] for i in C for j in D)
                        energy+=Fraction(edges*edges,9*len(C)*len(D))
            gain=energy-density*density
            assert gain>=Fraction(len(AA)*len(BB),9)*(witness-density)**2
            assert gain>=Fraction(1,3)**4
            energy_checks+=1
print('Exact energy-increment witness checks:',energy_checks)

from math import ceil
for c in [Fraction(1,8),Fraction(1,5),Fraction(2,5)]:
    rho=(c-Fraction(1,9))/4
    alpha=rho; d=rho/10; eps=(rho/100)**2
    k0=ceil(10/rho); m0=ceil(100/eps); D=c-2*rho
    assert D>Fraction(1,9)
    # sqrt(eps)=rho/100 exactly.
    assert Fraction(1,k0)+eps+3*rho/100+d<rho
    assert eps+2*rho/100<rho
    assert alpha*m0-3>=eps*m0
    assert (d-eps)*(alpha*m0-3)>=2
    assert (1-2*eps)*m0>3
print('Regularity-cleaning and robust-path parameter inequalities checked.')
