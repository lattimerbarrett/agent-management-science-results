import networkx as nx,itertools,json,z3
from collections import Counter
from pathlib import Path
H=nx.node_link_graph(json.load(open('workspace/agent2_glue_b_vs_clique.json')))

def no_two_p3(F):
    triples=[set(T)for T in itertools.combinations(F,3)if F.subgraph(T).number_of_edges()>=2]
    return not any(not S&T for i,S in enumerate(triples)for T in triples[:i])

def certificate(F,f):
    q=len(F);N=q+3;vs=list(H);S=z3.Solver();S.set(timeout=30000);ls={v:z3.Int('l'+str(i))for i,v in enumerate(vs)}
    S.add(*[z3.And(x>=0,x<N)for x in ls.values()])
    for u,v in H.edges():
        x,y=ls[u],ls[v]
        S.add(z3.Or(x==0,y==0,z3.And(x==2,y==2),*[z3.Or(z3.And(x==u+3,y==v+3),z3.And(x==v+3,y==u+3))for u,v in F.edges()]))
    # x=0,y=0 is permitted, with the induced graph constrained to a matching.
    for v in H:
        for c in [0,2]:S.add(z3.Implies(ls[v]==c,z3.PbLe([(ls[w]==c,1)for w in H[v]],1)))
    S.add(z3.PbLe([(ls[v]==2,1)for v in H],2*f))
    for c in range(3,N):S.add(z3.PbLe([(ls[v]==c,1)for v in H],1))
    st=S.check();assert st==z3.sat,(len(F),list(F.edges()),f,st)
    m=S.model();lab={v:m.eval(ls[v]).as_long()for v in H}
    # Build an actual finite host, then explicitly inject H into it.
    h=len(H);A=list(range(2*h));Bc=list(range(2*h,3*h));Bm=list(range(3*h,3*h+2*f));Br=list(range(3*h+2*f,3*h+2*f+q));B=Bc+Bm+Br
    R=nx.Graph();R.add_nodes_from(A+B);R.add_edges_from((x,y)for x in A for y in B);R.add_edges_from((i,i+1)for i in range(0,2*h,2));R.add_edges_from((Bm[i],Bm[i+1])for i in range(0,2*f,2));R.add_edges_from((Br[u],Br[v])for u,v in F.edges())
    image={}
    for c,pairs,available in [(0,[(i,i+1)for i in range(0,2*h,2)],A),(2,[(Bm[i],Bm[i+1])for i in range(0,2*f,2)],Bm)]:
        Q=H.subgraph([v for v in H if lab[v]==c]);used=set();pi=iter(pairs)
        for u,v in Q.edges():
            a,b=next(pi);image[u]=a;image[v]=b;used|={a,b}
        avail=iter([i for i in available if i not in used])
        for v in nx.isolates(Q):image[v]=next(avail)
    for v,i in zip([v for v in H if lab[v]==1],Bc):image[v]=i
    for v in H:
        if lab[v]>=3:image[v]=Br[lab[v]-3]
    assert len(image)==h and len(set(image.values()))==h
    assert all(R.has_edge(image[u],image[v])for u,v in H.edges())
    return {'F_graph6':nx.to_graph6_bytes(F,header=False).decode().strip(),'extra_matching':f,'H_nodes':[str(v)for v in H],'H_edges':[[str(u),str(v)]for u,v in H.edges()],'image':{str(v):i for v,i in image.items()},'host_edges':list(R.edges())}

if __name__=='__main__':
    out=[]
    for F in nx.graph_atlas_g():
        if len(F)<3 or not nx.is_connected(F)or max(dict(F.degree()).values())>3 or not no_two_p3(F):continue
        f=8-F.number_of_edges();assert f>=0
        out.append(certificate(F,f));print(len(out),len(F),F.number_of_edges(),f,flush=True)
    assert len(out)==21
    out.append(certificate(nx.empty_graph(0),8))
    Path('workspace/agent4_H47_B8_certificates.json').write_text(json.dumps(out))
    print('ALL22 positive actual-host certificates passed (21 connected types + pure matching).')
