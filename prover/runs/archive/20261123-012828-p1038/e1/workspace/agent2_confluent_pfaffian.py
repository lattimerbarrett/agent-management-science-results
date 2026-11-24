"""Confluent Schur-Pfaffian numerical checks, independent high derivatives."""
import mpmath as mp
import random
from agent2_elliptic_pfaffian import pf

def check(cases=30,dps=100):
    mp.mp.dps=dps; rng=random.Random(274); worst=mp.mpf(0)
    for case in range(cases):
        q=mp.mpf(rng.uniform(.1,.9)); tau=mp.mpf(rng.uniform(.1,3))
        def y(x):
            a=q*(x-1/x)-tau
            return 2/(mp.sqrt(a*a+4)-a)
        def z(x): return y(x)/x
        def L(s,t): return (y(t)-y(s))/(mp.sqrt(q*z(s)*z(t))*(1+s*t))
        j=rng.randint(1,3)
        ds=[rng.randint(1,3) for _ in range(j)]
        if sum(ds)%2:ds[-1]+=1
        centers=sorted(mp.mpf(v) for v in rng.sample(range(2,80),j))
        centers=[v/20 for v in centers]
        ids=[(c,k) for c,d in zip(centers,ds) for k in range(d)]
        matrix=[[mp.diff(L,(c,d),(p,r))/(mp.factorial(p)*mp.factorial(r)) for d,r in ids] for c,p in ids]
        actual=pf(matrix); expected=mp.mpf(1)
        for c,d in zip(centers,ds):
            kap=mp.diff(y,c)/(mp.sqrt(q)*z(c)*(1+c*c))
            expected*=kap**(d*(d-1)//2)
        for i,c in enumerate(centers):
            for k in range(i+1,len(centers)):
                expected*=L(c,centers[k])**(ds[i]*ds[k])
        err=abs(actual-expected)/abs(expected)
        worst=max(worst,err)
        assert actual>0 and expected>0
        assert err<mp.mpf('1e-60'), (case,ds,err)
    return {'cases':cases,'digits':dps,'worst_relative_error':str(worst)}
if __name__=='__main__':print(check())
