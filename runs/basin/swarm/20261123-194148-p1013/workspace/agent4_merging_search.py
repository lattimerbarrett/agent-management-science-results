import networkx as nx,itertools,json,time
from functools import lru_cache
atlas=nx.graph_atlas_g()
def strip(G):return nx.convert_node_labels_to_integers(G.subgraph([u for u in G if G.degree(u)]))
buckets={}; reps=[]
def canon(G):
    G=strip(G);key=(len(G),G.number_of_edges(),tuple(sorted(dict(G.degree()).values())))
    for idx in buckets.get(key,[]):
        if nx.is_isomorphic(G,reps[idx]):return idx
    idx=len(reps);reps.append(G);buckets.setdefault(key,[]).append(idx);return idx
empty=canon(nx.Graph())
Fids=sorted(set(canon(F) for F in atlas if len(F)<=5))
@lru_cache(None)
def emb(p,q):
    P,Q=reps[p],reps[q]
    return len(P)<=len(Q) and P.number_of_edges()<=Q.number_of_edges() and nx.algorithms.isomorphism.GraphMatcher(Q,P).subgraph_is_monomorphic()
Hs=[]
for H in atlas:
    if nx.is_bipartite(H) or not any(nx.is_bipartite(nx.subgraph(H,[u for u in H if u!=v])) for v in H):continue
    prof=set();match=False;vs=list(H)
    for mask in range(1<<len(vs)):
        A=[v for j,v in enumerate(vs) if mask>>j&1];B=[v for j,v in enumerate(vs) if not(mask>>j&1)]
        p,q=canon(H.subgraph(A)),canon(H.subgraph(B));prof.add((p,q))
        if p==empty and max(dict(reps[q].degree()).values(),default=0)<=1:match=True
    if match:Hs.append((H,prof))
print('Hs',len(Hs),'Ftypes',len(Fids),'patterns',len(reps),flush=True)
cases=0
for hi,(H,prof) in enumerate(Hs):
    one={q for p,q in prof if p==empty}
    for ai,a in enumerate(Fids):
        for b in Fids[ai:]:
            if any(emb(p,a) and emb(q,b) for p,q in prof):continue
            merged=canon(nx.disjoint_union(reps[a],reps[b]))
            cases+=1
            if any(emb(p,merged) for p in one):
                result={'counterexample':True,'H':list(H.edges),'H_order':len(H),'A':list(reps[a].edges),'B':list(reps[b].edges),'cases':cases}
                print(json.dumps(result),flush=True);open('workspace/agent4_merging_search.json','w').write(json.dumps(result));raise SystemExit
print(json.dumps({'counterexample':False,'Hs':len(Hs),'Ftypes':len(Fids),'Hfree_pairs_checked':cases}),flush=True)
open('workspace/agent4_merging_search.json','w').write(json.dumps({'counterexample':False,'Hs':len(Hs),'Ftypes':len(Fids),'Hfree_pairs_checked':cases}))
