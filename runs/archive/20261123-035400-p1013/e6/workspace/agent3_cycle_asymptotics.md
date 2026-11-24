# Multipartite cycle asymptotics used by the boundary construction

Fix r>=3, p=(r-1)/r, and let n_i=n/r+O(1). Let A_cyc(n_1,...,n_r) count color strings at labeled cyclic positions 1,...,n, with no equal consecutive colors (including n and 1), using color i exactly n_i times. Let A_open denote the corresponding linear strings. Then for a constant K_r>0,
 A_cyc = K_r*(r-1)^n*n^(-(r-1)/2)*(1+o(1)),
 A_open/A_cyc -> r/(r-1).
The errors are uniform when the bounded displacements range over any fixed finite set.

Here is a Fourier proof, so no unquoted graph counting theorem is needed. Let M(z)_{ij}=z_j for i!=j and 0 otherwise. The two generating functions are tr M(z)^n and 1^T diag(z) M(z)^(n-1)1. Extract coefficients with z_i=exp(i theta_i), theta_r=0. At theta=0, M has simple eigenvalue r-1 and remaining eigenvalues -1. Its normalized Perron chain is the stationary uniform Markov chain which chooses uniformly a color different from its current color. Every mean-zero function has transition eigenvalue rho=-1/(r-1). Hence its occupation covariance on the sum-zero subspace is
 Sigma=(1/r)*(1+rho)/(1-rho)*I=(r-2)/r^2*I,
which is positive definite for r>=3. Analytic perturbation gives the usual quadratic expansion of the leading eigenvalue; the Gaussian integral supplies K_r. Bounded count displacements affect the integrand only by a phase tending to 1 in the n^(-1/2) saddle neighborhood. Away from theta=0, the spectral radius is strictly below r-1: equality in the triangle inequality would require phases z_j*w_j=omega*w_i for every i!=j; using three distinct colors forces all w_i equal and all z_i equal, so theta_r=0 forces every theta_i=0. Compactness makes the outside integral exponentially negligible. Finally the leading amplitudes at theta=0 are 1 for the trace and r/(r-1) for the open-string generating function. This proves both formulas by the Gaussian saddle calculation.

Since
 h(K_{n_1,...,n_r})=A_cyc*prod_i(n_i!)/(2n),
fixed contractions/deletions give the following ratios. For balanced n_i=m=n/r, and fixed k,
 h(K_{m-k,m,...,m})/h(T_r(n)) ~ [r/((r-1)n)]^k.
For fixed deletions j_i, j=sum j_i, the analogous ratio is [r/((r-1)n)]^j. The same formulas hold for O(1)-imbalanced starting classes.

## Bounded-degree insertions in one class
Let F_n be an internal graph in the first class, maximum degree bounded, with e(F_n)/n -> beta. A Hamilton cycle uses a path forest L of internal edges. Contracting its k edges yields the complete multipartite graph with first class m-k; each nontrivial path has two orientations. Thus exactly
 h(T_r(n)+F_n)=sum_{L path forest in F_n} 2^(number of nontrivial paths of L)*h(K_{m-e(L),m,...,m}).
For fixed k, all but O(n^(k-1)) selected k-edge forests are matchings; their number is e(F_n)^k/k!+O(n^(k-1)). Therefore the k-edge contribution divided by h(T_r(n)) tends to
 [2r*beta/(r-1)]^k/k!.

Domination for ALL k is elementary. Reinsert k labeled ordinary vertices of the first class into a Hamilton cycle of K_{m-k,m,...,m}. At each stage at least n-2m=(r-2)n/r cycle edges have both ends outside the first class, and insertion into each gives a valid distinct Hamilton cycle. Therefore
 h(K_{m-k,m,...,m})/h(T_r(n)) <= [(r-2)n/r]^(-k).
There are at most binom(e(F_n),k) path forests of k edges, and orientation multiplicity is at most 2^k. Hence the k-edge terms are dominated by C^k/k!, for a constant C. Dominated convergence gives
 h(T_r(n)+F_n)/h(T_r(n)) -> exp(2r*beta/(r-1)).
The proof is unchanged for O(1) class-size displacements or deleting O(1) vertices of F_n.

## One universal vertex
Let U_n=K1 join T_r(n-1), and take n divisible by r. Its Hamilton cycles correspond to unoriented Hamilton paths of T_r(n-1), so
 h(U_n)=A_open(m-1,m,...,m)*(m-1)!*(m!)^(r-1)/2.
Using the open/closed color-string ratios above gives
 h(U_n)/h(T_r(n)) -> (r/(r-1))^2=p^(-2).

## Passing from Hamilton cycles to all cycles
For both families above, fixed deletions of j ordinary vertices give
 h(G-S)/h(G) ~ (1/(p*n))^j.
Summing over choices of S gives fixed-j contribution p^(-j)/j!. In U_n the choices including its single universal vertex contribute only O(1/n) at every fixed j.

For domination, these graphs have minimum degree p*n-O(1). For j<=gamma*n, with gamma<(2p-1)/2 fixed, insert any fixed set S of j omitted vertices in a fixed order into a Hamilton cycle of G-S. At each step at least gamma*n edges have both ends adjacent to the inserted vertex, so
 binom(n,j)*max_{|S|=j} h(G-S)/h(G) <= gamma^(-j)/j!.
For larger j the total number of cycles is at most n!/(floor(gamma*n))! times a polynomial, negligible relative to h(G)>=n!*exp(-O(n)). Thus dominated convergence gives
 c(G)/h(G) -> exp(1/p).
The factor is the same for both boundary families. Consequently the two Hamilton-cycle ratios above also hold for total-cycle ratios.
