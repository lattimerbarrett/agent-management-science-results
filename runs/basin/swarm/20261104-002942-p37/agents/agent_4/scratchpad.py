from pathlib import Path
s=r'''# Rigorous upper-bound components

## 1. Lexicographic decision trees

Use coordinates [d]. A rooted binary decision tree has at each internal node a nonempty proper set A⊂[d]; its two outgoing edges carry A and A^c. Every leaf x has a sequence of edge labels. Suppose (i) the labels on each root-to-leaf path are pairwise intersecting, and (ii) for every leaf x there is a partition [d]=G_x,1 ⊔ G_x,2 ⊔ G_x,3 such that every path label meets all three parts.

For each i order leaves lexicographically, putting at each node the child whose label contains i later. This is a total order h_i. For leaves x≠y their first separating node shows S(x,y)={i:h_i(x)>h_i(y)} is exactly the edge label used by x there. Hence S(x,y) meets all three G_x,c. For distinct x,y,z, the first branching that separates these three either puts x alone (then its label gives coordinates where x is later than both), or puts x with one other. In the latter case the earlier separating label and x's later separating label intersect; any coordinate in their intersection puts x later than both others. Thus the d orders are 3-suitable: each member of each triple is last in some order. Pair separation follows as well.

One may build a subtree from an intersecting selfdual upset F on a complement-closed subposet D⊆2^[d]. List the complementary pairs of D in any fixed order and encode F by its choices. The full trie of all such encodings has at its tests the corresponding complementary labels. Every label on a leaf's path belongs to F, so the paths are intersecting. If every member of D meets each part of a fixed three-part partition, all paths are rainbow for that partition. Unary trie nodes may be suppressed.

## 2. Absorbing three dimensions of P

Suppose such d orders exist on n vertices. Let P have dimension t≥3 and integer coordinate realization a_1,...,a_t:P→[H], obtained from ranks in t linear extensions. Let c_x(i) be the part containing i in the partition at vertex x. For K>H define

 z_i(p,{x})=K h_i(x)+a_{c_x(i)}(p),
 z_i(p,{x,y})=max(z_i(p,{x}),z_i(p,{y})).

Append coordinates a_4(p),...,a_t(p), obtaining d+t−3 coordinates. These maps are order preserving.

If A⊄B, choose x∈A\B. Pair separation or 3-suitability gives an i with h_i(x)>h_i(y) for all y∈B, so z_i(p,A)>z_i(q,B), independently of p,q.

If A⊆B but p≰q, some a_j(p)>a_j(q). If j≥4 the appended coordinate separates. Otherwise j∈{1,2,3}. For B={x}, choose any i of local color j. For B={x,y}, choose an endpoint x∈A (if A=B either endpoint may be used) and choose i∈S(x,y) of local color j. At this coordinate both edge maxima are determined by x; hence z_i(p,A)>z_i(q,B). Thus this is an order embedding into a product of d+t−3 chains, which implies dimension at most d+t−3. To see the last implication directly, for each coordinate order by its value, breaking ties with any fixed linear extension; these coordinate orders realize the poset.

No 1/2 offset for edges is necessary: the A⊄B argument already separates an edge from either of its incident vertices in the required direction.

## 3. Safe sets and standard large subtrees

Given a partition into three groups, call a set safe if it meets and omits at least one element of each group. Safe sets form a complement-closed poset D. Every selfdual upset on D is intersecting: if A,B in F were disjoint, then A⊆B^c, so upward closure would force B^c∈F, contradicting selfduality.

For d=2r even, take arbitrary choices from each complementary pair of safe r-sets, all safe sets of size>r, and no smaller sets. Every choice is a selfdual upset. This gives 2^N leaves where N is half the number of safe r-sets.

For d=2r+1 odd, let I be any intersecting family of safe r-sets. For each J⊆I choose J at level r, choose precisely the safe (r+1)-sets whose complements are not in J, choose all larger safe sets and no smaller ones. This is a selfdual upset: an obstruction to upward closure would give two disjoint chosen r-sets. It gives 2^|I| leaves. The standard choice I consists of safe r-sets containing a specified coordinate in a smallest group.

## 4. d=8

Use groups of sizes2,3,3. There are18 safe triples,36 safe4sets (18 complementary pairs), and18 safe5sets. Choose arbitrary orientations of the18 middle pairs. A safe triple is eligible iff all its safe4-supersets were selected. Any subset of eligible triples may then be selected, and safe5sets are determined by selfduality. Eligible triples automatically intersect, because otherwise their required middle supersets would include a complementary pair. The exact sum over262144 middle orientations is783558 (checked by agent4_root_doubling.py).

Now put A={0,1,2,5} at the root. On its A-branch use groups {0,1},{2,3,4},{5,6,7}. The root label A meets each group and contains the entire first group, so A meets every internal safe set. On the complementary branch use groups {3,4},{0,2,6},{1,5,7}. Its root label A^c likewise is rainbow and contains the first group. Thus the two subtrees yield1567116 locally rainbow suitable vertices. The separately computed λ(7)=1422564, so this exceeds λ(7)+1.

## 5. d=9

Use groups3,3,3. The81 safe4sets form a graph under disjointness. Let I be the36 containing coordinate0 and J the45 others. I is independent. For each independent T⊆J with |T|≤3, and every U⊆I\N_I(T), T∪U is an intersecting family, all these choices being distinct. Exact enumeration gives contributions

 |T|=0: 68719476736
 |T|=1: 347892350976
 |T|=2: 1019517861888
 |T|=3: 2246100123648

Total3682229813248>D(7)+1=2414682040999, where D(m) is the number of upsets of B_m. Each intersecting family of safe4sets extends uniquely to the safe selfdual upset described above. Since λ(8)≤D(7), this gives more than enough leaves. Both integers are computed from scratch by agent3_D7.py and agent3_d9.py.

## 6. Hansel bound, proved elementarily

Write W_m=binom(m,floor(m/2)). Then D(m)≤3^W_m.

Construct an ordered symmetric chain decomposition recursively. Begin with the one-element chain of B_0. For each old chain C=(c_1,...,c_l), in the old chain order, output first the short chain (c_1,1),...,(c_{l−1},1) if nonempty, and then the long chain (c_1,0),...,(c_l,0),(c_l,1). This partitions the next Boolean lattice into symmetric chains; consequently it has exactly W_m chains.

Inductively every three consecutive members a<b<c of a chain have their alternative Boolean-diamond midpoint z between a and c in an earlier chain. For a triple inherited from an old chain, its alternative midpoint belongs to an earlier parent chain, all of whose derived chains were output first. The only new triple at the end of a long chain has alternative midpoint in its own short chain, output earlier.

After a monotone Boolean function is fixed on earlier chains, its still-undetermined points on the current chain form an interval. If three consecutive points a,b,c were undetermined, their earlier midpoint z is known. If f(z)=0, monotonicity forces f(a)=0; if f(z)=1 it forces f(c)=1. Contradiction. There are at most two undetermined points, hence at most three monotone completions on each chain. Multiplying proves D(m)≤3^W_m. agent4_hansel.py checks the construction through m=12.

## 7. d=10,...,13

Compute D(7)=2414682040998. Since D(m+1) counts ordered comparable pairs in the inclusion poset of the D(m) upsets of B_m,

 D(m+1)≤D(m)(D(m)+1)/2.

Balanced group partitions give standard subtree exponents N_10=90,N_11=164,N_12=396,N_13=690. Applying the above recurrence from D(7) gives D(d−2)<2^N_d in each case (integer arithmetic suffices). Since λ(d−1)≤D(d−2), there are enough vertices.

## 8. Every d≥14

Take balanced groups g_1,g_2,g_3, and for odd d specify a coordinate in a smallest group. Let N_d be the standard subtree exponent in section3 and W=binom(d−2,floor((d−2)/2)). Then N_d≥(8/5)W, as follows.

For d=14,15,16,17,19 exact coefficient extraction gives N=1550,2800,6100,11008,42805 respectively and verifies the inequality.

For even d≥18, the safe fraction of middle sets is at least 1−2Σ_j2^(−g_j)≥29/32. The unrestricted middle-pair count divided by W is2−2/d≥17/9. Their product493/288 exceeds8/5.

For odd d≥21, the unrestricted number of lower-middle sets containing the specified coordinate divided by W is2−4/(d+1)≥20/11. The unsafe fraction is at most

 2^(−(g_1−1)) + Σ_{j=2,3}[(11/20)^g_j+2^(−g_j)]
 ≤1/64+2[(11/20)^7+1/128].

Here missing another group has probability at most[(m+1)/(2m)]^g≤(11/20)^g for d=2m+1,m≥10; containing that group has probability at most2^(−g); containing all of the specified group has probability at most2^(−(g_1−1)). Multiplying the surviving fraction by20/11 exceeds8/5, by rational arithmetic.

Since 2^8>3^5, we have 2^N_d>3^W≥D(d−2)≥λ(d−1). Hence the number of leaves is at least λ(d−1)+1. Coefficients and rational inequalities are checked in agent1_binomial.py.
'''
Path('workspace/agent4_upper_proof.md').write_text(s)
print('wrote',len(s),'characters')
