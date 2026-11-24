import numpy as np
rng=np.random.default_rng(731)
d=4
cs=[]
for _ in range(12):
 x=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
 cs.append(x.conj().T@x)
R=sum(cs)
scale=np.linalg.eigvalsh(R).max()
cs=[c/scale for c in cs]
s=[np.zeros((d,d),complex)]
for c in cs:s.append(s[-1]+c)
eta=.035
a=s[0]
last=0
errs=[]
while True:
 candidates=[k for k in range(last+1,len(s)) if np.trace(s[k]-a).real/d >= eta]
 if not candidates:break
 k=candidates[0]
 gap=np.trace(s[k]-a).real/d
 t=eta/gap
 anew=(1-t)*a+t*s[k]
 assert np.linalg.eigvalsh(anew-a).min()>-1e-12
 assert np.linalg.eigvalsh(s[k]-anew).min()>-1e-12
 errs.append(abs(np.trace(anew-a).real/d-eta))
 a=anew;last=k
print('Finite noncommuting interpolation checks:',len(errs))
print('Maximum increment error:',max(errs, default=0))
print('This checks the finite interpolation identities only, not infinite-dimensional gluing.')
