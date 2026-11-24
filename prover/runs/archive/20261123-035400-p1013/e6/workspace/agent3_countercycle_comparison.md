# Rigorous first-order cycle comparison for the proposed counterphase

Let T=T_r(n), n=rm, r>=3 fixed. Put bounded-degree forests F_n,F'_n inside its first class. Assume
 e(F_n)/n,e(F'_n)/n -> beta>0,
 e(F_n)-e(F'_n)=d (fixed),
 (W(F_n)-W(F'_n))/n -> omega,
where W(F)=sum_v binom(d_F(v),2). Then
 n*(c(T+F'_n)/c(T+F_n)-1) -> -2*alpha*d+2*alpha^2*omega,
 alpha=r/(r-1).
This statement concerns ONLY bounded-degree forests in one class; it does not assert that fewer edges imply more cycles generally.

## Exact path-forest decomposition
For integers k>=1 and 1<=t<=k, let N_{k,t}(F) count k-edge path forests in F with t nontrivial components. Let R_{k,t}(n) count cycles of K_{m-k,m,...,m} containing t specified vertices of the first class. Contracting each chosen path gives
 c(T+F)=c(T)+sum_{k,t} 2^t N_{k,t}(F) R_{k,t}(n)+E_F.
Here E_F counts cycles contracting to a two-vertex double-edge: one internal path plus one outside vertex. Since maximum internal degree is bounded, E_F<=n^3*max(1,Delta)^n=exp(O(n)), negligible relative to c(T)/n^A for every fixed A. (There are no entirely internal cycles because F is a forest.)
For fixed k,t,
 R_{k,t}(n)/c(T) ~ (alpha/n)^k.
Indeed the ordinary complete-multipartite contraction ratio follows from the color-word Fourier calculation in agent3_cycle_asymptotics.md; requiring finitely many specified vertices changes the answer by 1+O(1/n), by the insertion bound for omitted fixed vertices.

For fixed k, bounded-degree overlap counting gives
 N_{k,k}(F)=binom(e,k)-W*binom(e-2,k-2)+O_k(n^(k-2)),
 N_{k,k-1}(F)=W*binom(e-2,k-2)+O_k(n^(k-2)),
and sum_{t<=k-2}N_{k,t}(F)=O_k(n^(k-2)).
A nonmatching choice contains an adjacent edge pair; two or more overlaps have O(n^(k-2)) choices. Thus the k-th contribution to n*(c(T+F')-c(T+F))/c(T) tends to
 2^k*alpha^k * [ -d*beta^(k-1)/(k-1)! + (omega/2)*beta^(k-2)/(k-2)! ],
with the second summand zero for k=1.

## Uniform summation justification (strongest, elementary version)
Discard original cycles shorter than n-L_n, with L_n=floor(n/sqrt(log n)). Their total number in ANY n-vertex graph is at most n!*poly(n)/L_n!, which is o(c(T)/n^A) for every fixed A, since c(T)>=n!*p^n*n^(-C). In the concrete phase all internal double-edge contractions have original length at most 23, so they are discarded too.

Let Q_{k,t}^{long} be the kernel restricted to cycles whose original uncontracted length is at least n-L_n. A compressed cycle has length ell>=n-k-L_n, and uses at most m-k vertices of the first class. Thus it has at least
 ell-2*a_used >= n-2m+k-L_n
edges with both ends outside that class. Insert k fixed fresh ordinary vertices of the first class in a fixed order. Each insertion lowers the number of admissible edges by one, so throughout there are at least n-2m-L_n>=n/4 choices (r=3). The output is a cycle of T, and deleting the fixed fresh labels is a unique inverse. Consequently, for EVERY k,t,
 Q_{k,t}^{long}/c(T) <= (4/n)^k.
For general fixed r>=3 replace 4 by any constant larger than r/(r-2).

The nonmatching k-edge count is at most W*binom(e-2,k-2), by marking an adjacent edge pair. Also
 |binom(e,k)-binom(e-d,k)| <= |d|*binom(max(e,e-d),k-1).
Thus the difference of matching counts in the two forests is bounded by this last expression plus (W+W')*binom(e_max-2,k-2), and the sum of all nonmatching counts has the latter bound. Since e,e',W,W'=O(n), after multiplying by n, the orientation factor <=2^k, and the kernel bound (4/n)^k, the difference terms are dominated by
 C_1^k/((k-1)!)+C_2^k/((k-2)!),
a summable series, UNIFORMLY in n and all k. This is a genuine difference-tail estimate: using individual cycle terms would incorrectly lose a factor n.

For fixed k,t the cutoff changes the kernel only by a negligible amount, so its first-order ratio remains (alpha/n)^k. Dominated convergence therefore justifies summing the fixed-k limits computed above. The resulting sum equals
 exp(2*alpha*beta)*[-2*alpha*d+2*alpha^2*omega].
Finally c(T+F)/c(T)->exp(2*alpha*beta), proving the displayed relative-ratio limit.

## Exact substitution for the candidate phase
Take r=3, n=33q, m=11q,
 F_A=P22 disjoint union (q-2) copies of K1,10,
 F_B=q copies of P11.
Then
 e_A=10q+1, e_B=10q,
 W_A=20+45(q-2)=45q-70, W_B=9q.
Thus beta=10/33, d=1, omega=12/11, alpha=3/2, and
 n*(c(T+F_B)/c(T+F_A)-1) -> -3+(9/2)*(12/11)=21/11>0.
This proves the strict cycle comparison for ALL sufficiently large q, independently of the finite numerical checks.
