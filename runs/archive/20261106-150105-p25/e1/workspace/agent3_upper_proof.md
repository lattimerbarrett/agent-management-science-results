# Complete upper-bound module

Let c>1/5. Pick integer m>=3 with (5m-8)c>m-1.
Saturate G by adding edges while keeping it C3,C5-free. Minimum degree does not decrease. In the saturated graph every nonedge has a walk of length 2 or 4: adding a missing edge must create a triangle or pentagon. Write F for the odd-third-power graph: distinct vertices adjacent when joined by a walk of length 1 or 3. No odd closed walk of length <=5 exists. Consequently every neighborhood N_G(x) is independent in F.

## Ladder obstruction

Suppose a_0,...,a_{m-1}, b_0,...,b_{m-1} form a halfgraph, i.e. a_i b_j is an edge iff i<j, and every diagonal nonedge has an existing three-walk. A common neighbor on a diagonal would form an odd closed five-walk, so saturation supplies a four-path a_i-p_i-q_i-r_i-b_i. These paths may overlap: no disjointness assumption is required.

Take abstract T_m with disjoint blocks (a_i,p_i,q_i,r_i,b_i), each a P5, and all edges a_i b_j for i<j. There is a homomorphism T_m -> G. Put U={a_0,b_{m-1}} union all five vertices in each interior block i=1,...,m-2.

Every set independent in T_m's odd-third-power contains at most m-1 vertices of U. Indeed within each interior block the guaranteed edges are ap,pq,qr,rb,ar,pb,ab, so independent sets have size at most two, and the only doubles are {a,q},{p,r},{q,b}. For i<j the following cross edges are guaranteed (row earlier block, column later block):

 a -> p,q,b; p -> a,r; q -> b; r -> b; b -> a,r.

Every pair of doubles in two different blocks conflicts. Hence at most one double occurs, giving (m-2)+1. If a_0 is included, only a_i,r_i remain in each interior block, and they conflict; if b_{m-1} is included only p_i,b_i remain, and they conflict. The two endpoints themselves conflict. This proves the claim.

For each x in G, the preimage of N_G(x) under T_m -> G is odd-third-power-independent: any forbidden edge would give an odd closed walk of length 3 or 5 in G. Therefore

 (5m-8)cn <= sum_{u in U} deg_G(phi(u)) <= (m-1)n,

a contradiction. This argument allows repeated path images and repeated phi(u).

## VC bound

If the neighborhood set system shatters m+2 vertices s_0,...,s_{m+1}, choose prefix witnesses t_j with N(t_j) intersect S={s_0,...,s_{j-1}}, j=1,...,m+1. The shattered vertices are independent because a witness adjacent to all gives common neighbors and G is triangle-free. All nonempty-prefix witnesses lie outside S, and distinct prefixes have distinct witnesses.

Take a_i=s_{i+1}, b_i=t_{i+1}, i=0,...,m-1. Then a_i b_j iff i<j. The sentinel s_0 and t_{m+1} give a_i-t_{m+1}-s_0-b_i, a three-walk on every diagonal. This yields the forbidden ladder. Thus VC dimension <m+2.

## Bounded domination

Let d=m+1. Choose t>=8/c with 2(2t+1)^d 2^{-ct/2}<1. The standard double-sampling epsilon-net argument gives a t-element multiset meeting every neighborhood of size >=cn. Here are the details. Let S,T be independent t-samples from the uniform vertex distribution. If S misses a neighborhood R, then with conditional probability >=1/2, |T intersect R|>=ct/2 (Chebyshev, since t>=8/c). On the combined 2t-sample the number of distinct traces is <=sum_{i=0}^d binomial(2t,i) <=(2t+1)^d by Sauer's lemma. Conditional on the combined sample, random equal splitting puts a fixed trace with >=ct/2 sample positions wholly in T with probability <=2^{-ct/2}. Union bound proves failure probability <=2(2t+1)^d 2^{-ct/2}<1. Thus a dominating set D of size at most t exists.

Color each vertex by one of its neighbors in D. Vertices with the same color lie in one neighborhood and are independent in F. Thus chi(F)<=t.

## Universal triangle-free target

W_t has vertices (i,A), i in [t], A subset [t] not containing i (empty A allowed). Two vertices (i,A),(j,B) are adjacent iff i in B, j in A, and A intersect B empty. A triangle would have the third vertex's first coordinate in the intersection of the first two second-coordinates, impossible. Given a proper coloring q of F, map v -> (q(v), {q(w):w in N(v)}). For an edge uv the membership conditions hold. If the second-coordinate sets intersect, choose neighbors x of u and y of v with equal q-color; x-u-v-y is an odd-three-walk, contradicting proper q (x=y would give a triangle). Hence the map is a homomorphism. The target depends only on c.

All finite independence-certificate assertions and symbolic walk witnesses are checked in agent3_ladder_certificate.py. The universal-target reduction is exhaustively checked on all labeled C3,C5-free graphs with <=6 vertices and all proper three-colorings of their odd-third-power, in agent3_oddpower.py.


## Two elementary auxiliary facts (to avoid external theorem dependencies)

**Odd-walk fact.** Any closed odd walk of length at most five contains a triangle or pentagon: take a shortest odd closed subwalk. Any repeated internal vertex splits it into two closed walks, one odd and shorter. Thus the shortest is an odd cycle, necessarily of length three or five in a simple graph.

**Sauer bound.** If a family of subsets of an r-element set has VC dimension at most d, it has at most sum_{i=0}^d binomial(r,i) members. Induct on r. Strip the last element and let U be the union of the two resulting subfamilies, I their intersection. Then |family|=|U|+|I|, VC(U)<=d, and VC(I)<=d-1: otherwise a d-set shattered by I, together with the stripped element, is shattered by the original family. Apply induction and Pascal's identity. The base cases r=0 or d=0 are immediate. Finally sum_{i=0}^d binomial(r,i)<=(r+1)^d, by encoding an increasing subset of size at most d as a d-tuple padded with zeros, for d>=1; the d=0 case is one.
