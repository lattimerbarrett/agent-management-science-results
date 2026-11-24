"""Exact cyclic color-word Hamilton marginal computation; integers only."""
from functools import lru_cache
from math import comb
from fractions import Fraction

def ham_word_counts(m,r=3):
    @lru_cache(None)
    def f(counts,last,bad):
        if sum(counts)==r*m:
            return int(bad+(last==0)==0),int(bad+(last==0)==1)
        ans=[0,0]
        for j in range(r):
            if counts[j]<m and bad+(j==last)<=1:
                cc=list(counts);cc[j]+=1
                v=f(tuple(cc),j,bad+(j==last))
                ans[0]+=v[0];ans[1]+=v[1]
        return tuple(ans)
    return f((1,)+(0,)*(r-1),0,0)

def marginal(m,r=3):
    a,b=ham_word_counts(m,r)
    return Fraction(b,a*r*comb(m,2))

if __name__=='__main__':
    for m in (3,5,10,15,20,30):
        q=marginal(m)
        print(m, 'n times internal marginal:',float(3*m*q), 'cross:',3)
