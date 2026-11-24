import numpy as np
from scipy.special import roots_jacobi, eval_gegenbauer, gammaln

def mat(n,l,K):
    alpha=l+(n-2)/2;beta=l+(n-3)/2
    z,w=roots_jacobi(900,beta,beta)
    fs=np.array([(1+z)**i/(1-z)**(l-1+i) for i in range(K+1)])
    Q=np.zeros((K+1,K+1))
    for k in range(max(0,2-l),240):
        L=k+l
        pol=eval_gegenbauer(k,alpha,z)
        norm=np.dot(w,pol*pol)
        co=(fs@(w*pol))/np.sqrt(norm)
        N=np.exp(gammaln((L-1)/2)+gammaln((L+n)/2)-np.log(2)-gammaln(L/2)-gammaln((L+n+1)/2))
        q=((L-1)*(L+n-1))**2*N
        Q+=q*np.outer(co,co)
    return Q*2.**(2-2*l)
for n in range(17,31):
    l=2;d=n-1;K=min(4,(n-5)//4)
    Q=mat(n,l,K);Qlow=mat(n,l-1,K);Qup=mat(n,l+1,K-1)
    i=np.arange(K+1); dd=l-1+2*i
    D=(dd[:,None]+dd[None,:])*Q;S=(dd[:,None]+dd[None,:])**2*Q
    b=1+2*i/(2*l+d-2)
    G=l*(2*l+d-2)*b[:,None]*b[None,:]*Qlow
    G[1:,1:]+=(l+d-2)/(2*l+d-2)*4*i[1:,None]*i[None,1:]*Qup
    C=np.zeros_like(Q)
    C[:,1:]=Q[:,:-1]*(2*i[1:]*(2*l+d+2*i[1:]-2))[None,:]
    E=2*G+C+C.T
    scale=np.sqrt(np.diag(Q));Dn=D/scale[:,None]/scale[None,:]
    ev,vec=np.linalg.eigh(Dn)
    if ev[0]>=0: print(n,'positive scale derivative');continue
    a=vec[:,0]/scale
    aa=D[0,0];bb=2*np.dot(D[0,1:],a[1:]);cc=a[1:]@D[1:,1:]@a[1:]
    vals=[]
    for root in np.roots([aa,bb,cc]):
        a[0]=root
        vals.append((float(a@S@a/(a@Q@a)),float(a@E@a/(a@Q@a))))
    print(n,'(scale Hessian, translation trace):',vals)
