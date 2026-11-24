## Complete proof for s=1

Diagonalize A and group equal eigenvalues. Write the distinct active eigenvalues as 0<lambda_1<...<lambda_m and let e_i be the fixed unit vector in the direction of the initial residual's projection onto its lambda_i eigenspace. Every residual is sum_i rho_{k,i} e_i. Define w_{k,i}=rho_{k,i}^2/sum_j rho_{k,j}^2. For s=1 the residual update is r_{k+1}=(I-A/mu_k)r_k, where mu_k=sum_i lambda_i w_{k,i}. Therefore

T(w)_i=w_i(lambda_i-mu)^2/V,
V=sum_i w_i(lambda_i-mu)^2.

Nontermination implies V>0. Let m_j=sum_i w_i(lambda_i-mu)^j. Direct substitution gives
V(Tw)-V(w)=(V*m_4-m_3^2-V^3)/V^2.
The numerator is the determinant of the Gram matrix of the functions 1, lambda-mu, (lambda-mu)^2 in L^2(w), hence is nonnegative. It vanishes precisely when these functions are linearly dependent on the support, which holds precisely when the support has at most two distinct nodes. (A nonzero quadratic cannot vanish at three distinct points; the first two functions are independent when V>0.)

Consequently V_k increases to some V_infty>=V_0>0. All weights stay in the compact set K={w in simplex: V(w)>=V_0}; T is continuous on K. If w_{k_j}->w, continuity and V_{k+1}-V_k->0 imply the Gram determinant at w vanishes. Thus every cluster point has exactly two positive weights, since V(w)=V_infty>0. There are only finitely many such cluster points: select the supporting pair (a,b); its mass p satisfies p(1-p)(b-a)^2=V_infty, a quadratic equation.

On every two-node measure, T exchanges the two masses and hence T^2w=w. By compactness and continuity, it follows that ||w_{k+2}-w_k||->0. The even sequence therefore has a finite cluster set and successive increments tending to zero, and must converge. To justify the last assertion, choose disjoint balls around the finitely many possible cluster points. Eventually the sequence lies in their union and its increment is smaller than the minimum distance between these balls, so it cannot move from one ball to another. Let w_{2k}->w_bar, supported on lambda_a<lambda_b. Then w_{2k+1}->T(w_bar). Both limiting means lie strictly between lambda_a and lambda_b. Hence for both persistent eigencomponents, the product (1-lambda_i/mu_{2k})(1-lambda_i/mu_{2k+1}) is eventually positive: both factors are positive at lambda_a and both are negative at lambda_b. Thus the corresponding normalized residual coordinates have eventually constant sign along the even subsequence, while their magnitudes converge to sqrt(w_bar_i). All remaining normalized coordinates tend to zero. This proves Euclidean convergence of y_{2k}.
