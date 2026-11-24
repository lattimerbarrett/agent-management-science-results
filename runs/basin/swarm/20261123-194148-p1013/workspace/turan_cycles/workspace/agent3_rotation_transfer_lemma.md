# A self-contained coarse vertex-replacement lemma for r>=3

This supplies the analytic entry step of agent4's cycle-template regularization. It does NOT assert the later finite-hole/component reduction or the r=2 case.

## Hypotheses and statement
Fix r>=3, a positive zeta, and a positive delta. There are positive epsilon,gamma,tau,kappa depending only on r,zeta,delta with the following property for all sufficiently large n. Partition V into r parts of sizes n/r+o(n). A set B of o(n) exceptional vertices is designated; all other vertices are regular. Assume:

* every regular vertex misses at most epsilon*n vertices in OTHER parts among regular vertices;
* regular-to-regular edges within the parts have maximum degree at most a fixed Q;
* EVERY vertex has at least zeta*n regular neighbors;
* c(G)>=n!*C^(-n)/n^C for a fixed C.

Let x belong to B, in assigned part A. Put S=N_G(x) intersect A, P=N_G(x) outside A, D=(V outside A) minus N_G(x), with s=|S|, d=|D|. If d>=delta*n and s<=kappa*d, then replacing x by a pure vertex of A (delete xS, add xD) STRICTLY increases the total number of cycles. Constants are uniform as B=o(n), and the assumptions remain valid while other exceptional vertices are successively made pure.

## Typical cycles
Choose fixed small gamma,tau>0. A cycle is initially typical if its length is at least (1-gamma)n and it uses at most tau*n/2 edges whose endpoints are in the same assigned part. The total number of atypical cycles is exp(-Omega(n log n))*n!*C^(-n), hence is o(c(G)). Indeed, short cycles have at most n^((1-gamma)n+1) descriptions. A cycle uses at most 2|B| edges incident with B. If it has tau*n same-part steps, at least tau*n/2 are regular-regular same-part steps for large n. At each specified such step there are at most Q choices for the next vertex instead of n. Summing over step-position choices gives the crude upper bound

 n^n * 2^n * (Q/n)^(tau*n/2-1),

which is exp(-Omega(n log n)) times the stated factorial lower scale. We may ignore exponentially negligible additive errors below. Every bounded sequence of rotations changes the number of same-part steps by O(1), so all resulting paths have at most tau*n same-part steps for large n.

The factorial lower scale holds for the balanced Turan graph: fix ONE proper cyclic part word with the balanced part multiplicities (such a word exists since the largest part is <=n/2), and permute vertices within the part positions. This gives at least product_i(n_i!)/(2n)>=n!/(2n*r^n) Hamilton cycles. Thus the hypothesis is available for every cycle-maximizer and after cycle-increasing or edge-adding steps.

## Two Posa rotations change one REGULAR endpoint
Write an oriented simple path as p_0=u,...,p_i=w,...,p_j=z,...,p_{ell-1}=v. A Posa rotation at p_j deletes p_j p_{j+1} and adds u p_{j+1}, reversing the initial segment; it changes endpoint u to z, and keeps endpoint v fixed.

Apply the rotation at z and then at w. If j>i, the two added edges are

 u p_{j+1},   z p_{i-1}.

If j<i, they are

 u p_{j+1},   z p_{i+1}.

The new path starts at w and ends at v. These identities and their unique inverse sequence (rotate at z, then at u) are exact; exceptional coincident/adjacent positions exclude only O(1) choices.

Suppose u,w and BOTH neighbors of w along the current path are regular. The first added edge can fail its cross-part condition for at most |part(u)| choices of z, plus epsilon*n crossholes. For z BEFORE w, the second condition excludes the vertices in part(p_{i+1}) in that prefix; for z AFTER w it excludes the vertices in part(p_{i-1}) in that suffix. On any path segment of L vertices, if a particular part occurs h times and there are b consecutive steps within that part, then 2h<=L+b+1. Thus the two prefix/suffix exclusions together account for at most ell/2+tau*n/2+O(1) positions. The second added edge also has at most epsilon*n missing-edge exceptions, because the neighbor of w is regular. Excluding B and O(1) special positions, the number of valid pivots z is at least

 ell/2 - n/r - (tau/2+2epsilon)n - o(n)
 >= (1/2-1/r-gamma/2-tau/2-2epsilon-o(1))*n.

Choose gamma,tau,epsilon small. Since r>=3, this is at least c_r*n for a fixed c_r>0. This is the only place r>=3 is essential.

## Clean up an ARBITRARY endpoint first
For a path with arbitrary endpoint u, at least zeta*n-gamma*n regular neighbors of u occur on the path. Each has a predecessor pivot z. All but o(n) such predecessors are regular. A single Posa rotation therefore gives at least zeta*n/2 choices making the endpoint regular, if gamma<<zeta. For a fixed target w whose path neighbors were regular, exclude the O(1) clean-up choices which touch w or create a bad neighbor at w. Follow this clean-up by the preceding two-rotation transfer to w. For a fixed w this produces at least c*zeta*n^2 valid ROTATION DESCRIPTIONS, preserving the opposite endpoint. For fixed original endpoint u and final path, the two intermediate endpoints specify the unique inverse sequence; hence there are at most n^2 inverse descriptions. The bound is uniform even if u is exceptional.

If w ranges over a linear-sized set D of regular targets, exclude at most 2|B|+O(1) target positions whose path neighbors are exceptional. Thus the forward description count is at least c*zeta*d*n^2. The inverse count, if the original endpoint u was required to lie in a set U, is at most C*|U|*n^2 (constant factors allow orientation). Consequently

 #resulting paths >= c'*(d/|U|)*#original paths.          (T)

Constants absorb zeta. All descriptions have the same vertex set as the input path. Performing the procedure at BOTH ends yields the analogous lower factor c'*(d/|U|)^2, with distinct target endpoints; the inverse has four freely chosen intermediate endpoints, and |U|^2 choices for the old ends.

## Compare lost and gained cycles of a vertex replacement
Delete x from each cycle containing it, making a path with old endpoints in N_G(x). Orient endpoints in at most two ways. Classify typical old cycles into R (both endpoints in P), L1 (one endpoint in S and one in P), L2 (both in S), and O (cycles omitting x).

For R, transfer one endpoint from P to D and restore x, obtaining a NEW cycle in G' (the xD edge did not exist in G). Formula (T) gives at least c*(d/n)*R distinct gained cycles.

For L1, transfer the S endpoint to D, keeping the P endpoint, obtaining at least c*(d/s)*L1 gained cycles.

For L2, transfer both endpoints to distinct vertices in D, obtaining at least c*(d/s)^2*L2 gained cycles.

All edges used by the rotations lie in G-x=G'-x; the restored x-edges belong to G'. Images of different classes may overlap, so take the maximum of the three lower bounds, which is at least their sum divided by three. By taking kappa sufficiently small, the last two coefficients exceed (say) 12. Therefore

 gained - (L1+L2) >= c_0*delta*(R+L1+L2)

for a constant c_0>0, up to the exponentially negligible atypical loss. (For example use max{aR,12L1,12L2} >= aR/3+4L1+4L2.)

If at least half the old cycles contain x, this positive gain is Omega(c(G)) and dominates all atypical losses. Otherwise at least half omit x. Every typical cycle omitting x has at least ell-2|A|>=c*n edges whose two ends lie outside A. Insert the new pure x into any such edge. Each resulting cycle determines its unique predecessor by deleting x. Hence G' has at least c*n*O cycles containing x, which exceeds c(G) for large n. This covers the omitted-dominated case too and proves strict improvement.

## Application to simultaneous exceptional replacement
Before comparison, add enough REGULAR neighbors in each OTHER assigned part to each TRUE bad vertex x in X to make its regular-neighbor count there at least zeta*n; add no same-part edges and add NO edges incident only with benign vertices in B minus X. Benign vertices already have linear regular neighborhoods. All prefill edges incident X survive the final pure-X completion. This only increases cycles and gives the uniform regular-neighbor lower bound; importantly, the final graph differs from the original ONLY at X. Let C be the original regular core and B its o(n)-vertex complement. Replace only the TRUE bad set X subset B: vertices with two eta-sparse core parts, or with one such part and crossdeficit at least delta*n after assignment. The remaining benign vertices B minus X miss at most delta*n vertices in every opposite CORE part. The final graph obtained by replacing ALL vertices of X is H-free: map the new pure vertices greedily to unused old core vertices in the same parts. Existing copy vertices in C miss at most epsilon*n opposite core vertices, and benign vertices miss at most delta*n; for delta<<1/|H| every required common cross-neighborhood has linear size. The analytic exceptional set remains the ENTIRE original B (not just X), so the regular-core degree bound Q is never asserted for benign vertices prematurely.

For a vertex with a UNIQUE eta-sparse part, the critical-star embedding bounds its regular-core neighbors in that assigned part by a constant, so s<=O_H(1)+|B|=o(n). Its unfilled crossdeficit is >=delta*n/2 after prefill when zeta<<delta. For a vertex with TWO eta-sparse parts, choose one assigned part: s<=eta*n+|B| and some other sparse part supplies d>=(1/r-eta-zeta-o(1))*n. Choose eta much smaller than the transfer constant (which depends on zeta), and epsilon<<eta. Then the lemma applies at every sequential replacement of X. Benign vertices already have linear core neighborhoods, and all true bad vertices receive the prefill. Intermediate graphs need not be H-free; only the final simultaneous replacement of X must be. Hence a cycle-maximizer has X empty. All vertices now miss at most delta*n+o(n) opposite-part vertices; choosing delta sufficiently small in terms of H, the critical-star greedy embedding then bounds the GLOBAL internal degree by mu-1, including edges among former exceptional vertices.

The parameter choices can be made in order: delta fixed, zeta<<delta, then eta sufficiently small in terms of r,zeta,delta, then regular-core epsilon<<eta, and finally n large. The cleanup threshold gamma is chosen <<zeta and tau,epsilon small in terms of 1/2-1/r.

## Executed checks
workspace/agent3_rotation_transfer_checks.py checks 1630 exact two-rotation identities/inverse sequences for path lengths 5..19, and 8188 exhaustive binary-word instances of the prefix half-density inequality. All assertions PASS. The counting proof above is general and does not rely on extrapolating these checks.


# Extension: arbitrary (even constant) crossdeficit once ALL vertices are regular

Assume now every vertex has at most delta*n crossholes, internal degree <=Q, and the parts are balanced up to o(n), where delta is sufficiently small in terms of r,H. There are no exceptional endpoints. The transfer argument extends to targets w NOT present on the old path, so no assumption d>=delta*n is needed.

If w is already on the path use the two rotations above, with Omega(n) descriptions and at most n inverse descriptions per fixed old endpoint u. If w is absent, choose a pivot z such that u--succ(z) and w--z are present cross edges. At most |part(u)|+|part(w)|+2delta*n positions are excluded, leaving (1-2/r-O(delta)-o(1))*n choices. Rotate u to z once, and then add the NEW vertex w at the start by edge wz. This produces a path w,z,...,v on one extra vertex. Restoring x produces a gained cycle because xw was absent before the replacement. For fixed final path and old endpoint u, deleting w and rotating at u recovers the old path uniquely; so this case has at most ONE inverse description per u.

Combining present and absent targets, EVERY w in D gives Omega(n) forward descriptions per typical old path; the inverse is at most |U|*(n+1) when old endpoint u ranged in U. Thus the same factor c*d/|U| holds for arbitrary d>=1. Transfer both lost endpoints similarly; the final cycle may have zero, one, or two extra vertices, but there are only four presence/absence cases and the inverse bound is O(|U|^2*n^2).

The retained/lost/omitted comparison therefore works whenever d>K_r*s, for a constant K_r depending on the small fixed cross-regularity threshold. In particular s<=Q implies that a cycle-maximizer has maximum crosshole degree at most K_r*Q.

Pureifying a SINGLE vertex is H-safe in this all-cross-regular regime: in a newly created H-copy the new pure vertex has no required same-part edges, so replace it by an unused old vertex of the same part adjacent to all opposite-part vertices of the copy. Those common neighbors number at least n/r-|H|delta*n-o(n)>0. This proves the constant crosshole-degree bound directly, without replacing whole bounded components and without an edge-probability blackbox.

The missing-target rotation/inverse identity is additionally checked for all path lengths4..19 and all internal pivots in workspace/agent3_rotation_transfer_checks.py.
