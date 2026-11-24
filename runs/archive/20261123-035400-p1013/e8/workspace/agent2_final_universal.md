# Universal half: final structural and comparison proof block

This block uses the analytic multipartite cycle expansion supplied by agent4,
Erdős--Simonovits stability, and Bregman's permanent inequality. The edge
high-minimum-degree cleaning lemma is proved separately in
agent2_edge_cleaning_lemma.md. The coarse marginal switching lemma is proved
separately in agent2_cycle_marginal_lemma.md (no external counting theorem).

Fix r>=3 and put d=5 for r=3, d=7 for r=4, d=2r for r>=5. Assume
 ex(N,H)<=t_r(N)+a*N+C,  a<d/((d+1)*r).
Let h=|H|.

## 1. Finite tests forced by the assumed edge bound

Every fixed graph sequence with surplus slope greater than a must eventually
contain H. Apply this to the balanced complete r-partite graph with:

(a) a spanning star in one part (slope 1/r);
(b) disjoint copies of any chosen tree on d+1 vertices in one part
    (slope d/((d+1)r));
(c) disjoint copies of any chosen cycle in one part (slope 1/r);
(d) perfect matchings in two parts (slope 1/r).

Restricting an H embedding to its used vertices gives constant-size tests.
In (a) obtain a fixed K_{1,L} whose presence inside one class, with sufficiently
large complete-cross padded classes, forces H. This is the star test used in
both cleaning lemmas.

## 2. Cycle-extremal graphs are close to Turán

For A=A(G), each cycle contributes a permutation to per(I+A), so
 c(G)<=per(I+A)<= product_v ((deg(v)+1)!)^(1/(deg(v)+1)).
Integral factorial bounds and AM--GM give
 log c(G)<= n log(2e(G)/n+O(log n))-n.
The standard multipartite saddle estimate gives
 log c(T_{n,r})=n log((r-1)n/r)-n-O(log n).
Since a cycle maximizer has at least c(T_{n,r}) cycles, it has
 e(G)>=t_r(n)-O(n log n). The assumed H extremal bound and stability therefore
supply an r-partition with parts n/r+o(n) and o(n^2) total internal/missing
cross edges.

Every vertex has o(n) neighbors in SOME part, uniformly: otherwise it has
eta*n neighbors in all parts for a fixed eta>0. All but o(n) bulk vertices
miss at most theta*n cross neighbors, where theta<<eta/h. Select L good
neighbors in any one part as star leaves and greedily embed the star test,
using the center's eta*n neighbor sets in the other parts. Contradiction.
Assign each vertex to a part where it has fewest neighbors. Only o(n)
vertices change their original stability part; hence the resulting partition
still has balanced o(n) offsets and maximum internal degree o(n).

## 3. Cycle cleaning: every cross deficit is O(1)

Fix sufficiently small eps>0 and let B be vertices missing >=eps*n cross
neighbors. The edit-distance bound gives |B|=o(n). Let W fill ALL missing
cross edges incident with B. Its maximum cross deficit is <=eps*n.
Let G' be W with ALL internal edges incident with B removed.

G' is H-free. If H appeared, all its internal edges would be among OLD
vertices outside B. Reroute each used B position to a fresh vertex of the
same part outside B. All fixed old positions and candidate new positions
have <=eps*n cross holes, and there are no required within-part edges at
the rerouted positions. A greedy common-neighborhood choice (eps<1/(10rh))
therefore embeds H already in G.

Apply the coarse marginal lemma uniformly along the following deletions.
Deleting the o(n)|B| internal edges W\G' costs log cycle count o(|B|).
For each b in B choose floor(eps*n/4) originally missing cross edges to
vertices outside B (possible because |B|=o(n)). Delete these edges from W
to obtain W0. Each vertex outside B loses only o(n) such edges, so every
intermediate graph stays uniformly cross-dense. There are Omega(eps*n|B|)
deletions; their lower marginal costs at least c*eps*|B| in log cycle count.
But W0 contains G. Thus c(G')>c(G) unless B is empty. Since eps was arbitrary,
a cycle maximizer has maximum cross deficit o(n).

The star test now forces maximum internal degree D=L-1: any internal L-star
can be extended greedily, as every vertex has o(n) cross holes.
For a vertex u with M missing cross edges, fill them and then delete its
at most D internal edges. The resulting isolated-within-part/full-cross
replacement is H-free: reroute its position in any putative H to a fresh
old vertex in the same part, using cross holes o(n). The coarse marginal
bounds show log cycle gain >=c*M/n-C*D/n. Hence M<=K for a constant K.

At this point parts are n/r+o(n), internal degree bounded, and cross holes
per vertex bounded. Part offsets O(1) will follow below, NOT from this step.

## 4. Canonical finite-component structure

This applies to both cleaned cycle maximizers and high-minimum-degree
edge-saturated graphs. The latter have the same bounded degree/hole properties
by the edge-cleaning lemma (and have O(1) offsets immediately).

With bounded internal degree, choose a sufficiently large constant number of
vertex-disjoint copies of each tree on d+1 vertices. The tree test in section1
embeds H while avoiding all bounded cross holes: each prescribed finite
choice forbids only O(1) copies in a different part. Thus each tree has bounded
packing number in every part. Greedily remove maximal disjoint copies, for
all finitely many tree types. The remaining components have size <=d.
The removed vertex set X has bounded size. Since internal degree is bounded,
original components meeting X contain at most |X|(1+D*d) vertices. Cycle
tests similarly bound the number of cyclic components of order <=d. Hence
all but O(1) internal vertices lie in tree components of order <=d.

The two-matching test shows at most ONE part has an unbounded number of
internal edges. Indeed bounded degree converts unbounded edge count into
unbounded matching number; sufficiently many matching edges in both parts
allow the fixed test embedding, chosen to avoid bounded cross holes.
All other parts therefore have O(1) internal edges.

Collect all exceptional components and all copies of each ordinary tree type
whose number is below M=h(K+1)+h+10 into an exceptional set X, of bounded
size. Every missing cross edge must have BOTH endpoints in X. To see this,
add a missing cross edge incident with an ordinary component. Saturation
produces H. Reroute all H vertices in that component to an unused isomorphic
copy; h fixed vertices exclude at most hK copies through missing cross edges,
and at most h more copies are already used. This gives H before the edge was
added, contradiction. Thus there are only O(1) missing cross edges in total.
Saturation is valid for cycle maximizers because adding any missing cross
edge creates cycles once all cross deficits are bounded and parts large.

Consequently each graph is a complete-cross graph apart from a bounded
exceptional core, with one active class containing arbitrary copies of
finitely many trees of orders <=d; the other classes have only bounded
exceptional internal edges. H-freeness depends only on the finite core and
the numbers of each ordinary component type truncated at h. This follows
because copies are symmetric and completely cross-adjacent outside the core.
There are therefore finitely many regimes.

## 5. Density and edge extremality

In a regime its asymptotic internal-edge slope per ACTIVE vertex is
 rho=(s-1)/s, where s is the largest ordinary tree order allowed arbitrarily
often; or rho=0 if only isolated vertices can occur arbitrarily often.
All smaller-density types cost an edge-density gap, and can be treated as
bounded exceptions in any graph within O(1) of the maximum edge count.
Initially take ONLY regimes obtained from high-minimum-degree saturated
graphs with the FIXED threshold delta(G)>=(1-1/r)n-2. Let rho_* be their
largest regime slope. It exists in a finite set and
 rho_* <=(d-1)/d.
Regimes are independent of part capacities once these exceed fixed constants;
their feasibility is determined by clipped counts. Thus a maximal-slope
regime can be realized with balanced parts and
 e=t_r(n)+rho_* n/r+O(1).

For completeness, the global matching upper bound follows progressive
induction, without assuming edge-extremal minimum degree. If a vertex has
degree <=t_r(n)-t_r(n-1)+rho_*/r, delete it. Otherwise minimum degree is
(1-1/r)n-O(1), with constant independent of the induction additive constant.
Apply edge cleaning, saturate, and use the canonical regime edge bound.
Thus
 ex(n,H)=t_r(n)+rho_* n/r+O(1).
Now every edge-extremal graph has minimum degree >=ex(n)-ex(n-1)
=(1-1/r)n-O(1), so all the canonical conclusions apply to it too.
Now enlarge the finite core/hole constants once to cover both cleaned cycle
graphs and these edge graphs. No newly admitted regime can have slope above
rho_*: balanced padding of that regime would contradict the global edge upper
bound just proved. Thus the largest slope is unchanged. The fixed initial
threshold -2 suffices in the induction since
t_r(n)-t_r(n-1)+rho_*/r >= (1-1/r)n-1.

## 6. Cycle balance and maximum density

Use the uniform moderate-offset analytic estimate (agent4's expansion): for
n_i=n/r+s_i, s_i=o(n), a canonical graph satisfies
 log c(G)=K_n - A*sum(s_i^2)/n + lambda*E(G)/n
          +O(1/n+max|s_i|/n+sum|s_i|^3/n^2),
 A=r/(r-2), lambda=2r/(r-1),
where E is total internal edges minus the bounded number of cross holes.
Always E<=rho_*(n/r+s_active)+O(1). A balanced feasible rho_* regime has
log cycle count >=K_n+lambda*rho_*/r-O(1/n). Comparison and absorption of
the cubic term imply sum s_i^2=O(max|s_i|+1), hence every s_i=O(1).
The bounded-offset leading term then forces rho=rho_* for cycle maximizers.
It also forces their edge deficit from ex(n,H) to be O(1), since all
shape-dependent corrections are O(1/n), whereas each missing edge costs a
fixed positive multiple of 1/n. Thus all lower-density ordinary components
occupy only O(1) vertices.

## 7. One-dimensional discrete comparison

Write n=rq+t, 0<=t<r; active class size m=q+j. Inactive classes may be taken
balanced: their capacities do not affect feasibility, and any unnecessary
cross-edge loss has strictly negative first-order cycle effect. Let L_t(j)
be the loss of crossing edges compared with T_{n,r} when the inactive classes
are balanced. Let E(j) maximize the adjusted number of internal edges minus
cross holes among H-free canonical graphs of active size q+j.

For large capacities, E(j+1)-E(j) is 0 or 1. To increase active capacity,
move an ordinary inactive isolated vertex into the active class, making it
internal-isolated/full-cross. This is H-safe by common-cross-neighborhood
rerouting and does not lose adjusted internal edges. Conversely move an
ordinary active leaf (or isolated vertex) into an inactive class as an
internal-isolated/full-cross position; at most one internal edge is lost.
Choose ordinary vertices outside the exceptional core, so no cross hole is
changed.
Furthermore E(j)=rho_*(q+j)+O(1).

Set rho=rho_*, alpha=(r-2)/(r-1), c=2rho/(r-1). Ignoring a common term,
edge score and the first-order cycle score without shape correction are
 K(j)=E(j)-L_t(j),
 R(j)=alpha*E(j)-L_t(j)+c*j.
One checks directly
 L_t(j+1)-L_t(j)=j-floor((t-j-1)/(r-1)).
For both K and R all maximizers are at j in {0,1,2}. The only relevant losses
are: at j=0 this difference is 1 if t=0 and 0 otherwise; at j=1 it is 2 if
t=0,1 and 1 otherwise. Checking the four 0/1 increment pairs shows that for
rho>=1/2, every NON-edge-optimal candidate has
 R(candidate)-max_{edge-optimal}R <= -1+2rho/(r-1).
A candidate using fewer than E(j) edges loses at least alpha; the same bound
holds because alpha>=1-c exactly when rho>=1/2.
This finite inequality is proved symbolically in agent1_discrete_lemma.py.

If rho=0, E is eventually constant and all bulk vertices are isolated.
Then balanced parts and largest E simultaneously optimize both first-order
scores with a strict gap from any non-edge-optimal candidate. There is no
other rho<1/2, because rho=(s-1)/s for an integer s.

## 8. Shape bound and the strict threshold

Let W(F)=sum_v binom(deg_F(v),2) in the active forest bulk. The full
first-order cycle score is
 R(j)-beta*w, beta=(r-2)/(r-1)^2, w=r*W/n.
All bounded internal/core/cross-hole effects already enter E and do not
contribute to w at this order. For any forest with components of order <=d,
 W <=(d-2)e/2,
because on a component with m edges, at most binom(m,2) edge-pairs meet.
For every forest, W>=max(0,2e-v), by binom(k,2)>=k-1 on positive degrees.
For rho>=1/2 this bounds the difference of w between any edge maximizer
and a cycle competitor by
 (d-2)rho/2-(2rho-1).
Hence the competitor's normalized first-order cycle advantage is at most
 -1+2rho/(r-1)+(r-2)/(r-1)^2*((d-2)rho/2-(2rho-1)).
This is increasing in rho for r>=3,d>=2. Substituting rho<=(d-1)/d gives
 G_r(d)=-1+2(d-1)/(d(r-1))
       +(r-2)(d-2)(d-3)/(2d(r-1)^2).
The exact values are
 G_3(5)=-1/20,
 G_4(7)=-1/9,
 G_r(2r)=-(r-4)/(2r(r-1))<0 for r>=5.
Thus every non-edge-extremal graph has strictly fewer cycles than some
edge-extremal graph for all sufficiently large n. A cycle maximizer therefore
is edge-extremal, proving the universal half.
