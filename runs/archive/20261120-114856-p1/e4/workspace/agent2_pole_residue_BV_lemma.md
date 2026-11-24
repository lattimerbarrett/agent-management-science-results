# Bounded variation of persistent Dirichlet residues (full 2s core)

Assume the global limiting core S has 2s nodes, F=qr=P_S+H. Write q_k M_k=a_k P+t_k on the full retained spectrum; a_k is monic degree s-1, t_k has degree n-s-1 and leading coefficient h_k. Let zeta_j,k be the s-1 persistent roots of t_k, one in each interband gap, and eta_j,k the correspondingly matching roots of a_k. Put R_j,k=zeta_j,k-eta_j,k. All other roots xi of t_k converge to off-core spectral nodes beta with weights summable; indeed xi_k-beta=O(w_k,beta), uniformly, because setting w_beta=0 makes t_k divisible by z-beta and the limiting root is simple. Thus the xi sequences have bounded variation.

All persistent a/t roots stay separated from each other and from the xi. The auxiliary identity is
 a t'-a't=q_k B,
where B has leading coefficient K=h_{k+1}-h_k and B/K is a compression characteristic polynomial. Its roots lie in the spectral interval, hence |B|+|B'|<=C K on the fixed interval containing all roots.

At zeta_j, this identity gives |R_j Delta zeta_j|<=C K. Comparing its evaluations at zeta_j and zeta_j' gives
 R_j'=C_j R_j+O(K),
 C_j=(h'/h)(q_k(zeta_j')/q_k(zeta_j))
      *[prod_{l!=j}(zeta_j-eta_l)/prod_{l!=j}(zeta_j'-eta_l')]
      *[prod_{other t roots v'}(zeta_j-v')/prod_{other t roots v}(zeta_j'-v)].
These coefficients tend uniformly to 1 and are positive. Evaluation of q_next M_next=a'P+t' at zeta_j' gives
 Delta zeta_j=c_j R_j', 0<=c_j<=C.
Therefore |Delta zeta_j|^2<=C K. In particular all persistent pole increments are square summable.

We now prove sum_j |Delta R_j|<=C K+C sum_external |Delta xi|, eventually. Take logarithms of C_j, multiply by R_j, and use R_j'=C_j R_j+O(K). The h'/h term costs O(K). The q evaluation term is O(|R_j Delta zeta_j|)=O(K), since it evaluates the SAME polynomial q_k at two nearby arguments. Each external-root factor costs O(|R_j Delta zeta_j|+|Delta xi|), also acceptable.

For a pair of persistent poles l!=j, substitute eta_l=zeta_l-R_l. Its four-factor logarithm splits as
 T0=log|zeta_j-zeta_l|+log|zeta_j-zeta_l'|
    -log|zeta_j'-zeta_l'|-log|zeta_j'-zeta_l|,
plus H_l-H_l', where H_l=log|1+R_l/(zeta_j-zeta_l)|. The exact bound |T0|<=C|Delta zeta_j| has NO Delta zeta_l term. Also
 |Delta H_l|<=C|Delta R_l|+C|R_l|(|Delta zeta_j|+|Delta zeta_l|),
after increasing C and absorbing higher terms for sufficiently late indices. Multiplication by |R_j| turns the first term into o(1)|Delta R_l|. Both remaining products are O(K): use |R_j Delta zeta_j|<=C K and |R_l Delta zeta_l|<=C K. Summing over j and absorbing the o(1) sum_l |Delta R_l| term yields the claimed bound. Hence every R_j has bounded variation.

This proof does not by itself prove pole convergence: sin(log k)/k has bounded variation and can still integrate to an oscillatory position. Its main additional use is that once all but one poles have bounded variation, the remaining scalar homogeneous connection can be controlled by one-dimensional discrete line-integral estimates.
