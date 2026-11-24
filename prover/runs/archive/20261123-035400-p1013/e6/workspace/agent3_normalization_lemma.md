# Coarse cycle normalization via Dirac supergraphs

## Dirac edge-addition lemma
For every gamma>0 there exist positive constants c_gamma,C_gamma and n0 such that if delta(F)>=(1/2+gamma)n, n>=n0, and xy is absent, then
 c_gamma/n <= (c(F+xy)-c(F))/c(F) <= C_gamma/n.

Proof input: h(F)>=n!*exp(-O_gamma(n)), proved in workspace/agent2_dirac_count.md by random logarithmic blocks, regular bipartite factors, van der Waerden permanents, and directed Dirac closing. Agent3 audited all steps of that proof. This avoids any Cuckler--Kahn input.

1. Hamilton path endpoint counts in a graph of minimum degree >=(1/2+gamma)m differ by at most a constant factor. Change one endpoint x to u by the two-cut switching described in agent1 Slack #136. The two arcs cut by the edge following u together supply >=2delta-m-O(1)>=gamma m admissible pivots. Every output has O(m) preimages. Reverse the comparison and change the second endpoint as needed.
2. Write P_ab for unoriented Hamilton paths with endpoints a,b. Since sum_{ab in E}P_ab=m h(F), endpoint comparability implies P_xy=Theta_gamma(h(F)/m) for ALL distinct x,y, adjacent or not.
3. Cycles/paths of length <=(1-gamma/2)n number at most n!/(floor(gamma n/2))! times a polynomial, and hence are negligible compared with h(F)/n^A for every fixed A.
4. Any long cycle omitting a fixed vertex v has Omega_gamma(n) insertion positions for v: number of its edges with both ends adjacent to v is at least 2d_C(v)-|C|. Each resulting cycle has one inverse deletion. Thus cycles omitting x or y are O_gamma(c(F)/n).
5. For every long vertex set S containing x,y, F[S] remains uniformly Dirac. Apply step 2 to F[S], then sum over S. This gives the displayed lemma.

## Eliminating all coarse bad vertices
Suppose a cycle maximizer G has an r-partition, r>=3, with class sizes n/r+o(n), total missing cross-edges M=o(n^2), and maximum internal degree eta*n=o(n). Such a partition should come from ordinary stability plus the color-critical-vertex embedding argument.

Choose tau->0 with eta=o(tau), M/n^2=o(tau^2). Let B be vertices with at least tau*n missing cross-neighbors, b=|B|. Then b<=2M/(tau*n)=o(tau*n). Let G* replace all B vertices by ordinary vertices in their assigned classes: remove every internal edge incident with B; fill every cross-edge incident with B. Good vertices have missing cross-degree <tau*n. If H has a color-critical vertex and the partition is chosen as usual, G* is H-free by greedily replacing every newly added ordinary H-vertex by an unused good vertex of the same class; required same-class edges never involve the new vertices, and each cross-neighbor constraint excludes only o(n) choices.

Let J=G union G*. Both J and G* have minimum degree (1-1/r)n-o(n), so they are uniformly Dirac. The number D of edges in J-G* satisfies
 D<=eta*n*b+b^2=o(tau*n*b).
By the upper Dirac edge-addition bound,
 log(c(J)/c(G*))<=C D/n=o(tau*b).

Each bad vertex has at least (1-o(1))*tau*n missing GOOD cross-neighbors in G. Choose exactly floor(tau*n/2) of these for each bad vertex, obtaining an edge set A subset E(J)-E(G), with |A|=(1+o(1))*tau*n*b/2. Put K=J-A. Then G is a subgraph of K. Moreover K is uniformly Dirac: bad vertices lose only tau*n/2 from degree (1-1/r)n-o(n), and good vertices lose at most b=o(n). Every intermediate graph from K to J remains uniformly Dirac. The lower Dirac edge-addition bound yields
 log(c(J)/c(K))>=c |A|/n >=c' tau*b.
Since c(G)<=c(K), combining gives
 log(c(G*)/c(G))>=c'tau*b-o(tau*b)>0
whenever b>0, a contradiction. Thus the cycle maximizer has maximum missing cross-degree o(n).

No path kernels involving bad endpoints, no bad-cluster expansion, and no asymptotic 1+o(1) endpoint estimates are needed.


## Obtaining the initial stability partition without sharp edge estimates
Let p=(r-1)/r. Since T_r(n) is H-free, a cycle maximizer G satisfies
 log c(G) >= n log(p*n)-n-o(n).
The multipartite Hamilton-cycle local limit estimate suffices for this bound.

The permanent of I+A(G) is at least 1+2c(G): every individual cycle, in either orientation, together with fixed points elsewhere is a permutation counted by the permanent. By Bregman's theorem,
 log per(I+A) <= sum_v log((d(v)+1)!)/(d(v)+1).
For every fixed L, the number k_L of vertices with d(v)<=L is O_L(n/log n). Indeed those rows contribute at most a fixed constant per row, while every other row contributes at most log(n)-1+epsilon_L, with epsilon_L bounded; comparison with the lower bound forces k_L*log n=O_L(n).

Uniform Stirling gives
 log(s!)/s = log s-1+O(log(s+1)/s).
The total error here is o(n): first remove the o(n) bounded-degree rows, then let L tend to infinity. Jensen therefore gives
 log per(I+A) <= n log((2e(G)+n)/n)-n+o(n).
Comparing with c(T_r(n)) yields e(G)>=p*n^2/2-o(n^2).

Ordinary Erdos--Simonovits stability now yields r near-balanced classes with o(n^2) internal edges and missing cross-edges. Remove o(n) bad vertices so that every remaining good vertex has both internal degree o(n) and missing cross-degree o(n), uniformly.

Let h be a color-critical vertex of H and fix an r-coloring of H-h. For every epsilon>0, no vertex v can have at least epsilon*n GOOD neighbors in every one of the r classes, for then greedily embedding each color class of H-h into those good neighbors (avoiding at most |H|*o(n) cross-nonneighbors at each choice) embeds H with h mapped to v. Uniformly, every vertex therefore has o(n) neighbors in some good class. Reassign each bad vertex to such a class. Only o(n) vertices move, so the classes remain balanced and cross-deficit remains o(n^2); every vertex now has internal degree o(n).

This supplies exactly the hypotheses of the supergraph-normalization argument above. No O(n log n) edge deficit or O(log n) exceptional-set bound is required.


## Exact cross-completion once internal components are bounded
Assume now that all internal components have at most K vertices and only finitely many isomorphism types, as supplied by agent2's factor-packing lemma; absorb its O(1) exceptional components into the bound K.

A cycle maximizer is H-saturated, because it is uniformly Dirac and every added edge lies on a new Hamilton cycle. For any internal component type occurring linearly many times, every such component is cross-complete to EVERY vertex. Otherwise add a missing cross-edge xy with x in one such component C. In the resulting H-copy, replace all selected vertices of C by the corresponding vertices in a fresh component of the same type. At most |H|*o(n) components are excluded by the cross-nonneighbors of the other H-vertices, so a fresh suitable component exists; this reproduces H in G, contradiction. Every class has at least one linear-multiplicity type, hence an unbounded supply of vertices cross-complete to all other classes, chosen from distinct components when needed.

For any internal component C, define G_C by deleting its internal edges and filling all its missing cross-edges. This remains H-free: if a new H-copy used a vertex of C, that vertex has no required same-class neighbors, and can be replaced by a fresh reservoir vertex from another component of the same class. Reservoir vertices are cross-complete even to exceptional vertices, so all required edges survive. The union J=G union G_C and G_C are uniformly Dirac. The edge-addition lemma shows
 log(c(J)/c(G)) >= c_gamma*m(C)/n+O(m(C)/n^2),
 log(c(J)/c(G_C)) <= C_gamma*K^2/n+O(1/n^2).
Thus cycle maximality forces m(C)<=D for a fixed constant D (choose D>2C_gamma*K^2/c_gamma). In particular every vertex has at most D missing cross-neighbors.

Repeat the saturation-and-fresh-copy argument. Now a type with more than |H|*D+|H| components is cross-complete to every vertex: only |H|*D vertices, hence at most that many components, can be prohibited by fixed H-vertices. All types with fewer copies together occupy O(1) vertices. Put these in R. Outside R, the graph is an exact complete join of r classes, each a disjoint union of bounded trees; cross-nonedges lie only in R by R. There can be several common tree types in a class.

Finally the upper bound with a<1/r forces H to embed in the complete r-partite graph augmented by matchings in TWO classes. Therefore two distinct classes cannot both contain arbitrarily many nontrivial common components: choose the finitely many required matching edges and extra vertices in distinct components, then fill the other independent classes from reservoirs. Consequently, after increasing R by O(1), at most one normal class contains nontrivial trees.

This proves the required finite-template reduction, but DOES NOT prove edge-priority between different rare templates R. The team has exact examples showing that bounded internal forests alone do not imply that priority. The remaining argument must use the fact that all cells arise from one forbidden H with a color-critical vertex and ex<t_r+n/r.
