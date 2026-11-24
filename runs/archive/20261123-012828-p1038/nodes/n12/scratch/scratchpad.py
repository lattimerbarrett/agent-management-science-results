import numpy as np, json, time
from pathlib import Path

def canonical(m, low, up, r,d,R):
    # Real coefficients built using conjugate-paired factors.
    def prod(fs):
        p=np.array([1.])
        for f in fs: p=np.convolve(p,f)
        return p
    H=prod([[1.,2*np.sin(np.pi*k/m),1.] for k in range(1,(m+1)//2)]) if m>1 else np.array([1.])
    # H pairs are 1+2sin(pi k/m)T+T², plus middle 1+T.
    if m%2==0: H=np.convolve(H,[1,1])
    ca=[]; cb=[]
    for k in range(m//2+1):
        th=2*np.pi*k/m
        w=R*np.exp(1j*th)-r
        D=d+np.hypot(d,abs(w))
        c=np.conj(w)/D; b=np.exp(1j*th)*c
        if k==0 or (m%2==0 and k==m//2):
            ca.append([1.,-c.real]); cb.append([b.real,1.])
        else:
            ca.append([1.,-2*c.real,abs(c)**2]); cb.append([abs(b)**2,2*b.real,1.])
    A=np.convolve(H,prod(ca)); B=np.convolve(H,prod(cb))
    heights=list(low)+list(up)
    xs=[];ys=[]
    for h in heights:
        x=np.exp(np.arcsinh(h/r)); y=np.exp(np.arcsinh((h-d)/R))
        xs.append(x);ys.append(y)
        A=np.convolve(A,[x,1]); B=np.convolve(B,[y,1])
        A/=np.max(np.abs(A)); B/=np.max(np.abs(B))
    blocks=[]; signs=[]; logs=[]
    c=len(heights); n=c+2*m
    for q in range(m):
        ids=list(range(q,c,m)); size=len(ids)+2
        K=np.zeros((size,size))
        for j,i in enumerate(ids):
            u=xs[i]**m;v=ys[i]**m
            vrow=np.array([1,-u-v,u*v]); vrow/=np.max(np.abs(vrow))
            K[j,j:j+3]=vrow
        K[-2,:]=A[q:n:m];K[-1,:]=B[q:n:m]
        K[-2:]/=np.max(np.abs(K[-2:]),axis=1)[:,None]
        sg,lg=np.linalg.slogdet(K)
        signs.append(sg);logs.append(lg);blocks.append(K)
    return signs,logs,blocks

rng=np.random.default_rng(137)
start=time.time(); best=1e99; bad=[]
for it in range(10000):
    m=int(rng.integers(1,25));a=int(rng.integers(1,25)); b=int(rng.integers(1,25))
    r=1.; R=1+10**rng.uniform(-2,2); d=10**rng.uniform(-2,2)
    low=-np.sort(10**rng.uniform(-2,2,a))[::-1]
    up=d+np.sort(10**rng.uniform(-2,2,b))
    signs,logs,blocks=canonical(m,low,up,r,d,R)
    if min(signs)<=0:
        item=dict(it=it,m=m,a=a,b=b,r=r,R=R,d=d,low=low.tolist(),up=up.tolist(),signs=signs,logs=logs)
        bad.append(item)
        if len(bad)<=4: print('candidate',json.dumps(item),flush=True)
        if len(bad)>=20: break
print('iterations',it+1,'bad',len(bad),'seconds',time.time()-start)
Path('candidates.json').write_text(json.dumps(bad))
