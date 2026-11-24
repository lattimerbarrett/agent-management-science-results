from fractions import Fraction as Q
from itertools import product
from math import floor

def losses(r,t,j):
    # Relative to j=0; signed sum of exact edge-loss increments.
    inc=lambda z:z-((t-z-1)//(r-1))
    return sum(inc(z) for z in range(j)) if j>=0 else -sum(inc(z) for z in range(j,0))

def verify_profiles(max_r=10):
    checks=0
    js=list(range(-3,5))
    for r in range(3,max_r+1):
      for t in range(r):
       L={j:losses(r,t,j) for j in js}
       for bits in product((0,1),repeat=len(js)-1):
        E={js[0]:0}
        for j,b in zip(js,bits):E[j+1]=E[j]+b
        K={j:E[j]-L[j] for j in js}
        mx=max(K.values()); opts=[j for j in js if K[j]==mx]
        assert set(opts)<= {0,1,2}
        assert (0 if t==0 else 1) in opts
        for rho in (Q(1,2),Q(2,3),Q(5,6),Q(7,8),Q(1)):
          c=2*rho/(r-1);d=Q(r-2,r-1)
          R={j:-L[j]+c*j+d*E[j] for j in js}
          edge_best=max(R[j] for j in opts)
          for j in js:
            # Candidate can additionally sacrifice one internal edge.
            deficit=0 if j not in opts else 1
            cand=R[j]-d*deficit
            assert cand-edge_best<=-1+c,(r,t,bits,rho,j,cand-edge_best,-1+c)
            checks+=1
    return checks

if __name__=='__main__':print(verify_profiles(),'discrete-profile inequalities passed')
