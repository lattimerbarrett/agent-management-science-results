# Python 3; requires networkx, sympy, numpy, z3-solver.
import itertools as it, math
from fractions import Fraction as F
import networkx as nx
import sympy as sp
import z3

def choose(n,k): return math.comb(n,k) if 0<=k<=n else 0

# Exact identities and every candidate cutoff through r=300.
r,k=sp.symbols('r k');q=(r-1)/r;rho=(k-1)/k
P=(r-2)*k*k+(-2*r*r+3*r+4)*k+2*r-8
A=-2/q+2*r/((r-1)*(r-2))*(2*rho-1)+2*r/(r-1)**2*(k-2)*(k-3)/(2*k)
assert sp.cancel(A-r*P/(k*(r-2)*(r-1)**2))==0
assert sp.expand(P.subs(k,2*r)+2*(r-1)*(r-4))==0
assert sp.expand(P.subs(k,2*r+1)-6*(r-1))==0
for R in range(3,301):
    cutoff=6 if R==3 else 8 if R==4 else 2*R+1
    p=lambda K:(R-2)*K*K+(-2*R*R+3*R+4)*K+2*R-8
    assert all(p(K)<0 for K in range(2,cutoff))
    assert p(cutoff)==0 if R==4 else p(cutoff)>0
nt=0
for K in range(2,13):
    ws=[sum(choose(d,2) for _,d in T.degree()) for T in nx.nonisomorphic_trees(K)]
    assert min(ws)==K-2 and max(ws)==choose(K-1,2)
    nt+=len(ws)
assert nt==986

# Exact rational finite-phase optimization (no floating point).
def phasecheck(R,K):
    q=F(R-1,R);L=F(R,(R-1)*(R-2));B=F(2*R,(R-1)**2);rho=F(K-1,K)
    best=None
    for s in range(R):
        vals=[]
        for x in range(-2*R,2*R+1):
            z,b=divmod(s-x,R-1)
            ds=[F(R*x-s,R)]+[F(R*z-s,R)]*(R-1-b)+[F(R*(z+1)-s,R)]*b
            Q=sum(d*d for d in ds);vals.append((x,-Q/2,Q,ds[0]))
        profiles=[]
        for u in range(K):
            data=[(cross+x-((x-u+K-1)//K),-L*Q+4*L*rho*d) for x,cross,Q,d in vals]
            em=max(e for e,p in data);pm=max(p for e,p in data if e==em)
            profiles.append((data,em,pm))
        for df,ef,pf in profiles:
            for dg,eg,pg in profiles:
                shift=ef-eg-1
                for e,p in dg:
                    adv=2/q*(e+shift-ef)+p-pf+B*F((K-2)*(K-3),2*K)
                    best=adv if best is None else max(best,adv)
    assert best==-2/q+2*L*(2*rho-1)+B*F((K-2)*(K-3),2*K)
for R in range(3,9):
    for K in range(2,2*R+5):phasecheck(R,K)

# H17, the bounded-excess r=2 witness.
H=nx.Graph([(0,1),(8,9)])
for a,ls in [(0,[2,3,4]),(1,[5,6,7]),(8,[10,11,12]),(9,[13,14,15])]:
    H.add_edges_from((a,x) for x in ls)
H.add_edges_from((16,x) for x in list(range(2,8))+list(range(10,16)))
assert [v for v in H if nx.is_bipartite(H.subgraph(set(H)-{v}))]==[16]
base=nx.bipartite.color(H.subgraph(range(16)))
for flips in it.product(range(2),repeat=2):
    col={v:base[v]^flips[int(v>=8)] for v in range(16)}
    assert sum(col[v] for v in H.neighbors(16))==6

# Exact embedding in an infinite complete bipartite host with finite internals.
def embeds(A,B,holes=()):
    qa,qb=len(A),len(B);n=len(H);s=z3.Solver()
    c=[z3.Bool('c%d'%v) for v in range(n)];t=[z3.Int('t%d'%v) for v in range(n)]
    for v in range(n):
        s.add(t[v]>=-1,t[v]<qa+qb)
        s.add(z3.Implies(t[v]>=0,z3.If(c[v],t[v]>=qa,t[v]<qa)))
    for u,v in it.combinations(range(n),2):
        s.add(z3.Implies(z3.And(t[u]>=0,t[v]>=0),t[u]!=t[v]))
    es=list(A.edges())+[(qa+u,qa+v) for u,v in B.edges()]
    for u,v in H.edges():
        same=z3.Or(*[z3.Or(z3.And(t[u]==a,t[v]==b),z3.And(t[u]==b,t[v]==a)) for a,b in es])
        s.add(z3.Implies(c[u]==c[v],same))
        for a,b in holes:
            s.add(z3.Not(z3.Or(z3.And(t[u]==a,t[v]==qa+b),z3.And(t[v]==a,t[u]==qa+b))))
    return s.check()==z3.sat
empty=nx.Graph();tri=nx.complete_graph(3)
assert not embeds(tri,tri)
assert not embeds(empty,nx.star_graph(5))
assert embeds(nx.disjoint_union(nx.path_graph(2),nx.path_graph(2)),empty)
assert embeds(nx.star_graph(6),empty)
assert embeds(nx.star_graph(3),nx.path_graph(2),list(it.product(range(4),range(2))))

# Exact cycle counts: options (edges, nontrivial path components) -> multiplicity.
TRI={(0,0):1,(1,1):3,(2,1):3};STAR5={(0,0):1,(1,1):5,(2,1):10};EMPTY={(0,0):1}
def cycles2(a,b,oa,ob,internal=0):
    ans=F(internal)
    for (ja,pa),va in oa.items():
        for (jb,pb),vb in ob.items():
            for ell in range(max(1,pa,pb),min(a-ja,b-jb)+1):
                if ja+jb==0 and ell==1:continue
                ans+=F(va*vb*choose(a-ja-pa,ell-pa)*choose(b-jb-pb,ell-pb)*2**(pa+pb)*math.factorial(ell)*math.factorial(ell-1),2)
    assert ans.denominator==1
    return ans.numerator
def brute(G):
    ans=0
    for ell in range(3,len(G)+1):
        for S in it.combinations(G,ell):
            a=min(S)
            for p in it.permutations([v for v in S if v!=a]):
                C=(a,)+p
                if C[1]<C[-1] and all(G.has_edge(C[j],C[(j+1)%ell]) for j in range(ell)):ans+=1
    return ans
G=nx.complete_bipartite_graph(3,3);G.add_edges_from(tri.edges());G.add_edges_from((a+3,b+3) for a,b in tri.edges())
assert cycles2(3,3,TRI,TRI,2)==brute(G)==197
G=nx.complete_bipartite_graph(1,6);G.add_edges_from((a+1,b+1) for a,b in nx.star_graph(5).edges())
assert cycles2(1,6,EMPTY,STAR5)==brute(G)
for m in [20,40,80,160,320]:assert cycles2(m,m+1,EMPTY,STAR5)>cycles2(m,m+1,TRI,TRI,2)

# Dictatorship and robust equality/inequality: exact SMT, not sampling.
for R,M in [(3,1),(3,2),(3,3),(4,2)]:
    V=list(it.product(range(R),repeat=M));c=[z3.Int('p%d'%i) for i in range(len(V))];s=z3.Solver()
    s.add(*[z3.And(x>=0,x<R) for x in c])
    for i,x in enumerate(V):
        for j,y in enumerate(V[:i]):
            if all(a!=b for a,b in zip(x,y)):s.add(c[i]!=c[j])
    for a in range(R):s.add(c[V.index((a,)*M)]==a)
    for j in range(M):s.add(z3.Or(*[c[i]!=x[j] for i,x in enumerate(V)]))
    assert s.check()==z3.unsat
for R,Q in [(3,0),(3,1),(3,2),(4,1)]:
    M=R*Q+1;na=(R-1)*M;T=list(range(na,na+M+1));v=na+M+1
    edges=[(a,b) for a in range(na) for b in range(a) if a//M!=b//M]+list(it.product(range(na),T))
    for inequality in [False,True]:
        E=edges+([(v,t) for t in T[1:]] if inequality else [])
        n=v+int(inequality);c=[z3.Int('g%d'%i) for i in range(n)];s=z3.Solver()
        s.add(*[z3.And(x>=0,x<R) for x in c])
        for u in range(n):
            s.add(z3.Sum([z3.If(c[u]==c[b if a==u else a],1,0) for a,b in E if u in (a,b)])<=Q)
        s.add(c[v]==c[T[0]] if inequality else z3.Or(*[c[t]!=c[T[0]] for t in T[1:]]))
        assert s.check()==z3.unsat

# Exact Posa identities/inverses and the finite replacement coefficient.
def rot(p,z):
    j=p.index(z);return p[:j+1][::-1]+p[j+1:]
for n in range(5,16):
    p=list(range(n))
    for i,j in it.permutations(range(1,n-1),2):
        if abs(i-j)<=1:continue
        out=rot(rot(p,j),i)
        assert out[0]==i and out[-1]==n-1 and rot(rot(out,j),0)==p
        E={frozenset(e) for e in zip(out,out[1:])}
        assert frozenset((0,j+1)) in E
        assert frozenset((j,i-1 if j>i else i+1)) in E
w=lambda G:sum(choose(d,2) for _,d in G.degree())
assert w(nx.star_graph(15))-w(nx.disjoint_union(nx.star_graph(7),nx.cycle_graph(8)))==76
assert F(2*76,1)/F(3,4)**2==F(2432,9)
for U in range(3,30):
    X=nx.cycle_graph(3);X.add_edges_from((0,j) for j in range(3,U))
    assert w(X)-U==(U-2)*(U-3)//2
print('PASS: exact thresholds, 986 trees, phase lattice, H17 embeddings/cycles, SMT gadgets, rotations, endpoint wedges.')
