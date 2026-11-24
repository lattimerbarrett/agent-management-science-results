# A finite integral certificate criterion for degree-two injectivity

Let G be a group, let V=G/[G,G] be free abelian of finite rank, and let
beta: Lambda^2 V -> gamma_2(G)/gamma_3(G)
be the canonical surjection, beta(u wedge v)=[u,v].
Let J: gamma_2(G)/gamma_3(G) -> W be a homomorphism to a free abelian group.
Suppose an integer matrix B represents J beta.

For each pair of commuting elements a,b in G, the column
[a]_ab wedge [b]_ab belongs to ker beta. More generally, if theta is any
automorphism of G, then theta_ab([a]_ab) wedge theta_ab([b]_ab) belongs
to ker beta, because theta(a),theta(b) still commute.

Form the integer matrix R whose columns are any such relations. If
(1) B R=0,
(2) rank_Q R = dim_Q ker B,
(3) every nonzero Smith invariant of R is 1,
then J is injective.

Proof: let N be the number of rows of R. Condition (3) says that
Z^N/im R is torsion-free, i.e. im R is saturated. Conditions (1),(2)
then imply im R=ker B: for x in ker B, equality of rational spans gives
a nonzero integer m with mx in im R; saturation gives x in im R.
Every R column is killed by beta, while ker beta is contained in ker B,
so ker beta=ker B. Therefore the induced J is injective. No presentation
of G, finiteness assumption on its relation set, or torsion-freeness
assumption on gamma_2(G)/gamma_3(G) is used.

For G=IA_n, V=H^* tensor Lambda^2 H by the Magnus-generator argument.
Take W=Hom(H,L_3(H)), or its canonical embedding in
Hom(H,H^{tensor 3}). Then B is the degree-two derivation bracket map.
The standard Johnson calculation identifies J with the restriction of
tau_2 to gamma_2(G). Therefore the three conditions prove
 gamma_2(IA_n) intersect A_3(n) = gamma_3(IA_n).
Combining with A_2(n)=gamma_2(IA_n) gives A_3(n)=gamma_3(IA_n).

CAUTION: rational ranks alone do not suffice: condition (3) is essential.
