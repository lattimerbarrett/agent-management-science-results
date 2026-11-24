import numpy as np
D=np.load('workspace/agent4_positive_ray_audit.npz');x=D['x'];p=D['p'];q=D['q'];C=float(D['C']);w=D['w'];h=D['h'];amp=D['A'];kap=float(D['kap']);V=x[:,None]**np.arange(4)
assert max(abs(p[:6]*q[:6]-C))<1e-10
assert max(abs(p[6:]*q[6:]+C))<1e-10
assert max(abs(V.T@(w*p)))<1e-10
z=w*p*p/C;M=V.T@(w[:,None]*V);Mz=V.T@(z[:,None]*V);ac=-C*np.linalg.solve(M,Mz);Frow=(w*p**3)@V
beta=-(q[6:,None]*(V[6:]@ac)+p[6:,None]*(C*V[6:])+Frow)/C
force=4/C*np.linalg.solve(Mz,V[6:].T*p[6:])
# Active relative shear, no second- or third-jet code used.
rel=2*(p*(V@h)-q*(V@(np.linalg.solve(M,Mz@h)))-(Frow@h)/C)
b=w*rel
assert np.linalg.norm(b)<2e-9
assert np.linalg.norm(force@(amp*amp)+kap*h)<2e-8
assert max(abs(beta@h+kap))<2e-9
E=-(Frow@h)/C
assert E>0
print('Independent analytic projection audit PASS: cycle, zero shear, force=-kappa*h, amplitude decay=-kappa, positive fuel.')
print('kappa=',kap,'fuel=',E,'radialrate=',kap/E)
