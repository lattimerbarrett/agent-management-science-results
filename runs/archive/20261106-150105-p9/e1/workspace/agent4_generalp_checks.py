"""Finite-step Hilbert compression. Numerical values are certified test-vector
lower bounds modulo floating-point arithmetic, NOT claims of global p-norm maxima.
"""
import numpy as np
from scipy.linalg import svdvals

def spower(A,t):
    d,U=np.linalg.eigh(A)
    if min(d)<=0: raise ValueError('matrix is not positive definite')
    return (U*d**t)@U.conj().T

def logprimitive(t):
    return 0. if t==0 else t*np.log(abs(t))-t

def integrated_kernel(edges):
    n=len(edges)-1; C=np.zeros((n,n))
    for i in range(n):
        a,b=edges[i:i+2]
        for j in range(i):
            c,d=edges[j:j+2]
            z=(logprimitive(b-c)-logprimitive(a-c)-logprimitive(b-d)+logprimitive(a-d))/np.pi
            C[i,j]=z; C[j,i]=-z
    return C

def compression(factors,lengths,p):
    factors=np.asarray(factors); lengths=np.asarray(lengths)
    C=integrated_kernel(np.r_[0,np.cumsum(lengths)])
    inverse=np.linalg.inv(factors); n=len(lengths)
    T=np.empty((2*n,2*n),dtype=np.result_type(factors,float))
    for i in range(n):
        for j in range(n):
            T[2*i:2*i+2,2*j:2*j+2]=C[i,j]*lengths[i]**(1/p-1)*lengths[j]**(-1/p)*(factors[i]@inverse[j])
    return T

def blocknorm(x,p):
    return np.sum(np.linalg.norm(np.reshape(x,(-1,2)),axis=1)**p)**(1/p)

def dualitymap(x,p):
    x=np.reshape(x,(-1,2)); norms=np.linalg.norm(x,axis=1)
    z=np.zeros_like(x); nz=norms>0
    z[nz]=x[nz]*(norms[nz]**(p-2))[:,None]
    return z.reshape(-1)

def testvector_lower(T,p,starts=12,iterations=200,seed=71):
    rng=np.random.default_rng(seed); best=0.; bestx=None
    q=p/(p-1)
    for k in range(starts):
        x=rng.normal(size=T.shape[1]); x=x/blocknorm(x,p)
        for it in range(iterations):
            y=T@x; u=T.conj().T@dualitymap(y,p)
            nx=dualitymap(u,q); n=blocknorm(nx,p)
            if not np.isfinite(n) or n==0: break
            nx/=n
            # Iteration is exploratory; only explicit evaluated vectors are returned.
            value=blocknorm(T@nx,p)
            if value>best: best=value; bestx=nx.copy()
            if blocknorm(nx-x,p)<1e-10: break
            x=nx
    return best,bestx

def interval_char(factors,lengths,p,left=0.,right=None):
    lengths=np.asarray(lengths); edges=np.r_[0,np.cumsum(lengths)]
    if right is None: right=edges[-1]
    masses=np.maximum(0,np.minimum(edges[1:],right)-np.maximum(edges[:-1],left))
    if sum(masses)<=0: raise ValueError('empty interval')
    masses/=sum(masses); n=len(masses); inv=np.linalg.inv(factors)
    K=np.array([[np.linalg.norm(factors[i]@inv[j],2) for j in range(n)] for i in range(n)])
    q=p/(p-1)
    return np.dot(masses,(K**q@masses)**(p-1))

def gauge_factors(detone_weights,p):
    ans=[]
    for V in detone_weights:
        lam=np.linalg.eigvalsh(V)[-1]
        ans.append(lam**(1/p-.5)*spower(V,.5))
    return np.array(ans)

if __name__=='__main__':
    rng=np.random.default_rng(781)
    n=7; lengths=np.exp(rng.normal(size=n)); lengths/=sum(lengths)
    factors=[]
    for j in range(n):
        theta=rng.uniform(-np.pi,np.pi)
        U=np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])
        factors.append((U*np.exp(rng.uniform(-2,2,2)))@U.T)
    factors=np.array(factors)
    T=compression(factors,lengths,2.)
    value,x=testvector_lower(T,2.)
    exact=svdvals(T)[0]
    assert abs(value/exact-1)<1e-7
    # Independent block Euclidean expression equals direct weighted average H.
    edges=np.r_[0,np.cumsum(lengths)]; C=integrated_kernel(edges)
    f=np.array([np.linalg.solve(factors[j],x[2*j:2*j+2]/np.sqrt(lengths[j])) for j in range(n)])
    h=(C@f)/lengths[:,None]
    direct=np.sqrt(sum(lengths[j]*np.linalg.norm(factors[j]@h[j])**2 for j in range(n)))
    assert abs(direct-value)<1e-10
    for p in [1.25,1.5,2.,3.,5.]:
        T=compression(factors,lengths,p)
        value,x=testvector_lower(T,p)
        assert abs(blocknorm(x,p)-1)<1e-10
        assert abs(value-blocknorm(T@x,p))<1e-10
        ch=interval_char(factors,lengths,p)
        assert ch>=1-1e-10
        print('p=',p,'whole-interval char=',ch,'compressed test lower=',value)
    # Gauge identities checked spectrally for all noncommuting examples.
    for p in [1.25,1.5,2.,3.,5.]:
        for F in factors:
            d,U=np.linalg.eigh(F); V=(U*(d/d.prod()**.5))@U.T
            lam=np.linalg.eigvalsh(V)[-1]
            G=gauge_factors([V],p)[0]; W=spower(G,p); S=spower(W,-1/(p-1))
            assert np.allclose(np.linalg.eigvalsh(W),[lam**(1-p),lam])
            assert np.allclose(np.linalg.eigvalsh(S),[lam**(-1/(p-1)),lam])
    print('All compression, normalization, p=2 SVD and p-gauge tests passed.')
    from pathlib import Path
    Path('workspace/agent4_generalp_checks.py').write_text(Path(__file__).read_text())
