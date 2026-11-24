# Constant Turan excess obstruction (r >= 3)

Theorem. Fix r>=3 and H with chi(H)=r+1. If ex(n,H)<=t_r(n)+C eventually, then every cycle-maximizing H-free n-vertex graph is edge-maximizing for all sufficiently large n.

Use the structural lemmas in agent3_structural_lemmas.md and the endpoint-count lemma in agent2_path_lemma.md, with the moderate-deviation exponential tilt correction in Slack #81 and analytic q=0 correction in #83.

Put p=(r-1)/r. Three consequences of the endpoint-count calculation, uniformly for complete r-partite cores of order m whose sizes are m/r+O(sqrt(m log m)), are needed:

(E1) If k<=K log m added vertices each have between alpha*m and beta*m core neighbors, alpha>0 fixed, then their cycle count (allowing all mutual edges) divided by that for k added ordinary clones is at most (1+o(1))*product_i(d_i/(pm))^2. This remains true after O(1) core-edge edits. To see this, first count cycles using all k new vertices, no mutual edge, and distinct core neighbors. Their count is a common endpoint-path-system factor times product_i d_i(d_i-1), with relative error o(1) uniform by the path lemma. Colliding endpoint choices are O(k^2/m). Selecting j mutual edges joins j endpoint pairs and lowers the pole order by j; their sum costs O(k^2/m). Omitting j added vertices similarly costs O((K'/m)^j)*binom(k,j); hence costs O(k/m) total. Allowing omitted core vertices multiplies the path EGF by exp(sum x_i), a smooth analytic factor at the common saddle. All errors remain o(1) for k=O(log m).

(E2) Write delta_i=n_i-n/r and s=n mod r, and S_s=s(r-s)/r. For bounded delta and any fixed finite edge-edit template with q internal-minus-missing-cross edges,
  c(template)/c(T_nr)=1+[B*q-A*(sum delta_i^2-S_s)]/n+O(n^-2),
where A=r/(r-2)>0 and B=2r/(r-1)>0. The error is uniform over finitely many templates. The exact unedited cycle EGF is
  product n_i! [x^n] exp(sum x_i)*(-1/2 log Q(x)-1/2 sum_{i<j}x_i*x_j),
  Q=det(I-diag(x)*(J-I))=1-sum_{j=2}^r(j-1)e_j(x).
The log-pole renewal calculation gives the expansion. The occupation covariance of the uniform no-repeat color chain, on the zero-sum subspace, is (r-2)/r^2. Its Gaussian exponent is -r^2 sum(delta_i^2)/(2(r-2)n). Stirling for product n_i! contributes +r sum(delta_i^2)/(2n), leaving -A sum(delta_i^2)/n. Symmetry eliminates all linear displacement terms; smooth prefactors change only by O(n^-2) for bounded displacements. One fixed-edge edit has marginal B/n, by the one-path formula, independent of endpoint colors. Intersections of two prescribed edge events are O(n^-2), so edits add at first order. The ratio with T_nr removes the common expansion terms and replaces sum delta_i^2 with sum delta_i^2-S_s.

(E3) Uniformly when max|delta_i|=O(sqrt(n log n)),
  log[c(K_n1,...,nr)/c(T_nr)]
   =-A*(sum delta_i^2-S_s)/n+O(n^-1+sum|delta_i|^3/n^2).
Also O(1) inserted edges increase cycles by a factor 1+O(n^-1). Thus if a bounded-edit template has at least c(T_nr) cycles, its displacement is bounded. Indeed, if the squared displacement tends to infinity, both error terms are little-o of its negative main term. E3 is the same uniform saddle expansion used in E2, before restricting displacement to bounded size.

Proof of theorem.

A cycle maximizer G has at least c(T_nr) cycles. Bregman's inequality applied to I+A_G, concavity of log(k!)/k, and Stirling imply
  log c(G) <= n log(2e(G)/n+1)-n+O(log n),
when the average degree is bounded below linearly. If it is not, the weaker row-sum/Jensen bound first establishes a positive linear lower bound, after which the displayed estimate applies. Meanwhile the color-word local limit calculation gives
  log c(T_nr)=n log(pn)-n+O(log n).
Consequently e(G)>=t_r(n)-O(n log n).

Fix epsilon small enough for the high-minimum-degree structural lemma, with epsilon<p/4. Repeatedly delete a vertex of degree below (p-epsilon) times the current order. If F(m)=t_r(m)-e(G_m), one deletion decreases F by at least epsilon*m-O(1). Every remaining graph is H-free, so F(m)>=-C. Since initially F(n)=O(n log n), the process stops after k=O(log n) deletions, while m=n-k. The remaining graph G_m satisfies the high-minimum-degree hypothesis.

Complete G_m by the completion lemma to an H-free bounded-edit complete multipartite graph K. Since e(G_m)>=t_r(m)-O(n log n), and only boundedly many internal edges occur, the core class sizes are m/r+O(sqrt(n log n)). Each deleted vertex has at most (p-epsilon)n+O(log n) neighbors in the core. For an upper counting bound, pad its core neighborhood to a size between (p-2epsilon)n and (p-epsilon/2)n and allow every mutual edge among deleted vertices. Let E be this enlarged graph. Then G is a subgraph of E. Instead add k ordinary clones to K to obtain an H-free graph F of order n. E1 gives, if k>=1,
  c(G)/c(F)<=c(E)/c(F)
     <=(1+o(1))*(1-epsilon/(3p))^(2k)<1,
contradicting maximality. Thus no deletion occurred: every cycle-maximizer satisfies the structural high-minimum-degree hypothesis.

Its completion cannot add any missing edge: minimum degree is greater than n/2, so every added edge creates a triangle, strictly increasing the number of cycles. Therefore G itself is an exact bounded-edit complete r-partite template, with all edits supported on a set of bounded size S. H-freeness of the template depends only on the graph on S and class labels, once every ordinary twin class has at least |H| vertices. There are finitely many such templates. The rough edge lower bound yields deviations O(sqrt(n log n)); E3 and c(G)>=c(T_nr) improve these to bounded deviations.

Let Qmax be the maximum integer q (internal edges minus missing cross edges) among these finitely many eventual H-free templates. Include the pure r-partite template so Qmax>=0. Any such template can be realized on balanced class sizes, independently of n once n is large, by the cloning/remapping argument. Hence a balanced template with q=Qmax is H-free and has t_r(n)+Qmax edges. All edge-extremal graphs satisfy high minimum degree (degree >= t_r(n)-t_r(n-1)-C), and hence are among the same finite templates. Thus ex(n,H)=t_r(n)+Qmax eventually.

For a cycle-maximizer, E2 gives coefficient
  B*q-A*(sum delta_i^2-S_s).
Here q<=Qmax and sum delta_i^2>=S_s, with equality exactly for balanced integer class sizes. The balanced q=Qmax template has strictly larger first-order coefficient unless both q=Qmax and the class sizes are balanced. The coefficient gap is bounded below by a positive constant, since q and the squared-displacement gap range over a finite set and are integral in the relevant edge units. The O(n^-2) error cannot reverse the comparison. Thus every cycle-maximizer has exactly t_r(n)+Qmax=ex(n,H) edges for all sufficiently large n.

In particular 0 is not in S_r for r>=3, contradicting the requested answer. No claim about the complete correct set S_r or the exceptional periodic bipartite case r=2 is made here.
