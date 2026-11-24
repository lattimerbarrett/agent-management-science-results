"""Cyclic Atiyah matrix reduction, arbitrary precision (mpmath)."""
import mpmath as mp

def mul(p,q):
    ans=[mp.mpc(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q): ans[i+j]+=x*y
    return ans

def prod(fs):
    p=[mp.mpf(1)]
    for f in fs:p=mul(p,f)
    return p

def ratio(d,r): return r/(d+mp.sqrt(d*d+r*r))

def data(m,lower,upper,h0=0,h1=1,r=1,R=2):
    lower=list(map(mp.mpf,lower));upper=list(map(mp.mpf,upper))
    h0,h1,r,R=map(mp.mpf,(h0,h1,r,R))
    a,b=len(lower),len(upper)
    xs=[ratio(h0-l,r) for l in lower]
    ys=[ratio(h1-l,R) for l in lower]
    us=[ratio(u-h0,r) for u in upper]
    vs=[ratio(u-h1,R) for u in upper]
    z=mp.exp(2j*mp.pi/m)
    C=prod([[1,1j*mp.exp(-1j*mp.pi*k/m)] for k in range(1,m)])
    HA=[];HB=[]
    for k in range(m):
        w=R*z**k-r
        d=h1-h0+mp.sqrt((h1-h0)**2+abs(w)**2)
        HA.append([1,-mp.conj(w)/d])
        HB.append([(R-r*z**k)/d,1])
    PA=prod([[x,1] for x in xs]+[[1,u] for u in us]+[C,prod(HA)])
    PB=prod([[y,1] for y in ys]+[[1,v] for v in vs]+[C,prod(HB)])
    blocks=[]
    for e in range(m):
        triples=[]
        for i in range(e,a+b,m):
            if i<a:
                x,y=xs[i]**m,ys[i]**m
                triples.append((1,-x-y,x*y))
            else:
                u,v=us[i-a]**m,vs[i-a]**m
                triples.append((u*v,-u-v,1))
        A=PA[e::m];B=PB[e::m]
        block=mp.matrix(len(A))
        for k,(d0,d1,d2) in enumerate(triples):
            for j,c in enumerate((d0,d1,d2)):block[k,k+j]=c
        for j,c in enumerate(A):block[len(A)-2,j]=c
        for j,c in enumerate(B):block[len(A)-1,j]=c
        blocks.append((block,triples,A,B))
    return blocks

def reduced(triples,A,B):
    """Return 2x2 annihilator pairing. Vanishes iff full block determinant."""
    W=[]
    for init in [(1,0),(0,1)]:
        w=list(map(mp.mpf,init))
        for k,(d0,d1,d2) in enumerate(triples):
            w.append(-(d0*w[k]+d1*w[k+1])/d2)
        W.append(w)
    return mp.matrix([[sum(c*w for c,w in zip(row,ww)) for ww in W] for row in (A,B)])

def coordinates(m,lower,upper,h0=0,h1=1,r=1,R=2):
    z=mp.exp(2j*mp.pi/m)
    return [(mp.mpf(t),mp.mpc(0)) for t in lower]+[(mp.mpf(h0),r*z**k) for k in range(m)]+[(mp.mpf(h1),R*z**k) for k in range(m)]+[(mp.mpf(t),mp.mpc(0)) for t in upper]

def full_matrix(points):
    n=len(points);polys=[[mp.mpf(1)] for _ in points]
    for i,(li,wi) in enumerate(points):
        for j in range(i+1,n):
            lj,wj=points[j];d=lj-li+mp.sqrt((lj-li)**2+abs(wj-wi)**2)
            polys[i]=mul(polys[i],[1,-mp.conj(wj-wi)/d])
            polys[j]=mul(polys[j],[(wj-wi)/d,1])
    return mp.matrix(polys)
