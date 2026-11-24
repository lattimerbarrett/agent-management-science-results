"""Exact lower count for d=9 safe-set construction."""
import itertools

def certificate():
    groups=[set(range(0,3)),set(range(3,6)),set(range(6,9))]
    V=[frozenset(S) for S in itertools.combinations(range(9),4) if all(set(S)&g for g in groups)]
    I=[S for S in V if 0 in S]
    J=[S for S in V if 0 not in S]
    assert len(I)==36 and len(J)==45
    N=[sum(1<<i for i,S in enumerate(I) if not(S&T)) for T in J]
    sums=[];counts=[]
    for r in range(4):
        total=0;count=0
        for ids in itertools.combinations(range(len(J)),r):
            if all(J[i]&J[j] for i,j in itertools.combinations(ids,2)):
                U=0
                for i in ids: U|=N[i]
                total+=1<<(36-U.bit_count());count+=1
        sums.append(total);counts.append(count)
    return counts,sums

if __name__=='__main__':
    from agent3_D7 import compute_D7
    counts,sums=certificate()
    D7=compute_D7()[0]
    assert sum(sums)>D7+1
    print('independent outside subsets counts:',counts)
    print('independent total subsets per outside size:',sums)
    print('total',sum(sums),'> D7+1 =',D7+1)
