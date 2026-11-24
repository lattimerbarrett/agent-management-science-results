# Duality and characteristic normalization
Let q=p/(p-1) and U=W^{-1/(p-1)}. Then U^{1/q}=W^{-1/p}. We prove

(1/16)[W]_{A_p}^{1/p} <= [U]_{A_q}^{1/q} <= 16[W]_{A_p}^{1/p}.

First U has locally integrable entries. Fix I. Finiteness of the defining integral provides x0 in I with W(x0) positive definite and integral_I ||W(x0)^{1/p} W(y)^{-1/p}||^q finite. Multiplication by W(x0)^{-1/p} shows integral_I ||W(y)^{-1/p}||^q finite. This equals integral_I ||U(y)||. Thus U is a matrix weight.

For any norm rho on C^2, there is positive definite B with
  2^{-1/2}|Bv| <= rho(v) <= 2^{1/2}|Bv|.
Indeed choose a pair of vectors in the rho-unit ball maximizing absolute determinant; compactness and nonempty interior make the maximum positive and attained. Replacing one column by an arbitrary unit-ball vector shows its coordinates in this basis have modulus at most 1. If T is the coordinate map, max_j|(Tv)_j| <= rho(v) <= sum_j|(Tv)_j|. Set B=(T*T)^{1/2}.

For a matrix family M and r>=1, let rho(v)=(avg_I |M(y)v|^r)^{1/r}, and choose B as above. For any fixed T,
  2^{-1/2}||BT|| <= (avg_I ||M(y)T||^r)^{1/r} <= 2sqrt(2)||BT||.
The lower bound tests a maximizing unit vector; the upper uses ||MT||<=|MT e1|+|MT e2|, Minkowski, and |BT ej|<=||BT||.

For fixed I take A reducing (avg_I |W^{1/p}v|^p)^{1/p} and B reducing (avg_I |W^{-1/p}v|^q)^{1/q}. In the defining A_p kernel take adjoints to put W(y)^{-1/p} on the left. Apply the preceding estimate first in y and then in x (using ||B W(x)^{1/p}||=||W(x)^{1/p}B||). This proves
  (1/2)||AB|| <= [W]_{A_p,I}^{1/p} <= 8||AB||.
For U the roles A,B are interchanged; ||BA||=||AB|| since A,B are Hermitian. Comparing and taking sup_I gives the claim.

Weighted duality under the unweighted pairing identifies L^p(W)* with L^q(U), since the dual of multiplication by W^{1/p} is multiplication by W^{-1/p}. Compact smooth functions are dense: truncate in support and size, approximate bounded functions by continuous functions for the finite measure ||W|| dx on compact sets, then uniformly approximate continuous functions by smooth ones. The identity H*=-H on compact smooth functions, followed by duality, proves exact equality of the bounded operator norms of H on L^p(W) and L^q(U).

Consequently admissible power exponents obey beta(p)=beta(q)/(p-1). Indeed a bound with exponent gamma at q gives an exponent gamma*q/p=gamma/(p-1) at p, and reversing gives equality of infima. In particular alpha(p)=1+1/(p(p-1)) is consistent with this relation. This reduction does NOT establish alpha at any p, and does not transfer the p=2 lower example to other p.

Finally for each fixed nonzero e, scalar w_e=|W^{1/p}e|^p has [w_e]_{A_p} <= [W]_{A_p}. Pointwise the kernel dominates |W(x)^{1/p}e|/|W(y)^{1/p}e|; insert this in the defining averages. The analogous inverse direction satisfies [|W^{-1/p}e|^q]_{A_q} <= 16^q [W]_{A_p}^{1/(p-1)}.
