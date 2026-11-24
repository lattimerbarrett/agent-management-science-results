# Same-part bounded-degree cycle-comparison lemma (r>=3)

Fix r>=3 and p=(r-1)/r. Let a_i=n/r+O(1). Let X_n,Y_n be complete-cross r-partite templates on these same part sizes, with internal edges only in the first part, all internal maximum degrees bounded independently of n. Write E_X,E_Y for internal edge numbers and W_X,W_Y for sums of binomial(d(v),2). Suppose E_X-E_Y=b is fixed, E_X/n -> alpha, and (W_X-W_Y)/n -> Delta. Then

n(c(Y_n)/c(X_n)-1) -> -2b/p+2Delta/p^2.

Sketch with all essential enumerative identities: For a spanning linear forest F in the internal graph J, let k=|E(F)| and s(F) its number of nontrivial components. Contract F into path blocks; there are 2^s orientations and the remaining cycle uses only cross edges. Thus the exact Hamilton count is
h(X_n)=sum_F 2^s(F) h(K_{a_1-k,a_2,...,a_r}).
Put f_J(k)=sum_{F:|E(F)|=k}2^s(F). For fixed k and bounded internal maximum degree,
f_J(k)=2^k binom(E_J,k)-2^(k-1) W_J binom(E_J-2,k-2)+O(n^(k-2)).
The leading term counts all k-edge sets with independent edge orientations; every selected adjacent pair of edges has actual orientation weight half this value. Edge sets involving two independent wedges, a path of three edges, or a triangle contribute only O(n^(k-2)); these cover all remaining cases. Constants depend on k and the degree bound.

The needed dense-template asymptotic is only the leading fixed-decrement ratio
h(K_{a_1-k,a_2,...,a_r})/h(K_{a_1,...,a_r}) ~ (pn)^(-k).
One way to establish it is the finite-state local central limit theorem for the Markov chain on r colors which moves uniformly to a distinct color. Its nontrivial eigenvalues are -1/(r-1); its occupation covariance on the sum-zero subspace is (r-2)/r^2. Consequently, uniformly for a_i=n/r+O(1),
h(K_{a_1,...,a_r}) ~ ((n-1)!/2) p^n (r/(r-2))^((r-1)/2).
This gives the fixed-decrement ratio immediately.

Subtract the X/Y linear-forest formulas BEFORE taking asymptotics. The binomial leading-term difference from E_X-E_Y=b contributes -2b/p after multiplication by n. The wedge correction contributes 2Delta/p^2. Higher terms vanish. Summing over k gives the common factor exp(2alpha/p), which cancels from the ratio.

All cycles, rather than only Hamilton cycles, are obtained by also selecting omitted vertices. Each omitted vertex contracts a label count without introducing an edge; the leading omitted-vertex sum is exp(1/p). Its first-order interaction with selected edges depends only on E, not W; since E_X-E_Y=O(1), it cannot affect the displayed limit. Thus the same comparison holds for total cycles. Bounded degree gives factorially decaying domination of the finite-decrement sums; the r>=3 assumption is indispensable to the local central limit statement.

Application to the explicit component pair: If X has F-factors and Y has F'-factors plus one half G, then b=1 and Delta=(W(F)/v(F)-W(F')/v(F'))/r. The comparison is positive precisely when this wedge-density gap exceeds r-1. For the component pair constructed by agent_3, the exact gap is 2(k-1)(k-2)^2/(k^2-3k+3), which tends to infinity, while rho=e(F)/v(F)=1+(k-2)/(k^2-3k+3) tends to 1. Parameter arithmetic is checked by workspace/agent4_pair_checks.py.

CAUTION: This lemma compares the indicated templates only. It supplies no global H-free extremal structure or ex(n,H) bound.
