import numpy as np

def matrix(Q):
    Q=np.asarray(Q,float)
    Q=Q[np.argsort(Q[:,0],kind='stable')]
    n=len(Q)
    P=[np.array([1.+0j]) for i in range(n)]
    for i in range(n):
      for j in range(i+1,n):
        d=Q[j]-Q[i]
        w=d[1]+1j*d[2]
        D=d[0]+np.linalg.norm(d)
        P[i]=np.convolve(P[i],[1,-w.conjugate()/D])
        P[j]=np.convolve(P[j],[w/D,1])
    return np.array(P)

def normdet(Q):
    Q=np.asarray(Q,float)
    Q=Q[np.argsort(Q[:,0],kind='stable')]
    M=matrix(Q)
    scale=1.
    for i in range(len(Q)):
      for j in range(i+1,len(Q)):
        d=Q[j]-Q[i]
        scale*=2*np.linalg.norm(d)/(d[0]+np.linalg.norm(d))
    return np.linalg.det(M)/scale

Q=np.array([[-3,0,0],[-2,1,0],[-2,-.5,.8],[-2,-.5,-.8],[1,2,0],[1,-1,1.7],[1,-1,-1.7],[4,0,0.]])
print('original',np.linalg.det(matrix(Q)),normdet(Q))
Qp=Q[[0,2,1,3,4,5,6,7]]
print('permuted',np.linalg.det(matrix(Qp)),normdet(Qp))
rng=np.random.default_rng(3)
for i in range(5):
    O,R=np.linalg.qr(rng.normal(size=(3,3)))
    O[:,0]*=np.linalg.det(O)
    Qr=Q@O
    print('rotated',np.linalg.det(matrix(Qr)),normdet(Qr))
