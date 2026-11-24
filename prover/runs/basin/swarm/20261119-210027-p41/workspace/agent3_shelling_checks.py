"""Independent exhaustive shellability / append-lemma check, d=3,n=6."""
from itertools import combinations

def check(n=6,d=3):
    facets=tuple(sum(1<<v for v in c) for c in combinations(range(n),d+1))
    N=len(facets); full=(1<<N)-1
    def appendable(mask,j):
        F=facets[j]
        intersections=[F&G for i,G in enumerate(facets) if mask>>i&1]
        ridges=[T for T in intersections if T.bit_count()==d]
        return bool(ridges) and all(any(T&R==T for R in ridges) for T in intersections)
    shell=bytearray(1<<N)
    for mask in range(1,full+1):
        if mask.bit_count()==1:
            shell[mask]=1
        else:
            shell[mask]=any(shell[mask^(1<<j)] and appendable(mask^(1<<j),j)
                            for j in range(N) if mask>>j&1)
    transitions=0
    for mask in range(1,full+1):
        if not shell[mask]:continue
        for j in range(N):
            if not mask>>j&1 and shell[mask|(1<<j)]:
                transitions+=1
                assert appendable(mask,j), (mask,j)
    finish=bytearray(1<<N);finish[full]=1
    for mask in range(full-1,0,-1):
        if shell[mask]:
            finish[mask]=any(not mask>>j&1 and finish[mask|(1<<j)] for j in range(N))
    assert all(not shell[mask] or finish[mask] for mask in range(1,full+1))
    return dict(n=n,d=d,shellable=sum(shell),checked_transitions=transitions,
                all_shellable_completable=True)
if __name__=='__main__':print(check())
