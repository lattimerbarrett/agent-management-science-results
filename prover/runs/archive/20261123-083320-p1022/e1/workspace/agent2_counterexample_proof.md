# Explicit contradiction to d=infinity with the stated PGL definition

Let V=C^6, P^5=P(V) parameterize lines, and Q be the universal quotient in 0->O(-1)->V tensor O->Q->0. Put B=Lambda^2 Q, rank ten. Choose basis e0,...,e5 and
omega=e0 wedge e1+e2 wedge e3+e4 wedge e5 in Lambda^2 V.
Its skew matrix has determinant one and rank six. The induced section of B has no zero: if its value at a line ell vanished, then omega would lie in ell wedge V, whose elements have skew rank at most two. Thus
0->O --omega--> B -> E_omega ->0
is an exact sequence of algebraic vector bundles, with rank(E_omega)=9<2*5.

## Uniformity on every projective line
Take any U subset V of dimension two. On L=P(U),
Q|L=O_L(1) plus (V/U) tensor O_L,
B|L=O_L(1)^4 plus O_L^6.
The degree-zero component of omega is its projection to Lambda^2(V/U). This component never vanishes. If it did, omega would lie in U wedge V. Writing a basis u1,u2 of U, any such bivector is u1 wedge a+u2 wedge b, hence has skew rank at most four; our omega has rank six. Thus omega|L has a nonzero constant component in O_L^6. A bundle automorphism of O_L(1)^4 plus O_L^6 kills its O_L(1)^4 component and takes its constant component to the first basis vector. The quotient is therefore
E_omega|L=O_L(1)^4 plus O_L^5
for every L. This proves uniformity, not merely generic splitting.

## Simplicity of B, with an elementary proof
The exterior Euler sequence gives
0->Q(-1)->Lambda^2 V tensor O->B->0.
The ordinary Euler sequence shows H^0(Q(-1))=H^1(Q(-1))=0, so H^0(B)=Lambda^2 V. B is globally generated, and its evaluation kernel at [ell] is ell wedge V. Therefore an endomorphism of B induces an endomorphism A of Lambda^2 V preserving ell wedge V for every ell.
For independent u,v, (u wedge V) intersection (v wedge V)=C(u wedge v). Hence every decomposable bivector spans an A-invariant line. In particular A(e_i wedge e_j)=lambda_ij(e_i wedge e_j). Applying this to (e_i+e_j) wedge e_k for distinct indices forces lambda_ik=lambda_jk. All eigenvalues are equal, so A is scalar. Global generation makes the action on H^0 faithful. Thus End(B)=C.

## Recovering omega from E_omega
Dualizing gives
0->E_omega^*->B^*->O->0.
Here B^*=Omega^2_P5(2). Its H^0 and H^1 vanish. Indeed the exterior Euler resolution has global section complex
0->Lambda^2 V^* -> V^* tensor V^* -> Sym^2 V^* ->0,
which is exact: the first map is antisymmetrization and the second symmetrization. The intervening positive line bundles have no higher cohomology. Consequently
Ext^1(E_omega,O)=H^1(E_omega^*)=C.
The defining extension is nonzero, since otherwise B would have O as a direct summand, contradicting H^0(B^*)=0.

If E_omega is isomorphic to E_eta for two nondegenerate bivectors, the isomorphism identifies their one-dimensional extension spaces and takes the nonzero defining class to a nonzero scalar multiple. After rescaling O, it therefore lifts to an automorphism of B taking the subline C omega to C eta. Simplicity of B forces eta to be proportional to omega. We have proved
E_omega isomorphic E_eta iff [omega]=[eta].

## A projective automorphism not preserving E_omega
Let g in PGL(V) be induced by diag(1/2,1,1,1,1,1). Under the canonical identification g^*B=B, pullback takes omega to
eta=2 e0 wedge e1+e2 wedge e3+e4 wedge e5.
This is not proportional to omega. Hence g^*E_omega=E_eta is not isomorphic to E_omega. Thus E_omega is not homogeneous according to the definition in the question.

Conclusion: the stated hypotheses admit a uniform, non-PGL-homogeneous bundle of rank 9 on P^5. Therefore d<=5, and in particular d cannot equal infinity. This proof does not claim the exact lower bound d>=5; it decisively disproves the imposed answer. Every finite linear-algebra identity used above is checked in agent2_counterexample_checks.py, and the all-lines argument is the rank bound proved algebraically above.
