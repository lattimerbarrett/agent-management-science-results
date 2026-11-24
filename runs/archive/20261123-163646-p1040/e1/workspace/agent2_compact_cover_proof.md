# Certified compact central L-cover of IA_3

Input: `agent2_compact_cover_seeds.json`; generator: `agent2_compact_cover_seeds.py`.
There are nine free Magnus generators, eight free-group automorphisms
(forward/inverse T,P,I,C), and 261 iterated relators, only 107 nonempty,
total 4990 letters, longest 682. No fixed relators are needed.

## Exact action lifts
The four Aut(F3) generators are T:x0->x0*x1, P swapping x0,x1,
I inverting x0, C cyclically permuting x0,x1,x2. Their conjugation
images of all nine Magnus generators are supplied as exact words in
`agent2_nielsen_actions_n3.json`. Those identities were checked as
literal reduced free-group automorphisms. All four word maps are
actually automorphisms of the FREE group on nine symbols. Their
inverses are `agent2_nielsen_inverse_words_n3.json`; both substitution
composites reduce to each original generator, without any relations.

## Full signed-permutation action
First impose that these six operator words act trivially:
 P^2, C^3, (PC)^2, I^2, (IP)^4, [I,CPC^-1].
They present B3=C2^3 semidirect S3: P,C present S3; CPC^-1 fixes
coordinate0, so the last relation makes I invariant under its
stabilizer. Its three S3-conjugates are thus well defined involutions;
(IP)^4 says two distinct conjugates commute, and S3 conjugation makes
all three commute. Hence the presented group has order at most48;
its actual signed-permutation images have order48, giving equality.
Each operator loop is imposed on every one of the nine generators.

Consequently any consecutive signed-permutation subword of a longer
operator word may be replaced by a shortest representative of its
actual signed permutation. The generator uses an exhaustively checked
48-state Cayley table for this shortening. This is a proved operator
identity in the quotient, NOT an assumed free-endomorphism identity.

## Aut(F3) action and Peiffer relations
The complete four-generator Aut(F3) presentation is encoded and checked
in `agent4_AutF3_four_generator_presentation.json` (Tietze expansion
of GAP/FGA's classical Nielsen S,T,U presentation). All fourteen of
its loops are shortened as above and imposed on all nine generators.
Together with the B3 action relations this makes the operator action
factor through Aut(F3).

For every Magnus generator g_i choose its exact Aut(F3) word W_i from
`agent2_magnus_aut_words_n3.json`. Signed-permutation shortening is
again valid. Impose all81 Peiffer relations
 phi_(W_i)(g_j) * g_i * g_j^-1 * g_i^-1 = 1.
The Magnus images of W_i were independently checked as exact free-group
automorphisms. Every one of the resulting261 seed words was additionally
checked by literal evaluation in IA_3, not merely truncated expansions;
all evaluate to identity, with maximum intermediate total F3 wordlength177.

Let H be the invariant L-presented group, where the entire orbit of
all these relations under the eight operators is imposed. Thus all
operators and inverses descend to automorphisms of H. The map sending
the nine generators to the actual Magnus generators gives a surjection
mu:H->IA_3 by Magnus generation and is equivariant for Aut(F3).
Peiffer on generators extends to every x,y in H:
 phi_(mu(x))(y)=x*y*x^-1.
If mu(x)=1 this forces x central. Therefore ker(mu) is central.
No assertion H=IA_3 is made.

## Integral nilpotent audit
`agent2_lpres_cover.py` loads LPRES with OnlyNeeded:=true and computes
its integral nilpotent quotients entirely inside GAP (no external nq).
Class3 finishes in0.3sec. The lower-central factors are
 Z^9, Z^18, Z^43 directsum (Z/2)^14 directsum (Z/3)^9.
This agrees exactly with the separately audited class3 BCH computation.
These extra torsion factors may be artifacts of the central kernel;
they prove NO IA_3 discrepancy by themselves.
