from itertools import combinations
from agent4_checker import dec

def check_all():
    n=6
    candidates=[sum(1<<v for v in c) for c in combinations(range(n),4)]
    counts={1:0,2:0}
    for z in range(1,1<<len(candidates)):
        fs=tuple(sorted(f for j,f in enumerate(candidates) if z>>j&1))
        sk=tuple(sorted({f^(1<<v) for f in fs for v in range(n) if f>>v&1}))
        for k in [1,2]:
            if dec(fs,k):
                counts[k]+=1
                assert dec(sk,k-1),(fs,k,sk)
    return counts

if __name__=='__main__':
    print(check_all())
