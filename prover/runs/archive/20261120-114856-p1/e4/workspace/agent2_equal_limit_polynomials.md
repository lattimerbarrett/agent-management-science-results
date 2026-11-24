# All-s convergence when the two limiting polynomials coincide

Use the globally established notation h_k=E_{w_k}q_k^2, h_k increases to H>0, and q_{2k}->q,q_{2k+1}->r. The BV identity gives the quantitative tail bound ||q_k-q_parity||<=C(H-h_k), after increasing C to handle the adjacent block index. Suppose q=r=p.

The limiting product is p^2. Every retained initial node has p(lambda)^2<=H. Let S={i:p(lambda_i)^2=H}. There can be no negative-neutral nodes, since p^2 is nonnegative. Thus all weights outside S decrease exponentially under the two-step map. Write eta_k=sum_{i notin S}w_{k,i}; then eta_k<=C rho^k for some rho<1.

The orthogonal-polynomial projection identity holds exactly:
 E_{w_k}p^2=h_k+E_{w_k}(p-q_k)^2,
because p-q_k has degree less than s. Therefore
 H-h_k=E_{w_k}(p-q_k)^2+sum_{i notin S}(H-p(lambda_i)^2)w_{k,i}.
In particular H-h_k<=C||p-q_k||^2+C eta_k. With d_k=||p-q_k||, the BV tail bound yields
 d_k<=C d_k^2+C eta_k.
Since d_k tends to zero, absorption gives d_k<=C eta_k, and then H-h_k<=C eta_k. Thus both polynomials and monic norms converge exponentially.

On S, the two-step weight multiplier q_k(lambda_i)^2 q_{k+1}(lambda_i)^2/(h_k h_{k+1}) differs from 1 by O(eta_k+eta_{k+1}). Consequently sum_k||w_{k+2}-w_k|| is finite; the outside weights already tend exponentially to zero. Hence even weights converge. At persistent components, the two-step signed normalized-residual multiplier tends to p(lambda_i)^2/H=1, so the corresponding signs are eventually fixed. Therefore y_{2k} converges.

This proves a global all-dimensional result for every restart length s under the single additional condition q=r, and rules out all p^2-H maximal-polytope candidates as nonconvergent examples.
