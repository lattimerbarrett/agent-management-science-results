# Quadratic bound on negative-neutral outsider weights
Fix the even-block indexing. Write t_k=L-N_{2k}>0 and p_k=p_{2k,mu} for an active spectral node mu satisfying f(mu)g(mu)=-L. The all-s polynomial-TV tail estimate implies
p_{k+1}/p_k = (f_{2k}(mu)f_{2k+1}(mu))^2/(N_{2k}N_{2k+1}) = 1+O(t_k).
Hence p_k-p_{k+1} <= C t_k p_k. The strict monic Lyapunov identity gives t_k-t_{k+1} >= c p_k for all large k: the mu coordinate of F^2 y-y equals (-2+o(1))y_mu, so the squared step controls p_k, and the norm gain controls the squared step uniformly since N>=N0>0.
Thus, telescoping (p_k->0),
p_k = sum_{j>=k}(p_j-p_{j+1}) <= (C/c) sum_{j>=k} t_j(t_j-t_{j+1}) <= (C/c)t_k^2.
The summands on the left need not be positive; finite partial sums suffice and the right converges. This proves p_{2k,mu}=O((L-N_{2k})^2) without any regular-variation assumption.

Furthermore an active negative-neutral outsider forces sum_k t_k=infinity: otherwise sum|log(p_{k+1}/p_k)|<infinity, contradicting p_k->0. Since t_k->0, log p_k=o(k), and the bound p_k<=C t_k^2 yields log t_k=o(k) from below. Hence all strictly contracting outsider weights O(rho^k) are o(t_k^2). On the limiting positive root set, f_{2k}f_{2k+1}-N_{2k}=O(t_k), so the variance identity now yields N_{2k+1}-N_{2k}=O(t_k^2), and the analogous odd estimate yields t_k-t_{k+1}=O(t_k^2).

Consequently any nontrivial negative-neutral asymptotic regime admits the compact normalization epsilon=t_k: polynomial errors divided by epsilon are uniformly bounded by TV, and negative-neutral weights divided by epsilon^2 are uniformly bounded by this lemma. This rules out using unbounded normal-form trajectories as evidence of actual fixed-target asymptotics.
