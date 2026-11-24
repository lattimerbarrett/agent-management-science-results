# All-rank degree-two injectivity: weight classification audit

Uses the exact rank-3/rank-4 lattice certificate and the two universal
relations proved in `agent4_degree2_relations.md`.
Write a(i;jk) = e_i^* tensor [X_j,X_k], with j != k and antisymmetry
in j,k. Each is the signed Johnson image of one Magnus generator.
Call it K-type if i is j or k, and C-type otherwise. K-type has
weight e_t; C-type has weight e_j+e_k-e_i.

The abelian group Lambda^2(V) is weight graded. All relations below
are genuine relations in gr_2(IA_n). Its bracket map is integral.
For <=4 labels, any relation with zero derivation image is a genuine
relation by the exact n=4 certificate (and n=2/3 results).

Universal relations:
1. Same-target C-type pairs vanish in gr_2 (partial-inner identity).
2. Dummy collapse: a(i;pk) wedge a(p;qr) equals
   a(i;qk) wedge a(q;qr) when the initial and cross terms commute.
   This follows by shearing X_p -> X_p+X_q in the commuting relation
   a(i;pk) wedge a(q;qr)=0 and subtracting commuting terms.
   Besides the five-distinct-label case, it remains valid when k=i,
   provided i,p,q,r are distinct. If k=q choose r instead of q.

## Weights with a negative entry
Two distinct negative entries: neither target occurs in the opposite
tail, so the automorphisms commute exactly. An entry -2 means two
C-types with the same target, covered by relation 1.

Exactly one negative entry -e_i leaves three positive output labels
(counted with multiplicity). The derivation image has only target i
and is an integral degree-three free Lie element on those labels.
Any intermediate contracted target outside these labels is eliminated
by dummy collapse. Of q,r at least one differs from k because q!=r,
so an allowed collapse always exists. All remaining columns of any
fixed weight are supported on i plus the positive labels, at most four
labels. Consequently every kernel relation is a local rank<=4 relation.

## Weight e_a+e_b with a!=b
For each s outside {a,b}, put
 U_s=e_s^* [[s,a],b], V_s=e_s^* [[s,b],a],
 Z_a=e_a^* [a,[a,b]], Z_b=e_b^* [[a,b],b].
Use the following actual degree-two bracket columns:
 W_s=a(s;sa) wedge a(s;sb), image U_s-V_s;
 L_s=a(s;ab) wedge a(a;as), image U_s+Z_a;
 G=a(a;ab) wedge a(b;ab), image -Z_a+Z_b.
Their images are integrally independent: inspecting U_s,V_s forces
all W_s,L_s coefficients to vanish, and then inspecting Z_b kills G.

All K-K pairs either commute exactly or have support<=3.
A C-K pair must be a(i;ab) wedge K(p;i). If p lies outside {a,b,i},
dummy collapse (the allowed k=target case) replaces it by a bracket
on {a,b,p}; otherwise it already has support<=3.
A C-C pair must be
 E_ip=a(i;pa) wedge a(p;ib), with i,p outside {a,b} and i!=p.
Its image is -V_i+U_p, hence by rank4 injectivity
 E_ip=-L_i+L_p+W_i.
Every column supported on {a,b,s} has image in the primitive lattice
spanned by W_s,L_s,G: their 3 columns have a unit 3x3 minor in the
4-dimensional coordinate group (U_s,V_s,Z_a,Z_b). The elementary
degree-two trace identity for brackets is c_U+c_V-c_Za-c_Zb=0.
Thus these 3 columns are a basis of the full integral trace kernel.
The identity follows either directly by expanding both derivations,
or from trace(e_t^*[[u,v],w])=delta_tu*v*w-delta_tv*u*w
and trace(e_t^*[u,[v,w]])=-delta_tv*u*w+delta_tw*u*v
in the symmetric square; the two contributions in a bracket cancel.
Thus every column reduces integrally to W_s,L_s,G, whose independent
images prove injectivity.

## Weight 2e_a
K-K pairs commute (same conjugator). C-K is impossible because the
C-type has two distinct positive output labels. The only C-C columns
are E_ip=a(i;pa) wedge a(p;ia), i,p!=a, i!=p.
Put T_i=e_i^* [[i,a],a]. Their images are T_p-T_i.
Fix t!=a; the columns E_it (i!=a,t) have independent images.
Every E_ip=E_it+E_tp follows from rank4 injectivity on {a,i,p,t}.
Thus there is no kernel in this weight either.

These exhaust weights (sum of coordinates is two), proving
ker[Lambda^2(V)->Der_2]=relations in gr_2(IA_n), for every n.
Consequently gamma_2(IA_n) intersect A_3(n)=gamma_3(IA_n).
Together with the degree-one theorem this also gives A_3=gamma_3.
