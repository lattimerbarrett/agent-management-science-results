import numpy as np
rng=np.random.default_rng(123)
# Explore the exhaustion bound in matrix examples.  This is a check
# only; normalized matrix traces do not establish the quasitrace lemma.
for N in [4,16,64]:
    d=8
    raw=[]
    for _ in range(N):
        x=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
        raw.append(x.conj().T@x)
    S=sum(raw)
    w,U=np.linalg.eigh(S)
    inv=(U*(1/np.sqrt(w)))@U.conj().T
    b=[inv@x@inv for x in raw]
    values=[np.trace(x).real/d for x in b]
    print(f'N={N}, sum={sum(values):.12f}, min={min(values):.6f}, max={max(values):.6f}')
