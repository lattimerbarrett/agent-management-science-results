import mpmath as mp

def mul(a,b):
    c=[mp.mpc(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return c

def blocks(m,lows,ups,h0,h1,r,R,dps=100):
    mp.mp.dps=dps
    lows=list(map(mp.mpf,lows)); ups=list(map(mp.mpf,ups)); h0,h1,r,R=map(mp.mpf,[h0,h1,r,R])
    def c(rad,z): return rad/(z+mp.sqrt(z*z+rad*rad))
    al=[c(r,h0-x) for x in lows]; be=[c(R,h1-x) for x in lows]
    de=[c(r,x-h0) for x in ups]; ep=[c(R,x-h1) for x in ups]
    A=[mp.mpc(1)]; B=A[:]
    for x,y in zip(al,be): A=mul(A,[x,1]); B=mul(B,[y,1])
    for x,y in zip(de,ep): A=mul(A,[1,x]); B=mul(B,[1,y])
    for k in range(1,m):
        fac=[1,mp.j*mp.exp(-mp.j*mp.pi*k/m)]
        A=mul(A,fac); B=mul(B,fac)
    H=h1-h0
    for k in range(m):
        zeta=mp.exp(2*mp.j*mp.pi*k/m)
        D=H+mp.sqrt(H*H+R*R+r*r-2*r*R*zeta.real)
        z=(R*zeta-r)/D; w=(R-r*zeta)/D
        A=mul(A,[1,-mp.conj(z)]); B=mul(B,[w,1])
    a=len(lows); b=len(ups)
    result=[]
    for rho in range(m):
        indices=list(range(rho,a+b,m)); d=len(indices)
        C=mp.matrix(d+2,d+2)
        for q,j in enumerate(indices):
            if j<a: u,v=al[j]**m,be[j]**m; row=[1,-u-v,u*v]
            else: u,v=de[j-a]**m,ep[j-a]**m; row=[u*v,-u-v,1]
            for t,val in enumerate(row): C[q,q+t]=val
        for j,x in enumerate(A[rho::m]): C[d,j]=x.real
        for j,x in enumerate(B[rho::m]): C[d+1,j]=x.real
        result.append(C)
    return result

def signs(*args,**kwargs):
    out=[]
    for C in blocks(*args,**kwargs):
        # Positive row normalization; does not change determinant sign.
        for i in range(C.rows):
            norm=max(abs(C[i,j]) for j in range(C.cols))
            for j in range(C.cols): C[i,j]/=norm
        d=mp.det(C)
        out.append((int(mp.sign(d)),mp.nstr(mp.log10(abs(d)),12)))
    return out
