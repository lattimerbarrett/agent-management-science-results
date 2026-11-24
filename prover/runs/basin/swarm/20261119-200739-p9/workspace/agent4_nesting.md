# Two exact additional lemmas

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
