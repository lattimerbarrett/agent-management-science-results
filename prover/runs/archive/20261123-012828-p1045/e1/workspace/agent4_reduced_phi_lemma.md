# A lower-dimensional necessary inequality for the final k=3 case

Let theta_i>=0 sum to s=1-r, and suppose the greedy partition moment
constraints hold. Write G_R=r Z (r>0), where Z is symmetric nonnegative PSD.
Its diagonal entries lie in[0,1], and the greedy cost budget is
  sum_i theta_i Z_ii <=a-r.
Define the convex nonincreasing function
 phi(t)=1-2t                    (0<=t<=1/4),
        2(1-sqrt(t))²           (1/4<=t<=1),
        0                       (t>=1).
Then every model satisfies
 3b >= s+sum_{k=0}² theta_k phi((a-r Z_ij)/theta_k)
            +r[3-2sqrt(sum_{ij}Z_ij)+tr Z],
where {i,j,k}={0,1,2}. At theta_k=0 use the limiting perspective value0.

Proof: On V_k rows i,j are the only possibly positive ones. For scalars
u,v in[0,1], the minimum of (1-u)²+(1-v)² at fixed product t is phi(t):
write S=u+v and minimize2-2S+S²-2t over2sqrt(t)<=S<=1+t.
The mean product on V_k is at most(a-rZ_ij)/theta_k, by the red pair cap.
Convexity and monotonicity of phi give the displayed perspective bound
for its blue energy. Each row k contributes theta_k from its zero class.
On R, Cauchy gives sum_i int_R f_i <=r sqrt(sum_ij Z_ij).
Add the three blue-row caps.

If sum_i sqrt(Z_ii)<=1, replacing Z by the rank-one matrix with the same
diagonal and offdiagonal sqrt(Z_ii Z_jj) can only DECREASE the right side.
Indeed increase each offdiagonal toward this value; entrywise nonnegativity
holds, and it is harmless to compare directly without requiring the path
PSD. The total sum stays<=1, and derivative of the perspective part with
respect to an offdiagonal is between0 and2r because -2<=phi'<=0, while the
R term derivative is -2r/sqrt(sum Z)<=-2r. The resulting matrix is PSD.
Thus this subcase reduces to theta,r and3nonnegative scalar R crossvalues.

It remains UNPROVED that the displayed right side is always at least
3min{b3(a),b_hom(a)} for all feasible theta,Z. Numerical constrained
optimization at a=.09 and.1 found no violation, but this is not evidence
sufficient for a proof. The case sum sqrt(diag Z)>1 also requires analysis.
