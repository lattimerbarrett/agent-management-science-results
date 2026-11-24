"""Exact finite checks for the elementary dense-Dirac counting proof.
The proof itself is in agent2_dirac_count.md. These are finite checks,
not a substitute for the quantified max-flow and counting arguments.
"""

def check_factor_cuts(max_side=50):
    checks=0
    for m in range(2,max_side+1):
        for delta in range(m//2+1,m+1):
            r=min(delta//2,2*delta-m)
            for x in range(1,m+1):
                for y in range(1,m+1):
                    s=x+y-m
                    if s<=0:continue
                    lower=max(x*max(0,delta-m+y),y*max(0,delta-m+x))
                    assert lower>=r*s,(m,delta,r,x,y,lower,r*s)
                    checks+=1
    return checks

if __name__=='__main__':
    print('r-factor cut checks:',check_factor_cuts())
