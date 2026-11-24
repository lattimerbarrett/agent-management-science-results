import numpy as np
rng=np.random.default_rng(2026)
worst=0.0
for size in [2,3,5]:
    for _ in range(40):
        z=rng.normal(size=(size,size))+1j*rng.normal(size=(size,size))
        b=z.conj().T@z
        b/=np.linalg.norm(b,2)
        z=rng.normal(size=(size,size))+1j*rng.normal(size=(size,size))
        u,_=np.linalg.qr(z)
        vals=rng.uniform(.2,1.7,size)
        c=(u*vals)@u.conj().T
        ci=(u*(vals**-.5))@u.conj().T
        transformed=ci@b@ci
        tb=np.trace(b).real/size
        tt=np.trace(transformed).real/size
        low=tb/vals.max(); high=tb/vals.min()
        assert low-1e-10<=tt<=high+1e-10
        worst=max(worst,max(low-tt,tt-high))
print('120 matrix checks of the congruence gap bounds passed.')
print('Analytic bound used: b^(1/2)c^(-1)b^(1/2) lies between b/||c|| and b/minspec(c).')
print('This checks the formulas, not the missing sharp-endpoint theorem.')
