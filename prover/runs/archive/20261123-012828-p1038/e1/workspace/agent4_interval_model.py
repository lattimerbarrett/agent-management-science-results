"""High precision experiments for interval-constrained algebraic model.
This is NOT proof of the universal claim, nor a proof of the problem.
"""
import mpmath as mp
import numpy as np

def conv(a,b):
    c=[mp.mpc(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c

def blocks(m,r,d,x,y,precision=100):
    mp.mp.dps=precision
    r=mp.mpf(float(r));d=mp.mpf(float(d))
    x=list(map(lambda t:mp.mpf(float(t)),x));y=list(map(lambda t:mp.mpf(float(t)),y))
    H=[mp.mpf(1)];A=H[:];B=H[:]
    for j in range(1,m):H=conv(H,[1,mp.j*mp.exp(-mp.j*mp.pi*j/m)])
    for j in range(m):
        z=mp.exp(2*mp.j*mp.pi*j/m)
        D=d+mp.sqrt(d*d+abs(z-r)**2)
        c=(z.conjugate()-r)/D;b=(1-r*z)/D
        A=conv(A,[1,-c]);B=conv(B,[b,1])
    A=conv(H,A);B=conv(H,B)
    for u,v in zip(x,y):A=conv(A,[u,1]);B=conv(B,[v,1])
    k=len(x);n=k+2*m;out=[]
    for q in range(m):
        cols=list(range(q,n,m));ix=list(range(q,k,m));Q=mp.matrix(len(cols))
        for j,i in enumerate(ix):
            Q[j,j]=1;Q[j,j+1]=-x[i]**m-y[i]**m;Q[j,j+2]=(x[i]*y[i])**m
        for j,t in enumerate(cols):
            Q[len(cols)-2,j]=A[t].real
            Q[len(cols)-1,j]=B[t].real
        out.append(mp.det(Q))
    return out

def search(trials=1000,seed=552):
    rng=np.random.default_rng(seed);checked=0
    for tt in range(trials):
        m=int(rng.integers(1,16));k=int(rng.integers(0,35))
        r=np.exp(rng.uniform(-6,-.0001));d=np.exp(rng.uniform(-7,6))
        c=(1-r)/(d+np.hypot(d,1-r))
        x=np.sort(np.exp(rng.uniform(-7,7,k)));s=int(np.sum(x<c));l=int(np.sum(x<1))
        y=x+rng.random(k)*(c-x)
        y[l:]=1+rng.random(k-l)*(x[l:]-1)
        y=np.r_[np.sort(y[:s]),np.sort(y[s:l]),np.sort(y[l:])]
        vals=blocks(m,r,d,x,y)
        for q,v in enumerate(vals):
            if v<=0:
                return dict(failed=True,trial=tt,m=m,k=k,q=q,r=r,d=d,x=x.tolist(),y=y.tolist(),value=str(v))
        checked+=m
    return dict(failed=False,seed=seed,trials=trials,positive_blocks=checked,precision=100)

if __name__=='__main__':print(search())
