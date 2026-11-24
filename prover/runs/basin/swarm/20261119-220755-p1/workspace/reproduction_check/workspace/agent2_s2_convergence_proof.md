# Complete convergence argument for restart s=2

Use the following already proved general lemmas: the monic orthogonal residual polynomials f_j of degree s have norms N_j increasing to L>0; the trajectory closure has uniformly positive definite degree-(s-1) moment Gram matrices; each polynomial parity has finite coefficient total variation and the tail estimate ||f_{2k}-f||+||f_{2k+1}-g|| <= C(L-N_{2k}); and ||y_{j+2}-y_j|| -> 0. The normalized monic map differs from the actual residual map by (-1)^s, so even sequences agree.

After the last coordinate annihilation, use distinct active eigenvalues, all positive spectral weights p_{j,i}. Let K_j=f_j f_{j+1}. The exact identities are
p_{j+2,i}=p_{j,i} K_j(lambda_i)^2/(N_j N_{j+1}),
SUM p_{j,i}(K_j(lambda_i)-N_j)^2 = N_j(N_{j+1}-N_j).
Consequently all omega points of p_even are supported on S={i:f(lambda_i)g(lambda_i)=L}, and |S|<=4. Any active outsider with |f_i g_i|>L is impossible (its two-step weight ratio eventually exceeds 1); strict |f_i g_i|<L gives exponential decay. The only other outsiders have f_i g_i=-L.

Let T be the union of supports of all omega points. The omega set is connected because successive even increments tend to zero. All its points satisfy SUM p=1, SUM p f=SUM p lambda f=0. If |T|<=3 these equations determine a unique p: every omega point has >=3 support nodes (since N>=N0); at a positive 3-node feasible point a dependence a+b f+c lambda f=0 has a=0 by averaging, and then b=c=0 since f is nonzero at every node. Thus convergence follows. If |T|=4, the same rank argument gives an affine line of feasible weights. A non-singleton connected omega set is an interval on this line; because T is the full support union, a relative interior point of that interval has all four weights positive.

## Global exclusion of negative outsiders, with no interior trapping assumption
Write the four nodes in T as lambda_1,...,lambda_4 and P(x)=PROD(x-lambda_i). Then fg=P+L. Fix an active negative outsider mu, so P(mu)=-2L. Let ell_i be the degree-3 Lagrange coefficients at mu. Since K_j is monic quartic,
K_j(mu)=-2L+SUM ell_i K_j(lambda_i), SUM ell_i=1.
Set t_j=L-N_j, R_j=sqrt(N_j N_{j+1}), e_{j,i}=K_j(lambda_i)-R_j. The polynomial TV tail implies |e_{j,i}|<=C t_j, and t_j/2<=L-R_j<=t_j. Define
Psi_j=log p_{j,mu}+SUM ell_i log p_{j,i}.
For even j, its two-step increment is exactly
2 log(2L-R_j-E_j)+2 SUM ell_i log(R_j+e_{j,i})-4 log R_j,
where E_j=SUM ell_i e_{j,i}. Taylor expansion on a fixed neighborhood of L gives
Psi_{j+2}-Psi_j = 2 log((2L-R_j)/R_j)+O(t_j^2) >= c t_j-C t_j^2 >=0
for all sufficiently large j. The linear E_j terms are O(t_j^2), since their coefficient is 2(1/R_j-1/(2L-R_j))=O(t_j). If t_j=0, exact strictness already excludes an active negative outsider. Along the omega subsequence with four positive base weights, Psi_j tends to minus infinity because p_{j,mu}->0, contradicting eventual monotonicity. Thus there are no negative outsiders. All outsiders decay exponentially.

## Reduction to an exponentially perturbed four-node map
Condition the weights on the four nodes T; call them q_j. They obey q_{j+1}=F(q_j)+O(rho^j), where F is the exact four-node restart-2 map and 0<rho<1. All required moment Gram matrices remain uniformly positive definite, even at limiting faces, since each omega support has >=3 nodes. Therefore F, its monic polynomial phi(q), and all functions below are uniformly smooth near the relevant compact closure. Also phi(q_j)-f_j=O(rho^j).

Put d_i=P'(lambda_i), nu(q)=SUM q_i phi(lambda_i)^2. Four-node orthogonality gives the exact dual formula
q_i=nu(q)(lambda_i-theta(q))/(d_i phi(q)(lambda_i)).
Equivalently the interpolant d_i q_i phi_i/nu is the monic linear polynomial x-theta(q). This provides a smooth formula for theta(q), including boundary limits. Because f_i g_i=L>0, phi(q_j) has the same eventual sign for both parities at each of the four nodes; hence theta(q_j) lies in one fixed eigenvalue gap for all sufficiently large j.

For the exact map define delta(q)=theta(Fq)-theta(q). The reciprocal-mean formula yields
 delta(Fq)=a(q) delta(q),
 a(q)=SUM Q_i r_i / SUM Q_i r_i^2,
 Q_i proportional 1/(d_i^2 q_i), r_i=(lambda_i-theta(q))/(lambda_i-theta(Fq)).
This follows by expanding (lambda-theta(q))^2/(lambda-theta(Fq)).
Moreover the polynomial identity
 r_i=nu(Fq)/(phi(q)(lambda_i) phi(Fq)(lambda_i))
shows r_i->1 uniformly at the four nodes, EVEN if theta approaches a node. Thus a(q_j)>0 eventually and a(q_j)->1.

Uniform smoothness of delta(q), together with exponentially small perturbations, now gives for theta_j=theta(q_j), delta_j=theta_{j+1}-theta_j,
 delta_{j+1}=a_j delta_j+O(rho^j), a_j->1, a_j>0.
A scalar lemma completes the proof. Pick eta with rho<eta<1 and eventually a_j>=eta. For D large, either delta_j remains in [-D rho^j,D rho^j] forever (so it is summable), or it leaves this band and its sign can never change again (because each exterior cone is forward invariant). Thus the bounded sequence theta_j converges.

Finally q_{2k,i}=nu(q_{2k})(lambda_i-theta_{2k})/[d_i phi(q_{2k})(lambda_i)] converges, and outsiders vanish. Even residual-coordinate signs stabilize on T because K_j(lambda_i)->L>0; outsider residual components vanish. Hence y_even converges in Euclidean norm.
