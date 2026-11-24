from functools import lru_cache
from time import time

def dedekind(n):
    N=1<<n
    adj=[sum(1<<y for y in range(N) if y!=x and (x&y==x or x&y==y)) for x in range(N)]
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
    answer=f((1<<N)-1)
    return answer,f.cache_info()

if __name__=='__main__':
    expected=[3,6,20,168,7581,7828354,2414682040998]
    for n,e in enumerate(expected,1):
        start=time();a,info=dedekind(n)
        assert a==e
        print(n,a,info,time()-start,flush=True)
