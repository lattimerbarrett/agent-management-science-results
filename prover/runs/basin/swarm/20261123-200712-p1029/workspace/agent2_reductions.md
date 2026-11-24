# Rigorous reductions (not a complete solution)

## Elementary bound and downward closure
Set d_n=a_{n+1}-a_n. For n>=1, d_0<=a_n and d_n<=1-a_n. Monotonicity and scalar-shift linearity of q imply eta<=q(a_n)<=1-eta, hence eta<=1/2. Scaling every a_n by theta/eta proves downward closure of G and preserves absence of a least upper bound.

## Closedness of the positive cone for the quasitrace topology
Write rho(z)^2=q(z*z). For self-adjoint z and projection p,
(pzp)^2<=pz^2p and q(pz^2p)=q(zpz)<=q(z^2).
Thus compression contracts rho. If x_j>=0, x_j -> x in rho, and p=1_{(-infinity,-delta]}(x) is nonzero, then p(x_j-x)p>=delta p. Its squared quasitrace is at least delta^2 q(p)>0, contradicting compression contractivity. Star continuity gives self-adjointness of the limit first. Consequently the positive cone and the positive unit interval are rho-closed.

## Reconstruction of bounded quasitracial completeness
Inputs: standard finite-AW* dimension continuity, projection normality also in M2(M), and the standard quasitrace quasi-triangle inequality.

For a rho-Cauchy sequence 0<=x_n<=1 choose a subsequence with q(|x_{n+1}-x_n|^2)<=2^{-4n}. Let p_n=1_{[0,2^{-n}]}(|x_{n+1}-x_n|), e_k=meet_{n>=k}p_n. Then D(1-e_k)<=sum_{n>=k}2^{-2n}->0. For every fixed k, x_n e_k has a norm limit y_k; ||y_k||<=1 and y_k e_l=y_l for l<=k.

Let P_k in M2(M) be the projection onto the module graph {(e_k z,y_k z):z in M}. It equals V_k(e_k+y_k*y_k)^{-1}V_k*, where V_k is the column [e_k;y_k] and inverse is in e_k M e_k. Compatibility implies P_k<=P_{k+1}. Also (P_k)11>=e_k/2 and P_k<=diag(2,2/3). The latter follows from V_k*diag(1/2,3/2)V_k<=V_k*V_k because y_k*y_k<=e_k.

Let P be the projection join. Projection normality makes it the SA supremum, whence P11>=1/2 and P22<=2/3. Put a=P11,b=P12,c=P21,d=P22. The Schur residual r=d-ca^{-1}b is positive, satisfies r^2=r, and is <=d<1; hence r=0. Therefore P is the graph of x=ca^{-1}. From P_k<=P we get xe_k=y_k. The estimate rho((x_n-x)(1-e_k))^2<=9D(1-e_k), together with norm convergence on e_k and the quasi-triangle inequality, gives x_n->x in rho. Closedness of the positive unit interval gives 0<=x<=1.

The exact graph formulas/order estimates are checked for rational matrices, and the identity r^2=r is checked in the free algebra in agent2_boundary_checks.py. These checks support the algebra, not the structural dimension/projection-normality inputs.

## Exact-increment interpolation
Assume the bounded completeness just reconstructed. A bounded increasing sequence with no SA supremum cannot be rho-Cauchy: otherwise its rho-limit is its supremum, by positive-cone closedness.

Hence there is epsilon>0 such that beyond every index there are m>n with q((a_m-a_n)^2)>=epsilon. Since 0<=a_m-a_n<=1, also q(a_m-a_n)>=epsilon. Let A(t) be the increasing polygonal norm-continuous interpolation of a_n, and set eta=epsilon/2. Given t_k, there is s>t_k with q(A(s)-A(t_k))>=epsilon. Continuity and monotonicity give an earliest crossing t_{k+1}>t_k with q(A(t_{k+1})-A(t_k))=eta. If the t_k were bounded, norm continuity on a compact parameter interval would force successive differences to zero in norm, contradicting their quasitrace eta. Thus t_k->infinity. The extracted sequence is cofinal with the original, so it has exactly the same upper bounds and no least upper bound.

Therefore the exact positive-increment condition does not weaken the no-supremum problem once bounded quasitracial completeness is available. The missing main step is monotone sequential completeness / quasitracial exhaustivity, not interpolation.
