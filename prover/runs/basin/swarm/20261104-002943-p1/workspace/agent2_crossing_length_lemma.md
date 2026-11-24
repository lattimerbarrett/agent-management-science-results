# Finite length of dual-root steps crossing spectral nodes

Let the orbit retain N distinct spectral nodes forever, let p_k be the monic degree-s orthogonal polynomial, H_k=||p_k(A)y_k||, and let f_k be the monic ambient dual polynomial of degree d=N-s-1. Write its ordered roots as t_{k,1}<...<t_{k,d}.

Assume the standard Lyapunov identities and barycentric duality already proved by the team. Then

    sum_{k,j : [t_{k,j},t_{k+1,j}] contains a spectral node} |t_{k+1,j}-t_{k,j}| < infinity.

Proof. Orthogonality implies G_{w_{k+1}}(z)=p_k(z)f_k(z)/(H_k^2 Delta(z)). Consequently p_k f_k has exactly one simple root in each spectral gap, and f_k has at most one root in each gap. Also f_{k+1}-f_k ->0 coefficientwise: both extend continuously to the compact omega set, and f(Fu)=f(u) at every two-cycle u. Thus ordered root increments tend to zero. Eventually a crossing step can cross only one spectral node.

At sufficiently late crossing times at a fixed node lambda_i, the crossing root is uniformly separated from every other root of both f_k and f_{k+1}. Otherwise take a convergent subsequence of crossing times with two roots tending to lambda_i. These two roots must occupy the two immediately adjacent gaps at both times k and k+1, since each polynomial has at most one root in each gap and root increments tend to zero. Thus the number of roots on either side of lambda_i does not change, contradicting the crossing. This also shows that at most one ordered root crosses a given node at a late step (different roots may cross different nodes in the same step).

Barycentric duality gives

    f_k(lambda_i) = Delta'(lambda_i) w_{k,i} p_k(lambda_i)/H_k^2.

All p_k(lambda_i) are uniformly bounded, while H_k>=H_0>0. Uniform separation of the other roots now gives |t_{k,j}-lambda_i|<=C w_{k,i}. The analogous estimate at k+1 gives |t_{k+1,j}-lambda_i|<=C w_{k+1,i}<=C' w_{k,i}. Here the last inequality follows from w_{k+1,i}=w_{k,i}p_k(lambda_i)^2/H_k^2.

Because only one root crosses, f_{k+1}(lambda_i)/f_k(lambda_i)<0. Exact duality implies that the normalized residual's two-step coordinate multiplier M_{k,i} is negative. Hence

    w_{k,i} <= |y_{k+2,i}-y_{k,i}|^2 <= ||y_{k+2}-y_k||^2.

Therefore each late crossing length is bounded by C||y_{k+2}-y_k||^2. There are finitely many spectral nodes, so summing and using the Lyapunov square-summability proves the claim. Finitely many early steps do not affect it.

This lemma does NOT establish convergence: arbitrarily short repeated crossings can act as reflections at a spectral node, while the paths between crossings may have large length. It is a precise localization of the remaining difficulty, not a solution of the universal s=2,3 claims.
