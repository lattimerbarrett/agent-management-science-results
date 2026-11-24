from functools import lru_cache

def intersecting_upsets(n):
    # Minimal members of an intersecting upset form an antichain
    # of nonempty sets which is pairwise intersecting, and conversely.
    vertices=list(range(1,1<<n));N=len(vertices)
    adj=[sum(1<<j for j,y in enumerate(vertices) if x!=y and (x&y==x or x&y==y or not(x&y))) for x in vertices]
    @lru_cache(None)
    def f(S):
        if not S:return 1
        degmax=-1;v=None;isolated=0;T=S
        while T:
            b=T&-T;T-=b;x=b.bit_length()-1
            d=(adj[x]&S).bit_count()
            if d==0:isolated|=b
            elif d>degmax:degmax=d;v=x
        if isolated:return (1<<isolated.bit_count())*f(S^isolated)
        return f(S^(1<<v))+f(S&~((1<<v)|adj[v]))
    return f((1<<N)-1),f.cache_info()

if __name__=='__main__':
    for n,e in enumerate([1,2,4,12,81,2646,1422564]):
        answer,info=intersecting_upsets(n)
        assert answer==e,(n,answer,e)
        print(f'lambda({n+1})={answer}',info,flush=True)
