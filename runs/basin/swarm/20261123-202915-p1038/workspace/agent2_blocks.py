import numpy as np
from numpy.polynomial.polynomial import polymul

def axis_params(m,lows,ups,h0,h1,r,R):
    lows=np.array(lows,dtype=float); ups=np.array(ups,dtype=float)
    def c(rad,z): return rad/(z+np.hypot(z,rad))
    return c(r,h0-lows),c(R,h1-lows),c(r,ups-h0),c(R,ups-h1)

def ring_polys(m,lows,ups,h0,h1,r,R):
    al,be,de,ep=axis_params(m,lows,ups,h0,h1,r,R)
    A=np.array([1.+0j]); B=A.copy()
    for x,y in zip(al,be): A=polymul(A,[x,1]); B=polymul(B,[y,1])
    for x,y in zip(de,ep): A=polymul(A,[1,x]); B=polymul(B,[1,y])
    for k in range(1,m):
        fac=[1,1j*np.exp(-1j*np.pi*k/m)]
        A=polymul(A,fac); B=polymul(B,fac)
    for k in range(m):
        zeta=np.exp(2j*np.pi*k/m)
        D=h1-h0+np.sqrt((h1-h0)**2+R**2+r**2-2*r*R*zeta.real)
        z=(R*zeta-r)/D; w=(R-r*zeta)/D
        A=polymul(A,[1,-z.conjugate()]); B=polymul(B,[w,1])
    assert max(np.max(abs(A.imag)),np.max(abs(B.imag)))<1e-5*max(np.max(abs(A)),np.max(abs(B)))
    return A.real,B.real

def blocks(m,lows,ups,h0,h1,r,R):
    a=len(lows); b=len(ups)
    al,be,de,ep=axis_params(m,lows,ups,h0,h1,r,R)
    A,B=ring_polys(m,lows,ups,h0,h1,r,R)
    result=[]
    for rho in range(m):
        indices=list(range(rho,a+b,m)); d=len(indices)
        C=np.zeros((d+2,d+2))
        for q,j in enumerate(indices):
            if j<a: u,v=al[j]**m,be[j]**m; C[q,q:q+3]=[1,-u-v,u*v]
            else: u,v=de[j-a]**m,ep[j-a]**m; C[q,q:q+3]=[u*v,-u-v,1]
        C[-2]=A[rho::m]; C[-1]=B[rho::m]
        result.append(C)
    return result

def direct(m,lows,ups,h0,h1,r,R):
    Q=[(z,0j) for z in lows]+[(h0,r*np.exp(2j*np.pi*k/m)) for k in range(m)]+[(h1,R*np.exp(2j*np.pi*k/m)) for k in range(m)]+[(z,0j) for z in ups]
    n=len(Q); P=[np.array([1.+0j]) for _ in Q]
    for i in range(n):
        for j in range(i+1,n):
            h=Q[j][0]-Q[i][0]; w=Q[j][1]-Q[i][1]; D=h+np.hypot(h,abs(w))
            P[i]=polymul(P[i],[1,-w.conjugate()/D]); P[j]=polymul(P[j],[w/D,1])
    return np.array([np.pad(p,(0,n-len(p))) for p in P])
