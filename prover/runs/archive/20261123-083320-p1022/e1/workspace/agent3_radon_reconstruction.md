# Radon mutation and reconstruction lemma

Let X=P(V), dim X=n, G=Gr(2,V), I=P(S), with p:I->X, q:I->G. Write h=p*c1(O_X(1)), H=q*c1(det S*). All functors below are derived, and [1] is cohomological shift.

Set Phi(E)=Rq_*(p*E tensor O(-h)). The right adjoint is
Psi(A)=Rp_*(q*A tensor O(-h+H))[1],
because omega_q=O(-2h+H) and q has relative dimension one.

There is a natural distinguished triangle
RΓ(X,E) tensor O_X -> E -> Psi Phi(E) -> .

Proof: let Z=I x_G I, with two point projections and f:Z->X x X. It parametrizes two ordered points on one line and is the blowup of the diagonal. Write D for its exceptional divisor. The Pluecker determinant section of the span of the two points gives H=h1+h2-D. (Equivalently the resolved rational map X x X --> G is given by wedge products of homogeneous coordinates, whose base ideal is the diagonal ideal.) The kernel computing Psi Phi is therefore
Rf_* O_Z(H-h1-h2)[1]=Rf_*O_Z(-D)[1]=I_Delta[1].
The last identity follows from blowup pushforward, with all higher direct images zero: O(-D) is relatively O(1) on exceptional P^{n-1} fibers. Thus Psi Phi(E)=Rp1_*(p2*E tensor I_Delta)[1]. Applying Rp1_* to 0->I_Delta->O->O_Delta->0 proves the triangle.

For a width-one uniform E, Phi(E) is a vector bundle A in degree zero by base change, because E(-1)|L=O^{a}+O(-1)^b. This is the usual top relative-evaluation bundle.

Consequences:

1. If A=O_G(-1)^a, then Psi(A)=O_X(-1)^a[1]. The triangle forces H^i(E)=0 for every i>0 and an actual resolution
0->O_X(-1)^a->H0(E) tensor O_X->E->0.

2. If A=S tensor O_G(-1), then Psi(A)=O_X(-2)[1]. Indeed tensoring the tautological sequence 0->p*O(-1)->q*S->O(h-H)->0 by O(-h) leaves O(-2h) and O(-H); the latter is acyclic on p-fibers. Hence
0->O_X(-2)->H0(E) tensor O_X->E->0.

In both cases the cohomology long exact sequence of the triangle establishes the displayed resolution; mere equality in K-theory is not being substituted for exactness.

For the second case and for the first with a>=2, rank(E)>=2n if E is width-one uniform. The first case is the linear Steiner tensor-rank obstruction. For the second case, dualize/twist to get 0->E*(1)->O(1)^{r+1}->O(3)->0; restrictions to each line force the defining quadrics to span every binary quadratic space. A subspace W of quadrics with this property must have dim W>=2n+1: its annihilator avoids the projective variety of rank-at-most-two symmetric tensors, which has projective dimension 2n. Projective dimension therefore gives dim W>=2n+1 and r>=2n. This is also the general binary-support tensor formula dim X=2(n-1)+d with d=2, giving dim X=2n. 
