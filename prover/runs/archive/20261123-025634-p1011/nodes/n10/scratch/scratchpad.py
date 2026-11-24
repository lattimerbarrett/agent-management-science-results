import numpy as np
from scipy.special import gammaln, betaln, logsumexp

def calc(n,l=2,K=2,J=100000,k0=0):
    j=np.arange(max(0,2-l),J,dtype=float)
    beta=(n-3)/2+l
    logh=np.log(np.pi)-2*beta*np.log(2)+gammaln(j+2*beta+1)-gammaln(j+1)-np.log(j+beta+.5)-2*gammaln(beta+.5)
    L=j+l
    logq=2*np.log(L-1)+2*np.log(L+n-1)-np.log(2)+gammaln((L+n)/2)+gammaln((L-1)/2)-gammaln((L+n+1)/2)-gammaln(L/2)
    logs=[]
    for k in range(k0,k0+K):
        Is=[]
        for i in range(k+1):
            a=l+k-1-i
            if a<=0: continue
            logI=(2*beta-a+1)*np.log(2)+betaln(beta-a+1,beta+1)+gammaln(j+2*beta+1)-gammaln(2*beta+1)-gammaln(j+1)+gammaln(j+a)-gammaln(a)-gammaln(j+2*beta-a+2)+gammaln(2*beta-a+2)
            from math import comb
            Is.append(((-1)**i*comb(k,i)*2**(k-i),logI))
        mx=Is[0][1]
        val=sum(c*np.exp(v-mx) for c,v in Is)
        logs.append(mx+np.log(val))
    Q=np.empty((K,K))
    for a in range(K):
        for b in range(K):Q[a,b]=np.exp(logsumexp(logq+logs[a]+logs[b]-logh))
    return Q

for n in range(17,20):
    best=(1e100,None)
    for l in range(0,min(n//2+1,8)):
        k0=max(0,2-l)
        K=(n-1-2*l)//4+1-k0
        if K<=0:continue
        Q=calc(n,l=l,K=K,J=40000,k0=k0)
        d=np.arange(k0,k0+K)*2+l
        Q=Q/np.sqrt(np.diag(Q)[:,None]*np.diag(Q)[None,:])
        D=Q*(d[:,None]+d[None,:]-2)
        eig=np.linalg.eigvalsh(D)[0]
        print('sector',n,l,K,eig)
        if eig<best[0]:best=(eig,(l,K))
    print(n,best)

