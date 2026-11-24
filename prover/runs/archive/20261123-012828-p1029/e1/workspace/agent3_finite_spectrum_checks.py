import numpy as np
from scipy.linalg import expm
rng=np.random.default_rng(301)
worst=0.0
for n in range(2,9):
    for _ in range(50):
        lam=np.linspace(0.1,0.9,n)
        A=np.diag(lam)
        X=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
        C=X.conj().T@X
        C/=np.linalg.norm(C,2)
        # Kato first-order conjugation: U*=exp(-tK), offdiag(C+[A,K])=0.
        K=np.zeros((n,n),complex)
        for i in range(n):
            for j in range(n):
                if i!=j: K[i,j]=-C[i,j]/(lam[i]-lam[j])
        assert np.linalg.norm(K+K.conj().T)<1e-12
        D=np.diag(np.diag(C))
        errors=[]
        for t in [1e-4,5e-5,2.5e-5]:
            U=expm(t*K)
            err=np.linalg.norm(U.conj().T@(A+t*C)@U-(A+t*D),2)
            errors.append(err)
        assert errors[1] <= .251*errors[0]+1e-14
        assert errors[2] <= .251*errors[1]+1e-14
        # Operator pinching inequality C <= n*diag(C), valid for PSD C.
        assert np.linalg.eigvalsh(n*D-C)[0]>-1e-12
        worst=max(worst,errors[0])
print('350 seeded finite-spectrum perturbation and PSD pinching checks passed.')
print('Largest first-step block-diagonalization error:',worst)
