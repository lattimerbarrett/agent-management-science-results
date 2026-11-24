# Reconstruction of width-one uniform bundles on P3 of ranks 4 and 5

This proves reconstruction from the exact Chern list computed by agent1. Together these results classify all width-one cases in ranks below 6.

Conventions: V0=C^4; G=Gr(2,V0), with tautological S and quotient R. H=c1(S*) and sigma2=c2(R). Let I=F(1,2;4), p:I->P3 and q:I->G. Write Q=T_P3(-1). Normalize E to have splitting (1^a,0^b), a+b=r<6. Dualizing and twisting permits a<=b. Cases a=1 are proved separately by agent2; the only remaining cases are (a,b)=(2,2),(2,3).

Relative evaluation gives 0 -> p*O(1) tensor q*V -> p*E -> q*W -> 0, where V has rank 2. The exact necessary Chern list is (c2(E),c3(E))=(1,0),(2,0),(2,2). Divided-difference computation gives:

* (1,0): c1(V)=0,c2(V)=0;
* (2,0): c1(V)=-H,c2(V)=sigma2;
* (2,2): c1(V)=-H,c2(V)=0.

These identities are checked by agent3_P3_width1_reconstruction_checks.py.

## Two elementary facts

A globally generated rank-two bundle B on P2 with c1(B)=1 is O+O(1) or Q_P2. Indeed a general section has finite reduced zero scheme Z and gives 0->O->B->I_Z(1)->0. The quotient is globally generated, so its degree-one sections generate its ideal sheaf. A nonempty finite scheme cut out by linear forms is one reduced point. Thus Z is empty or one point. In the first case H1(O(-1))=0 splits the extension. In the second case Ext1(I_point(1),O)=C; its unique nonzero locally free extension is Q_P2.

A bundle B on G trivial on every Grassmannian line is trivial. On every alpha-plane (lines through a fixed point of P3), B is trivial by the trivial-on-lines lemma on P2. Thus q*B descends via p to a bundle C on P3. Restricting to every q-fiber gives C trivial on every line; hence C is trivial. Finally q_*O=O shows B is trivial.

## Case c1(V)=0

On every alpha-plane A, V is a subbundle of O_A^r. Thus V*|A is globally generated. Its determinant has degree zero, so V*|A is trivial: choose sections forming a basis at one point; their determinant is a nonzero constant and hence they form a basis everywhere. Consequently V is trivial on every Grassmannian line and therefore trivial. The top evaluation subbundle then descends to O(1)^2 in E. The quotient is trivial on every line, hence trivial. H1(O(1))=0 splits E.

## Cases c1(V)=-H

V*|A is globally generated rank two with c1=1. By the preceding lemma, its restriction to each alpha-plane is O+O(1) or Q_P2. Both have splitting (1,0) on lines. Every Grassmannian line lies in an alpha-plane, so V is uniform of type (0,-1) on G.

On every beta-plane (two-subspaces in a fixed three-space), c2(V) restricts to zero: this is immediate for c2(V)=0, and c2(R) restricts to zero since R|beta=O(1)+O. The rank-two P2 classification now gives V|beta=O+O(-1).

Let Y=F(2,3;4), pi:Y->G, and s:Y->Gr(3,4). Set K=s*c1(O(1)). The top relative line along the beta-plane fibers is therefore O(aK), and its quotient in pi*V is O(-H-aK). Hence
c2(V)=-a HK-a^2 K^2.
The classes HK and K^2 are independent in A^2(Y); the universal flag sequence gives pi*sigma2=HK-K^2.

If c2(V)=0, comparison gives a=0. The line O descends to V, giving V=O+O(-H), since H1(G,O(H))=0.

If c2(V)=sigma2, comparison gives a=-1. Dualizing the flag sequence gives
0->O(H-K)->pi*V*->O(K)->0.
On every pi-fiber P1, the first term has degree -1 and has no cohomology, so V*=pi_*O(K). At U in G, the fiber parametrizes lines in V0/U. Therefore pi_*O(K)=det(S*) tensor R*=R (rank-two duality). Thus V=R*.

## Reconstruct E

If V=O+O(-H), the trivial summand of V gives a descended O(1) subbundle in E. Its quotient has splitting (1,0^{r-2}), so the top-multiplicity-one theorem identifies it as Q+O^{r-4} (the Chern data excludes the split alternative). The extension splits because H1(Q*(1))=H1(Omega1(2))=0. Hence E=O(1)+Q+O^{r-4}.

If V=R*, dualizing relative evaluation and applying p-adjunction gives
E* -> p_*(p*O(-1) tensor q*R)=Q(-1).
The displayed pushforward follows by pushing
0->p*O(1) tensor q*O(-H)->p*Q->q*R->0;
the first term restricts to O(-1) on p-fibers and is acyclic. On each p-fiber, the original dual map is a surjection O^r->Q_P2. Such a surjection must induce a surjection C^r->H0(Q_P2)=C^3: a two-dimensional section space cannot generate Q_P2 since its determinant section would vanish (equivalently c2(Q_P2)=1). Thus E*->Q(-1) is a bundle surjection. Dualizing gives Q*(1)=Omega1(2) as a subbundle of E. Its top line-degree-one part has rank two and matches the full top part of E, so the quotient is trivial on every line and hence trivial. Finally H1(Omega1(2))=0 splits the extension:
E=Omega1(2)+O^{r-3}.

All three reconstructed bundles are homogeneous, as are their duals and twists.
