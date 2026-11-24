import numpy as np
from math import comb

def matrix(m, lo, hi, hm, hp, r, R):
    z=np.exp(2j*np.pi*np.arange(m)/m)
    points=[(x,0j) for x in lo]+[(hm,r*w) for w in z]+[(hp,R*w) for w in z]+[(x,0j) for x in hi]
    n=len(points)
    ps=[np.ones(1,complex) for i in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            h=points[j][0]-points[i][0]; w=points[j][1]-points[i][1]
            D=h+np.sqrt(h*h+abs(w)**2)
            q=w/D
            ps[i]=np.polynomial.polynomial.polymul(ps[i],[1,-q.conjugate()])
            ps[j]=np.polynomial.polynomial.polymul(ps[j],[q,1])
    M=np.zeros((n,n),complex)
    for i,p in enumerate(ps): M[i,:len(p)]=p
    return M

def blocks(m,lo,hi,hm,hp,r,R):
    M=matrix(m,lo,hi,hm,hp,r,R)
    a,b=len(lo),len(hi); n=len(M)
    # P_(orbit,k)(T) = scalar * P_(orbit,0)(zeta^(-k)T).
    # scalar is determined from the number of earlier axis points and
    # earlier same-height points, so use coefficients of orbit base row.
    out=[]
    for c in range(m):
        cols=np.arange(c,n,m)
        rows=[i for i in range(a) if i%m==c]
        rows += [a,a+m]
        rows += [a+2*m+j for j in range(b) if (a+j)%m==c]
        out.append(M[np.ix_(rows,cols)])
    return out

if __name__=='__main__':
    m=5; lo=[-3.,-1.]; hi=[2.,4.,7.]; hm=0.; hp=1.; r=.8; R=1.7
    M=matrix(m,lo,hi,hm,hp,r,R)
    a=len(lo); b=len(hi); n=len(M)
    zeta=np.exp(2j*np.pi/m)
    F=M.copy()
    for start in [a,a+m]:
        scales=M[start:start+m,0]/M[start,0]
        for c in range(m):
            F[start+c]=sum(zeta**(k*c)*M[start+k]/scales[k] for k in range(m))/m
    off=0.
    for i in range(n):
        if i<a: residue=i%m
        elif i<a+2*m: residue=(i-a)%m
        else: residue=(i-2*m)%m
        off=max(off,np.max(np.abs(F[i,np.arange(n)%m!=residue])))
    print('Fourier off-block error:',off)
    for c,B in enumerate(blocks(m,lo,hi,hm,hp,r,R)):
        print('character',c,'block shape',B.shape,'rank',np.linalg.matrix_rank(B))
    nu=-5.
    Mnew=matrix(m,[nu]+lo,hi,hm,hp,r,R)
    errs=[]
    for start,h,radius in [(a,hm,r),(a+m,hp,R)]:
        q=radius/(h-nu+np.hypot(h-nu,radius))
        for k in range(m):
            expected=np.polynomial.polynomial.polymul(M[start+k],[q*zeta**k,1])
            errs.append(np.max(np.abs(expected-Mnew[start+1+k])))
    print('Added lower axial point multiplication error:',max(errs))
    rng=np.random.default_rng(538)
    for m in range(1,9):
        best=1; worst=0; negative=0; imag=0
        for rep in range(150):
            a=int(rng.integers(1,9)); b=int(rng.integers(1,9))
            lo=-np.sort(np.exp(rng.uniform(-3,3,a)))[::-1]
            hi=1+np.sort(np.exp(rng.uniform(-3,3,b)))
            r=np.exp(rng.uniform(-2,2)); R=r+np.exp(rng.uniform(-2,2))
            M=matrix(m,lo,hi,0,1,r,R)
            # Row scalings and column binomial scalings improve conditioning.
            n=len(M)
            W=M/np.sqrt(np.array([comb(n-1,k) for k in range(n)],float))
            W/=np.linalg.norm(W,axis=1)[:,None]
            sig=np.linalg.svd(W,compute_uv=False)
            best=min(best,sig[-1]/sig[0])
            phase,logdet=np.linalg.slogdet(M)
            negative+=phase.real<0
            imag=max(imag,abs(phase.imag))
        print(m,'smallest normalized sv ratio',best,'negative phase count',negative,'phase imaginary max',imag)
