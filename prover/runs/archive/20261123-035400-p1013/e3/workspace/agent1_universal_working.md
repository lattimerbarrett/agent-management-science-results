# Universal cycle reduction for r>=3: working proof

Assume chi(H)=r+1 and ex(n,H)<=t_r(n)+a*n+O(1), a<1/r.

1. Test hosts show H embeds K1 join T_{m,r}, and the join of
r-1 large independent classes with arbitrarily many copies of ANY fixed tree
T for which (v(T)-1)/(r*v(T))>a. In particular it embeds a long-path decorator.

2. Cycle stability: 2c(G)<=per(A+I). Bregman plus Jensen gives
log c(G)<=n log(2e(G)/n+epsilon*n)-n+o(n), for every fixed epsilon>0.
Comparison with c(T_{n,r}) gives e(G)>=t_r(n)-o(n^2). Standard forbidden-
subgraph stability gives a near-Turan partition.

3. Assign every exceptional vertex to a class where it has o(n) neighbors.
If it had epsilon*n neighbors into each good core class, embed H by its
K1 join T_{m,r} coloring, using the vertex as special apex and choosing
neighbors greedily from these sets (cross defects in core are o(n)).
Thus after assignment every internal degree is o(n), and all except o(n)
vertices have cross defect o(n).

4. CLEANING SWITCH LEMMA. Let B be vertices with cross defect>=epsilon*n,
and replace them by independent class clones, adding every missing cross
edge and removing every internal edge incident B. Let d be the maximum
number of removed internal neighbors, M the minimum number of added cross
neighbors per vertex of B. Here d=o(n), |B|=o(n), M>=epsilon*n.
The resulting graph G' is H-free: any H using new clone vertices can be
relocated greedily to distinct old core vertices in the same classes.
Each fixed vertex not replaced has cross defect<epsilon*n; choose
h(H)*epsilon<1/(2*r).

To compare cycles, fix theta with 2/r<theta<1. A destroyed cycle of
length>=theta*n has k removed edges, k<=2|B|. Repair the k edges in all k!
orders. For removed edge v-u, v in B, choose a new neighbor w of v,
avoiding O(k+|B|) protected vertices. If w is outside the cycle, first
insert w in a canonical core edge whose endpoints avoid part(w).
Now write cyclic order v-u ... w-x ... v. An auxiliary oriented core edge
a-b after w gives replacement edges v-w,u-a,x-b; an edge before w gives
v-w,u-b,x-a. Both produce ONE cycle (verify by tracing the three cut arcs).
If u has class i and x has class j, the number of auxiliary positions
excluded by class constraints is at most n_i+n_j+O(1), not twice that:
inside each of the two segments only one incidence of each i-vertex and
one incidence of each j-vertex is forbidden. Hence there are
(theta-2/r-o(1))*n valid positions. Missing adjacencies at u,x exclude
o(n) further positions if the endpoint is core; a replaced endpoint has
all new cross edges. Protect old gained edges, losing O(k) positions.
Every step offers at least c*M*n choices, and creates between 1 and 5
newly added edges, removing no gained edge of an earlier step.

Reverse a step by choosing one of at most 5k gained edges v-w, a removed
neighbor u of v (<=d choices), and O(n) further data to recover the cut
positions and orientations. Thus for D_k destroyed long cycles and C_l
created long cycles,
 D_k <= R^(-k) sum_{l=k}^{5k} C_l,
where R=M/(C_r*d), after using (5k)^k<= (5e)^k k!.
Sum k, obtaining sum D_k <= (R-1)^(-1) sum C_l. For large n, R>=3.

There are many independently constructed new cycles through any added
edge: use only clean core vertices and one clone, a fixed proper balanced
color word, and greedily select (1-eta)*n vertices, leaving eta*n unused.
For epsilon small relative to eta, each step has >=c_eta*n choices, and
closure is enforced by choosing the final color suitably. Thus at least
(c_eta*n)^((1-eta)*n) created cycles. Take eta<1-theta. All cycles shorter
than theta*n are at most n^(theta*n+O(1)), negligible. Therefore G' has
strictly more cycles. Contradiction. Consequently max cross defect=o(n).

5. Now internal Delta is bounded: H embeds Tr with a fixed star in one
part (use its critical vertex). Any such internal star embeds the rest
of H using common cross neighborhoods, since every chosen vertex has
only o(n) missing cross neighbors. Apply the same cleaning lemma with
B={v}, d<=D_H, and M>C_r*D_H, giving a constant bound on every cross
defect. This establishes a bounded-degree perturbation of a complete
multipartite graph.

6. REMAINING ANALYTIC DETAIL: show part imbalances are bounded by cloning
a vertex from a larger part into a smaller part. Need uniform local
saddle-point comparison for bounded-degree perturbations at n_i/n near
1/r, giving cycle gain proportional to (n_i-n_j)/n plus O_H(1/n).
Once this is supplied, all part sizes are n/r+O_H(1).

7. H embeds a long-path decorator, so bounded internal Delta implies
bounded internal component orders: any sufficiently large bounded-degree
component contains enough disjoint long paths to embed the required
internal forest, then use common cross fillers.

Let R0 bound component order and D0 bound cross defect. A type with
more than h(H)*(D0+1)*R0 copies can be relocated away from any prescribed
H-sized set of vertices and nonneighbors. Thus any missing cross edge
whose endpoint components have abundant types could be filled safely;
a new H could have its endpoint components relocated to clean copies.
All remaining missing cross edges touch one of O_H(1) rare vertices,
therefore there are O_H(1) missing cross edges in total.

This gives a finite collection of exceptional gadgets plus arbitrarily
many bounded components. H-freeness depends only on component counts
clipped at h(H), so arbitrary replication of abundant components is safe.

8. FINITE PACKING DETAIL: show a cycle maximizer uses, outside a bounded
exception, only trees of a common maximum order q in a SINGLE active
part; counts of smaller components bounded. Non-tree abundance yields
slope>=1/r; two active parts yield slope>=1/r from two matchings. For
forests, larger component order means larger e/v. Repacking inferior
components as maximal q-trees increases edges linearly in their number
and cycles by the first-order contraction expansion. This must be made
quantitative for unbounded-but-o(n) inferior component counts.

9. Within each profile e_int(m)=m-ceil((m-v)/q)+K. Exact finite score bound
for losing one total edge is
Delta(r,q)=-2r/(r-2)+4r*(q-1)/(q*(r-1)*(r-2))
             +r*(q-2)*(q-3)/((r-1)^2*q).
This is negative for q<6 when r=3, q<8 when r=4, and q<=2r when r>=5.
The bound comes from best imbalance advantage
 r/((r-1)*(r-2))*(4*(q-1)/q-2)
and maximum wedge advantage between star and path.
A proof that the residue optimization is bounded by this closed formula,
not merely finite tests, is still needed.

CAUTION: steps 6,8,9 are specified gaps, not established theorems here.
The detailed double-counting in step 4 should receive independent audit.


## Updates closing specified architecture gaps (independent audit still needed)

Step 6: agent3_clone_lemma.md gives the analytic uniform saddle-point
local-clone comparison. It uses bounded-degree inclusion-exclusion for
missing cross edges and path contractions for internal edges. For p near
uniform the cumulant error is O(1/n), uniformly in the perturbation.
One clone changes all correction parameters by O(1/n). The multipartite
entropy Hessian on sum-zero vectors is -2r/(r-2), giving the desired
strict gain whenever max part size minus min part size exceeds a fixed
constant.

Step 8 local repacking: retain R copies of each abundant type. If a
tree T of order t<q has at least R+q copies, replace q copies of T by
t copies of an abundant q-tree. The number of affected vertices is qt,
a fixed constant; the edge gain is q-t>=1. The finite-profile condition
is unchanged, so the replacement is H-free. The contraction expansion
gives a log-cycle gain 2r(q-t)/((r-1)n)+O_H(n^-2)>0. Hence smaller types
have bounded multiplicity, with no unbounded-o(n) uniformity argument.

Step 9 exact residue argument: put n=rk+j, 0<=j<r. For each branch
f(m)=m-ceil((m-v)/q)+K, internal increments are 0 or 1. The baseline
active part has m=k if j=0, m=k+1 otherwise. A cycle optimizer in that
branch can only use this baseline or baseline+1; the latter is possible
only when j=0 or j>=2, and only when the next internal increment is 1.
Indeed, if active m is already at least max other part+1, the score
increment for another increase is <=A-4B+C*alpha<0, with
A=2r/(r-1), B=r/(r-2), C=4r/((r-1)(r-2)), alpha=(q-1)/q.
If active m is smaller than all other classes, increasing it improves.
For j>=1, the move floor(n/r) to ceil(n/r) preserves Q and gains the
positive cross term C*alpha, so choose the ceiling, which is also
edge-optimal. The optional baseline+1 move loses one cross edge and
gains one internal edge, hence is edge-tied; its cycle score advantage
is r/((r-1)*(r-2))*(4*alpha-2). If its internal increment is zero, its
cycle score strictly decreases. Therefore cycle-optimal part sizes
within every branch are edge-optimal, and the normalized branch-score
range over all packing residues is at most that optional-shift gain.
Combined with the star/path wedge range, an edge deficit of 1 gives
the upper bound Delta(r,q). Larger edge deficits are even worse.

Exact Python audit: agent1_threshold_verify.py symbolically verifies
Delta identities and derivative, and exhaustively checks 356180
candidate rows for r=3..10, q=2..2r+1, all n mod r and packing phases.
It confirms the stated range bound and common single-branch argmax.

The remaining gap for the WHOLE PROBLEM is not these r>=3 steps but the
universal r=2 theorem. Generic finite matching profiles do NOT suffice:
there are hereditary abstract q=2 classes with disjoint edge/cycle
optimizers. A single chi=3 forbidden graph imposes additional nontrivial
profile closure. All simple recombination conjectures tried so far have
explicit counterexamples. Matching-cut uncrossing (intersection/union
of matching cuts are P3 forests) is verified, but has not yet yielded
the required directed/weighted closure theorem.
