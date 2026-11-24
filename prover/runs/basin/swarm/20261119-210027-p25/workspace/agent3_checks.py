import itertools, json, math
from pathlib import Path

def shift_graph(m,k):
    V=list(itertools.combinations(range(m),k)); idx={v:i for i,v in enumerate(V)}
    E=[(idx[a[:-1]],idx[a[1:]]) for a in itertools.combinations(range(m),k+1)]
    return V,E

def checks_shift():
    out=[]
    for m,k in [(5,3),(8,6),(9,7),(10,7)]:
        V,E=shift_graph(m,k)
        maxerror=0
        # All sign assignments, all edges; exact alternating-score cancellation.
        for z in itertools.product((-1,1),repeat=m):
            scores=[sum((-1)**(i+1)*z[a] for i,a in enumerate(v)) for v in V]
            for u,v in E:
                error=abs(scores[u]+scores[v]); assert error<=2
                maxerror=max(maxerror,error)
                if scores[u]>3: assert scores[v]<=3
        # Adjacency-matrix boolean powers detect every closed odd walk <=5.
        import numpy as np
        A=np.zeros((len(V),len(V)),dtype=object)
        for u,v in E: A[u,v]=A[v,u]=1
        A3=A@A@A; A5=A3@A@A
        if k>5:
            assert sum(A3[i,i] for i in range(len(V)))==0
            assert sum(A5[i,i] for i in range(len(V)))==0
        out.append(dict(m=m,k=k,vertices=len(V),edges=len(E),max_score_edge_error=maxerror))
    return out

def checks_packing(maxn=6):
    # Profile triangle conditions from the proof; verify six blocks literally
    # disjoint and hence |A|+|B|+|C|+3d <= n.
    counts=[]
    for n in range(1,maxn+1):
        pairs=list(itertools.combinations(range(n),2)); graphs=triples=0
        for mask in range(1<<len(pairs)):
            N=[0]*n
            for j,(u,v) in enumerate(pairs):
                if mask>>j&1: N[u]|=1<<v;N[v]|=1<<u
            d=min(map(int.bit_count,N))
            if d==0: continue
            graphs+=1
            prof=[]
            for a in range(1,1<<n):
                na=0
                for u in range(n):
                    if a>>u&1: na|=N[u]
                if not a&na: prof.append((a,na))
            for (a,na),(b,nb),(c,nc) in itertools.combinations(prof,3):
                if (a&b or a&c or b&c or na&nb or na&nc or nb&nc):continue
                if (a&(nb|nc) or b&(na|nc) or c&(na|nb)):continue
                blocks=[a,b,c,na,nb,nc]
                for x,y in itertools.combinations(blocks,2): assert not x&y
                assert sum(map(int.bit_count,blocks))<=n
                assert a.bit_count()+b.bit_count()+c.bit_count()+3*d<=n
                if min(a.bit_count(),b.bit_count(),c.bit_count())>=2*d:
                    assert 9*d<=n
                triples+=1
        counts.append(dict(n=n,positive_min_degree_graphs=graphs,admissible_profile_triples=triples))
    return counts

def support_ratios():
    out=[]
    for k in [7,31,127,511,2047]:
        num=sum(math.comb(k,j) for j in range((k+5)//2,k+1));den=1<<k
        p=num/den; out.append(dict(k=k,p=p,limiting_density=p/(3*(1+p))))
    return out

if __name__=='__main__':
    result=dict(shift=checks_shift(),packing=checks_packing(),support_ratios=support_ratios())
    print(json.dumps(result,indent=2))
    Path('workspace/agent3_checks.json').write_text(json.dumps(result,indent=2))
    Path('workspace/agent3_checks.py').write_text(Path(__file__).read_text())
