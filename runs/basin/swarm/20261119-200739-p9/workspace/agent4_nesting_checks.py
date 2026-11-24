import numpy as np
from pathlib import Path
from scipy.linalg import block_diag
rng=np.random.default_rng(42971)

def mpower(A,t):
    d,U=np.linalg.eigh(A)
    return (U*d**t)@U.T

def char(Ws,p):
    q=p/(p-1)
    A=[mpower(W,1/p) for W in Ws]
    B=[mpower(W,-1/p) for W in Ws]
    return np.mean([np.mean([np.linalg.norm(X@Y,2)**q for Y in B])**(p-1) for X in A])

J=np.array([[0.,-1.],[1.,0.]])
maxerr=0.
maxratio=0.
for trial in range(100):
    Ws=[]; As=[]
    n=5
    for k in range(n):
        theta=rng.uniform(0,2*np.pi)
        O=np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])
        lam=np.exp(rng.uniform(0,4))
        W=(O*np.array([lam,1/lam]))@O.T
        A=mpower(W,.5)
        maxerr=max(maxerr,np.linalg.norm(np.linalg.inv(A)-J@A@J.T))
        Ws.append(W); As.append(A)
    C2=char(Ws,2)
    for p in [2.,2.1,2.5,3.,4.,8.,20.]:
        Cp=char(Ws,p)
        maxratio=max(maxratio,Cp/C2)
        assert Cp <= C2*(1+1e-9)
    H=rng.normal(size=(n,n)); H=H-H.T
    A=block_diag(*As)
    K=A@np.kron(H,np.eye(2))@np.linalg.inv(A)
    JJ=np.kron(np.eye(n),J)
    err=np.linalg.norm(K.T + JJ@K@JJ.T)/max(1.,np.linalg.norm(K))
    maxerr=max(maxerr,err)
    assert err<1e-11
print('100 determinant-one random matrix weights, 7 p values: characteristic nesting passed.')
print('Largest Cp/C2:',maxratio)
print('Largest det-one inverse / transformed-adjoint error:',maxerr)
Path('workspace/agent4_nesting_checks.py').write_text(Path(__file__).read_text())
Path('workspace/agent4_nesting.md').write_text(r'''# Two exact additional lemmas

1. If U is matrix A2, then for every p>=2, [U]Ap <= [U]A2,
with exactly the normalization in the question.

Proof: for positive definite X,Y and 0<=t<=1, Cordes inequality gives
||X^tY^t|| <= ||XY||^t. It follows from three-lines applied to X^zY^z:
on Re z=0 the matrices are unitary; on Re z=1 the norm is ||XY||.
Put X=U(x)^(1/2), Y=U(y)^(-1/2), t=2/p. Then the inner q moment
is bounded by E_y k(x,y)^(2/(p-1)), where k=||X Y||. Jensen/Lyapunov,
since p-1>=1, gives (E_y k^(2/(p-1)))^(p-1)<=E_y k^2.
Integrate in x and take suprema.

2. Suppose A(x) is a real symmetric positive definite 2x2 matrix with
determinant one. Set K=A H A^(-1) on unweighted vector Lp. Then
||K||Lp=||K||Lq and ||K||Lp>=||K||L2 for every 1<p<infinity.
These are statements about a fixed root A, hence weights A^p, NOT about
one fixed weight at all p.

Proof: J=[[0,-1],[1,0]] is a fixed orthogonal matrix and
A^(-1)=J A J^T. Consequently K*=-A^(-1) H A=-J K J^T.
Banach duality and constant orthogonal invariance give
||K||Lp=||K||Lq. Interpolation between these equal endpoint norms
bounds ||K||L2 by their common value. Truncation/density handles
unbounded A whenever the indicated bounded operators exist.

Neither lemma bounds [A^p]Ap using [A^2]A2. This missing bound cannot
hold in general: scalar diagonal powers arbitrarily close to an A2
integrability endpoint leave Ap after the power p/2, for p!=2.
''')
