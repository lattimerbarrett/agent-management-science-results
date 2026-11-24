"""Actually construct finite colorings and count EVERY monochromatic book."""
import random, math

def construct(N, alpha, kind='tripartite', seed=8675309):
    rng=random.Random(seed)
    R=[0]*N
    p=(3*math.sqrt(alpha)/(math.sqrt(3-2*alpha)+2*math.sqrt(alpha))
       if kind=='tripartite' else math.sqrt(alpha)/(1+math.sqrt(alpha)))
    for i in range(N):
        for j in range(i+1,N):
            if (kind!='tripartite' or i%3!=j%3) and rng.random()<p:
                R[i]|=1<<j
                R[j]|=1<<i
    mask=(1<<N)-1
    B=[mask^r^(1<<i) for i,r in enumerate(R)]
    return R,B

def largest_books(R,B):
    ans=[0,0]
    for col,rows in enumerate((R,B)):
        for i,r in enumerate(rows):
            remaining=r & ~((1<<(i+1))-1)
            while remaining:
                bit=remaining & -remaining
                j=bit.bit_length()-1
                ans[col]=max(ans[col],(r & rows[j]).bit_count())
                remaining-=bit
    return tuple(ans)

if __name__=='__main__':
    for kind,alpha,n,N in [('tripartite',.2,500,600),('random',1.,250,600)]:
        R,B=construct(N,alpha,kind)
        redbook,bluebook=largest_books(R,B)
        assert redbook < math.ceil(alpha*n)
        assert bluebook < n
        print(kind, 'N=',N,'largest redbook=',redbook,'largest bluebook=',bluebook,
              'forbidden=',(math.ceil(alpha*n),n))
