import numpy as np

def hp(A,r):
    lam,U=np.linalg.eigh(A)
    return (U*lam**r)@U.conj().T

def verify(seed=9347):
    rng=np.random.default_rng(seed)
    err_pair=err_vector=0.
    for p in [1.2,1.5,1.9,2.,2.5,3.,5.,10.]:
        for _ in range(50):
            mats=[]
            for k in range(2):
                A=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
                A+=2*np.eye(2)
                mats.append(A)
            M,N=mats
            # W=(M* M)^(p/2); W^(1/p)=(M* M)^(1/2).
            W=hp(M.conj().T@M,p/2)
            V=hp(N.conj().T@N,p/2)
            lhs=np.linalg.norm(hp(W,1/p)@hp(V,-1/p),2)
            rhs=np.linalg.norm(M@np.linalg.inv(N),2)
            err_pair=max(err_pair,abs(lhs-rhs)/rhs)
            z=rng.normal(size=2)+1j*rng.normal(size=2)
            lhs=np.linalg.norm(hp(W,1/p)@z)
            rhs=np.linalg.norm(M@z)
            err_vector=max(err_vector,abs(lhs-rhs)/rhs)
    # Finite matrix operators verify triangular conjugation exactly numerically.
    n=7
    a=np.exp(rng.normal(size=n)); d=np.exp(rng.normal(size=n)); b=rng.normal(size=n)
    A=np.diag(a); D=np.diag(d); B=np.diag(b)
    I=np.eye(n); O=np.zeros((n,n))
    M=np.block([[A,A@B],[O,D]])
    H=rng.normal(size=(n,n))
    HH=np.block([[H,O],[O,H]])
    expected=np.block([[A@H@np.linalg.inv(A), A@(B@H-H@B)@np.linalg.inv(D)], [O,D@H@np.linalg.inv(D)]])
    err_tri=np.linalg.norm(M@HH@np.linalg.inv(M)-expected)
    assert err_pair<2e-4,err_pair
    assert err_vector<2e-4,err_vector
    assert err_tri<1e-10,err_tri
    return err_pair,err_vector,err_tri

if __name__=='__main__':
    print('max relative pair / vector errors and absolute triangular error:',verify())
