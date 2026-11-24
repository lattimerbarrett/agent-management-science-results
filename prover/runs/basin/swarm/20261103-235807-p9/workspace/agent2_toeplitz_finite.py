import numpy as np

def finite_block_check(p,Q):
    q=p/(p-1);ea=1/Q;ec=Q**(-1/(p-1));r=Q**(1/p)
    assert max(ea,ec)<=.5
    R=int(np.ceil(max(1/ea,1/ec)));N=6*R+2
    a=(1-ea)**(1/p);b=(1-ec)**(1/q)
    F=np.zeros(N);F[R:5*R+1]=1
    # U_k=sum_{m>k} b^(m-k)F_m, V_n=sum_{k<n}a^(n-k)U_k.
    U=np.zeros(N)
    for k in range(N-2,-1,-1):U[k]=b*(F[k+1]+U[k+1])
    V=np.zeros(N)
    for n in range(1,N):V[n]=a*(U[n-1]+V[n-1])
    Kf=r/(2*np.pi)*ea**(1/p)*ec**(1/q)*V
    lower_row=r/(2*np.pi)*ea**(1/p)*ec**(1/q)*sum(a**j for j in range(1,R+1))*sum(b**j for j in range(1,R+1))
    assert np.min(Kf[2*R:4*R+1])>=lower_row*(1-1e-11)
    ratio=np.linalg.norm(Kf,ord=p)/np.linalg.norm(F,ord=p)
    target=Q**(1+1/(p*(p-1)))
    return R,ratio,ratio/target

if __name__=='__main__':
    for p in (1.2,1.5,2.,3.,5.):
        for base in (4.,8.):
            Q=base**max(1,p-1)
            R,ratio,relative=finite_block_check(p,Q)
            print('p,Q,R,actual finite norm lower,target-normalized=',p,Q,R,ratio,relative)
