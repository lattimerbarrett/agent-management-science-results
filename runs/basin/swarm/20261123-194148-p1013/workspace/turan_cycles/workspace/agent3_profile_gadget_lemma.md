# Arbitrary finite color-profile gadget for r>=3

Fix r>=3 and Q>=0. Let X be a finite set of DISTINCT terminal vertices. Let E0 be an arbitrary graph on X, called the unprotected graph. Let R={t^1,...,t^m} be a nonempty finite collection of maps X -> {0,...,r-1}. There is a finite graph J containing the terminals X such that:

(a) In every partition of V(J) into r parts in which the graph induced on each part has maximum degree at most Q, the terminal-part map is t^i followed by a common permutation of colors, for some i.

(b) Every such prescribed map extends to a partition of J in which ALL edges outside E0 run between distinct parts. Thus J can be embedded into a sufficiently large complete r-partite graph with arbitrary added internal graphs iff, for some prescribed profile (and color permutation), the unprotected monochromatic-edge pattern can be embedded internally and its unprotected bichromatic edges can be embedded across the parts. All auxiliary vertices can use fresh pure bulk vertices.

(c) If every profile makes at least one E0 edge monochromatic, while there is a profile in which ALL monochromatic E0 edges belong to a star with center v in X, then chi(J)=r+1 and v is critical, provided this star has at least one edge. In particular J-v is r-colorable.

## Equality gadget
Put M=rQ+1. Take r-1 disjoint independent classes of M fresh vertices, complete between distinct classes. Join every vertex in a designated target set S to every anchor vertex. In any r-part assignment with internal degree <=Q, each anchor class contains >=Q+1 vertices in some part. These r-1 majority parts are distinct: otherwise a vertex from one majority sees >Q neighbors in its own part. Every target is adjacent to all majority sets, so every target lies in the single remaining part. Conversely if all targets share one part, assigning the anchor classes to the other parts makes every gadget edge proper. This forces equality of the part labels of arbitrary many DISTINCT vertices.

## Protected inequality
To enforce u != v, create M fresh twins u_1,...,u_M, force u,u_1,...,u_M equal by a fresh equality gadget, and join v to all u_j (retain edge uv too if desired). If v shared the color of u it would have M>Q internal neighbors. Conversely a proper assignment u!=v extends properly to the entire gadget. Protected edges can therefore NEVER be monochromatic in an internal-maximum-degree-Q host.

## Exact profile relation
Let P be the categorical tensor power K_r^m. Its vertices are words z in [r]^m and two words are adjacent iff they differ in EVERY coordinate. For each edge of P use a fresh protected inequality gadget. For each terminal x, put c_x=(t^1(x),...,t^m(x)) in V(P), and force x to equal c_x with a fresh equality gadget. Even if columns c_x coincide, the terminals remain DISTINCT, so column collisions cause no identifications and no problem. Add the unprotected graph E0 on X.

Every bounded-internal-degree partition extracts a proper r-coloring of P. Every proper r-coloring of P is one coordinate projection followed by a color permutation (proof below). This gives (a), and the proper extension observations give (b).

For (c), a proper r-coloring is also an internal-degree-Q partition; every extracted profile has an improper E0 edge, so J is not r-colorable. On deleting v the star profile extends to a proper r-coloring. The power contains the diagonal clique K_r, which is disjoint from the terminals, so J-v has chromatic number exactly r. Hence chi(J)=r+1 and v is critical.

## Self-contained dictatorship proof
The graph P has N=r^m vertices and degree d=(r-1)^m. A tensor eigenbasis is formed by constant vectors or sum-zero alphabet vectors in each coordinate. With s sum-zero coordinates the eigenvalue is (-1)^s(r-1)^(m-s). Since r>2, the least eigenvalue is lambda=-(r-1)^(m-1), occurring ONLY at s=1.

For an independent set C of size alpha, put f=1_C-(alpha/N)1. Then f^T A f=-d alpha^2/N and ||f||^2=alpha-alpha^2/N. The least-eigenvalue bound gives alpha<=N(-lambda)/(d-lambda)=N/r. A proper r-coloring partitions N vertices into r independent sets, so each class has size N/r and attains equality. Its centered indicator lies in the first-level eigenspace, hence

  1_C(z)=1/r+sum_j f_j(z_j).

A {0,1}-valued additive function can depend on at most ONE coordinate. If f_i and f_j are nonconstant, choose increasing values in each and hold every other coordinate fixed. The resulting rectangle takes values a,a+b,a+c,a+b+c with b,c>0. If all are binary, a=0 and b=c=1, making a+b+c=2, contradiction. Thus each color class depends on one coordinate. Since its size is exactly N/r it is one alphabet fiber. Fibers of DIFFERENT coordinates intersect; therefore all r color classes use the SAME coordinate and are its r fibers. This proves dictatorship, including all equality cases, without an external theorem.

## Important scope
The lemma realizes arbitrary PROFILE relations, not arbitrary forbidden graph families unless the inactive unprotected patterns can all be properly r-colored in the selected profiles. Disjoint forest/cycle patterns have this property for r>=3. For patterns consisting ONLY of monochromatic edges in selected parts and no unprotected cross edges between active terminals, finite crossholes do not obstruct the embedding because all auxiliary vertices can use pure bulk.

Actual exact checks: workspace/agent3_profile_gadget_checks.py. The executed run verifies full integer tensor eigenbases and Z3 UNSAT of every nondictatorial coloring for (r,m)=(3,1),(3,2),(3,3),(4,2); it also verifies equality and protected-inequality gadgets under all bounded-degree part assignments for (r,Q)=(3,0),(3,1),(3,2),(4,1). All assertions PASS in 7.8s. These finite checks support the completely general proof above; they do not replace it.
