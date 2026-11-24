# Elementary exponential-scale cycle lower bound for balanced Turan graphs

Fix r>=3 and q=(r-1)/r. We prove

 c(T_{n,r}) >= n! q^n exp(-O_r(n^(2/3) log n)).

This is enough for Bregman plus stability; no local central limit theorem is needed.

Let h=ceil(n^(2/3)), m=n-2rh and D=n-m. For large n, m>=3. Choose a uniformly random proper LINEAR r-color word of length m, starting with a uniform color and at each step choosing uniformly among the r-1 different colors. This is a stationary Markov chain with its nontrivial eigenvalue lambda=-1/(r-1). If N_a counts a specified color, then

 Var(N_a)=p(1-p)[m+2 sum_{d=1}^{m-1}(m-d)lambda^d]
 <= m p(1-p)(1+2/(r-2))=O_r(m), p=1/r.

Chebyshev and the union bound show every N_a lies within h of m/r with probability 1-O_r(n^(-1/3)). Such counts are less than floor(n/r) for large n. Also the probability the last and first colors differ is exactly q(1-lambda^(m-1)), bounded below by a positive constant. Therefore at least c_r r(r-1)^(m-1) proper linear words have all these count bounds AND give proper cyclic words on closing the last-first edge. Among their at most (m+1)^r count vectors choose one (N_1,...,N_r) occurring at least c'_r(r-1)^m/(m+1)^r times.

Let n_i be the balanced host part sizes. Every word with these counts can be labeled in product_i (n_i)_{N_i} ways. Put d_i=n_i-N_i>=0; sum d_i=D. Then

 product_i(n_i)_{N_i} = product_i n_i! / product_i d_i!
 >= n!/(r^n D!),

because n!/product n_i!<=r^n and D!/product d_i!>=1. Dividing by 2m orientations/roots of each cycle gives

 c(T_{n,r}) >= c'_r (r-1)^m n! / [2m(m+1)^r r^n D!]
 = n! q^n exp(-O_r(D log D + D + log n)).

Since D=O_r(n^(2/3)), this proves the claim. For r=2 use the direct alternating cycles on 2 floor(n/2) vertices; their count is (floor(n/2)!)^2/(2 floor(n/2)), giving the same exponential-scale assertion with a polynomial loss.

For every graph G, Bregman's permanent inequality applied to I+A_G gives

 2c(G)+1 <= [ (2e(G)/n+O(log n))/e ]^n.

Combining with the cycle lower bound and Stirling, a graph with c(G)>=c(T_{n,r}) satisfies 2e(G)/n >= qn-o(n), hence e(G)>=t_r(n)-o(n^2). The genuine Erdos-Simonovits stability theorem now gives an r-partition with balanced sizes and o(n^2) internal/cross-error edits. This is the only coarse entry hypothesis needed by the Posa replacement lemma.

Actual exact checks in workspace/agent3_turan_coarse_cycle_lower_checks.py verify the covariance/variance formula by enumerating every proper word for r3,m2..8 and r4,m2..6; the uniform variance bound is checked with exact fractions for r3..8,m1..100. All assertions PASS.
