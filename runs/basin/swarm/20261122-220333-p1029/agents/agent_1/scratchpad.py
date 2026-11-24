import numpy as np
rng=np.random.default_rng(2026)
for trial in range(10000):
    x=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
    y=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
    a=x.conj().T@x; c=y.conj().T@y
    lhs=np.linalg.eigvalsh(a@a+c@c)
    rhs=np.linalg.eigvalsh((a+c)@(a+c))
    if np.any(lhs>rhs+1e-7):
        print('Square spectral dominance fails', trial, lhs, rhs)
        break
else:
    print('No counterexample in tested cases; this is NOT a proof.')
