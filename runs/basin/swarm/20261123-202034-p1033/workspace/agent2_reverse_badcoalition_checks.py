from itertools import combinations
import json,time

def check(name,lines):
    start=time.time();W=sorted(set().union(*map(set,lines)));t=len(W);k=len(lines[0]);M=len(lines)
    assert all(len(F)==k for F in lines)
    assert all(set(F)&set(G) for F,G in combinations(lines,2))
    labels={x:i for i,x in enumerate(W)}
    blocks=[sum(1<<(i*(k-1)+j) for j in range(k-1)) for i in range(M)]
    v=1<<(M*(k-1));N=M*(k-1)+1
    def products(indices):
        out=[0]
        for i in indices:
            out=[s|(1<<(i*(k-1)+j)) for s in out for j in range(k-1)]
        return out
    Afams=[];Bfams=[]
    for x in W:
        Afams.append(products([i for i,F in enumerate(lines) if x in F]))
        Bfams.append([s|v for s in products([i for i,F in enumerate(lines) if x not in F])])
    INF=N+1;fullbest=[INF]*(1<<t);prunebest=[INF]*(1<<t)
    for S in range(1<<N):
        E=[i for i,q in enumerate(blocks) if S&q==q]
        U=set().union(*(set(lines[i]) for i in E)) if E else set()
        I=set.intersection(*(set(lines[i]) for i in E)) if E else set(W)
        predicted=U if S&v else U-I
        predmask=sum(1<<labels[x] for x in predicted)
        actual=0;prune=0
        for j,(A,B) in enumerate(zip(Afams,Bfams)):
            if all(S&a for a in A):
                prune|=1<<j
                if all(S&b for b in B):actual|=1<<j
        assert actual==predmask,(name,S,actual,predmask)
        assert prune==sum(1<<labels[x] for x in U)
        assert actual.bit_count()<=S.bit_count()
        z=S.bit_count();fullbest[actual]=min(fullbest[actual],z);prunebest[prune]=min(prunebest[prune],z)
    for j in range(t):
        for J in range(1<<t):
            if not J>>j&1:
                fullbest[J]=min(fullbest[J],fullbest[J|(1<<j)])
                prunebest[J]=min(prunebest[J],prunebest[J|(1<<j)])
    assert all(fullbest[J]>=J.bit_count() for J in range(1<<t))
    bad={J for J in range(1<<t) if prunebest[J]<J.bit_count()}
    minimal={J for J in bad if not any(K!=J and K&J==K for K in bad)}
    expected={sum(1<<labels[x] for x in F) for F in lines}
    assert minimal==expected,(name,minimal,expected)
    return dict(name=name,t=t,k=k,M=M,actual_points=N,all_actual_subsets=1<<N,
                explicit_colored_petals=sum(map(len,Afams))+sum(map(len,Bfams)),
                all_coalitions=1<<t,minimal_bad_masks=sorted(minimal),runtime=time.time()-start)

fano=sorted({tuple(sorted((a,b,a^b))) for a,b in combinations(range(1,8),2)})
results=[check('triangle',[(1,2),(1,3),(2,3)]),check('Fano',fano),check('Fano_minus_one',fano[:-1])]
print(json.dumps(results,indent=2))
Path('workspace/agent2_reverse_badcoalition_checks.json').write_text(json.dumps(results,indent=2))
