import networkx as nx,itertools

def matching_cut(H,S):
    return all(sum(((S>>v)&1)!=((S>>w)&1)for w in H[v])<=1for v in H)

def verify():
    tests=0;unsat=0;example=None
    for H in nx.graph_atlas_g():
        n=len(H)
        if n>5 or not nx.is_bipartite(H):continue
        sigma=nx.bipartite.color(H)
        valid=[S for S in range(1<<n)if matching_cut(H,S)]
        for S in valid:
            for T in valid:
                mid=[v for v in H if ((S>>v)&1)!=((T>>v)&1)]
                comps=list(nx.connected_components(H.subgraph(mid)));owner={v:i for i,C in enumerate(comps)for v in C}
                clauses=[]
                for v in H:
                    reg=((S>>v)&1,(T>>v)&1)
                    boundary=[owner[w]for w in H[v]if w in owner]
                    if len(boundary)==2 and ((reg==(1,1)and sigma[v]==0)or(reg==(0,0)and sigma[v]==1)):
                        clauses.append((reg==(1,1),boundary))
                anysat=False
                for pick in range(1<<len(comps)):
                    R=S&T
                    for i,C in enumerate(comps):
                        if pick>>i&1:
                            for v in C:R|=1<<v
                    E=[(v,w)for v,w in H.edges()if ((R>>v)&1)!=((R>>w)&1)]
                    ds={v:0 for v in H}
                    for v,w in E:ds[v]+=1;ds[w]+=1
                    assert max(ds.values(),default=0)<=2
                    assert all(not(ds[v]==ds[w]==2)for v,w in E)
                    sec_matching=all(ds[v]<=1 for v in H if sigma[v]^((R>>v)&1)==1)
                    sat=all(any(bool(pick>>i&1)==positive for i in inds)for positive,inds in clauses)
                    assert sec_matching==sat,(list(H.edges()),S,T,pick,clauses)
                    anysat|=sat
                    tests+=1
                if not anysat:
                    unsat+=1
                    example=(list(H.edges()),S,T,clauses)
    return tests,unsat,example
if __name__=='__main__':print('verified',verify(),'componentwise uncrossings and exact 2SAT constraints')
