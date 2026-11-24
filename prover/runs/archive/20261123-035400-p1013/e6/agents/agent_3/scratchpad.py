from pathlib import Path
p=Path('workspace/agent3_countercycle_comparison.md');s=p.read_text()
a=s.index('## Uniform summation justification');b=s.index('## Exact substitution')
s=s[:a]+r'''## Uniform summation justification (strongest, elementary version)
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

'''+s[b:]
p.write_text(s);print('updated',len(s))
