import numpy as np
rng=np.random.default_rng(421)
def normmat(A):return np.linalg.svd(A,compute_uv=False)[...,0]
def char(M,p):
 q=p/(p-1)
 P=M[:,None]@np.linalg.inv(M)[None,:]
 K=normmat(P)
 return np.mean(np.mean(K**q,axis=1)**(p-1))
maxratio=0.;maxcs=0.
for p in [1.2,1.5,2,3,5,10]:
 q=p/(p-1)
 for trial in range(100):
  n=6
  M=rng.normal(size=(n,2,2))+1j*rng.normal(size=(n,2,2))
  M+=np.eye(2)[None]*2
  v=rng.normal(size=2)+1j*rng.normal(size=2)
  MiH=np.linalg.inv(M).conj().transpose(0,2,1)
  z=np.linalg.norm(MiH@v,axis=1)
  u=z**(-p)
  for i in range(n):
   for j in range(i+1,n+1):
    A=char(M[i:j],p)
    B=np.mean(u[i:j])*np.mean(u[i:j]**(-1/(p-1)))**(p-1)
    maxratio=max(maxratio,B/A)
    assert B<=A*(1+1e-9)
  f=rng.normal(size=(n,2))+1j*rng.normal(size=(n,2))
  lhs=u*np.abs(np.einsum('ni,i->n',f,np.conj(v)))**p
  rhs=np.linalg.norm(np.einsum('nij,nj->ni',M,f),axis=1)**p
  maxcs=max(maxcs,np.max(lhs/rhs))
  assert np.all(lhs<=rhs*(1+1e-10))
print('600 random complex roots, all12600 interval characteristics checked')
print('maximum scalar/matrix characteristic ratio',maxratio)
print('maximum directional input ratio',maxcs)
# Check row frame identity with arbitrary invertible complex T.
for k in range(1000):
 T=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
 D=np.diag(np.exp(rng.normal(size=2)));M=D@T
 for j in range(2):
  v=T.conj().T[:,j]
  got=np.linalg.norm(np.linalg.inv(M).conj().T@v)
  assert np.isclose(got,1/D[j,j],rtol=1e-9)
print('2000 exact row-frame reciprocal identities checked numerically')
open('workspace/agent1_frame_checks.py','w').write(open('scratchpad.py').read())
open('workspace/agent1_frames.md','w').write('''# Fixed finite row frames cannot yield non-scalar sharpness\n\nLet M be any measurable invertible root (polar decomposition identifies its norm and pairwise characteristic with the positive root of W=(M* M)^(p/2)). Suppose M(x)=D(x)T_j on each of N measurable phases, with D positive diagonal and T_j fixed invertible.\n\nFor a fixed nonzero v, u_v=|M^{-*}v|^{-p} has scalar Ap characteristic at most the matrix characteristic A: indeed |M(y)^{-*}v|/|M(x)^{-*}v| is at most ||M(x)M(y)^{-1}||, and the exact nested integrals give the assertion. Also u_v |<f,v>|^p <= |Mf|^p pointwise by Cauchy-Schwarz.\n\nFor v_jk=T_j* e_k, on phase j one has |M^{-*}v_jk|=1/d_k, hence u_v_jk=d_k^p. Scalar Hilbert Ap estimates, componentwise commutation, and l2/lp equivalence give\n||MHf||_p^p <= C_p sum_jk ||H<f,v_jk>||_Lp(u_v_jk)^p <= C_p (2N) A^(p S(p)) ||Mf||_p^p,\nwhere S(p)=max(1,1/(p-1)). No constants depend on the directions or conditioning of T_j.\n\nDual roots M^{-*}=D^{-1}T_j^{-*} have the same number N of fixed row frames. Applying the result at q and using characteristic duality gives the additional N^(1/q) factor. Thus\n||H||_Lp(W) <= C_p N^min(1/p,1/q) A^S(p).\n\nIf the candidate F(p)=1+1/[p(p-1)] is sharp along weights of characteristic A, these weights must use at least order A^min(1,1/(p-1)) fixed row frames (up to constants). In particular binary h, or any uniformly bounded number of h-values, cannot attain F(p). This is an obstruction only, not an exact-beta proof.\n''')
