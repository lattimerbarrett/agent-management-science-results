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

for n in []:
    worst=(float('inf'),None)
    for l in range(0,n//2+1):
        k0=2 if l==0 else (1 if l==1 else 0)
        K=((n-1)//2-l)//2-k0+1
        if K<=0:continue
        Q=calc(n,l=l,K=K,J=30000,k0=k0)
        d=l+2*np.arange(k0,k0+K)
        Q=Q/np.sqrt(np.outer(np.diag(Q),np.diag(Q)))
        D=Q*(d[:,None]+d[None,:]-2)
        eig=np.linalg.eigvalsh(D)[0]
        if eig<worst[0]:worst=(eig,(l,K))
    print(n,worst)

from pathlib import Path
for filename in ['agent3_block_notes.txt','agent3_local_pohozaev_bridge.md','agent4_green_mass_reduction.md','agent1_high_dim_analytic_bridge.md']:
    p=Path('experiments/e3')/filename
    print('\nFILE',filename,'\n',p.read_text())
