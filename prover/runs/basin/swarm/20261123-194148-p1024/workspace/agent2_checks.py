import sympy as sp
import random, json

def verify_bounds(g):
    r=(g+2)//3; k=g-r; N=4*g-3; d=2*g-2; D=2*g-1-k
    assert D<=3*k
    for n in range(N):
        R=3*n+4*g
        # A source just beyond cutoff is safely past semigroup conductor.
        assert n-d+R+1>=2*g
        # Every later fiber coefficient stays in its row window.
        for j in range((N-1-n)//k+1):
            m=n+j*k
            assert -R-j*D>=-(3*m+4*g)
            # S horizontal to vertical costs just one extra t power.
            assert -R-j*D-1>=-(3*m+4*g+1)
    return True

def rank_check(g,b):
    r=(g+2)//3; s=max(i for i,c in enumerate(b) if c)
    for n in range(1,g+r-1):
        A=n//2; L=(g+r-2-n)//2
        if L<0: continue
        H=sp.Matrix([[b[a+l] if a+l<r else 0 for a in range(A+1)] for l in range(L+1)])
        expected=min(A+1,L+1,s+1)
        assert H.rank()==expected,(g,b,n,H,H.rank(),expected)

for g in range(2,151): verify_bounds(g)
random.seed(103)
for g in range(2,23):
    r=(g+2)//3
    for s in range(r):
        for rep in range(2):
            b=[random.randrange(-3,4) for _ in range(s)]+[random.choice([-2,-1,1,2])]+[0]*(r-s-1)
            rank_check(g,b)
print('Checked cutoff closure/conductor for all g=2..150; exact Hankel rank lemma for rational vectors at every support height, g=2..22.')
