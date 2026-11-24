# Tensor obstruction realizer (r >= 3)

Fix a finite collection of coloured profiles P_i. Each P_i is a graph J_i
on a separate vertex set, together with a colouring alpha_i:V(J_i)->[r]
(not necessarily proper). Require each J_i to be r-colourable, and at least
one alpha_i to have a monochromatic edge. Set J=disjoint union of all J_i.
For each i extend alpha_i to an assignment a_i:V(J)->[r] by choosing a fixed
proper r-colouring on every J_j, j != i. Let R={a_i}, deleting duplicates.

Put m=|R| and Q=K_r^{categorical m}. For every x in V(J), let t_x be the
vector (a(x):a in R) in V(Q). Let Q(M) be the independent M-blowup of Q.
Construct H by taking Q(M) and J, and joining each x in J to every clone
of every neighbour of t_x in Q. There are no further edges.

CLAIM: If G is a complete join of r graphs of maximum degree D, M>rD,
and every part has at least |H| vertices, then H embeds in G iff some
coloured profile (J_i,alpha_i) embeds in G respecting its colours up to a
permutation of the r host parts. Here a profile embedding only requires
edges whose ends receive the same colour to be internal; all remaining
edges are automatically present across the complete join.

Proof forwards. In each clone cluster select a host part containing at
least M/r clones and call it its dominant colour. Adjacent Q-vertices
cannot have the same dominant colour: otherwise the internal host degree
of any clone in one cluster is at least M/r>D. Hence dominant colours give
a proper r-colouring f of Q. Every proper r-colouring of Q is pi composed
with a coordinate projection; see tensor rigidity proof below. For an
actual vertex x, neighbours of t_x in Q realize every f-colour other than
f(t_x): choose the projected coordinate arbitrarily different from that
of t_x, and every other coordinate also different. If x has any such
other host colour it has at least M/r>D neighbours inside its own part.
Thus x has host colour f(t_x). The projected coordinate is some a_i,
so the actual J_i vertices supply the required profile.

Proof backwards. Use assignment a_i to place every Q(M) cluster in its
coordinate colour, put actual J_i on its given embedding, and put the
other actual vertices arbitrarily in their a_i colours. Since there are
at most |H| vertices and each part has at least that many vertices,
disjoint placements exist. Constraint edges all cross parts. Edges of
J_j for j != i also cross, and J_i is present by hypothesis.

If every a_i has a monochromatic edge then chi(H)>r, by applying exactly
the forward argument with D=0 to any hypothetical r-colouring of H
(or directly using rigidity and terminal-neighbour forcing).
If at least one profile J_i is a bipartite graph wholly in one colour,
then chi(H)<=r+1: use projection a_i and recolour one bipartition side of
J_i to a new colour. All other J_j are properly coloured and constraint
vertices keep old colours, so this is proper. In particular chi(H)=r+1
whenever a star profile is present and every profile has a monochromatic
edge.

If one profile is a star K_{1,L} wholly in one colour, then H embeds in a
complete r-partite host with just one internal K_{1,L}, using the backwards
construction. Hence sufficiently large complete-cross H-free graphs have
internal maximum degree at most L-1. Choosing M>r(L-1) validates the forward
argument without any circular bound involving |H|.

TENSOR RIGIDITY PROOF.
For r>=3, the adjacency matrix of Q is (J_r-I_r)^{tensor m}; its eigenvalues
are (-1)^k(r-1)^(m-k), k=0,...,m. The degree is (r-1)^m and unique least
eigenvalue is -(r-1)^(m-1), whose eigenspace is the direct sum of the m
one-coordinate mean-zero spaces. Hoffman's bound gives independence
number <= r^(m-1), attained by coordinate fibres. Any proper r-colouring
partitions r^m vertices into r independent sets, so all attain equality.
The equality condition in Hoffman's proof says the indicator of each
colour class is 1/r + sum_j g_j(x_j), with each g_j mean zero. A {0,1}-valued
additive function cannot depend on two coordinates: if two nonconstant
summands have nonzero differences delta,epsilon, fixing the remaining
coordinates produces four values a,a+delta,a+epsilon,a+delta+epsilon in
{0,1}; nonzero delta,epsilon must each be +/-1, and either equal or opposite
signs then force a value outside {0,1}. Thus every colour class is a fibre
of a single coordinate. Fibres of different coordinates intersect, so all
r classes use the same coordinate. Their values are then a permutation
of the r colours. This proves rigidity.
