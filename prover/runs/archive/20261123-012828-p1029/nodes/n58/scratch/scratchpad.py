import numpy as np
rng=np.random.default_rng(1029)
checks=0
for d in range(2,12):
 for rep in range(20):
  xs=[]
  for j in range(4):
   X=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
   xs.append(X.conj().T@X)
  S=sum(xs); scale=np.linalg.eigvalsh(S)[-1]
  xs=[B/scale for B in xs]; S=sum(xs)
  ev,U=np.linalg.eigh(S)
  for t in [.1,.3,.6,.9]:
   P=U[:,ev>t]@U[:,ev>t].conj().T
   Q=np.eye(d)-P
   h=int(np.sum(ev>t))
   for B in xs:
    tr=lambda X: np.trace(X).real/d
    assert tr(B)-tr(P@B@P)<=t+1e-10
    # Q removes h dimensions: retain at least the bottom d-h eigenvalue sum.
    Bvals=np.linalg.eigvalsh(B)
    assert tr(Q@B@Q)+1e-10>=Bvals[:d-h].sum()/d
    checks+=2
print('Passed',checks,'finite-matrix compression certificates.')
# Exponent comparison driving maximality.
for L in [0.1,0.25,0.4,0.49]:
 p=1/(1-L)
 print('Lambda',L,'forced lower exponent',p,'quadratic upper exponent',2,
       'incompatible as t -> 0:',p<2)
