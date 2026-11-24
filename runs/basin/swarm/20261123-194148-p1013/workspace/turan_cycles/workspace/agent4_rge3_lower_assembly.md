# Assembly of the r>=3 lower bound

## Theorem
Fix r>=3. Put
 P_r(k)=(r-2)k^2+(-2r^2+3r+4)k+2r-8.
Suppose chi(H)=r+1 and ex(n,H)<=t_r(n)+a*n+O(1), with a<1/r. Define k to be the largest order of a tree T for which a complete balanced r-partite graph with arbitrarily many disjoint copies of T in one part is H-free. Then k is finite, (k-1)/(kr)<=a, and if k=1 or P_r(k)<0, every sufficiently large n has an H-free graph maximizing both edges and cycles.

Together with the sharp constructions, this excludes all a<5/18 for r=3, a<7/32 for r=4, and a<2/(2r+1) for r>=5.

### 1. Two decompositions forced by a<1/r
The graph K_1 join T_{n-1,r} has t_r(n)+n/r+O(1) edges. Thus for some fixed large n it contains H; deleting the vertex mapped to the universal vertex leaves an r-colorable graph. Hence H has a chromatic-critical vertex. A proper r-coloring of H-v, with v placed in one color class, gives a one-part star decomposition K_{1,mu}.
Likewise T_{n,r} with a spanning path inside one part has t_r(n)+n/r+O(1) edges, so contains H for some fixed n. Its used internal edges form a fixed linear forest F. These are exactly the two decompositions needed below.

### 2. Both edge and cycle extremizers have finite-hole component structure
For cycles use Bregman's inequality and the elementary Turan cycle lower bound to get e(G)>=t_r(n)-o(n^2); ordinary Erdos-Simonovits stability gives an r-partition and a regular core with o(n) exceptions. The complete cycle regularization is proved in `agent3_rotation_transfer_lemma.md`. Its final output is global cross-delta-regularity for any sufficiently small fixed delta>0.

The SAME entry argument applies to EDGE extremizers without any rotation counting. In its notation, simultaneously replace the true bad set X by pure assigned vertices. Each unique-sparse vertex gains at least delta*n opposite-part edges and loses O_H(1)+o(n) internal edges. Each two-sparse vertex gains at least (1/r-eta)n crossedges and loses at most eta*n+o(n) internal edges. Double counting among X changes only O(|X|^2)=o(n)|X| edges. Thus the simultaneous operation strictly increases edges if X is nonempty. It is H-safe by exactly the final pure-vertex remapping argument of that lemma. Therefore all vertices of an edge extremizer are cross-delta-regular too.

Now apply `agent4_finite_hole_template_lemma.md` to cycle extremizers. It gives internal degree Q, component order K, maximum crosshole degree M, and holes only among boundedly many rare components. For EDGE extremizers the identical proof is simpler: purifying one entire internal component is H-safe and gains at least d-KQ edges if a vertex has d holes, so max hole degree is bounded; then the same abundance-remapping fills all holes incident with abundant types. Thus BOTH kinds of extremizers have:
* n_i=n/r+o(n);
* internal components of bounded order;
* only O_H(1) rare vertices, all holes among these;
* complete crossedges whenever one endpoint belongs to an abundant component.
This uses no Simonovits edge-decomposition theorem, only ordinary stability.

### 3. Admissible components; one active part and a largest tree
Any collection of abundant component types occurring together is freely repeatable in a complete r-partite host, with no rare context. Indeed an H-copy in such a host could be remapped component by component into distinct old abundant copies; at most h=|H| copies of any type are needed, and all old crossedges between abundant components exist. This would contradict H-freeness of the original graph.

An abundant connected cyclic component has e/v>=1, and would give an H-free construction of surplus n/r-O(1), impossible. Thus all abundant components are trees. If two parts have nontrivial abundant trees, each contributes density at least 1/2, again giving surplus at least n/r-O(1). Hence only one part is active.

Any admissible tree has maximum degree <mu and contains no f-vertex path, where f=|F|. These bounds give finite maximum order K, as in the post-entry lemma. Hence k in the theorem exists (k=1 is allowed). The pure k-tree construction gives (k-1)/(kr)<=a.

An EDGE extremizer must use a largest admissible k-tree abundantly: otherwise its surplus has strictly smaller linear coefficient than the pure k-tree construction. A CYCLE extremizer also must have active order k: the leading cycle factor of a j-tree bulk is exp(2(j-1)/(j(r-1))), while part imbalance only decreases the leading factor; finite rare gadgets have no leading effect. This statement follows directly from the uniform estimate in section 5 below. For k=1 all nontrivial components are rare.

### 4. All smaller bulk components can be absorbed into bounded context
Let T be an abundant maximum-order tree in an extremizer's active part, of order k. New copies of T or its subtrees can be inserted in place of any bounded collection of smaller abundant components H-safely: every H-copy using a new component remaps it into unused old copies of T. Modified vertices are outside the rare set, so their crossedges were already complete.

If there are k smaller components, their orders have a nonempty subset of at most k terms summing to a multiple of k (prefix sums modulo k). Replace that subset by full T copies. Since each old component has order <k, this increases edges by at least one and changes only O(k^2) vertices. It contradicts edge extremality; it also contradicts cycle extremality, since a fixed net internal-edge gain +1 changes the cycle count by factor 1+2/(qn)+o(1/n), whereas finite shape changes enter only at order n^-2. This finite perturbation assertion follows by the same path-contraction argument as the cycle expansion, uniformly when part deviations are o(n).

Consequently there are fewer than k small abundant components; absorb all of them into the bounded rare context R. Every other nontrivial active component has exactly k vertices. Choose one occurring k-tree T and replace all the others by T if desired: the operation is H-safe and edge preserving. For a cycle comparison choose T with minimum wedge count among the available k-types, so this replacement cannot decrease the first-order cycle score.

### 5. Uniform coarse imbalance estimate
Let q=(r-1)/r, delta_i=n_i-n/r, Q=sum delta_i^2, and M be the number of internal edges (holes are bounded). For bounded internal degree, bounded component order, n_i=n/r+o(n), and O(1) holes,
 log(c(G)/c(T_{n,r}))
 =2M/(qn)-[r/(r-2)]Q/n
  +O_H((1+||delta||)/n+||delta||^3/n^2).
The same estimate with a one-sided error suffices.

Derivation: the proper-color cyclic-word matrix has analytic Perron eigenvalue near the all-ones saddle. On the zero-sum color-count subspace the asymptotic occupation covariance is (r-2)/r^2 times identity. The analytic saddle moves with p_i=n_i/n. Uniform saddle integration gives a smooth amplitude and a rate function J(p), with
 J(p)=r/(r-2)*sum(p_i-1/r)^2+O(||p-p_0||^3).
(The occupation-rate Hessian is r^2/(r-2); multiplying by vertex-label factorials subtracts r, giving 2r/(r-2).) The amplitude changes by O(||delta||/n), and the uniform local error is O(1/n). Contracting j internal path edges multiplies by (qn)^(-j)*exp(O(j||delta||/n+j^2/n)); summing against its Poisson factorial majorant gives exp(2M/(qn)+O((1+||delta||)/n)). Omitted vertices have a factorial tail and contribute a smooth amplitude; fixed holes contribute O(1/n). This is the coarse version of `agent2_tree_cycle_expansion.md`; the full Fourier/saddle justification is proved in `agent3_uniform_imbalance_lemma.md` and independently in `agent2_uniform_imbalance_lemma.md`.

Fix the bounded context and the allowed abundant k-tree T. Rebalance all parts while keeping the context, and fill the active part by T copies and one subtree. This phase remains H-free by abundance remapping. Its internal edge count differs by O(1+||delta||), while its part deviations are O(1). Comparing this valid graph with a cycle extremizer in the displayed estimate gives
 Q<=C(1+||delta||)+o(Q),
 because ||delta||^3/n=o(Q). Hence ||delta||=O_H(1). For edge extremizers the same conclusion follows immediately from edges: the crossedge loss is Q/2 and internal-edge gain is at most O(1+||delta||).

### 6. Finite phases and the sharp comparison
With all deviations bounded, all rare contexts have bounded order, so there are finitely many phase descriptions. For each fixed context R and allowed k-tree T, put u=number of its active-part vertices. For active order a the maximal net internal-edge contribution is exactly
 m_u(a)=a-ceil((a-u)/k)+d,
 where d is an integer absorbing fixed context edges, holes and u. All inactive part sizes are as equal as possible in phase optimizers; balancing them changes neither the fixed context nor internal edges.

Let rho=(k-1)/k, L=r/((r-1)(r-2)), B=2r/(r-1)^2, and omega=w(T)/k. The first-order cycle score, up to phase-independent terms, is
 S=(2/q)E-LQ+4L*rho*delta_active-B*omega,
 where E is the actual total edge contribution (including holes). For mixtures use their average omega. Finite contexts influence only E at this order.

The exact lattice lemma `agent2_phase_bound_proof.md` shows:
(i) in a given phase a cycle-score optimum is edge optimal; every non-edge-optimal member loses a fixed positive score;
(ii) between phase edge optima whose edge counts differ by at least one, the maximum possible score advantage of the lower-edge phase is
 A(r,k)=-2/q+2L(2rho-1)+B*(k-2)(k-3)/(2k).
The wedge interval used here is the universal path-to-star interval for k-vertex trees, so no principal-tree-ideal hypothesis is made.

If a cycle extremizer were not edge optimal in its own phase, (i), choosing a minimum-wedge available T, would give an H-free phase member with a strictly larger first-order cycle score. If its phase edge optimum were smaller than ex(n,H), compare with a global edge extremizer phase. By (ii) the score difference is <=A(r,k), which is strictly negative exactly when P_r(k)<0. Uniform O(n^-2) errors cannot cancel this fixed negative coefficient divided by n. Hence the supposed cycle extremizer must itself be edge extremal. For k=1 the internal contribution is constant in all part sizes, both phase objectives select balanced parts, and the score is simply (2/q)E; the same conclusion follows.

### 7. Arithmetic thresholds
For r=3, P_3(k)=k^2-5k-2, negative through k=5 and positive at k=6.
For r=4, P_4(k)=2k(k-8), negative through k=7 and zero at k=8.
For r>=5, P_r(2r)=-2(r-1)(r-4)<0 and P_r(2r+1)=6(r-1)>0; convexity and P_r(2)=-4(r-1)(r-2)<0 show negativity throughout 2<=k<=2r.
Since (k-1)/(kr)<=a, the stated excluded intervals follow.

## Status
All structural and analytic steps above now refer to proved team lemmas, with no false normality or unique-tree closure assumption. The coarse uniform saddle estimate in section 5 has full independent Fourier proofs in `agent3_uniform_imbalance_lemma.md` and `agent2_uniform_imbalance_lemma.md`, audited by agent4 (Slack #473); the joint-tail bound is recorded in Slack #471. Thus the r>=3 lower pipeline is complete subject to final integration/audit by the lead. The r=2 case is deliberately not addressed here and is resolved separately by the H17 witness.
