"""Elementary shift-graph version: no use of the Kneser theorem."""
import itertools, math
from fractions import Fraction
import networkx as nx
import sys
sys.path.insert(0,'workspace')
from agent4_lower import subdivision,odd_closed_walks,check_symbolic_local_rule

def shift_graph(N,k):
    F=nx.Graph(); F.add_nodes_from(itertools.combinations(range(N),k))
    for t in itertools.combinations(range(N),k+1): F.add_edge(t[:-1],t[1:])
    return F

def permutation_cover(N,k,F):
    assert k%2==1
    perms=list(itertools.permutations(range(N)))
    labels={v:set() for v in F}
    for i,permutation in enumerate(perms):
        rank={v:j for j,v in enumerate(permutation)}
        for t in F:
            # position is 1-indexed, include iff even
            if (max(range(k),key=lambda j:rank[t[j]])+1)%2==0:
                labels[t].add(i)
    p=math.factorial(N)*(k-1)//(2*k)
    assert all(len(s)==p for s in labels.values())
    assert all(labels[u].isdisjoint(labels[v]) for u,v in F.edges())
    return labels,len(perms),p

def construction(N,k,L=1):
    F=shift_graph(N,k);labels,m,p=permutation_cover(N,k,F)
    G,typ,lab=subdivision(F)
    for t in range(3):
        big=[('pool',t,i,j) for i in range(m) for j in range(L)]
        small=[('leaf',t,j) for j in range(p*L)]
        G.add_edges_from(itertools.product(big,small))
    for v in typ:
        G.add_edges_from((v,('pool',typ[v],i,j)) for i in labels[lab[v]] for j in range(L))
    assert len(G)==3*(m+p)*L+len(F)+2*F.number_of_edges()
    assert min(dict(G.degree()).values())>=p*L
    return F,G,m,p

def check_color_descent(N,k):
    # Color vertices distinctly; iterated sets give proper lower-shift coloring.
    F=shift_graph(N,k)
    color={v:i for i,v in enumerate(F)}
    for j in range(k-1,0,-1):
        lower=shift_graph(N,j)
        new={t:frozenset(color[t+(y,)] for y in range(t[-1]+1,N)) for t in lower}
        assert all(new[u]!=new[v] for u,v in lower.edges())
        color=new
    return len(set(color.values()))

def choose_k(c):
    c=Fraction(c); assert 0<=c<Fraction(1,9)
    k=3
    while Fraction(k-1,3*(3*k-1))<=c: k+=2
    return k

if __name__=='__main__':
    print('Universal local checks:',check_symbolic_local_rule())
    for N,k in [(4,3),(5,3)]:
        F,G,m,p=construction(N,k)
        assert odd_closed_walks(G,3)==0
        assert odd_closed_walks(G,5)==0
        assert check_color_descent(N,k)==N
        print('N,k=',N,k,'F vertices/edges=',len(F),F.number_of_edges(),
              'm,p=',m,p,'G vertices/edges/min degree=',len(G),G.number_of_edges(),min(dict(G.degree()).values()))
    print('k for c=0, .10, .11:',[choose_k(c) for c in [0,Fraction(1,10),Fraction(11,100)]])
