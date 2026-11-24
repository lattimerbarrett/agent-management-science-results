# An explicit Bregman near-extremal-edge reduction

For every n>=2 put L=3(log(n+1)+1). For 1<=k<=n,
  (k!)^(1/k) <= (k+L)/e.
Indeed log(k!) <= k log k-k+log k+1 by integral comparison.
If k<=L/(e-1), then (k+L)/e>=k>=(k!)^(1/k).
Otherwise k log(1+L/k)>=Lk/(k+L)>L/e>log(n)+1>=log(k)+1.

For adjacency matrix A of G, every unoriented simple cycle gives TWO
permutations contributing to per(A+I), all other vertices being fixed.
Therefore 2c(G)+1 <= per(A+I). Bregman's theorem and AM-GM imply
  2c(G)+1 <= product_v [(d(v)+1+L)/e]
            <= [(2e(G)/n+1+L)/e]^n.
This explicit version does not require a concavity assertion about factorial
roots or a minimum-degree assumption.

For fixed r>=2, the standard exact multipartite color-word count (or its
local central limit estimate) gives
  c(T_{n,r}) >= n! ((r-1)/r)^n / n^K
for some fixed K=K(r), along the appropriate parity classes for r=2.
Consequently if c(G)>=c(T_{n,r}), the displayed Bregman bound gives
  e(G)>=t_r(n)-O_r(n log n).
Combining with Erdos-Simonovits stability, for H-free G with chi(H)=r+1,
any cycle extremizer is o(n^2)-close to a balanced complete r-partite graph.

This only proves the initial approximate-structure reduction; it does not
assert the exact bounded-template result needed later.
