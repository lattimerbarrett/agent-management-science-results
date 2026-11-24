# DIAGNOSTIC: weighted linear estimate and its seven-dimensional application

This is an independent audit of the analytic, rather than combinatorial, part of SP7. It proves a local weighted estimate under explicit hypotheses and checks that the proposed n7 first/second approximations meet them. It is not labeled as a global compactness theorem or a disproof of the supplied answer.

## 1. Weighted linear lemma

Let 0<s<n-2, epsilon_i->0, R_i=delta0/epsilon_i. Let D_i=B_{R_i} intersect {t>F_i(z)}, with F_i(0)=DF_i(0)=0 and

    |DF_i|<=C delta0, |F_i|<=C delta0 |z|,
    |kappa_i(y)|<=C epsilon_i^2 |y|.

Suppose e_i solves

    Delta e_i+c_i e_i=A_i in D_i,
    partial_nu e_i+kappa_i e_i=B_i on the graph,

where |c_i|<=C(1+r)^-4 and c_i->n(n+2)U^{4/(n-2)} locally. Assume e_i(0)=0 and all tangential first derivatives at 0 vanish. Define

    Lambda_i=sup_D (1+r)^(s+2)|A_i|
              +sup_graph(1+r)^(s+1)|B_i|
              +R_i^s sup_outer|e_i|.

For sufficiently small fixed delta0 there is C independent of i such that

    sup_D (1+r)^s |e_i|<=C Lambda_i.                   (L)

### Exterior barrier

For fixed large r0, put psi=C0 r^-s-D0 t r^(-s-1), with C0>D0>0. Direct calculation gives

    -Delta r^-s=s(n-2-s)r^(-s-2),
    Delta(t r^(-s-1))=-(s+1)(n-s-1)t r^(-s-3).

Choose C0 sufficiently large compared with D0. Then -Delta psi>=c r^(-s-2), and psi is positive on the whole upper halfspace and on a small adjoining angular collar. The potential term is absorbed by r0 large. On the graph, partial_nu(-D0 t r^(-s-1))=D0 r^(-s-1)+O(D0 delta0^2 r^(-s-1)), while partial_nu(C0 r^-s)=O(C0 delta0 r^(-s-1)). The Robin contribution is at most C C0 epsilon_i^2 r^2 r^(-s-1)<=C C0 delta0^2 r^(-s-1). Choose delta0 sufficiently small after C0,D0. Thus

    -(Delta+c_i)psi>=c r^(-s-2),
    (partial_nu+kappa_i)psi>=c r^(-s-1).

A positive strict supersolution supplies the exterior maximum principle even if kappa_i changes sign: divide the comparison function by psi. Consequently

    sup_{r>=r0}(1+r)^s |e_i|
         <=C[Lambda_i+sup_{r<=2r0}|e_i|].              (E)

This includes the outer boundary because psi>=cR_i^-s there.

### Interior kernel contradiction

If (L) failed, divide by eta_i=sup(1+r)^s|e_i| with Lambda_i/eta_i->0. Local boundary estimates give a Jacobi limit phi, with |phi|<=C(1+r)^-s,

    (Delta+n(n+2)U^{4/(n-2)})phi=0, phi_t=0,
    phi(0)=0, D_z phi(0)=0.

This limit is a kernel combination. Indeed phi/U, transferred to the hemisphere and reflected evenly, grows at its missing point at most rho^(-(n-2-s)), which is strictly weaker than rho^(2-n). Annular estimates give the same first-derivative growth. Integrating by parts around the missing point produces boundary errors O(rho^s) or better, so the eigenfunction equation holds distributionally across it. Elliptic regularity makes the singularity removable. The smooth eigenspace is exactly the first spherical harmonics even under reflection, namely scale and tangential translations. The value and tangential gradients at the bubble center kill all of them. Thus phi=0. Divide (E) by eta_i and pass to the limit to contradict its normalized supremum. This proves (L).

Gradient estimates follow on smaller concentric domains from the equation and scaled boundary Schauder estimates:

    |De_i|<=C Lambda_i(1+r)^(-s-1),

provided the corresponding local Holder norms of A_i,B_i obey their differentiated weights. All model sources below have these bounds.

## 2. n7 first approximation

Here U=(1+r^2)^(-5/2), p=9/5. Let w_i satisfy isolated-simple decay w_i<=CU and local bubble convergence, and write its physical graph as

    F_i=epsilon_i f2_i+epsilon_i^2 f3_i+epsilon_i^3 f4_i+...,
    tr D^2f2_i=0, H_i(0)=0.

Let b_i=|f2_i|. Let Phi2_i solve the physical linearized problem, with |D^jPhi2_i|<=C b_i(1+r)^(-4-j), center value/gradient zero. Put W1=U+epsilon_i Phi2_i. Its residual has bounds

    |Delta W1+35 W1^p|<=C epsilon_i^2(1+r)^-5,
    |B_i W1|<=C epsilon_i^2(1+r)^-4.

The interior nonlinear remainder is bounded by C U^(p-2)(epsilon_i Phi2_i)^2=O(epsilon_i^2 b_i^2 r^-7), better than the stated weight. Boundary cubic geometry is the limiting weight. In the thin negative-t extension strip, use the reflection extension Q(z,t)=Q(z,-t)+2t Q_t(z,0); its extra linearized source is 2t(Delta_z b+Vb). For Phi2, b=O(b_i r^-5), so after multiplication by epsilon_i the largest strip source is epsilon_i^2 b_i^2 r^-5; higher graph terms add factors epsilon_i r. Thus it obeys the displayed bound. All constants are uniform for one fixed outer delta0.

W1/U differs from 1 by at most C epsilon_i b_i r<=C b_i delta0, so it is positive and comparable to U. For e1=w_i-W1 use the exact divided difference coefficient

    c_i=35(w_i^p-W1^p)/(w_i-W1),

which satisfies |c_i|<=CU^(p-1)<=Cr^-4 and has the correct local limit. The first weighted lemma with s=3 applies. Its outer datum has weighted size O(R_i^-2+epsilon_i b_i/R_i)=O_delta0(epsilon_i^2). Therefore

    |e1|<=C_delta0 epsilon_i^2(1+r)^-3,
    |De1|<=C_delta0 epsilon_i^2(1+r)^-4.

## 3. Coarse quadratic-jet rate

This step still uses the exact stress calculation, but no cubic positive coefficient. Its relevant unsigned bound is

    P_adapted(r)>=c b_i^2/epsilon_i^3
                      -C b_i/epsilon_i^2-C/epsilon_i-C_r.

The first-error cross is b_i/epsilon_i^2; all cubic/first-error terms are bounded by C/epsilon_i. Pure b_i^3/epsilon_i^2 absorbs into the leading term since epsilon_i b_i->0. The fixed-radius adapted flux is bounded by strong decay and local elliptic estimates. Multiplying the inequality by epsilon_i^3 and applying Young gives b_i=O(epsilon_i). This is the coarse rate assumed in the next analytic step; completeness of this stress bound is audited separately in the exhaustive grading documents.

## 4. n7 second approximation and the subquadratic issue

Let Phi3_i be the cubic physical Jacobi correction, with center value and tangential gradient zero and |D^jPhi3_i|<=C(1+r)^(-3-j). Put

    W2=U+epsilon_i Phi2_i+epsilon_i^2 Phi3_i.

Its relative correction is bounded by C(epsilon_i b_i r+epsilon_i^2r^2). Choose fixed delta0 small so W2/U lies between 1/2 and 2. Although p<2, ordinary Taylor is therefore uniform on the whole segment from U to W2:

    |W2^p-U^p-pU^(p-1)(W2-U)|
          <=C U^(p-2)|W2-U|^2.

The three quadratic pieces have weights epsilon_i^2 b_i^2 r^-7, epsilon_i^3 b_i r^-6, epsilon_i^4 r^-5. With b_i=O(epsilon_i), each is <=C epsilon_i^3 r^-4. Thus subquadraticity does not by itself invalidate the residual estimate.

The graph's remaining quartic boundary source is epsilon_i^3 r^-3. The quadratic-squared normal/Robin errors are epsilon_i^2 b_i^2 r^-4<=Cepsilon_i^3r^-3. Higher graph terms add epsilon_i r. The Phi3 extension source has largest terms epsilon_i^3 b_i r^-4 and epsilon_i^4r^-3; the latter is <=delta0 epsilon_i^3r^-4. The Phi2 extension has terms epsilon_i^2b_i^2r^-5, epsilon_i^3b_i r^-4, epsilon_i^4b_i r^-3; all are controlled by the target since epsilon_i r<=delta0. Consequently

    |Delta W2+35 W2^p|<=C epsilon_i^3(1+r)^-4,
    |B_i W2|<=C epsilon_i^3(1+r)^-3.

For e2=w_i-W2 the exact divided difference again gives c_i<=Cr^-4, without any Taylor expansion involving unknown e2. The weighted lemma now has s=2. Its outer term is

    O(R_i^-3+epsilon_i b_i/R_i^2+epsilon_i^2/R_i)
           =O_delta0(epsilon_i^3).

Therefore

    |e2|<=C_delta0 epsilon_i^3(1+r)^-2,
    |De2|<=C_delta0 epsilon_i^3(1+r)^-3.

These are precisely the estimates used in the SP7 diagnostic. No concrete analytic obstruction to them was found in this proof. This file does not itself establish the complete nonlinear stress inequality or conclude seven-dimensional compactness; those must be combined and audited separately before any contradiction claim.
