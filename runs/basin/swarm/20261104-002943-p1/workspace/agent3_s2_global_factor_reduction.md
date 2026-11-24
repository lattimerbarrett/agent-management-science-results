# Universal s=2 reduction to a fixed four-node cycle interval

This is valid for arbitrary initial dimension and spectrum. It is not a proof of s=2 convergence.

Reduce to distinct eigenvalues and the fixed initial eigenspace directions. Let F be the normalized residual map. The general Lyapunov theorem says that the even omega set Omega is compact and connected, every u in Omega satisfies F^2(u)=u, H(u)=h>0, and its support has at least 3 and at most 4 nodes. Put C=h^2.

Suppose the normalized even sequence fails to converge. If u in Omega has support S of size 3, the minimal-support trapping lemma implies that at least one initially present eigenvalue mu outside S has two-step multiplier +1 at u. Therefore, writing P=q_u and Q=q_Fu, the monic quartic P Q-C vanishes on the four distinct actual spectral nodes S union {mu}; hence P Q=prod_(lambda in S union {mu})(x-lambda)+C. If u instead has support of size 4, the same identity holds with those four active nodes.

There are finitely many four-node subsets of the fixed spectrum. For each such subset, the monic quartic prod(x-lambda)+C has only finitely many monic quadratic factor pairs (including possible repeated roots). Consequently the continuous map u -> (q_u,q_Fu) from connected Omega has finite image and therefore is constant. Call the constant pair (P,Q). Compactness implies q_(2k)->P and q_(2k+1)->Q along the entire orbit.

Let T be the four actual roots of P Q-C. Every omega support is a subset of T, so all coordinates outside T tend to zero. No outside node can have multiplier +1, since the quartic already has the four distinct roots T. Its multiplier also cannot have absolute value >1: the product q_k q_(k+1)/(H_k H_(k+1)) tends uniformly to that limiting constant at the node, and otherwise its positive weight would eventually increase instead of tending to zero. Thus outside nodes have absolute limiting multiplier <=1, not +1. By the exact two-step increment identity, their weights are summable whenever the limiting multiplier differs from +1, including the -1 case. If absolute multiplier <1 the decay is exponential.

The cycle weights on T have the explicit form
 w_i=C(lambda_i-t)/(Delta_T'(lambda_i)P(lambda_i)),
 where t ranges over the single complementary spectral gap, including endpoints for boundary cycles. Hence Omega is contained in the closed affine interval parametrized by t. Every point in the relative interior has four active coordinates. At either endpoint exactly one coordinate vanishes, giving a three-node cycle. If Omega contains no relative-interior point, it is a connected subset of the two endpoints and therefore a singleton, contradicting nonconvergence. Any hypothetical counterexample for s=2 must thus oscillate on a nontrivial subinterval of this single four-node cycle interval while outside weights tend to zero.

The remaining unresolved issue is to exclude repeated endpoint passages driven indirectly by summable outside -1 weights through the unipotent shear. Summability alone does not justify discarding that forcing.
