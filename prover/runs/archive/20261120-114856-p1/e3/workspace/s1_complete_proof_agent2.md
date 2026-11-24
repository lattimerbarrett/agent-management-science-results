# Complete proof for s=1
Let the distinct active eigenvalues be lambda_1,...,lambda_m, and let P_i be their orthogonal spectral projectors. Put p_{k,i}=||P_i r_k||^2/||r_k||^2. The one-block minimizer is x_{k+1}=x_k+r_k/mu_k where mu_k=sum lambda_i p_{k,i}>0. Thus residual weights obey
T_i(p)=p_i(lambda_i-mu)^2/V,
where V=sum p_i(lambda_i-mu)^2. Nontermination implies V>0 at every step.

Write central moments M_j=sum p_i(lambda_i-mu)^j. The transformed mean is mu+M_3/V, and its variance is M_4/V-M_3^2/V^2. Consequently
V(Tp)-V(p)= E[((lambda-mu)^2-(M_3/V)(lambda-mu)-V)^2]/V >=0.
The equality follows by expanding the square, using E(lambda-mu)=0 and E(lambda-mu)^2=V. Since V is bounded on the finite simplex, V(p_k) tends to L>=V(p_0)>0.

Consider any cluster point p. It has V(p)=L>0. The map T is continuous near p, so V(Tp)=L as well. Equality in the preceding identity means the monic quadratic (lambda-mu)^2-(M_3/V)(lambda-mu)-V vanishes at every spectral node carrying positive mass. Hence p has support at most two; because V(p)>0, it has exactly two.

On a pair alpha<beta, write p=(t,1-t) with 0<t<1. Then V=t(1-t)(beta-alpha)^2, and direct substitution gives T(p)=(1-t,t), hence T^2(p)=p. For fixed L>0, only finitely many two-point probability measures on the finite set {lambda_i} have variance L: each of finitely many pairs gives at most two t's. Thus the cluster set of p_k is finite. Moreover ||p_{k+2}-p_k|| tends to zero: otherwise a convergent subsequence p_{k_j}->p would, by continuity, have p_{k_j+2}-p_{k_j}->T^2(p)-p=0, a contradiction.

A sequence in a compact metric space with finite cluster set and successive increments tending to zero converges. To prove this, choose disjoint small balls around the cluster points. All sufficiently late terms lie in their union; successive distances eventually are smaller than the positive separation of the balls, so the late sequence stays in one ball. Shrinking the ball proves convergence. Apply this separately to the even and odd weight sequences. In particular p_{2k}->p_inf, supported on a pair alpha<beta, and p_{2k+1}->T(p_inf).

It remains to recover signs, not just squared norms. Each spectral component P_i r_k is always a scalar multiple of the fixed nonzero vector P_i r_0. On the limiting pair, both limiting masses are positive. The means of p_inf and T(p_inf) lie strictly between alpha and beta. Thus, eventually, for every k, the two factors 1-alpha/mu_k and 1-alpha/mu_{k+1} have the same sign, and likewise the two beta factors. Therefore the scalar multiples of P_alpha r_{2k} and P_beta r_{2k} have eventually constant signs. Their normalized magnitudes converge to sqrt(p_inf,alpha) and sqrt(p_inf,beta). Every other normalized component tends to zero. Orthogonality of spectral eigenspaces proves convergence of y_{2k} in Euclidean norm.

This applies to arbitrary multiplicities of eigenvalues, and arbitrary n,A,b,x0. The only excluded initial case V(p0)=0 terminates after one block, as required.
