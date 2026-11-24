# Dimension-six renormalized isolated-simple Pohozaev sign

This is a local calculation conditional on bubble convergence and isolated-simple strong decay, as in agent2_n5_n6_weighted_first_approximation.md. It is supplied for independent audit before treating it as a completed compactness theorem. Selection and Green mass are separate.

## Setup

Let n=6,beta=2/5,c=1/5,a=2,k=24,q=3. In a locally Euclidean chart at a boundary maximum normalize H(0)=0 and write
h=f2+f3+f4+f5+O(r6), tr D2f2=0.
Here f_j is homogeneous of degree j and the jets are uniformly bounded. Set epsilon=M^(-1/2), v(y)=M^(-1)u(epsilon y), U=(1+r2)^(-2). Fix one outer delta0; all local estimates below use its one constant and are evaluated at delta<delta0/2. Put b=|D2h(0)|.

Let P be the linear spherical Pohozaev flux. The exact critical flux for Mu differs from P by k epsilon^2 r(Mu)^3/3, which tends zero on each fixed physical sphere by strong decay. Define
I4=integral_[S4]f4,
Ptilde_delta(Mu)=P_delta(Mu)+8I4/(5delta).
The exact Robin stress identity is the general identity displayed in agent2_n5_renormalized_SP.md, with these n6 constants.

## Stage1: coarse umbilicity rate

The proved first approximation is v=U+epsilon Phi2+e1,
|e1|<=C epsilon^2(1+r)^(-2), |De1|<=C epsilon^2(1+r)^(-3).
The positive quadratic model coefficient is C2||f2||^2 epsilon^2, C2=25pi/128. Its proof is identical to n5: integrating f2(DU.DPhi2-kU^pPhi2) by parts gives the Jacobi energy of Phi2. The general finite coefficient formula stated in agent2_n5_n6_local_coefficients.md specializes to this C2.

Use the exact stress identity and temporarily estimate every cubic contribution by its absolute value. Quadratic geometry paired with De1 has size epsilon^3 b integral_1^R r^(-2)dr <=Cepsilon^3 b. Cubic geometry paired with De1, and linear cubic H paired with Ue1, have size Cepsilon^4 integral_1^R r^(-1)dr <=Cepsilon^4 log(2+R). The pure-quadratic cubic terms are O(epsilon^3b^3), absorbed into epsilon^2b^2 because epsilon b tends0. Quadratic/quartic mixed terms have size epsilon^4 b logR, absorbed by Young into epsilon^2b^2 plus o(epsilon^4). All other terms are bounded by the same groups or by C_delta epsilon^4.

Linear f2 has zero angular mean and f3,f5 are odd. The linear f4 graph flux is, per unit mean,
(8/5)R^7(R2-2)/(1+R2)^5=8/(5R)+O(R^-3).
Thus its normalized spherical flux is -8I4/(5delta)+o(1), precisely removed by Ptilde. The checker verifies this expression exactly from c[-3R8(U2)'-16R7U2]. Higher linear jets are O(epsilon^4delta).

Since Ptilde on any one fixed evaluation sphere is uniformly bounded by strong decay and elliptic estimates, the stress estimate gives
c b^2/epsilon^2 <= C_delta+C b/epsilon+C log(1/epsilon).
Apply Young to b/epsilon. Fix that evaluation delta once. Consequently
b<=C_delta0 epsilon sqrt(log(1/epsilon)).
No favorable cubic sign or second approximation is used to derive this coarse rate.

## Stage2: genuine weighted second approximation

Let Phi3 be the physical Jacobi correction for f3, constructed in agent2_n5_n6_local_coefficients.md. It is odd in z and obeys |D^j Phi3|<=C(1+r)^(-2-j), j<=3. Its tangential gradient at0 can be made zero by adding translation kernel modes; its value at0 is automatically zero. This does not change its tail, energy coefficient or any asymptotic.

Set W=U+epsilon Phi2+epsilon^2 Phi3. It is comparable to U for small fixed delta0 because epsilon Phi2/U=O(epsilon b(1+r)) and epsilon^2Phi3/U=O(epsilon^2(1+r)^2). After C2 extension of the corrections below the plane, the exact residual satisfies
|Delta W+24W^2|<=C epsilon^3(1+r)^(-3),
|B_scaled W|<=C epsilon^3(1+r)^(-2).
Here is the full source grouping:
* All linear cubic graph terms cancel against epsilon^2Phi3.
* The remaining quadratic-squared sources are bounded by epsilon^2b^2 r^-4 in the bulk and epsilon^2b^2r^-3 on the boundary. Stage1 implies epsilon^2b^2<=Cepsilon^4log(1/epsilon)=o(epsilon^3), so these have the stated stronger weights.
* A quartic graph gives epsilon^3r^-2 boundary data. Normal-shift extension errors for Phi3 are epsilon^3b r^-3 in bulk from the quadratic graph and epsilon^4r^-2 from the cubic graph; the latter is bounded by delta0 epsilon^3r^-3 since epsilon r<=delta0.
* The nonlinear equation is quadratic. Phi2/Phi3 products give epsilon^2b^2r^-6, epsilon^3b r^-5 and epsilon^4r^-4, all bounded by the target. The Robin/normal terms obey the same grading.
* Higher graph jets have an additional epsilon r factor and are dominated on the fixed chart.

Let e2=v-W and put its exact divided-difference nonlinearity into a coefficient A_i<=C(1+r)^(-4). Apply the weighted inverse proof from the first-approximation lemma, now with weight (1+r)^1 instead of (1+r)^2. The exterior supersolution is
C r^-1-D t r^-2.
Its key identities are -Delta r^-1=3r^-3 and Delta(t r^-2)=-8t r^-4, with outward plane derivative partial_nu(-t r^-2)=r^-2. Metric and Robin errors are absorbed by choosing delta0 small; the positive supersolution gives the exterior maximum principle. Outer data are O(R^-4), whose weighted norm is O(R^-3)=O_delta0(epsilon^3).

In the contradiction argument, a normalized global Jacobi limit decays O(r^-1). Under stereographic transfer its growth is O(r^3), strictly milder than the fundamental rho^-4 pole in six dimensions. The puncture is therefore removable, and the center value/tangential gradient constraints kill all Jacobi modes exactly as in the first lemma. Thus
|e2|<=C_delta0 epsilon^3(1+r)^(-1),
|De2|<=C_delta0 epsilon^3(1+r)^(-2).
As before, prove C0 on2delta0 and restrict to delta0 for the gradient estimate.

## Stage3: the sharp sign

Insert v=U+epsilon Phi2+epsilon^2Phi3+e2 into the exact stress identity. The quadratic part is C2||f2||^2epsilon^2. For a homogeneous graph of degree j the bilinear graph/correction Pohozaev coefficient is (j-1) times its Jacobi energy: integrate f_j(DU.DPhi-kU^pPhi)-beta Delta f_j U Phi by parts and use z.Df_j=jf_j. The bracket equals the exact outward Neumann datum of Phi paired with Phi. Truncation produces only a boundary term of order R^(2j-n); in the critical case n=2j this is O(1), not logarithmic.

For j3 the previously proved correction energy is
L(Phi3;B_R)=C3 logR+O(||f3||^2),
C3=(9pi/2)||H3||_[S4]^2+(18pi/25)||L1||_[S4]^2>0,
where f3=H3+r2L1. Therefore its positive Pohozaev contribution is 2epsilon^4 C3logR+O(epsilon^4||f3||^2). The mixed quadratic/cubic term is odd under z reflection and has zero tangent-disc integral.

The remaining stress terms obey:
1. Quadratic geometry times De2: epsilon b*r2*r^-5*epsilon^3r^-2*r4dr=epsilon^4 b r^-1dr. Normalized error <=Cb logR=o(1) by Stage1.
2. Cubic geometry times De2: epsilon^2*r3*r^-5*epsilon^3r^-2*r4dr=epsilon^5dr. Normalized integral <=Cepsilon R=Cdelta.
3. Cubic H times Ue2 and its edge term have the same Cdelta bound.
4. Error-gradient squares give at worst Cb delta^3+Cdelta^4; H^2(x.nu) gives Cb delta+Cdelta^2.
5. Nonlinear pure-quadratic cubic terms normalize to Cb^3/epsilon=o(1); fourth-order quadratic terms to Cb^4logR=o(1). Quadratic/quartic cross terms normalize to Cb logR=o(1). All higher even jet/correction pairs have total degree at least7 and hence contribute O(delta); odd pairs vanish.
6. The linear f4 contribution is the counterterm already displayed; f5 is odd, f6 and higher are O(delta). Cap/Jacobian/normal remainders have the same bounds by their extra slope or epsilon r factors.
The checker verifies the critical radial exponents and the epsilon-log limits. All constants use the single fixed delta0 estimate.

Hence
Ptilde_delta(Mu)>=c0 b^2/epsilon^2+2C3 log(delta/epsilon)-C||f3||^2-o_i(1)-C_delta0(delta+delta2+delta3+delta4).
Since C3 is positive definite in f3, absorb its finite negative term into half the growing log term for large i. This is the desired renormalized isolated-simple sign. In particular finite fixed-delta limits force II(p_infinity)=0 and DII(p_infinity)=0; dropping the positive terms yields a nonnegative terminal adapted Pohozaev limit as delta tends0.

## Green mass matching (separate input)

At II=DII0, graph f4+f5+O(r6), the harmonic Green corrections are q4=r^-1Y and q5 homogeneous0 odd. The former has mean integral_[S5+]Y=4I4/15; its cross Pohozaev term with r^-4 is -8I4/(5r), exactly canceled above. The mass-order f5 jet has zero average by oddness. The boundary ADM mass is therefore the finite Green coefficient B, and P_adapted tends -4|S5|B. AF decay3>2 makes the standard dimension-six boundary positive-mass theorem applicable. Agent3's general counterterm/mass calculation proves these coefficients. The full Green parametrix and PMT rigidity must be supplied separately; this document is the local nonlinear sign calculation.
