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
        if not Is:
            logs.append(np.full_like(j,-np.inf))
        else:
            mx=Is[0][1]
            val=sum(c*np.exp(v-mx) for c,v in Is)
            logs.append(mx+np.log(val))
    Q=np.empty((K,K))
    for a in range(K):
        for b in range(K):Q[a,b]=np.exp(logsumexp(logq+logs[a]+logs[b]-logh))
    return Q

if __name__=='__main__':
    # Full normalized-energy second variation on the unit hemisphere:
    # Y''/2 = V^(-beta) [a int(|grad v|^2-n v^2)
    # + an/V (int v)^2 + 4 int H'v + 4m/V A int v
    # + m(n-2)/(nV) A^2], H'=-(Delta+m)w, A=int w.
    # Round cap check: w=1, v=-(n-2)/2*z_normal (volume gauge).
    # int z_normal = area(equator)/n; int(|grad z|^2-n z^2)=0.
    import sympy as sp
    nn,A,V=sp.symbols('n A V', positive=True)
    aa=4*(nn-1)/(nn-2)
    Iv=-(nn-2)*A/(2*nn)
    cap=aa*nn/V*Iv**2+4*(nn-1)/V*A*Iv+(nn-1)*(nn-2)/(nn*V)*A**2
    print('Full cap second variation:',sp.simplify(cap))
    for n in range(5,41):
        mineig=1.; where=None
        for l in range(0,n//2+1):
            k0=max(0,2-l)
            K=(n-1-2*l)//4-k0+1
            if K<1:continue
            Q=calc(n,l=l,K=K,k0=k0,J=10000)
            d=l+2*np.arange(k0,k0+K)
            Q=Q/np.sqrt(np.outer(np.diag(Q),np.diag(Q)))
            P=(d[:,None]+d[None,:]-2)*Q/np.sqrt(np.outer(2*d-2,2*d-2))
            eig=np.linalg.eigvalsh(P)[0]
            if eig<mineig:mineig=eig;where=(l,K)
        print(n,mineig,where)

