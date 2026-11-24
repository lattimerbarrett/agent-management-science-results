from pathlib import Path
p=Path('workspace/agent1_complete_checks.py')
p.write_text('''import itertools as it
from fractions import Fraction as Q
import networkx as nx
import z3

def wide(G):
    V=list(G); N={v:set(G[v]) for v in V}; reps=[]
    for size in range(1,len(V)+1):
        candidate=next((C for C in it.combinations(V,size)
                        if all(not N[a]&N[b] for a,b in it.combinations(C,2))),None)
        if candidate is None: break
        reps=candidate
    assert len(reps)<=4
    L={v:frozenset(i for i,r in enumerate(reps) if N[v]&N[r]) for v in V}
    assert all(L.values())
    S={i:{v for v in V if L[v]=={i}} for i in range(len(reps))}
    core={v for v in V if len(L[v])>=2}
    assert nx.is_bipartite(G.subgraph(core))
    parity=nx.bipartite.color(G.subgraph(core))
    color={v:('S',next(iter(L[v]))) if len(L[v])==1 else
              ('C',parity[v],frozenset(i for i in S if N[v]&S[i])) for v in V}
    assert len(set(color.values()))<=36
    for a,b in G.edges():
        assert color[a]!=color[b]
        for x in N[a]:
            for y in N[b]: assert color[x]!=color[y]

def no35(G):
    if any(nx.triangles(G).values()): return False
    for v in G:
        D={w for u in G[v] for w in G[u]}
        if any(set(G[u])&D for u in D): return False
    return True

atlas=0
for G in nx.graph_atlas_g():
    if len(G) and 5*min(dict(G.degree()).values())>len(G) and no35(G):
        wide(G); atlas+=1
assert atlas==22
# All putative triangles of the FULL universal target, symbolically.
m=36
A,B,C=z3.BitVecs('A B C',m); i,j,k=z3.Ints('i j k')
def member(i,A):
    return z3.Or(*[z3.And(i==r,z3.Extract(r,r,A)==1) for r in range(m)])
def edge(i,A,j,B): return z3.And(member(i,B),member(j,A),(A&B)==0)
s=z3.Solver(); s.add(i>=0,i<m,j>=0,j<m,k>=0,k<m)
s.add(edge(i,A,j,B),edge(j,B,k,C),edge(k,C,i,A))
assert s.check()==z3.unsat

def shift(N,k):
    F=nx.Graph();F.add_nodes_from(it.combinations(range(N),k))
    F.add_edges_from((a[:-1],a[1:]) for a in it.combinations(range(N),k+1))
    return F

def cover(F,order):
    rank={x:i for i,x in enumerate(order)}; out=set()
    for v in F:
        j=max(range(len(v)),key=lambda j:rank[v[j]])
        if 0<j<len(v)-1 and j%2==0: out.add(v)
    return out

cover_results=[]
for N,k in [(5,4),(6,4),(7,4),(8,6)]:
    F=shift(N,k); counts=dict.fromkeys(F,0); M=0
    for order in it.permutations(range(N)):
        I=cover(F,order); M+=1
        assert all(not(u in I and v in I) for u,v in F.edges())
        for v in I: counts[v]+=1
    assert set(counts.values())=={M*(k-2)//(2*k)}
    col=nx.coloring.greedy_color(F)
    sets={a:frozenset(col[a+(b,)] for b in range(a[-1]+1,N))
          for a in shift(N,k-1)}
    assert all(sets[a]!=sets[b] for a,b in shift(N,k-1).edges())
    cover_results.append((N,k,M,next(iter(counts.values()))))

def base(F):
    B=nx.Graph(); typ={}; lab={}
    for u in F: B.add_node(('U',u));typ['U',u]='U';lab['U',u]=u
    for u,v in F.edges():
        x=('X',u,v); y=('Y',u,v)
        B.add_edges_from([(('U',u),x),(x,y),(y,('U',v))])
        typ[x]='X';typ[y]='Y';lab[x]=u;lab[y]=v
    return B,typ,lab

local=0
for n in range(1,5):
    pairs=list(it.combinations(range(n),2))
    for choices in it.product(range(3),repeat=len(pairs)):
        F=nx.DiGraph();F.add_nodes_from(range(n))
        for (u,v),a in zip(pairs,choices):
            if a: F.add_edge(*((u,v) if a==1 else (v,u)))
        B,T,label=base(F)
        for a in B:
            for b in B[a]:
                for c in B[b]:
                    for d in B[c]:
                        if T[a]==T[d]:
                            u,v=label[a],label[d]
                            assert F.has_edge(u,v) or F.has_edge(v,u)
        local+=1
assert local==760
# End-to-end lower construction using an actual shift cover.
F=shift(5,4); sets=[cover(F,p) for p in it.permutations(range(5))]
G,T,label=base(F); old=list(G); M=len(sets); r=sum(next(iter(F)) in I for I in sets)
for t in ['U','X','Y']:
    pads=[('P',t,i) for i in range(M)]
    G.add_nodes_from(pads)
    for i,I in enumerate(sets):
        G.add_edges_from((pads[i],v) for v in old if T[v]==t and label[v] in I)
    G.add_edges_from((('L',t,j),p) for j in range(r) for p in pads)
assert len(G)==len(F)+2*F.number_of_edges()+3*(M+r)
assert min(dict(G.degree()).values())>=r
assert no35(G)
for c in [Q(0),Q(1,20),Q(1,10),Q(11,100),Q(111,1000)]:
    k=4
    while Q(k-2,3*(3*k-2))<=c: k+=2
    M=2*k; r=k-2; b=37
    gap=r-3*c*(M+r); assert gap>0
    W=int(c*b/gap)+1
    assert Q(r*W,b+3*(M+r)*W)>c
print('Upper atlas graphs:',atlas,'; target H36 triangle constraints: UNSAT')
print('Shift covers (N,k,M,r):',cover_results)
print('Local oriented seeds:',local)
print('End-to-end lower graph (vertices,edges,min degree):',
      len(G),G.number_of_edges(),min(dict(G.degree()).values()))
print('Exact rational parameter checks passed')
''')
exec(compile(p.read_text(),str(p),'exec'))
