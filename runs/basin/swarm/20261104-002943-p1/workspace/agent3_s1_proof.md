# General reduction and complete s=1 proof

Discard eigenspaces on which r0 has zero projection. Within each remaining eigenspace every residual is a scalar multiple of its initial projection, so choose the unit initial direction as coordinate. We obtain d distinct positive eigenvalues lambda_i, and a unit residual y in R^d. A nonterminating orbit has at least s+1 nonzero coordinates at every step.

For unit y supported on >s nodes, let q_y be its monic degree-s orthogonal polynomial for weights y_i^2; equivalently q minimizes ||q(A)y|| among monic degree-s polynomials. Put H(y)=||q_y(A)y||>0. Its roots lie strictly in the positive spectral interval (indeed, if there were fewer than s sign changes on the positive support interval, multiplying q by the polynomial whose simple roots are those sign-change locations would give a polynomial of degree <s having nonzero, constant-sign weighted inner product with q, contradicting orthogonality; thus all s roots are simple and lie in that interval), so q_y(0) has sign (-1)^s. The block minimizer has residual q_y(A)r/q_y(0), by its normal equations. Thus the normalized residual map is F(y)=(-1)^s q_y(A)y/H(y).

The squared norm H^2 extends continuously to every unit y as the minimum monic-polynomial norm (zero on support size <=s), since it is a Gram determinant quotient wherever the degree-(s-1) moment matrix is invertible; continuity at smaller supports follows by choosing a monic polynomial vanishing on those supports and using nonnegativity. At any point with H>0 the moment matrix is positive definite and F,H are real analytic.

If z=F(y), monicity and orthogonality give
  <q_y(A)y,q_z(A)y>=H(y)^2.
Consequently
  <y,F^2(y)>=H(y)/H(F(y)).
Cauchy-Schwarz yields H(F(y))>=H(y), and
  ||F^2(y)-y||^2=2(1-H(y)/H(F(y))).
Equality in monotonicity is equivalent to F^2(y)=y.

Since H is bounded on the unit sphere, H(y_k) tends to h>0. Every cluster point has H=h, so continuity of F there implies it is a two-cycle. Further ||y_{k+2}-y_k|| tends to zero. In fact summability follows since 1-a/b <= log(b/a), giving sum_k ||y_{k+2}-y_k||^2 <= 2 log(h/H(y0)).

At a two-cycle y,z, q_z(A)q_y(A)y=h^2 y. Hence the nonzero coordinates are supported among roots of the monic degree-2s polynomial q_z q_y-h^2, and there are at most 2s distinct active eigenvalues.

The cluster set of a bounded sequence with successive distances tending to zero is compact and connected: if it split into two nonempty compact subsets a positive distance apart, infinitely many transitions between their neighborhoods would force a cluster point outside both. Apply this to the even subsequence.

For s=1, every cluster point has precisely two active nodes a<b (one node would give H=0). Write their squared weights t,1-t. The orthogonal polynomial is q(x)=x-mu with mu=at+b(1-t), and
  h^2=t(1-t)(b-a)^2.
For each pair (a,b) this equation has at most two values t. There are finitely many node pairs and at most four sign choices for their coordinates. Thus the even cluster set is finite. Since it is also connected, it is a singleton. Compactness then implies y_{2k} converges in Euclidean norm.


# Additional local convergence lemma (all s)

Suppose the cluster set of the even subsequence lies on a fixed coordinate face S of size s+1 and every coordinate in S is nonzero at every cluster point. Suppose moreover that for each j outside S the continuous two-step residual multiplier
  M_j(y)=q_y(lambda_j) q_Fy(lambda_j)/(H(y)H(Fy))
is never +1 on that cluster set. Then the even subsequence converges.

Indeed compactness gives |M_j-1|>=delta>0 in a neighborhood of the cluster set, for all j outside S. The exact identity y_{k+2,j}-y_{k,j}=(M_j(y_k)-1)y_{k,j}, together with square summability of two-step increments, gives sum_k y_{2k,j}^2<infinity. The two-step squared-weight map G is analytic near the compact cluster set and depends only on squared weights. On the face S it is exactly the identity: if a_i=1/prod_{ell in S,ell !=i}(lambda_i-lambda_ell), orthogonality yields one-step weights proportional to a_i^2/w_i, an involution. Comparing any nearby weight vector to its normalized projection onto the face therefore gives |G_i(w)-w_i| <= C sum_{j outside S} w_j for each i in S. Thus even active weights have summable absolute increments and converge. Their limiting values are positive; since the active two-step multipliers approach +1, each even active coordinate eventually keeps its sign. All inactive coordinates tend to zero. Hence the normalized even residual itself converges.
