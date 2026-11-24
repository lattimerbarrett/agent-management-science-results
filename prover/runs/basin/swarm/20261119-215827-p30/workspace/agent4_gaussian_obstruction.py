"""Exact construction of Gaussian obstruction matrices; no numerics required."""
from fractions import Fraction as Q

def forms(k):
    assert k>=1
    n=2*k+2
    F=[]
    # Coordinates are x_0,...,x_k,y_0,...,y_k.
    for ell in range(2*k+1):
        A=[[0]*n for _ in range(n)]
        B=[[0]*n for _ in range(n)]
        for i in range(k+1):
            h=ell-i
            if 0<=h<=k:
                A[i][h]+=1
                A[k+1+i][k+1+h]-=1
                B[i][k+1+h]+=1
                B[k+1+i][h]+=1
        if ell in (0,2*k):
            for i in range(n): A[i][i]-=1
        F.extend([A,B])
    assert all(M[i][h]==M[h][i] for M in F for i in range(n) for h in range(n))
    H=[[-F[0][i][h]-F[-2][i][h] for h in range(n)] for i in range(n)]
    assert all(H[i][h]==0 for i in range(n) for h in range(n) if i!=h)
    assert min(H[i][i] for i in range(n))>=1
    # H=-F[0]-F[-2]. The change F_i -> 3H+F_i is invertible:
    # on simultaneous bilinear zeros all F_i=t, so H=-2t, hence t=6t.
    C=[[[3*H[i][h]+M[i][h] for h in range(n)] for i in range(n)] for M in F]
    # Exact strict diagonal dominance certifies positive definiteness.
    assert all(M[i][i]>sum(abs(M[i][h]) for h in range(n) if h!=i) for M in C for i in range(n))
    assert len(C)==4*k+2
    return F,H,C

def check():
    for s in range(3,9):
        k=2**(s-2)-1
        F,H,C=forms(k)
        n=2*k+2;j=4*k+2;d=3*j//2
        assert n+j-1==d
        print(f's={s}: j={j}, d={d}, covariance residual block size={n}; {len(C)} exactly PD matrices checked')

if __name__=='__main__': check()
