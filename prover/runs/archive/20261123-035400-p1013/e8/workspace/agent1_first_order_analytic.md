# First-order analytic lemma: proof skeleton with explicit coefficient reduction
Let r>=3, A=J-I, and x=(x_i). Set q(x)=1-sum_i x_i/(1+x_i).
The exact exponential generating function for all cycles in complete multipartite
hosts, with unused vertices allowed, is
 e^(sum x_i) [-1/2 log det(I-diag(x)A) -1/4 tr((diag(x)A)^2)].
For a host of part sizes n_i, multiply coefficient [x^n] by product n_i!.
The determinant is product(1+x_i) q(x). For n_i all linear in n, the
single-variable logarithms and length-two subtraction make no contribution.
Write S=sum_{i<r} x_i/(1+x_i), phi=(1-S)/S. Then q=S(phi-x_r)/(1+x_r).
Extracting x_r first reduces the problem to an ordinary (r-1)-dimensional
analytic Laplace integral with amplitude
 (1/(2 n_r)) exp(sum_{i<r} x_i+phi) (1+phi/n_r+O(n_r^-2))
and phase -sum_{i<r} n_i log x_i -n_r log phi.
Indeed sum_{j=0}^{n_r-1} phi^j/(j!(n_r-j))
 = exp(phi)/n_r [1+phi/n_r+(phi^2+phi)/n_r^2+O(n_r^-3)].
All errors are uniform for x near the positive critical point.

Critical point: write y_i=x_i/(1+x_i), p_i=n_i/n. Then
 sum_i y_i=1, p_i=y_i(1-y_i)/(1-sum_j y_j^2).
At balance p_i=y_i=1/r, x_i=1/(r-1). On zero-sum tangent directions,
 dy_i=(r-1)/(r-2) dp_i, d log x_i=r^2/(r-2) dp_i.
The Hessian of the logarithmic coefficient INCLUDING the label factorials is
 d^2 F = -2r/(r-2) sum_i dp_i^2.
The critical point is strictly minimal, nondegenerate, and aperiodic for r>=3.
Consequently the standard multivariable Laplace theorem gives a full expansion,
uniform for p in a fixed neighborhood of balance; coefficients are analytic in p.
In particular, if s_i=n_i-n/r=o(n),
 log C(parts)=log K_n-r/(r-2)n sum_i s_i^2
              +O(sum_i |s_i|^3/n^2)+O(1/n)+O(sum_i s_i^2/n^2),
where K_n is the analytic balanced continuation (sum s_i=0).

Adding bounded-degree internal graphs is handled by path contraction. For a fixed
linear forest with t internal edges and p nontrivial path components, contract its
paths, multiply by 2^p, and require the resulting distinguished vertices to occur
in the cross-only cycle. Bounded degree makes the total number of selected
internal edges have a uniformly exponentially decreasing tail after normalization,
so termwise expansions can be summed. A fixed edge in part i has leading weight
 alpha_i(p)/n, alpha_i(p)=2x_i(p)/p_i.
At balance alpha_i=2r/(r-1), and
 d log alpha_i=2r/(r-2) dp_i.
For e=Theta(n), W=sum_v binom(d_internal(v),2), the first shape-dependent term is
 -2r^2 W/((r-1)^2 n^2).
Proof: the t-matchings number
 e^t/t! - (e+2W)e^(t-2)/(2(t-2)!)+O(n^(t-2));
one-wedge-plus-(t-2)-edge linear forests number
 W e^(t-2)/(t-2)!+O(n^(t-2)), and their orientation factor is half the matching one.
Summing gives -lambda^2 W/(2e^2), lambda=2r e/((r-1)n).
All other first-order terms depend only on e/n (and r), not the component shape.
A bounded number q of cross nonedges contributes -[2r/(r-1)]q/n+O(n^-2)
by inclusion-exclusion and the same cross-edge coefficient.

Thus, for bounded s_i and total adjusted internal surplus E=e_internal-q,
with active-part size m=n/r+s and E=rho*m+delta, there is L_n(rho) independent
of the internal shapes, s_i, delta, and q, such that
 log c(G)=L_n(rho)+(2r/((r-2)n))*Q+o(1/n),
 Q=-1/2 sum_i s_i^2 + r*rho*s/(r-1)+(r-2)*delta/(r-1)
       -(r-2)/(r-1)^2 * W/m.
The statement is uniform over bounded-degree internal graphs and bounded exceptional
cores. The moderate-deviation version has leading internal term
 sum_i alpha_i(p)e_i/n+O(1/n), with uniform error, enough to force bounded offsets
once finite regimes give E<=rho_max*m+O(1).
