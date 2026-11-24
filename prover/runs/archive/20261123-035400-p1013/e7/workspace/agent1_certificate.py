from fractions import Fraction as Q
from math import factorial
import itertools
import networkx as nx

# Rational interval enclosure of sum x^j/(j!(j+shift)!), with a geometric tail.
def bessel_sum_interval(x, shift, prefactor=1, terms=18):
    vals=[Q(prefactor*x**j, factorial(j)*factorial(j+shift)) for j in range(terms)]
    first=Q(prefactor*x**terms,factorial(terms)*factorial(terms+shift))
    ratio=Q(x,(terms+1)*(terms+shift+1))
    assert ratio < 1
    return sum(vals),sum(vals)+first/(1-ratio)
lo,_=bessel_sum_interval(4,0)
_,hi=bessel_sum_interval(3,2,9)
assert lo-hi > Q(23,100)
print('Certified I0(4)-3I2(2sqrt(3)) >',lo-hi)

# Enumerate all proper colorings of K_r tensor K_r, not just selected ones.
for r in (3,4):
    vertices=list(itertools.product(range(r),repeat=2))
    nbr=[[j for j,y in enumerate(vertices) if j<i and all(a!=b for a,b in zip(x,y))] for i,x in enumerate(vertices)]
    colors=[-1]*len(vertices); count=[0]
    def visit(i):
        if i==len(vertices):
            count[0]+=1
            assert any(all(colors[j]==perm[x[c]] for j,x in enumerate(vertices)) for c in (0,1) for perm in itertools.permutations(range(r)))
            return
        for c in range(r):
            if all(colors[j]!=c for j in nbr[i]):
                colors[i]=c;visit(i+1)
        colors[i]=-1
    visit(0)
    assert count[0]==2*factorial(r)
    print('All tensor colorings certified:',r,count[0])

# Explicit high-wedge theta component and low-wedge regular-subdivision mate.
for k in (3,5,7,11):
    D=2*(k-1)**2; L=k
    F=nx.Graph();F.add_nodes_from((0,1));nextv=2
    for j in range(D):
        path=[0]+list(range(nextv,nextv+L-1))+[1];nextv+=L-1
        F.add_edges_from(zip(path,path[1:]))
    # Core: two K_(2k) minus perfect matchings, joined by an edge switch.
    core=nx.disjoint_union(nx.complete_graph(2*k),nx.complete_graph(2*k))
    for start in (0,2*k):
        core.remove_edges_from((start+2*j,start+2*j+1) for j in range(k))
    a,b=0,2;c,d=2*k,2*k+2
    core.remove_edges_from(((a,b),(c,d)));core.add_edges_from(((a,c),(b,d)))
    assert nx.is_connected(core)
    assert set(dict(core.degree()).values())=={2*k-2}
    low=nx.Graph();low.add_nodes_from(core);nextv=len(core)
    for a,b in core.edges():
        path=[a]+list(range(nextv,nextv+k-2))+[b];nextv+=k-2
        low.add_edges_from(zip(path,path[1:]))
    v=2*k*(k*k-3*k+3);e=2*k*(k-1)**2
    assert (len(F),F.number_of_edges())==(v,e)
    assert (len(low),low.number_of_edges())==(2*v,2*e)
    assert nx.is_bipartite(F) and nx.is_bipartite(low)
    w=lambda G:sum(d*(d-1)//2 for _,d in G.degree())
    gap=Q(w(F),v)-Q(w(low),2*v)
    assert gap==Q(2*(k-1)*(k-2)**2,k*k-3*k+3)
    assert Q(e,v)==1+Q(k-2,k*k-3*k+3)
    print('Component pair certified:',k,v,e,'wedge gap',gap)
print('All executed checks passed. These checks do NOT certify the missing global extremal theorems.')
