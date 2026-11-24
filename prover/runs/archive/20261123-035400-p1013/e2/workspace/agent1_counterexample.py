from collections import defaultdict
from fractions import Fraction as F
from math import factorial as fac
import networkx as nx

E=[(0,3),(0,4),(0,6),(0,7),(1,3),(1,5),(1,7),
   (2,5),(2,7),(3,7),(4,7),(6,7)]
H=nx.Graph(E)
assert nx.is_bipartite(H.subgraph(set(H)-{7}))
assert all(H.has_edge(*e) for e in [(0,3),(0,7),(3,7)])
certs=[({0,1,2,7},nx.star_graph(3)),
       ({0,1,5,7},nx.path_graph(4)),
       ({0,3,5,7},nx.disjoint_union(nx.cycle_graph(3),nx.empty_graph(1)))]
for S,D in certs:
    assert H.subgraph(set(H)-S).number_of_edges()==0
    assert nx.is_isomorphic(H.subgraph(S),D)
A={0,5,7}
assert {frozenset(e) for e in H.subgraph(A).edges()}=={frozenset((0,7))}
assert {frozenset(e) for e in H.subgraph(set(H)-A).edges()}=={frozenset((1,3))}
for mask in range(256):
    S={v for v in H if mask>>v&1}
    if H.subgraph(set(H)-S).number_of_edges():continue
    J=H.subgraph(S)
    assert any(len(C)>3 or J.subgraph(C).number_of_edges()>2
               for C in nx.connected_components(J))

def f(n):return max(a*(n-a)+(2*a)//3 for a in range(n+1))
for n in range(1,501):
    assert f(n)==(n*n)//4+(n+n%2)//3
    assert 2*(f(n)-f(n-1))>=n-1
for m in range(3,151,3):
    vals=[a*(2*m-a)+(2*a)//3 for a in range(2*m+1)]
    assert [a for a,v in enumerate(vals) if v==max(vals)]==[m]

# (selected vertices, contracted path blocks) -> oriented weight.
P={1:{(0,0):1,(1,1):1},
   2:{(0,0):1,(1,1):2,(2,2):1,(2,1):2},
   3:{(0,0):1,(1,1):3,(2,2):3,(2,1):4,
      (3,3):1,(3,2):4,(3,1):2}}
def cycles(a,b):
    q={(0,0):1}
    for z in [3]*(a//3)+([a%3] if a%3 else []):
        p=defaultdict(int)
        for (v,k),c in q.items():
            for (w,l),d in P[z].items():p[v+w,k+l]+=c*d
        q=p
    twice=sum(c*fac(k-1)*fac(b)//fac(b-k)
              for (v,k),c in q.items() if 1<=k<=b and v+k>=3)
    assert twice%2==0
    return twice//2

def host(a,b):
    G=nx.complete_bipartite_graph(a,b)
    for j in range(a//3):G.add_edges_from([(3*j,3*j+1),(3*j+1,3*j+2)])
    if a%3==2:G.add_edge(a-2,a-1)
    return G

def brute(G):
    total=0
    for s in G:
        def dfs(v,seen):
            ans=int(len(seen)>=3 and G.has_edge(v,s))
            for w in G[v]:
                if w>s and w not in seen:ans+=dfs(w,seen|{w})
            return ans
        total+=dfs(s,{s})
    assert total%2==0
    return total//2
for a,b in [(3,3),(4,2),(6,4),(6,5),(7,4)]:
    assert cycles(a,b)==brute(host(a,b))
z=F(7,3)
Aupper=sum(z**t/fac(t)**2 for t in range(3))+(z**3/fac(3)**2)/(1-z/16)
Dlower=sum(z**(t+2)/(fac(t)*fac(t+2)) for t in range(3))
assert Aupper==F(67849,13284)
assert Dlower==F(21217,3888)
assert Dlower>Aupper
assert cycles(25,23)>cycles(24,24)
print('All finite certificates passed.')
print('Exact n=48 cycle-ratio:',float(F(cycles(25,23),cycles(24,24))))
print('Rational limiting gap:',Dlower-Aupper)
