import networkx as nx

def F_graph(s):
    v,a,b=0,1,2
    ds=list(range(3,s+1))
    leaves=list(range(s+1,2*s+1));c=leaves[0]
    us=list(range(2*s+1,3*s-1))
    H=nx.Graph()
    H.add_edges_from((a,x) for x in leaves)
    H.add_edge(b,c)
    H.add_edges_from((v,x) for x in [a,b]+ds+leaves)
    H.add_edge(b,us[0]);H.add_edges_from(zip(us,us[1:]))
    for j,u in enumerate(us):
        H.add_edges_from((u,d) for d in (ds if j%2==0 else [c]))
    return H

def independent_masks(adj, available, mask=0):
    if not available:
        yield mask;return
    bit=available&-available;i=bit.bit_length()-1
    yield from independent_masks(adj,available^bit,mask)
    yield from independent_masks(adj,(available^bit)&~adj[i],mask|bit)

def check(s):
    H=F_graph(s);n=len(H);full=(1<<n)-1
    adj=[sum(1<<w for w in H.neighbors(i)) for i in range(n)]
    tested=0;triangle=False;longpath=False;longstar=False
    for mask in independent_masks(adj,full):
        tested+=1;R=full^mask;seen=0;comps=[]
        for i in range(n):
            if not(R>>i&1) or seen>>i&1:continue
            stack=[i];seen|=1<<i;ds=[]
            while stack:
                x=stack.pop();ds.append((adj[x]&R).bit_count())
                add=adj[x]&R&~seen
                while add:
                    bit=add&-add;add-=bit;seen|=bit;stack.append(bit.bit_length()-1)
            comps.append((len(ds),sum(ds)//2,max(ds)))
        def paths(t):return all(q<=t and e==q-1 and D<=2 for q,e,D in comps)
        def stars(t):return all(q<=t and e==q-1 and (q<=2 or D==q-1) for q,e,D in comps)
        assert not paths(s),(s,mask,comps)
        assert not stars(s),(s,mask,comps)
        triangle|=all(q==1 or(q==3 and e==3) for q,e,D in comps)
        longpath|=paths(s+1)
        longstar|=stars(s+1)
    assert triangle and longpath and longstar,(s,triangle,longpath,longstar)
    return tested

if __name__=='__main__':
    for s in [3,4,5,6,8,11]:
        print(s,check(s),flush=True)
