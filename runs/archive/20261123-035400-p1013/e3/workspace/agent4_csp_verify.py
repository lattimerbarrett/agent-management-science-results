import itertools,networkx as nx,z3

def check_dictators(r,m):
    vs=list(itertools.product(range(r),repeat=m));idx={v:i for i,v in enumerate(vs)}
    cs=[z3.Int('c_'+str(i)) for i in range(len(vs))]
    S=z3.Solver()
    S.add(*[z3.And(c>=0,c<r) for c in cs])
    for i,x in enumerate(vs):
        for j in range(i):
            if all(a!=b for a,b in zip(x,vs[j])):S.add(cs[i]!=cs[j])
    for a in range(r):S.add(cs[idx[(a,)*m]]==a)
    # An anchored non-dictator coloring must fail every projection.
    for t in range(m):S.add(z3.Or(*[cs[i]!=x[t] for i,x in enumerate(vs)]))
    assert S.check()==z3.unsat,(r,m)

def csp_graph(Fs,r):
    m=len(Fs);rows=[]
    # One row selects each Fi; all other port graphs properly r-colored.
    for i in range(m):
        row=[]
        for j,F in enumerate(Fs):
            proper=nx.coloring.greedy_color(F)
            assert max(proper.values())<r
            row.extend([0 if i==j else proper[v] for v in F])
        rows.append(row)
    D=list(itertools.product(range(r),repeat=m));H=nx.Graph();H.add_nodes_from(('h',x)for x in D)
    for i,x in enumerate(D):
        for y in D[:i]:
            if all(a!=b for a,b in zip(x,y)):H.add_edge(('h',x),('h',y))
    offset=0;portsets=[]
    for F in Fs:
        ports=[('p',offset+j)for j in range(len(F))];portsets.append(ports)
        H.add_edges_from((ports[a],ports[b])for a,b in F.edges())
        for j,p in enumerate(ports):
            col=tuple(rows[t][offset+j]for t in range(m));aux=[('a',offset+j,k)for k in range(r-1)]
            H.add_edges_from(itertools.combinations(aux,2))
            H.add_edges_from((a,('h',col))for a in aux);H.add_edges_from((a,p)for a in aux)
        offset+=len(F)
    return H,portsets

def k_colorable(H,k):
    vs=list(H);ids={v:i for i,v in enumerate(vs)};cs=[z3.Int('v'+str(i))for i in range(len(vs))];S=z3.Solver()
    S.add(*[z3.And(c>=0,c<k)for c in cs]);S.add(*[cs[ids[a]]!=cs[ids[b]]for a,b in H.edges()])
    return S.check()==z3.sat

if __name__=='__main__':
    for r,m in [(3,1),(3,2),(3,3),(4,2)]:
        check_dictators(r,m);print('dictators verified',r,m,flush=True)
    Fs=[nx.complete_graph(3),nx.path_graph(4),nx.star_graph(3)]
    H,ps=csp_graph(Fs,3)
    assert not k_colorable(H,3)
    assert k_colorable(H,4)
    H.remove_node(ps[2][0])
    assert k_colorable(H,3)
    print('CSP graph has chi4 and designated critical vertex; verified with Z3.')
