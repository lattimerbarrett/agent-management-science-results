"""Numerical verification of the exact cyclic-block reduction.
Ascending coefficient convention throughout. Not a proof of nonvanishing.
"""
import numpy as np

def configuration(m, lower, hm, r, hp, R, upper):
    return ([(h,0j) for h in lower]
        + [(hm,r*np.exp(2j*np.pi*k/m)) for k in range(m)]
        + [(hp,R*np.exp(2j*np.pi*k/m)) for k in range(m)]
        + [(h,0j) for h in upper])

def matrix(points):
    n=len(points); rows=[]
    for i,(hi,wi) in enumerate(points):
        p=np.array([1.+0j])
        for j,(hj,wj) in enumerate(points):
            if i==j: continue
            if i<j:
                dh=hj-hi; dw=wj-wi
                D=dh+np.hypot(dh,abs(dw))
                f=[1,-dw.conjugate()/D]
            else:
                dh=hi-hj; dw=wi-wj
                D=dh+np.hypot(dh,abs(dw))
                f=[dw/D,1]
            p=np.convolve(p,f)
        rows.append(p)
    return np.array(rows)

def reduce_blocks(M,a,b,m):
    """Returns direct blocks and full Fourier-transformed matrix for checking."""
    n=a+b+2*m; d=n-1; z=np.exp(2j*np.pi/m)
    A=M[a:a+m].copy(); B=M[a+m:a+2*m].copy()
    A/=A[:,-1,None]; B/=B[:,-1,None]
    # Remove the monic degree phase, then extract residue classes.
    FA=[]; FB=[]
    for q in range(m):
        weights=np.array([z**(k*(q-d))/m for k in range(m)])
        FA.append(weights@A); FB.append(weights@B)
    rows=[]; blocks=[]
    for q in range(m):
        cols=list(range(q,n,m))
        ar=[]
        for s in range(q,a+b,m):
            original_index=s if s<a else s+2*m
            ar.append(M[original_index])
        blockrows=ar+[FA[q],FB[q]]
        rows.extend(blockrows)
        blocks.append(np.array(blockrows)[:,cols])
    permcols=[e for q in range(m) for e in range(q,n,m)]
    return blocks,np.array(rows)[:,permcols]

def self_test(seed=1827,trials=40):
    rng=np.random.default_rng(seed); worst=0.
    for _ in range(trials):
        m=int(rng.integers(1,8)); a=int(rng.integers(1,8)); b=int(rng.integers(1,8))
        low=-np.cumsum(rng.uniform(.4,1,a))[::-1]
        up=2+np.cumsum(rng.uniform(.4,1,b))
        pts=configuration(m,low,0.,.7,1.,1.2,up)
        M=matrix(pts); blocks,X=reduce_blocks(M,a,b,m)
        target=np.zeros_like(X); off=0
        for block in blocks:
            k=len(block); target[off:off+k,off:off+k]=block; off+=k
        error=np.max(np.abs(X-target))/max(1,np.max(np.abs(X)))
        worst=max(worst,error)
        assert error<2e-11,(m,a,b,error)
        # Independent coefficient check for every axial row.
        for j,h in enumerate(low):
            x=(.7/(-h+np.hypot(-h,.7)))**m
            y=(1.2/(1-h+np.hypot(1-h,1.2)))**m
            expected=np.zeros(len(pts),complex)
            expected[j]=1; expected[j+m]=-x-y; expected[j+2*m]=x*y
            assert np.allclose(M[j],expected,atol=2e-10)
        for j,h in enumerate(up):
            x=(.7/(h+np.hypot(h,.7)))**m
            y=(1.2/(h-1+np.hypot(h-1,1.2)))**m
            expected=np.zeros(len(pts),complex); s=a+j
            expected[s]=x*y; expected[s+m]=-x-y; expected[s+2*m]=1
            assert np.allclose(M[a+2*m+j],expected,atol=2e-10)
    return {"trials":trials,"worst_relative_offblock_error":worst}

if __name__=="__main__": print(self_test())


def exact_fourier_test(max_m=30):
    """Exact polynomial-arithmetic checks; no floating point or conjectured signs."""
    import sympy as sp
    X=sp.Symbol("X"); count=0
    for m in range(1,max_m+1):
        phi=sp.Poly(sp.cyclotomic_poly(m,X),X,domain=sp.QQ)
        for shift in range(m):
            f=sp.Poly(sum(X**((k*shift)%m) for k in range(m)),X,domain=sp.QQ)
            actual=f.rem(phi)
            expected=sp.Poly(m if shift==0 else 0,X,domain=sp.QQ)
            assert actual==expected
            count+=1
        # Product of orbit factors 1−zeta^k*T equals 1−T^m;
        # coefficients computed in Q[X]/Phi_m, exactly.
        coeff=[sp.Poly(1,X,domain=sp.QQ)]
        for k in range(m):
            z=sp.Poly(X**k,X,domain=sp.QQ).rem(phi)
            new=[sp.Poly(0,X,domain=sp.QQ) for _ in range(len(coeff)+1)]
            for j,c in enumerate(coeff):
                new[j]+=c
                new[j+1]-=(c*z).rem(phi)
            coeff=[v.rem(phi) for v in new]
        assert all(c==sp.Poly(1 if j==0 else -1 if j==m else 0,X,domain=sp.QQ)
                   for j,c in enumerate(coeff))
        count+=1
    return {"max_m":max_m,"exact_identities_checked":count}


def exact_spectral_test(max_m=30):
    """Check Dickson recurrence quotient-curve parametrization symbolically."""
    import sympy as sp
    z,r,t=sp.symbols("z r t")
    P0=sp.Integer(2);P1=z;checks=0
    for m in range(1,max_m+1):
        P=P1
        expected=r**m*(t**(-m)+(-1)**m*t**m)
        actual=sp.expand(P.subs(z,r*(1/t-t)))
        assert sp.expand(actual-expected)==0
        checks+=1
        P0,P1=P1,sp.expand(z*P1+r*r*P0)
    return {"max_m":max_m,"exact_spectral_parametrizations":checks}
