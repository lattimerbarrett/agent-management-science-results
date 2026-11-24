from itertools import combinations

def H(k,mode):
    edges=[];adj=[0]*(1+2*k)
    def edge(u,v):edges.append((u,v))
    for i in range(k):
        a,b=1+2*i,2+2*i
        edge(0,a);edge(0,b);edge(a,b)
    pairs=list(combinations(range(k),2)) if mode=='complete' else [(i,i+1) for i in range(k-1)]
    for i,j in pairs:
        for d in (1,2):
            w=len(adj);adj.append(0);edge(d+2*i,w);edge(w,d+2*j)
    for u,v in edges:adj[u]|=1<<v;adj[v]|=1<<u
    return adj

def fit(color,adj):
    # A monochromatic graph embeds in two disjoint triangles iff its edge-support
    # has <=2 components, each having <=3 vertices.
    support=0
    for u,N in enumerate(adj):
        if (color>>u)&1 and N&color:
            if (N&color).bit_count()>2:return False
            support|=1<<u
    nc=0
    while support:
        nc+=1
        if nc>2:return False
        front=support&-support;comp=0
        while front:
            u=front.bit_length()-1;front^=1<<u;comp|=1<<u
            front|=adj[u]&color&~comp
            if (comp|front).bit_count()>3:return False
        support&=~comp
    return True

for k,mode in [(2,'chain'),(3,'chain'),(4,'chain'),(4,'complete')]:
    adj=H(k,mode);n=len(adj);full=(1<<n)-1;found=None
    for code in range(1<<(n-1)):
        c=code<<1 # fix common fan center in color0
        if fit(c,adj) and fit(full^c,adj):found=c;break
    print(k,mode,n,'embeds in split2K3',found is not None,'color',found,flush=True)
import shutil
shutil.copyfile('scratchpad.py','workspace/agent4_connector_test.py')
