import networkx as nx
from itertools import product
from pathlib import Path

def embeds(P,G):
    if len(P)>len(G) or P.number_of_edges()>G.number_of_edges(): return False
    return nx.algorithms.isomorphism.GraphMatcher(G,P).subgraph_is_monomorphic()

def template_contains(H,A,B):
    vs=list(H)
    for mask in range(1<<len(vs)):
        S=[v for i,v in enumerate(vs) if mask>>i&1]
        Q=[v for i,v in enumerate(vs) if not(mask>>i&1)]
        if embeds(H.subgraph(S),A) and embeds(H.subgraph(Q),B): return True
    return False

def unions(F,k): return nx.disjoint_union_all([F]*k)

H=nx.wheel_graph(7)
M=unions(nx.path_graph(2),4)
T=unions(nx.complete_graph(3),3)
I=nx.empty_graph(9)
E=nx.disjoint_union(nx.path_graph(2),nx.empty_graph(7))
EE=nx.disjoint_union(unions(nx.path_graph(2),2),nx.empty_graph(5))
checks=[('triangles/empty',T,I,False),('triangles/edge',T,E,False),('triangles/2edges',T,EE,True),('matchings/matchings',M,M,False)]
for name,A,B,answer in checks:
    got=template_contains(H,A,B)
    assert got==answer,(name,got)
    print(name, 'contains W7 =',got)
# Independent literal full-graph confirmation (induced matching is NOT used).
for name,A,B,answer in checks:
    G=nx.disjoint_union(A,B)
    G.add_edges_from((a,len(A)+b) for a in A for b in B)
    assert embeds(H,G)==answer
print('All eight independent subgraph checks passed.')
Path('workspace/agent3_w7_checks.py').write_text(Path(__file__).read_text())

# Two odd wheels sharing a rim edge; duplicate each common endpoint.
def gadget(k):
    Q=nx.wheel_graph(2*k+2)
    H=Q.copy()
    mapping={1:1,2:2}
    nxt=len(Q)
    for v in Q:
        if v not in mapping: mapping[v]=nxt; nxt+=1
    H=nx.compose(H,nx.relabel_nodes(Q,mapping))
    for v in [1,2]:
        H.add_node(nxt)
        H.add_edges_from((nxt,w) for w in list(H[v]))
        nxt+=1
    return nx.convert_node_labels_to_integers(H)

def residuals(H):
    n=len(H); full=(1<<n)-1
    edge_masks=[(1<<u)|(1<<v) for u,v in H.edges()]
    independent=[m for m in range(1<<n) if all(m&e!=e for e in edge_masks)]
    masks=set()
    for i in independent:
        for j in independent:
            if not i&j: masks.add(full^i^j)
    # Inclusion-minimal residuals suffice.
    minimal=[]
    for m in sorted(masks,key=int.bit_count):
        if not any(s&m==s for s in minimal): minimal.append(m)
    graphs=[]
    for m in minimal:
        G=H.subgraph([v for v in H if m>>v&1]).copy()
        if not any(nx.is_isomorphic(G,F) for F in graphs): graphs.append(G)
    return graphs
Path('workspace/agent3_gadget_checks.py').write_text(Path(__file__).read_text())
for k in [1,2,3]:
    H=gadget(k)
    Rs=residuals(H)
    print('gadget k',k,'order',len(H),'minimal residual types',len(Rs))
    for R in sorted(Rs,key=lambda R:(len(R),R.number_of_edges())):
        print(' residual',len(R),R.number_of_edges(),sorted(dict(R.degree()).values()), nx.to_graph6_bytes(nx.convert_node_labels_to_integers(R),header=False).decode().strip())
H=nx.convert_node_labels_to_integers(nx.line_graph(nx.petersen_graph()))
Rs=residuals(H)
print('Petersen line graph minimal residual types',len(Rs))
for R in sorted(Rs,key=lambda R:(len(R),R.number_of_edges())):
    print(' residual',len(R),R.number_of_edges(),sorted(dict(R.degree()).values()), nx.to_graph6_bytes(nx.convert_node_labels_to_integers(R),header=False).decode().strip())

from fractions import Fraction
import z3

def theta(D,L):
    F=nx.Graph(); F.add_nodes_from([0,1]); nxt=2
    for j in range(D):
        path=[0]+list(range(nxt,nxt+L-1))+[1]
        F.add_edges_from(zip(path,path[1:])); nxt+=L-1
    return F
for D,L in [(3,3),(4,3),(3,4)]:
    F=theta(D,L); es=list(F.edges()); target=Fraction(D*L,D*(L-1)+2)
    assert len(F)==D*(L-1)+2 and len(es)==D*L
    assert sum(d*(d-1)//2 for _,d in F.degree())==D*(D+L-2)
    for mask in range(1,1<<len(es)):
        chosen=[e for j,e in enumerate(es) if mask>>j&1]
        vertices=set(v for e in chosen for v in e)
        rho=Fraction(len(chosen),len(vertices))
        assert rho<=target
        if rho==target: assert len(chosen)==len(es)
    print('Theta strict balance checked',D,L,target)
for r,k in [(3,2),(3,3),(4,2)]:
    verts=list(product(range(r),repeat=k)); n=len(verts)
    es=[(i,j) for i in range(n) for j in range(i) if all(a!=b for a,b in zip(verts[i],verts[j]))]
    x=[z3.Int('x_%d'%i) for i in range(n)]; solver=z3.Solver()
    solver.add(*[z3.And(v>=0,v<r) for v in x]); solver.add(*[x[i]!=x[j] for i,j in es])
    count=0
    while solver.check()==z3.sat:
        model=solver.model(); coloring=[model.eval(v).as_long() for v in x]
        assert any(all(coloring[i]==coloring[j] if verts[i][q]==verts[j][q] else coloring[i]!=coloring[j] for i in range(n) for j in range(n)) for q in range(k))
        count+=1; solver.add(z3.Or(*[v!=c for v,c in zip(x,coloring)]))
    import math
    assert count==k*math.factorial(r)
    print('All proper tensor colorings dictator:',r,k,count)
Path('workspace/agent3_theta_tensor_checks.py').write_text(Path(__file__).read_text())

# Exact high/low-wedge equal-density connected pair.
def subdivide(C,length):
    S=nx.Graph(); S.add_nodes_from(C); nxt=max(C)+1
    paths={}
    for a,b in C.edges():
        p=[a]+list(range(nxt,nxt+length-1))+[b]
        nxt+=length-1; S.add_edges_from(zip(p,p[1:])); paths[frozenset([a,b])]=p
    return S,paths

def pair(k):
    D=2*(k-1)**2; F=theta(D,k)
    C=nx.disjoint_union_all([nx.complete_graph(2*k),nx.complete_graph(2*k)])
    for shift in [0,2*k]:
        C.remove_edges_from((shift+2*j,shift+2*j+1) for j in range(k))
    a,b=0,2; aa,bb=2*k,2*k+2
    C.remove_edges_from([(a,b),(aa,bb)]); C.add_edges_from([(a,aa),(b,bb)])
    S,paths=subdivide(C,k-1)
    side=set(range(2*k))
    for edge,p in paths.items():
        if edge in [frozenset([a,aa]),frozenset([b,bb])]: continue
        if p[0]<2*k: side.update(p[1:-1])
    for edge,num in [(frozenset([a,aa]),(k-2)//2),(frozenset([b,bb]),k-2-(k-2)//2)]:
        p=paths[edge]
        if p[0]>=2*k: p=list(reversed(p))
        side.update(p[1:1+num])
    G=S.subgraph(side).copy(); GG=S.subgraph(set(S)-side).copy()
    return F,S,G,GG,C
for k in [3,5,7,11,21]:
    F,S,G,GG,C=pair(k); v=len(F); e=F.number_of_edges()
    assert len(S)==2*v and S.number_of_edges()==2*e
    assert len(G)==v==len(GG) and G.number_of_edges()==e-1==GG.number_of_edges()
    if k<=7: assert nx.is_isomorphic(G,GG)
    assert nx.is_connected(C) and set(dict(C.degree()).values())=={2*k-2}
    assert nx.is_bipartite(S)
    wF=sum(d*(d-1)//2 for _,d in F.degree()); wS=sum(d*(d-1)//2 for _,d in S.degree())
    print('Pair k=',k,'v,e=',v,e,'rho=',Fraction(e,v),'high W/v=',Fraction(wF,v),'low W/v=',Fraction(wS,2*v))
DGH=nx.Graph([(0,4),(0,7),(0,8),(1,7),(1,8),(2,7),(2,8),(3,4),(3,5),(4,8),(5,8),(7,8)])
print('Diagnostic chromaticcritical:',nx.is_bipartite(DGH), nx.is_bipartite(nx.restricted_view(DGH,[8],[])))
print('Diagnostic in P3-factor:',template_contains(DGH,unions(nx.path_graph(3),4),nx.empty_graph(12)))
for nam,F0 in [('claw',nx.star_graph(3)),('P4',nx.path_graph(4)),('triangle',nx.complete_graph(3))]:
    print('Diagnostic in',nam,template_contains(DGH,nx.disjoint_union(F0,nx.empty_graph(12)),nx.empty_graph(12)))
print('Diagnostic in matching-both:',template_contains(DGH,unions(nx.path_graph(2),6),unions(nx.path_graph(2),6)))
def mul(P,Q):
    R=[0]*(len(P)+len(Q)-1)
    for i,a in enumerate(P):
        for j,b in enumerate(Q): R[i+j]+=a*b
    return R

def p3cycles(k,shift):
    P=[1]
    for _ in range(k): P=mul(P,[1,9,7,1])
    if shift: P=mul(P,[1,1])
    A=3*k+shift; B=3*k-shift
    total=B*(P[1]-A)//2
    for b in range(2,min(len(P)-1,B)+1):
        total+=P[b]*math.factorial(B)//math.factorial(B-b)*math.factorial(b-1)//2
    return total
for AA,BB in [(unions(nx.path_graph(3),2),nx.empty_graph(6)),(nx.disjoint_union(unions(nx.path_graph(3),2),nx.empty_graph(1)),nx.empty_graph(5))]:
    JJ=nx.disjoint_union(AA,BB); JJ.add_edges_from((i,len(AA)+j) for i in AA for j in BB)
    assert not embeds(DGH,JJ)
    print('Literal GraphMatcher H-free:',len(AA),len(BB))
def brute_cycles(G):
    ans=0
    def rec(start,v,seen):
        nonlocal ans
        for w in G[v]:
            if w==start and len(seen)>=3: ans+=1
            elif w>start and w not in seen: rec(start,w,seen|{w})
    for v in G: rec(v,v,{v})
    assert ans%2==0
    return ans//2
for kk in [1,2]:
    for ss in [0,1]:
        AA=unions(nx.path_graph(3),kk)
        if ss: AA=nx.disjoint_union(AA,nx.empty_graph(1))
        BB=nx.empty_graph(3*kk-ss)
        JJ=nx.disjoint_union(AA,BB); JJ.add_edges_from((i,len(AA)+j) for i in AA for j in BB)
        got=brute_cycles(JJ); exact=p3cycles(kk,ss)
        assert got==exact
        print('P3 cycle formula verified by independentDFS:',kk,ss,got)
for kk in [1,2,3,5,10,20]:
    b=p3cycles(kk,0); u=p3cycles(kk,1)
    print('Diagnostic cycles n=',6*kk,'unbalanced/balanced=',Fraction(u,b),'winner',u>b)
    if kk>=10: assert u>b
# Explicit quantitative audit of the elementary global counterproof.
import sympy as sp
xx=sp.symbols('xx',nonnegative=True)
assert sp.expand((100+xx)**2/2-40*(100+xx)-40)==xx**2/2+60*xx+960
assert 7*(10**8-9999)>9999*9998//2
fv=[0]
for nn in range(1,1001):
    val=max(a*(nn-a)+(2*a)//3 for a in range(nn+1))
    tt=(nn*nn)//4
    assert Fraction(tt)+Fraction(nn,3)-1<=val<=Fraction(tt)+Fraction(nn,3)+1
    assert Fraction(val-fv[-1])>Fraction(nn,2)-3
    fv.append(val)
for kk in range(1,166):
    nn=6*kk; mm=3*kk
    vals=[a*(nn-a)+(2*a)//3 for a in range(nn+1)]
    assert [a for a,val in enumerate(vals) if val==max(vals)]==[mm]
print('Explicit local threshold10000/global threshold1e8 arithmetic audit passed.')
Path('workspace/agent3_explicit_global_counterproof.md').write_text(r'''# Fully elementary explicit global upper bound for the diagnostic H
Use old labels V(H)={0,1,2,3,4,5,7,8} and E(H)={04,07,08,17,18,27,28,34,35,48,58,78}.
Put f(n)=max_{0<=a<=n}(a(n-a)+floor(2a/3)).
We prove ex(n,H)=f(n) for n>=10^8. No external stability theorem is needed.

H-8 is a tree on seven vertices. Every neighborhood in an H-free graph is therefore T_7-free and hence 5-degenerate (minimum degree6 embeds any seven-vertex tree greedily). In particular e(G[N(v)])<=5d(v).

LOCAL LEMMA: Suppose n>=10000, e(G)>=f(n), and delta(G)>=n/2-10.
For v with a=d(v), summing degrees of its neighbors gives
2e(N(v))>=a(delta(G)-n+a).
Together with e(N(v))<=5a this yields a<=n-delta+10<=n/2+20.
For A=N(v), B=V\A we have e(A,B)>=a(delta-10)>=a(n/2-20)>=n^2/4-15n.
Therefore a maximum cut A,B has e(A,B)>=n^2/4-15n, ||A|-n/2|<=sqrt(15n)<4sqrt(n), and at most15n missing cross edges.
If v has t internal neighbors, maximality of the cut gives at least t opposite-part neighbors. The cross edges among these two sets are edges of N(v), so t^2-15n<=e(N(v))<=5n. Thus t<5sqrt(n).
Every vertex consequently misses at most10+9sqrt(n) cross neighbors. Any four fixed vertices in one part have at least
n/2-40sqrt(n)-40>=960
common neighbors in the other part. (Write sqrt(n)=100+y, y>=0: the expression equals y^2/2+60y+960.)

The four explicit defect partitions show H embeds in (i) one internal claw plus an independent opposite part, (ii) one internal P4, (iii) one internal triangle plus an isolated vertex. The common-neighbor bound therefore forces each internal graph to have maximum degree2, no P4, and no triangle. Its components are P3,K2,K1.
Now each part has size between n/2-12 and n/2+12, and each vertex misses at most24 cross neighbors.
Since f(n)>=t_2(n)+n/3-1, at least one part A has >=n/6-1/2 internal edges. If B has an internal edge xy, exclude from A the at most48 vertices nonadjacent to x or y. At most96 internal A edges meet them. Thus choose an A edge uv adjacent to both x,y. Map H labels 7,8 to u,v and 0,4 to x,y. Choose label3 as a fresh A vertex adjacent to y, then labels1,2,5 as three fresh common B neighbors of the three chosen A vertices. Such vertices exist because cross deficits are at most24. This realizes all H edges, a contradiction. Thus B is independent.
Hence e(G)<=|A||B|+floor(2|A|/3)<=f(n), proving the local lemma.

GLOBAL: Directly t_2(n)+n/3-1<=f(n)<=t_2(n)+n/3+1. Therefore f(m)-f(m-1)>m/2-3.
Suppose n>=10^8 and an H-free G has e(G)>f(n). While order m>=10000, delete a vertex of degree<m/2-10 whenever possible. The positive integer defect e-f(m) increases by >7 at each deletion. The process cannot stop at order>=10000, by the local lemma. If it reaches order9999, its defect exceeds7(n-9999)>binom(9999,2), impossible. Therefore ex(n,H)<=f(n).
The reverse bound follows by taking K_{a,n-a} and inserting P3 components plus at most one K2 in the first part; these graphs are H-free by the direct two-case proof in agent2_counterexample_proof.md.

For n>=10^8+1 every extremal graph has minimum degree >=f(n)-f(n-1)>n/2-3, so the local classification applies. Equality requires a complete cross graph and maximum P3/K2 packing in the active part. At n=6k, f(n)=9k^2+2k, uniquely optimized at a=3k, and equality forces exactly k copies of P3 there. This yields the unique edge extremizer used in the exact cycle comparison.
''')
Path('workspace/agent3_component_pair_checks.py').write_text(Path(__file__).read_text())
Path('workspace/agent3_component_pair.md').write_text(r'''# Equal-density, sharply different wedge pairs
For odd k>=3 put D=2(k-1)^2 and let F be D internally vertex-disjoint paths of length k with common endpoints.
Then v=2k(k^2-3k+3), e=2k(k-1)^2 and rho=e/v=(k-1)^2/(k^2-3k+3), decreasing to 1.
Its wedge count W(F)=sum binom(d,2)=D(D+k-2), so W(F)/v~2k.
It is strictly balanced: prune degree-one vertices from a candidate density>1 subgraph; what remains consists of t whole endpoint-to-endpoint paths. Its density tk/[t(k-1)+2] is strictly increasing in t, so only t=D maximizes it.

Construct a connected (2k-2)-regular core C on 4k vertices as follows. In each of two copies of K_{2k}, remove a perfect matching, choose a remaining edge ab, remove both chosen edges, and cross-connect the corresponding endpoints. C remains regular and connected, with a two-edge cut separating the copies. Subdivide every core edge to length k-1 to produce F'. Since k-1 is even, F' is bipartite. Direct counting gives |F'|=2v and e(F')=2e.

A connected regular graph C is strictly balanced: any proper vertex subset has average degree strictly less than its regular degree (by connectivity), and deleting edges also strictly reduces density. Uniform subdivision preserves strict balance for density>1, since after pruning leaves any candidate subgraph is the subdivision of a core subgraph and its edge/vertex ratio is x*ell/[1+(ell-1)*x], a strictly increasing function of the core edge/vertex ratio x. Hence F' is strictly balanced.

Its wedge density is W(F')/(2v)=[(2k-2)(2k-3)/2+(k-2)(k-1)]/[1+(k-2)(k-1)], tending to 3, unlike F's unbounded wedge density.

Cut a central edge from each of the two subdivided cross-connecting paths, allocating floor((k-2)/2) internal vertices on one path and ceil((k-2)/2) on the other to the first half. The halves G,G' are isomorphic by swapping chosen-edge endpoints. Each has v vertices and e-1 edges. Thus F' is two copies of G joined by two edges.

This is a FINITE COMPONENT construction only; it does not by itself prove a global H-free extremal characterization. The missing global structural argument must not be claimed as proved.
''')
