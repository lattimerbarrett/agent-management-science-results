# A discrete logarithmic barrier excluding extinct -1 modes at full 2s support

Assume a nonterminating orbit has even cluster set entirely on a fixed support S of 2s nodes, with all coordinates in S uniformly nonzero at cluster points. Let h=lim H_k and C=h^2. Every cluster two-cycle satisfies P Q=Delta_S+C. This has finitely many monic factor pairs, so connectedness of the even cluster set and continuity of its orthogonal polynomials imply q_(2k)->P and q_(2k+1)->Q for one fixed pair. (Interchanging P,Q simply corresponds to the opposite parity.)

Let mu be an initially active spectral node outside S, so its weight remains positive at every finite iteration but tends to zero. Write R_k=q_k q_(k+1), a_k=H_k H_(k+1), and assume P(mu)Q(mu)=-C. Let L_i be the degree-(2s-1) Lagrange interpolation coefficient at mu for the nodes in S. Then sum_i L_i=1. Since R_k-(P Q) has degree <=2s-1,
 R_k(mu)+C=sum_i L_i(R_k(lambda_i)-C).
Put e=C-a_k>=0 and u_i=R_k(lambda_i)-a_k. The preceding identity says
 R_k(mu)=-C+sum_i L_i u_i-e.
For all sufficiently late k, R_k(lambda_i)>0 on S and R_k(mu)<0. Define the positive logarithmic-barrier quantity
 I_k=|y_(k,mu)| prod_(i in S) |y_(k,i)|^(L_i).
The exact two-step residual multiplier gives
 log I_(k+2)-log I_k
 =log[(a_k+2e-sum_i L_i u_i)/a_k]
   +sum_i L_i log[(a_k+u_i)/a_k].
All linear terms in u_i cancel, leaving the positive first-order term 2e/a_k. Taylor's theorem on a fixed neighborhood of 1 gives a uniform lower bound
 log I_(k+2)-log I_k >= e/a_k - K sum_i u_i^2
for sufficiently late k: the negative O(e^2) term is absorbed by the positive e/a_k term because e->0.

On S the even and odd residual coordinates are bounded away from zero. Since
 y_(k+2,i)-y_(k,i)=[R_k(lambda_i)/a_k-1] y_(k,i)=u_i y_(k,i)/a_k,
we have sum_i u_i^2 <= K' ||y_(k+2)-y_k||^2. The latter is summable. Therefore log I_(2k) is bounded below. But all active factors stay bounded above and below, whereas y_(2k,mu)->0, so log I_(2k)->-infinity, a contradiction.

Consequently no initially active outside node can have limiting two-step multiplier -1 under this full-support-cluster hypothesis. A limiting multiplier of absolute value >1 is also impossible, since its weight would eventually grow uniformly instead of tending to zero. Multiplier +1 is impossible outside S by the degree-2s support polynomial. Thus all outside weights decay exponentially.

This lemma does not itself prove convergence of the active coordinates: a separate finite-variation/root-ordering argument remains necessary. It does, however, rule out all full-2s-support minus-mode counterexamples under the stated cluster hypothesis, for every s.
