import os
os.makedirs('workspace',exist_ok=True)
code = r'''"""Executable checks for the 1/9 lower-bound construction. No external programs."""
import itertools
import networkx as nx

def seed_subdivision(F):
    B=nx.Graph()
    for u in F: B.add_node(('U',u),part='U',label=u)
    for u,v in F.edges():
        # Orientation inherited from the supplied edge iterator.
        x=('X',u,v); y=('Y',u,v)
        B.add_node(x,part='X',label=u); B.add_node(y,part='Y',label=v)
        B.add_edges_from([(('U',u),x),(x,y),(y,('U',v))])
    return B

def construction(F, independent_sets, W=1, leaf_size=None):
    B=seed_subdivision(F)
    counts=[sum(u in A for A in independent_sets) for u in F]
    k=min(counts)
    if leaf_size is None: leaf_size=k*W
    for A in independent_sets:
        assert all(not F.has_edge(u,v) for u,v in itertools.combinations(A,2))
    for typ,part in [('D','U'),('P','X'),('Q','Y')]:
        pads=[]
        for i,A in enumerate(independent_sets):
            for j in range(W):
                p=(typ,i,j); pads.append(p); B.add_node(p,part=typ)
                B.add_edges_from((p,z) for z,d in list(B.nodes(data=True))
                                if d['part']==part and d['label'] in A)
        for j in range(leaf_size):
            l=('L'+typ,j); B.add_node(l,part='L'+typ)
            B.add_edges_from((l,p) for p in pads)
    return B,k

def has_cycle5(G):
    # Every 5-cycle has a uniquely minimum vertex in this integer ordering.
    adj=[set() for _ in G]; ids={u:i for i,u in enumerate(G)}
    for u,v in G.edges():
        a,b=ids[u],ids[v];adj[a].add(b);adj[b].add(a)
    for a in range(len(adj)):
        for b in adj[a]:
            if b<=a: continue
            for c in adj[b]-{a}:
                if c<=a:continue
                for d in adj[c]-{a,b}:
                    if d<=a:continue
                    if (adj[d]&adj[a])-{a,b,c,d}:return True
    return False

def check_local_lemma():
    count=0
    for n in range(1,5):
        pairs=list(itertools.combinations(range(n),2))
        # absent, forward, backward = every orientation of every graph.
        for choices in itertools.product(range(3),repeat=len(pairs)):
            F=nx.DiGraph();F.add_nodes_from(range(n))
            for (u,v),c in zip(pairs,choices):
                if c:F.add_edge(*((u,v) if c==1 else (v,u)))
            B=seed_subdivision(F)
            for a in B:
                for b in B[a]:
                    for c in B[b]:
                        for d in B[c]:
                            if B.nodes[a]['part']==B.nodes[d]['part']:
                                x=B.nodes[a]['label'];y=B.nodes[d]['label']
                                assert F.has_edge(x,y) or F.has_edge(y,x)
            count+=1
    return count

def main():
    local=check_local_lemma()
    results=[]
    for N,k in [(3,1),(5,2),(7,3)]:
        verts=list(itertools.combinations(range(N),k));F=nx.Graph();F.add_nodes_from(verts)
        F.add_edges_from((u,v) for u,v in itertools.combinations(verts,2) if set(u).isdisjoint(v))
        independent=[{u for u in verts if i in u} for i in range(N)]
        G,kk=construction(F,independent)
        assert kk==k
        assert sum(nx.triangles(G).values())==0
        assert not has_cycle5(G)
        b=len(F)+2*F.number_of_edges()
        assert len(G)==b+3*(N+k)
        assert min(dict(G.degree()).values())>=k
        results.append((N,k,len(G),min(dict(G.degree()).values()),G.number_of_edges()))
    print('All oriented graphs on <=4 vertices checked:',local)
    print('Columns N,k,|G|,minimum degree,edges:')
    for r in results:print(r)
    print('Exact limiting ratio k/[3(N+k)] tends to 1/9 for N=2k+t, fixed t.')

if __name__=='__main__':main()
'''
open('workspace/agent2_lower_checks.py','w').write(code)
extra = r'''

def check_parameters():
    from fractions import Fraction
    tests=[]
    for c in map(Fraction,['0','1/20','1/10','11/100','111/1000']):
        k=4
        while Fraction(k-2,3*(3*k-2))<=c:k+=2
        p=Fraction(k-2,2*k)
        limit=p/(3*(1+p))
        assert Fraction(1,9)-limit==Fraction(4,9*(3*k-2))
        # M is any cover size divisible by k; arithmetic does not depend on N!.
        M=37*k; r=37*(k//2-1); b=1000
        gap=r-3*c*(M+r)
        assert gap>0
        W=int(c*b/gap)+1
        order=b+3*(M+r)*W
        assert Fraction(r*W,order)>c
        tests.append((str(c),k,W,str(Fraction(r*W,order))))
    print('Exact parameter checks c,k,W,degree/order lower bound:',tests)

if __name__=='__main__':check_parameters()
'''
open('workspace/agent2_lower_checks.py','a').write(extra)
exec(compile(code+extra,'workspace/agent2_lower_checks.py','exec'))