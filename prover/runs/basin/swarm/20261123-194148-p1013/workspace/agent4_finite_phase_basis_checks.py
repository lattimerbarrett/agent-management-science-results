import networkx as nx, itertools, json, random
from collections import Counter

def embeds(G,H):
    return len(G)<=len(H) and G.number_of_edges()<=H.number_of_edges() and nx.algorithms.isomorphism.GraphMatcher(H,G).subgraph_is_monomorphic()

def threecolor(G):
    order=sorted(G,key=lambda v:-G.degree(v)); col={}
    def rec(i):
        if i==len(order):return True
        v=order[i]
        for c in range(3):
            if all(col.get(w)!=c for w in G[v]):
                col[v]=c
                if rec(i+1):return True
                del col[v]
        return False
    return rec(0)

def connected_basis_check(hosts):
    cache={}
    def good(G):
        key=nx.weisfeiler_lehman_graph_hash(G) # only optimization; don't use collisions
        return any(embeds(G,H) for H in hosts)
    minimal=[]; connected=0
    for G in nx.graph_atlas_g():
        if not len(G) or not nx.is_connected(G):continue
        connected+=1
        if good(G):continue
        isminimal=True
        for v in list(G):
            F=G.copy();F.remove_node(v)
            if len(F) and nx.is_connected(F) and not good(F):isminimal=False;break
        if not isminimal:continue
        for e in list(G.edges):
            F=G.copy();F.remove_edge(*e)
            if nx.is_connected(F) and not good(F):isminimal=False;break
        if isminimal:
            assert threecolor(G), nx.to_graph6_bytes(G)
            assert len(G)<=max(map(len,hosts))+1
            minimal.append((len(G),G.number_of_edges()))
    return {'connected_atlas_graphs_checked':connected,'minimal_obstructions':len(minimal),'by_order':dict(Counter(v for v,e in minimal))}

def phase_check():
    # k=4, markers C5 and C6. Connected catalogue: paths <=6,
    # claw, C5, C6. Exact cycle embedding criterion for nonfree union.
    cat=[('P',j) for j in range(1,7)]+[('S',4),('C',5),('C',6)]
    def free(t,i):
        kind,j=t
        return (kind=='P' and j<= (3 if i==0 else 4)) or (i==0 and kind=='S')
    def accept(types,i):
        bad=[t for t in types if not free(t,i)]; u=5+i
        return (not bad or (all(t[0]=='P' for t in bad) and sum(t[1] for t in bad)<=u) or bad==[('C',u)])
    random.seed(7701); checked=0
    for trial in range(5000):
        types=[random.choice(cat) for _ in range(random.randrange(25))]
        if any(accept(types,i) for i in (0,1)):continue
        selected=set()
        for i in (0,1):
            witness=[]; inds=[]
            for j,t in enumerate(types):
                if free(t,i):continue
                before=sum(v for kind,v in witness)
                assert before<=5+i
                witness.append(t);inds.append(j)
                if not accept(witness,i):break
            assert not accept(witness,i)
            assert sum(v for kind,v in witness)<=5+i+6
            selected.update(inds)
        W=[types[j] for j in selected]
        assert sum(v for kind,v in W)<=5+6+12
        assert not any(accept(W,i) for i in (0,1))
        checked+=1
    return checked

def edge_profiles():
    cases=0
    for k in range(2,8):
        for u in range(k,10):
            G=nx.cycle_graph(u); es=list(G.edges)
            marker=[]
            for mask in range(1<<u):
                F=nx.Graph();F.add_edges_from(e for j,e in enumerate(es) if mask>>j&1)
                marker.append((len(F),F.number_of_edges(),mask==(1<<u)-1))
            for a in range(u,u+3*k+1):
                def bulk(x):return x-(x+k-1)//k
                target=a-(a-u+k-1)//k
                assert u+bulk(a-u)==target
                for v,e,full in marker:
                    val=e+bulk(a-v)
                    assert val<=target
                    if not full:assert val<target
                    cases+=1
    return cases

if __name__=='__main__':
    hosts=[nx.star_graph(3),nx.path_graph(4),nx.cycle_graph(5),nx.cycle_graph(6)]
    X=nx.cycle_graph(3);X.add_edges_from((0,v) for v in range(3,7))
    result={'cycle_catalogue':connected_basis_check(hosts),'unicyclic_leaf_catalogue':connected_basis_check([nx.star_graph(3),nx.path_graph(4),X,nx.cycle_graph(6)]),'random_failure_witnesses':phase_check(),'exhaustive_cycle_marker_edge_profile_inequalities':edge_profiles()}
    print(json.dumps(result,indent=2));open('workspace/agent4_finite_phase_basis_checks.json','w').write(json.dumps(result,indent=2))
