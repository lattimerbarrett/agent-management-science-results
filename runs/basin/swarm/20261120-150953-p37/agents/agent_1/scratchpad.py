import itertools, time
import networkx as nx
import z3

def maximal_intersecting_count(k):
    G=nx.Graph();G.add_nodes_from(range(1,1<<k))
    G.add_edges_from((a,b) for a in G for b in G if a<b and a&b)
    return sum(1 for _ in nx.find_cliques(G))

def masks(n):
    Q=[(v,) for v in range(n)]+list(itertools.combinations(range(n),2));N=len(Q)
    inc=[(v,e) for v in range(n) for e in range(n,N) if v in Q[e]]
    non=[(v,e) for v in range(n) for e in range(n,N) if v not in Q[e]]
    out=set(); total=3*len(inc)+len(non)
    # Exhaust all ranks. Labels can be identified on equality-components;
    # labels of components without an incidence affect no requirements.
    for rank in itertools.product(range(N),repeat=N):
        if any(rank[v]>rank[e] for v,e in inc):continue
        parent=list(range(N))
        def root(a):
            while parent[a]!=a:
                parent[a]=parent[parent[a]];a=parent[a]
            return a
        ties=[]
        for idx,(v,e) in enumerate(inc):
            if rank[v]==rank[e]:
                parent[root(e)]=root(v);ties.append((idx,v))
        groups={}
        for idx,v in ties:groups.setdefault(root(v),[]).append(idx)
        fixed=sum(1<<(3*len(inc)+j) for j,(v,e) in enumerate(non) if rank[v]>rank[e])
        groups=list(groups.values())
        for labels in itertools.product(range(3),repeat=len(groups)):
            mask=fixed
            for label,indices in zip(labels,groups):
                for idx in indices:mask|=1<<(3*idx+label)
            out.add(mask)
    return out,total

def min_cover(ms,R):
    from functools import lru_cache
    ms=[a for a in ms if not any(a!=b and a&b==a for b in ms)]
    print('undominated masks',len(ms),flush=True)
    candidates=[[m for m in ms if m>>r&1] for r in range(R)]
    @lru_cache(None)
    def search(left,k):
        if not left:return ()
        if not k:return None
        max_gain=max((m&left).bit_count() for m in ms)
        if max_gain*k<left.bit_count():return None
        bit=min((r for r in range(R) if left>>r&1),key=lambda r:len(candidates[r]))
        for m in sorted(candidates[bit],key=lambda m:-(m&left).bit_count()):
            rest=search(left&~m,k-1)
            if rest is not None:return (m,)+rest
        return None
    for D in range(3,R+1):
        witness=search((1<<R)-1,D)
        print('check',D,witness is not None,flush=True)
        if witness is not None:
            union=0
            for m in witness:union|=m
            assert union==(1<<R)-1 and len(witness)<=D
            return D

if __name__=='__main__':
    for k in range(1,8):
        t=time.time();print('lambda',k,maximal_intersecting_count(k),'seconds',time.time()-t,flush=True)
    t=time.time();ms,R=masks(3);print('n=3 masks',len(ms),'requirements',R,'seconds',time.time()-t,flush=True)
    print('exact D0',min_cover(ms,R),flush=True)
    a=[0]*(1<<R)
    for m in ms:a[m]=1
    for bit in range(R):
        step=1<<bit
        for start in range(0,1<<R,2*step):
            for j in range(start+step,start+2*step):a[j]+=a[j-step]
    full=(1<<R)-1
    for D in [3,4]:
        count=sum((-1 if t.bit_count()%2 else 1)*a[full^t]**D for t in range(1<<R))
        print('IE count',D,count,flush=True)
