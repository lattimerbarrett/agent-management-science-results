import networkx as nx,random,json
random.seed(4601)
h=5;M=2;L=h*(M+1)+1
G=nx.Graph();part={};comp={};position={};members={};types={};cid=0
for p in range(3):
    for j in range(L+1):
        size=3 if j<L else 4;vs=[]
        for k in range(size):
            v=len(G);G.add_node(v);part[v]=p;comp[v]=cid;position[v]=k;vs.append(v)
        members[cid]=vs;types[cid]=(p,size)
        G.add_edges_from(zip(vs,vs[1:]));cid+=1
for u in G:
    for v in G:
        if u<v and part[u]!=part[v]:G.add_edge(u,v)
holedeg={u:0 for u in G};holes=[]
for trial in range(20000):
    u,v=random.sample(list(G),2)
    if part[u]!=part[v] and G.has_edge(u,v) and holedeg[u]<M and holedeg[v]<M:
        G.remove_edge(u,v);holedeg[u]+=1;holedeg[v]+=1;holes.append((u,v))
assert max(holedeg.values())<=M
rare={c for c in members if len(members[c])==4}
completed=G.copy()
for u,v in holes:
    if comp[u] not in rare or comp[v] not in rare:completed.add_edge(u,v)
checked=0
for trial in range(5000):
    W=random.sample(list(G),h);HE=[(u,v) for u in W for v in W if u<v and completed.has_edge(u,v) and random.randrange(2)]
    groups={c:[u for u in W if comp[u]==c] for c in set(comp[u] for u in W)}
    current={u:u for u in W};occupied=set(groups)
    for c,selected in groups.items():
        if c in rare:continue
        candidates=[d for d in members if types[d]==types[c] and d not in occupied]
        chosen=None
        for d in candidates:
            proposal={u:members[d][position[u]] for u in selected}
            ok=True
            for u,v in HE:
                if u in selected and v in selected:
                    if not G.has_edge(proposal[u],proposal[v]):ok=False;break
                elif u in selected:
                    if not G.has_edge(proposal[u],current[v]):ok=False;break
                elif v in selected:
                    if not G.has_edge(current[u],proposal[v]):ok=False;break
            if ok:chosen=d;break
        assert chosen is not None,(c,selected,len(candidates))
        occupied.remove(c);occupied.add(chosen)
        for u in selected:current[u]=members[chosen][position[u]]
    assert len(set(current.values()))==h
    assert all(G.has_edge(current[u],current[v]) for u,v in HE)
    checked+=1
result={'r':3,'h':h,'hole_max_degree':M,'abundance_threshold':L,'host_order':len(G),'crossholes':len(holes),'original_rare_components':len(rare),'remapped_random_subgraphs':checked}
print(json.dumps(result,indent=2));open('workspace/agent4_finite_hole_template_checks.json','w').write(json.dumps(result,indent=2))
