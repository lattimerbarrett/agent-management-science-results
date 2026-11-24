import numpy as np
rng=np.random.default_rng(42)
a=.2
p=(-2*a+np.sqrt(3*a-2*a*a))/(1-2*a)
print('p',p,'nominal coefficient',3/(1+2*(1-p)**2))
for N in [300,900,1800]:
    part=np.arange(N)//(N//3)
    R=(rng.random((N,N))<p)&(part[:,None]!=part[None,:])
    R=np.triu(R,1); R=R|R.T
    B=~R; np.fill_diagonal(B,False)
    rr=R.astype(np.int32)@R.astype(np.int32)
    bb=B.astype(np.int32)@B.astype(np.int32)
    print('N',N,'red book',rr[R].max(),'blue book',bb[B].max(), 'pred red',p*p*N/3,'pred blue within',(1+2*(1-p)**2)*N/3)
    for same in [True,False]:
        mask=B&((part[:,None]==part[None,:])==same)
        print('blue', 'within' if same else 'between', 'max',bb[mask].max(), 'mean',bb[mask].mean())
    print('red mean',rr[R].mean(),'pred blue between',(2*(1-p)+(1-p)**2)*N/3)
q=1-p
print('all asymptotic edge types, normalized by N:')
print('red between',p*p/3)
print('blue within',(1+2*q*q)/3)
print('blue between',(2*q+q*q)/3)
print('difference within minus between',(1+2*q*q-2*q-q*q)/3,'= p^2/3',p*p/3)
