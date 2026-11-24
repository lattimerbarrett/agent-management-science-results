# Conditional transport-energy closure (fully proved abstract lemma)

This lemma is rigorous but conditional. Its application to the whole closed s=3 edge has NOT been established: uniform scalar transport at a two-facet corner and the global one-sided sign of the combined negative-action forcing remain open.

Let D_k>0 decrease to zero. Let u_k be bounded, R_k real, and A_k positive with c<=A_k<=C. Set z_k=R_k/A_k. Assume the following, for all sufficiently large k.

(1) |z_k|<=C D_k, and z_{k+1}-z_k=P_k-Q_k+epsilon_k, where P,Q are nonnegative summable sequences and sum_{i>=k}|epsilon_i|=o(D_k).

(2) There is a bounded scalar sequence Phi_k and a real sequence e_k=o(D_k) such that the tail series exists and

 D_k <= C_0 [ sum_{i>=k} z_i(Phi_{i+1}-Phi_i) + sum_{i>=k}P_i ] + e_k.

(3) sum_{i>=k}Q_i=o(D_k).

Then R_k<0 for all sufficiently large k. If additionally

 u_{k+1}-u_k=c_k R_{k+1}+delta_k, 0<=c_k<=C, sum|delta_k|<infinity,

then u_k converges.

PROOF. Write P[k],Q[k],E[k] for the tails of P,Q,|epsilon|. Because z tends to zero, summing (1) gives z_k=Q[k]-P[k]-sum epsilon. At an index with z_k>=0 this implies 0<=z_k<=Q[k]+E[k] and P[k]<=Q[k]+E[k]. The total variation tail of z is at most P[k]+Q[k]+E[k]. With B=sup|Phi|, summation by parts yields

 |sum_{i>=k} z_i(Phi_{i+1}-Phi_i)|
 <= B|z_k| + B sum_{i>=k}|z_{i+1}-z_i|
 <= 4B[Q[k]+E[k]].

Inserting into (2) shows D_k<=C_1[Q[k]+E[k]]+e_k=o(D_k), impossible for sufficiently large k. Thus z_k<0 and R_k<0 eventually. The final displayed pole-motion equation then bounds every positive pole increment by |delta_k|. A bounded real sequence with summable positive increments converges: write the positive and negative Jordan variations, and use boundedness to show the latter is finite. QED.

## Geometric quantities intended in the s=3 application

D=H-h; u=free Dirichlet pole; R=its residue; A=bounded homogeneous transport; P=far-band negative action after domination; Q=positive-ghost forcing, comparable to g S^2; Phi=a bounded primitive of the averaged energy coefficient after transport. The global BV polynomial/residue bounds give |R|+|S|<=CD. If the outward pole v has bounded-variation tail O(t_k)+o(1), t_k=xi-v_k->0, and its exact motion is Delta v=kappa S_next with kappa comparable to g, then

 sum_{i>=k}g_i S_i^2
 <=C sup_{i>=k}|S_i| [ Var_tail(v)+sup_tail(g) Var_tail(S) ]
 =o(D_k).

This verifies (3) once the stated comparability and BV bounds hold. It does not verify (1)-(2) uniformly at the other endpoint. In particular entropy proves far/near negative-action dominance only on compact open-edge segments; near the endpoint with another vanishing core weight, P need not remain nonnegative. These hypotheses must not be silently assumed.
