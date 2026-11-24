import numpy as np
from scipy.special import gammaln, comb

def block(n,l,K=10000):
    js=[j for j in range((n-1)//2+1) if 2<=l+2*j<n/2 and not(l==0 and j==1)]
    if not js:return None
    k=np.arange(K,dtype=float); alpha=l+(n-3)/2
    loghn=(2*alpha+1)*np.log(2)-np.log(2*k+2*alpha+1)+2*gammaln(k+alpha+1)-gammaln(k+1)-gammaln(k+2*alpha+1)
    def moment(beta):
        c=(2*alpha+beta+1)*np.log(2)+gammaln(alpha+beta+1)
        if beta<0:
            return np.exp(c+gammaln(alpha+k+1)+gammaln(k-beta)-gammaln(-beta)-gammaln(k+1)-gammaln(2*alpha+beta+k+2)-loghn/2)
        out=np.zeros(K)
        for kk in range(beta+1):
            # (-1)^k*(-beta)_k: sign cancellation; code drops common (-1)^k otherwise.
            out[kk]=(-1)**kk*np.exp(c+gammaln(alpha+kk+1)+gammaln(beta+1)-gammaln(beta-kk+1)-gammaln(kk+1)-gammaln(2*alpha+beta+kk+2)-loghn[kk]/2)
        return out
    C=[]
    for j in js:
        C.append(sum(comb(j,h)*2**(j-h)*(-1)**h*moment(1-l-j+h) for h in range(j+1)))
    C=np.array(C)
    L=k+l
    eig=np.zeros(K); valid=L>=2; z=L[valid]
    mu=2*np.exp(gammaln(z/2)+gammaln((z+n+1)/2)-gammaln((z-1)/2)-gammaln((z+n)/2))
    eig[valid]=((z-1)*(z+n-1))**2/mu
    A=(C*eig)@C.T; ds=l+2*np.array(js)
    B=A*(ds[:,None]+ds[None,:]-2)
    B/=np.sqrt(np.outer(np.diag(B),np.diag(B)))
    return js,np.linalg.eigvalsh(B),B
if __name__=='__main__':
    for n in range(5,36):
        worst=1.
        for l in range(n//2):
            r=block(n,l)
            if r is not None:
                js,vals,B=r
                worst=min(worst,vals.min())
                if vals.min()<-1e-7:
                    print('NEGATIVE',n,l,js,vals);print(B);raise SystemExit
        print(n,worst)
