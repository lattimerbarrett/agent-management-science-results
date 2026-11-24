import numpy as np
from pathlib import Path
rng=np.random.default_rng(210)
def power(A,t):
    e,U=np.linalg.eigh(A)
    return (U*e**t)@U.conj().T
def sharp(A,B,t):
    S=power(A,.5); T=power(A,-.5)
    return S@power(T@B@T,t)@S
def spd():
    M=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
    return M.conj().T@M+.1*np.eye(2)
def char(vals):
    A=sum(vals)/len(vals); B=sum(np.linalg.inv(W) for W in vals)/len(vals)
    return np.linalg.eigvalsh(power(A,.5)@B@power(A,.5)).max()
maxratio=0
for _ in range(300):
    A=spd(); vals=[spd() for j in range(6)]; t=rng.uniform()
    V=[sharp(A,B,t) for B in vals]
    ratio=char(V)/(char(vals)**t)
    assert ratio<1+1e-10,(ratio,t)
    maxratio=max(maxratio,ratio)
    for B,C in zip(vals,V):
        assert np.linalg.eigvalsh(A+B-C).min()>-1e-10
        assert np.linalg.eigvalsh(np.linalg.inv(A)+np.linalg.inv(B)-np.linalg.inv(C)).min()>-1e-10
print('300 geodesic interpolation and 3600 Loewner inequality tests pass; max A2 ratio',maxratio)
