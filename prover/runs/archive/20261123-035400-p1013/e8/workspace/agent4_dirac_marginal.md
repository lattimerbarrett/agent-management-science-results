# Dirac-margin edge-marginal lemma
Claim: For every gamma>0 there are positive c,C,N such that if |V(F)|=n>=N and delta(F)>=(1/2+gamma)n, then for every edge uv,
 c/n <= c_uv(F)/c(F) <= C/n,
where c_uv is the number of cycles containing uv. Constants depend only on gamma.

## 1. Short cycles are negligible
For every fixed epsilon>0 a Dirac-margin graph contains at least n^{(1-epsilon)n} simple cycles of length n-O(1), for sufficiently large n. Here is a classical-permanent proof, included to avoid needing an unproved Hamilton-count theorem.
Turn each undirected edge into both arcs. Fix depth k with2^-k<epsilon/2, and delete O(2^k) vertices to make n divisible by2^k. Every directed graph with minimum indegree and outdegree at least(1/2+eta)N has a partition A,B of equal sizes such that every vertex has at least(1/2+eta/2)|A| incoming and outgoing neighbors in each part: use a uniformly random balanced partition and Chernoff/hypergeometric concentration plus union bound. Between A and B, oriented from A to B, the resulting bipartite graph has minimum degree at least(1/2+eta/2)|A|. Such a balanced bipartite graph contains a spanning floor(eta|A|/2)-regular subgraph (max-flow/min-cut). Van der Waerden's permanent theorem then gives at least(c_eta N)^{N/2} perfect matchings A->B.
For each such matching, contract each matched pair(a_i,b_i) to a vertex and put arc i->j iff b_i->a_j was an arc. The resulting directed graph has minimum in/out degree at least(1/2+eta/2)N/2. Each directed Hamilton cycle in the contracted graph lifts to one in the original graph, and distinct matchings give disjoint families (the lifted cycle uniquely determines all its A->B edges). Repeat k times; at the final level use the directed Dirac theorem (minimum semidegree>N/2 implies Hamiltonicity). We obtain at least
 product_{j=0}^{k-1}(c_j n/2^j)^{n/2^{j+1}}=n^{(1-2^-k)n}exp(-O(n))
cycles of length n-O(1).
Thus, taking epsilon=gamma/2, the total number of cycles of length less than(1-gamma)n, at most n^{(1-gamma)n+1}, is exponentially negligible relative to c(F).

## 2. Missing endpoints are negligible among long cycles
Let C have length ell>=(1-gamma)n and omit vertex u. At least
 2|N(u) intersect V(C)|-ell >=2delta(F)-2(n-ell)-ell >=gamma n
edges of C have both endpoints adjacent to u. Insert u into any such edge. Each resulting cycle containing u has a unique inverse deletion of u. Consequently the number of long cycles omitting u is O(c(F)/n), with the same statement for v. Almost all cycles are long and contain u,v.

## 3. Two-switch upper bound
Fix a long cycle containing uv. Delete uv to obtain a spanning path on its vertex set. There are at least
 2delta(F)-2(n-ell)-ell-O(1)>=gamma n-O(1)
consecutive pairs a,b on that path for which swapping edges uv,ab to ua,vb (with the appropriate path orientation) gives a cycle not containing uv. Every target cycle has at most4 inverse two-switches because its neighbors of u,v determine the cut. Thus the number of long cycles containing uv is O(c(F)/n). Add the negligible short cycles.

## 4. Three-switch lower bound
Fix a long cycle containing u,v but not uv. Choose one orientation and write successor a of u and successor b of v. Delete ua,vb and add uv: this forms a path P from a to b on the same vertex set. At least gamma n-O(1) consecutive pairs c,d of P have bc,ad in E(F). Deleting cd and adding bc,ad closes one cycle containing uv (choose the orientation of c,d consistent with closing a SINGLE cycle). Each target cycle has at most O(n^2) inverse switches: choose a,b, and then all removed/added edges are determined up to a constant number of possibilities. Double counting therefore gives c_uv >=(c_gamma/n) times the number of long cycles containing u,v. Part2 makes this asymptotic to c(F).

This establishes the claim. The proof uses only standard classical facts: concentration for random balanced partitions, regular-factor max-flow criterion, van der Waerden's permanent theorem, and directed Dirac/Ghouila-Houri Hamiltonicity.

## Cycle-cleaning application outline
In a near-T_r H-free graph with H embedding T_r+K1,L, all vertices can be assigned to parts of internal degree o(n): if a vertex has linear neighborhoods in every part then it extends the star realization of H using the good bulk. Most vertices retain their stability-partition class.
Fix sufficiently small epsilon>0. Let B be the o(n) vertices with cross-deficit at least epsilon n. Replace all vertices of B by internal-isolated vertices complete across. This preserves H-freeness: any H using the replacement vertices can reroute them, one by one, to fresh old good vertices in their assigned parts, since every fixed old image outside B has at most epsilon n missing cross-neighbors. All required edges from replacement vertices are cross-edges. Let F=G plus every missing cross-edge incident to B, and R the internal edges incident to B. Then G'=F-R is this H-free replacement, and |R|=o(n)|B|.
Choose M among the added cross-edges with |M|>=epsilon n|B|/2 and maximum missing degree at most epsilon n+o(n): select floor(epsilon n) missing cross-edges at each bad vertex; all nonbad vertices receive at most|B| edges. Let J=F-M, so G subset J. Every graph between F-R and F-M has Dirac margin for r>=3 and small epsilon, because the other cross-deficits are at most epsilon n and all internal degrees o(n). Applying the edge-marginal lemma along an edge-by-edge path gives
 log c(J)-log c(G') <= C|R|/n-c|M|/n<0.
Contradiction to cycle maximality. This proves every cross-deficit is o(n), hence minimum degree=(1-1/r)n-o(n).
Then every internal K1,L extends to H greedily, so internal degree<=L-1. Repeat with B defined by cross-deficit at least a sufficiently large constant K: now |R|<= (L-1)|B| and choose |M|>=K|B|/2; sufficiently large K makes the same argument work. H-freeness of the replacement remains valid because all fixed old vertices have O(K) missing cross-neighbors. This yields part sizes n/r+O(1) and O(1) missing cross-degree.

WARNING: the last assertion about part sizes needs an independent step: minimum degree bound after fine cleaning plus bounded internal degree implies n_i=n/r+O(1). Before fine cleaning n_i=n/r+o(n), which suffices for Dirac margin and greedy embedding.
