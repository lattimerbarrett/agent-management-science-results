# Boundary construction for r>=3

Use the following standard form of Simonovits' decomposition theorem: if chi(H)=r+1 and H embeds in the join of a fixed path and r-1 sufficiently large independent sets, some edge extremizer lies in D(n,r,s), for a fixed s. In D, deleting at most s exceptional vertices leaves r near-balanced classes, each consisting of repeated mutually nonadjacent copies of one connected graph of order at most s, symmetric outside the copies. If the edge extremizer within D is unique up to isomorphism, it is globally unique. The exact theorem statement/reference must be supplied in the final proof.

Let F have vertices a,b,c,d,e,f, edges ad,ae,af,bc,be,bf,cd,ce,de. Equivalently it is a 5-wheel with the spoke ef removed. For L=2r and M=L+1 put H=F joined to r-2 independent M-sets, joined pairwise completely. Then chi(H)=r+1. Every F-v remains nonbipartite: deleting e leaves C5, deleting any cycle vertex leaves a triangle. Thus H has no color-critical vertex.

The six maximal independent sets of F are ab,ac,bd,cf,df,ef. Their complements contain respectively triangle cde, path d-e-b-f, path f-a-e-c, triangle ade, triangle bce, path a-d-c-b. Hence F embeds in the join of a graph J with a sufficiently large independent set iff J contains a triangle or P4. In particular, star forests are forbidden-F-free in this host. The reverse direction here uses the explicit decompositions: outside ab leaves triangle cde plus isolated f; outside bd leaves P4 f-a-e-c.

Also F embeds complete bipartite plus matchings on both sides: parts abc and def have respectively only edges bc and de. Finally F-{e,f} is bipartite and e,f are nonadjacent.

## D uniqueness
For an extremizer in D, each normal connected block must be a star: any triangle or P4 embeds H using independent reservoirs in the other normal classes. At most one normal class has nontrivial blocks, by the two-matching embedding. Suppose that class has blocks of order k>=2. Its normal internal edge contribution is at most (1-1/k)n/r+O(1). If an exceptional vertex sees a positive fraction of the active class and sees all other normal classes, it creates P4 with two star blocks, embedding H; thus every exceptional vertex has weighted normal degree at most (r-1)n/r+O(1). Consequently e(G)<=t_r(n)+(1-1/k)n/r+O(1), contradicting the H-free graph U_n=K1 join T_r(n-1), which has t_r(n)+n/r+O(1) edges.

Thus all normal blocks are singletons. Every exceptional vertex sees all or none of each normal class. At most one sees every class: two such vertices embed H by putting e,f there and using the bipartition of F-{e,f} plus the r-2 join classes. All other exception vertices see at most r-1 normal classes. To attain the lower bound from U_n, exactly one universal-type exception u exists and every other exception misses exactly one class. Assign each ordinary exception to its missing class.

Within the resulting r classes, all edges involve boundedly many ordinary exceptions, and each internal graph is a star forest (otherwise P4/triangle). If an internal edge xy has either endpoint adjacent to u, it gives a P4 together with u and a fresh normal vertex of its class (or a triangle), again embedding H. Hence u is nonadjacent to every vertex incident to an internal edge. Let B be its set of ordinary nonneighbors. Then total internal edges <=|B|-1 whenever any exists; in all cases internal edges-|B|<=0, equality only if both are empty. All missing cross-edges cause further loss. Therefore
 e(G)<=t_r(n-1)+(n-1),
with equality only for U_n. This proves unique D extremizer, hence globally unique extremizer by the quoted theorem. In particular ex(n,H)=t_r(n)+ceil(n/r)-1<=t_r(n)+n/r.

## Competing cycles
For n divisible by rL, take balanced r classes and put disjoint L-vertex stars in the first class, leaving all other classes independent; call this V_n. It is H-free. Indeed if an M-vertex join class of H has no vertex in a pure host class, it spans at least two distinct star components. Every other H-vertex, adjacent to all its M vertices, must then avoid the modified class; but H minus that join class has chromatic number r and cannot fit r-1 pure classes. Thus all r-2 join classes use distinct pure classes, leaving F at most one pure class, impossible by the six independent-set checks.

The standard multipartite local-limit/path-forest expansion gives, for r>=3, with p=(r-1)/r,
 c(U_n)/c(T_r(n)) -> p^(-2),
 c(V_n)/c(T_r(n)) -> exp(2(1-1/L)/(r-1)).
For clarity, contraction of k fixed disjoint internal edges multiplies Hamilton-cycle counts asymptotically by [2r/((r-1)n)]^k; bounded-degree forests yield a Poisson sum with mean 2r e(F_n)/((r-1)n). Adjacent internal edge selections are lower-order. Open color-word counts give p^(-2) for U_n. Passing from Hamilton cycles to all cycles multiplies both by exp(1/p), since deleting j vertices contributes asymptotically p^(-j)/j!.

For s=r-1,
 1-s log(1+1/s) = s int_0^(1/s) t/(1+t) dt > 1/[2(s+1)] = 1/L.
So the second limiting ratio is strictly larger. Therefore V_n eventually has more cycles than the unique edge extremizer U_n, for infinitely many n. This establishes a=1/r and all larger a.

The executed checker workspace/agent3_boundary.py verifies every finite F claim and the star path polynomial, and computes exact positive cycle gaps at r=3,n=108,144,180 using the separately brute-force-verified join formula.
