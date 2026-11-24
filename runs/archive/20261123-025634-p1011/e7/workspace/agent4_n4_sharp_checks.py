import sympy as s
from pathlib import Path
r,R,e=s.symbols('r R e',positive=True)
# Translation compatibility for the cubic trace graph |z|² z1 in n4.
I4=s.gamma(s.Rational(5,2))*s.gamma(s.Rational(3,2))/(2*s.gamma(4))
I6=s.gamma(s.Rational(7,2))*s.gamma(s.Rational(1,2))/(2*s.gamma(4))
assert s.simplify(I6-5*I4)==0
assert s.Rational(40-16,40+8)==s.Rational(1,2)
# Borderline source and gradient power counts.
assert s.expand(3-2-2)==-1 # volume Newton kernel r^-2, source r^-2
assert s.expand(2-2-1)==-1 # boundary Newton kernel, source r^-1
assert s.expand(3-2-1)==0 # source r^-1 has potential sizeR
assert s.expand(2-2)==0 # constant boundary source sizeR
assert s.expand(3-3-1)==-1 # gradient of source r^-1 giveslogR
print('n4 cubic-translation beta compatibility, coercivity and mixed-potential exponents checked.')

proof=r'''# Dimension-four sharp first remainder after the umbilicity rate

This is a conditional local estimate, not a full compactness theorem. Inputs: isolated-simple strong decay, local microscopic bubble convergence, and the already proved rate |A_i|² log R_i<=C from agent4_n4_umbilicity_rate.md. All estimates use one fixed small physical outer radius delta0; constants never depend on the later Pohozaev radiusr<delta0/2.

## 1. Graph and corrections

Set epsilon=M^−1, R=delta0/epsilon, U=(1+|y|²)^−1. In uniformly flat-normalized coordinates, the graph is

F(z)=epsilon f2(z)+epsilon² f3(z)+O(epsilon³|z|4),

with tr f2=0 and f2=(1/2)A[z,z]. The scaled mean curvature isO(epsilon²r). Strong decay gives w=M^−1u(epsilon y)<=C(1+r)^−2 and local C² convergence toU. Center normalizations are w(0)=U(0), D_z w(0)=0.

Let Phi2 be the quadratic correction in agent4_n4_log_proof.md. It satisfies L Phi2=0, L=Delta+24U², the exact first quadratic boundary source, and

|D^k Phi2|<=C|A|(1+r)^−1−k, k=0,1,2.

Its value and first tangential derivatives at0 vanish by angular degree2.

There is also a bounded cubic correction Phi3 satisfying L Phi3=0 and

partial_out Phi3=4f3/(1+|z|²)²−(Delta f3)/(3(1+|z|²)) at t0,
|Phi3|<=C, |D^k Phi3|<=C(1+r)^−k, k=1,2,
Phi3(0)=0, D_z Phi3(0)=0.

Here is its construction. Write f3=H3+|z|²L1. Its far homogeneous harmonic correction is the odd degree0 functionq from agent4_n4_green_umbilic.md. Cut q off near0. The remaining volume residual isO(r^−4) and boundary mismatchO(r^−3), both energy-dual. In angular degree3 the Jacobi form is coercive. In angular degree1 it is coercive after removing the translation kernel, and the forcing is compatible with that kernel: for f3=|z|²z1 the exact boundary forcing is (2/3)(r²−5)z1/(1+r²)², whose pairing with Z1 is a constant times∫_0^infinity r4(r²−5)/(1+r²)4dr=0 by the beta identityI6=5I4. Cutoffq adds a variational residual with the same compatibility, because its infinity Wronskian withZ1 vanishes. Lax-Milgram on the complement constructs eta inD^{1,2}. Its preliminary O(r^−1) annular estimate, followed by the Neumann Newton representation, improves it toO(log(2+r)/r²), with gradientO(log(2+r)/r³). Thus Phi3=q+eta is bounded. Add translation kernel functions to set D_zPhi3(0)=0; oddness already givesPhi3(0)=0.

## 2. Extension into the thin negative-t strip

For either correction extend by

Phi(z,t)=Phi(z,−t)+2t b(z), t<0, b=partial_tPhi(z,0).

It isC² across the plane. The needed strip satisfies |t|<=C(epsilon|A|r²+epsilon²r³)<=Cdelta0 r. The additional linearized residual is2t(Delta_z b+24U²b). Since b2=O(|A|r^−2), Db2=O(|A|r^−3), Delta b2=O(|A|r^−4), while b3=O(r^−1), Delta b3=O(r^−3), this gives exactly the source bounds below.

## 3. Quantitative residual of the approximation

Put V=U+epsilon Phi2+epsilon²Phi3 on the curved halfball. Taylor expansion of the exact Euclidean boundary normal and the graph formula, together with the preceding strip extension, gives volume residual and boundary residual bounded respectively by sums

volume: C[epsilon²|A|²(1+r)^−2+epsilon³(1+r)^−1+epsilon4]
        plus integrable termsO(epsilon²(1+r)^−4),
boundary: C[epsilon²|A|²(1+r)^−1+epsilon³].

Every power is explicit: quadratic graph times first quadratic correction produces the |A|² terms; cubic and higher graph jets give the epsilon³ terms; the epsilon²Phi3 strip extension givesepsilon4. Nonlinear terms24U(epsilonPhi2+epsilon²Phi3)²+8(epsilonPhi2+epsilon²Phi3)³ have mixed-Green potentialsO(epsilon²): the worst extra logarithm isepsilon4 logR=o(epsilon²). Outer comparison values have sizeO_delta0(epsilon²) by strong decay and the correction bounds.

The first volume and boundary terms have Newton potential at mostCepsilon²|A|² logR=O(epsilon²) by the rate input. The next terms have potentialO(epsilon³R)=O(epsilon²delta0), and the last has potentialO(epsilon4R²)=O(epsilon²delta0²). Thus the entire mixed-Green lift of the residual isO_delta0(epsilon²).

## 4. Uniform sup bound for the remainder

Let h=w−V. For delta0small, V ispositive andcomparable toU since epsilonPhi2/U=O(|A|epsilon r) andepsilon²Phi3/U=O(epsilon²r²). Hence the exact divided-difference equation is

Delta h+c_i h=−residual(V), 0<=c_i<=C(1+r)^−4,
partial_out h=−(H_scaled/3)h−boundary_residual(V).

The mixed Neumann/outer-Dirichlet Green kernel is bounded byC|x−y|^−2 with uniform constants. Its exterior potential operator for(1+r)^−4 has norm<=C/R0², and the Robin perturbation has norm<=Cepsilon²R²=Cdelta0². Consequently, withE=||h||infinity,

E<=C_delta0 epsilon²+C(R0)sup_{r<R0}|h|+(C/R0²+Cdelta0²)E.

IfE/epsilon² wereunbounded, h/E would converge locally to a bounded Jacobi function with homogeneous Neumann data and zero value/tangential gradient at0. Every bounded n4 Jacobi function has expansionC+O(logr/r²): write it as the Neumann Newton potential of24U²h plus a bounded Neumann harmonic constant. Its Wronskian with the scale mode forcesC=0. It then has finite Dirichlet energy; stereographic transfer identifies it with the translation/scale kernel. The center constraints kill that kernel. Thus the compact sup term divided byE tends0; choosingR0large anddelta0small contradicts the displayed inequality. Therefore

|h|<=C_delta0 epsilon².

## 5. Gradient bound

Once the uniformO(epsilon²) value bound is established, ordinary annular boundary gradient estimates suffice; there is no need to differentiate a singular kernel. On an annulus of radiusr>=1, dilate by r. The graph has uniformly bounded small slope andC²norm, the Robin coefficient after dilation isO(epsilon²r²)<=Cdelta0², and all source Holder norms obey the same displayed polynomial bounds. The scaled boundary gradient estimate gives

|Dh|<=C[sup|h|/r+r sup|residual_volume|+sup|residual_boundary|]
 <=C[epsilon²/r+epsilon²|A|²/r+epsilon³+epsilon4r]
 <=C_delta0 epsilon²/r,

becauseepsilon r<=delta0 andAisbounded. The potentialc_i h is included sinceitscoefficient after dilation isO(r^−2). Local estimates onr<=2 giveO(epsilon²). Thus forr<R/2,

|Dh|<=C_delta0 epsilon²/(1+r). SincePhi3isbounded andDPhi3=O((1+r)^−1), we obtain the useful final form

|w−U−epsilonPhi2|<=C_delta0 epsilon²,
|D(w−U−epsilonPhi2)|<=C_delta0 epsilon²/(1+r).

These estimates are conditional only on the listed strong-decay and umbilicity-rate inputs. Applying them in the exact Robin stress identity still requires a separate accounting of parity, edge fluxes, and coordinate caps; that SP calculation is not asserted in this file.
'''
Path('workspace/agent4_n4_sharp_remainder.md').write_text(proof)
Path('workspace/agent4_n4_sharp_checks.py').write_text(Path(__file__).read_text())
print('Saved n4 sharp remainder conditional proof and executed checks.')

# General Robin stress algebra and n4 error radial powers.
n=s.symbols('n',positive=True); beta=(n-2)/(2*(n-1)); aa=(n-2)/2
assert s.simplify(beta*(n-1)/2-beta*aa-beta/2)==0
assert s.simplify(beta**2/2-beta/2+beta*(1-beta)/2)==0
assert s.simplify((beta/2).subs(n,4)-s.Rational(1,6))==0
assert s.simplify((beta*(1-beta)/2).subs(n,4)-s.Rational(1,9))==0
# Forr>=0: r^k/(1+r)^k<=1; use polynomial dominant upperbounds.
for power,denom,boundpower in [(4,4,0),(4,3,1),(4,2,2),(6,6,0),(5,4,1),(6,4,2)]:
 assert power-denom==boundpower
print('n4 exact Robin stress coefficients and radial remainder exponents checked.')

spproof=r'''# Dimension-four isolated-simple Pohozaev sign

This file combines the independently derived n4 rate and sharp remainder with a complete stress calculation. Standard external inputs are the usual local elliptic/Green estimates used in those lemmas, entire bubble classification in the separate selection bridge, and the boundary positive mass theorem for the final contradiction.

## Inputs and fixed-radius convention

Use agent4_n4_umbilicity_rate.md and agent4_n4_sharp_remainder.md. With epsilon_i=M_i^−1 and microscopic profile w_i=M_i^−1 u_i(epsilon_i y), they give

|A_i|² log(1/epsilon_i)<=C, A_i→0,
w_i=U+epsilon_i Phi_i+E_i,
|E_i|<=C_delta0 epsilon_i², |DE_i|<=C_delta0 epsilon_i²/(1+r),

wherePhi_iis the EVEN tangential degree2 quadratic correction with|D^kPhi_i|<=C|A_i|(1+r)^−1−k. ONE physical outer radiusdelta0 is fixed for all estimates. A later physicalPohozaevradiusr tends to0 belowdelta0/2 with exactly these same constants.

The local boundary graph is

F_i=epsilon_i f2_i+epsilon_i² f3_i+O(epsilon_i³|z|4),

wheref2_i=(1/2)A_i[z,z]iseven andtracefree, f3_iisodd. Its outwardsupportfunction is

x·nu=epsilon_i f2_i+2epsilon_i² f3_i+O(epsilon_i³|z|4),

up to the harmless graph normalization factor1+O(epsilon_i²|z|²). Its scaled mean curvature is

H_i=epsilon_i² Delta f3_i+O(epsilon_i³|z|²),

with the leading termodd. Uniform Taylor bounds hold throughR_i=delta0/epsilon_i.

## Exact Robin stress identity

ForDelta w+8w³=0 the critical current is

J=(x·Dw+w)Dw−x|Dw|²/2+2xw4.

Its divergence vanishes. Thus its spherical fluxP is minus the graph flux. Substitutingpartial_nu w=−H w/3 and integrating one tangential derivative yields

∫graph J·nu =∫graph[(xT·DH+H)w²/6−H²(x·nu)w²/9
                    −(x·nu)|D_Tw|²/2+2(x·nu)w4]
              −∫edge H w²(xT·eta)/6.

For a generaln, the two curvature coefficients arebeta/2 and−beta(1−beta)/2, beta=(n−2)/(2(n−1)); this algebra is checked symbolically. In n4theyare1/6and−1/9.

## The unique logarithmic term

The firstgraph term epsilon f2 times the radial U-gradient orU4 has zeroangularaverage exactly. The terms epsilon² f3 andepsilon²Deltaf3 againstU andtheeven correctionPhi also have zeroangularaverage. The only divergent second-order integral in minus the graphflux is

epsilon_i²∫_{|z|<R} f2_i D_zU·D_zPhi_i dz.

Bytheexactfar tracePhi_i=(pi/4)f2_i/|z|3+O(|A_i|r^−2) andthegradientremainder, this integral equals

(pi²/15)|A_i|² epsilon_i² logR+O(|A_i|²epsilon_i²).

The nonlinear potential cross term is integrable at infinity and is included intheO(|A_i|²epsilon_i²)error. The coefficientpi²/15wascheckedindependentlybyangularDtNanddirectstresscrosscomputation.

## Every remaining term is small after normalization

SetR=r/epsilon_i. The normalizedPohozaevforv_i=M_i u_i is epsilon_i^−2P(w_i,R). BelowCdependsontheONEfixedouterdelta0, notonr. Replacing1+rbyrinthetailonly enlarges the displayed elementarybounds;thecore is uniformlyintegrable.

* ThecrossgradientwithE isboundedbyCepsilon_i∫_0^R s4/(1+s)4 ds<=Cr.
* ThePhi²gradient termhasthesameboundCr (A_iisuniformlybounded).
* ThePhi-EcrossisboundedbyCepsilon_i²∫_0^R s4/(1+s)3 ds<=Cr²/2.
* TheE²gradienttermisboundedbyCepsilon_i³∫_0^R s4/(1+s)2 ds<=Cr³/3.
* QuarticandhighergraphjetsagainsttheleadinggradientgiveCepsilon_i∫s6/(1+s)6<=Cr. CubicgraphtermswithEgiveCepsilon_i²∫s5/(1+s)4<=Cr²/2;theirtermsagainstUandPhicancelbyoddness.
* ThehigherpartofHhasboundCepsilon_i∫s4/(1+s)4<=Cr. TheleadingoddHpartcancelsagainst(U+epsilonPhi)²;itscrosseswithEareboundedbyC(r²+r³+r4).
* H²(x·nu)w²givesatmostCepsilon_i³∫s6/(1+s)4<=Cr³/3.
* TheedgeleadingoddHpartcancelsagainst(U+epsilonPhi)². TheedgehigherjetsgiveCr, andEcrossesgiveC(r²+r³+r4).
* Allremainingnonlinearpotentialerrorsareo_i(1)+Cr, bytheintegrabilityofU³Phiandratherfasternonlineartails.

The actualsphere-graphintersectiondiffersfromtheflatdiskradiusRbyarelativeO(r²). Itsworstpossiblecontributionisfromtheotherwisezero first radialf2term: its radialdensityisO(epsilon_i R^−2),andtheshellwidthisO(Rr²),givingafternormalizationO(r). Allothercaperrorsaresmaller. TangentialgradientversusEuclideanplanetracechangesaresecondorderinthegraphslopeorfromevaluationatt=F;theirworstboundisagainCr. Theseestimatesareuniformunderrescalingthebackgroundmetricinthenonsimpleandclusterarguments.

Consequently

P_r(M_i u_i)>= (pi²/15)|A_i|² log(r/epsilon_i)
               −C|A_i|²−C_delta0(r+r²+r³+r4)−o_i(1).

SinceA_i→0andthelogtermisnonnegativeforlargei, anyGreenlimithas

liminf_{r→0}P(G,r)>=0.

ThisistherequiredSPsignin n4. Atinteriorpoints,thelocallyflatEuclideanPohozaevidentitygivesthesameconclusionwithlesswork.

## TerminalGreenmass

Byagent4_n4_green_umbilic.md,theboundaryGreenprofileatumbilicp isG=a r^−2+a q_odd+B+O(r^alpha),a>0. The odd q cross has zero angular mean, and all q² terms tend to zero at rate r². Directradialcomputationgives

lim_{r→0}P(G,r)=−2aB|S³_+|=−2pi²aB.

ForasingleGreenpolethenonhemisphereboundaryPMTgivesB>0. Formultiplepolesorrescaledclusters,theotherpositivepolescontributepositiveconstantparts;theconditionalbridgeagent3_compactness_bridge.mdprovidesitsstandardcomparisonargument. ThusSPcontradictsthepositiveGreenmass. Subjecttotheexplicitanalyticinputsprovedinthenamedfiles,thisclosesn4compactness;itdoesnotaddressn5/6oranyn7..18construction.
'''
Path('workspace/agent4_n4_pohozaev_sign.md').write_text(spproof)
Path('workspace/agent4_n4_sharp_checks.py').write_text(Path(__file__).read_text())
print('Saved n4 Pohozaev sign proof and extra checks.')

rateadd=r'''# Direct-scale replacement for the n4 umbilicity-rate proof

This addendum replaces the C¹ energy-remainder step in agent4_n4_umbilicity_rate.md with an exact identity. It also allows the simpler PHYSICAL correction model, avoiding material-coordinate terms. The conclusion and assumptions of that lemma are unchanged.

Let W_delta=chi(x)delta^−1U(x/delta) in local Euclidean Cartesian coordinates on the actual curved domain, and let

m_delta=chi(x)delta^−1[U(x/delta)+delta Phi2(x/delta)],

wherePhi2is the physical quadratic correction, extended through the thin negative-t strip as in the sharp-remainder proof. Projectm_delta−W_delta off the Jacobi span. The projection changes the model byo(delta) inH¹: flat angular orthogonality is exact, while the curved-domain strip changes the pairing byO(delta²(1+|A|²log(1/delta))). The inverse theorem holds for these Cartesian bubbles as well as for Fermi bubbles: their rescaled limits and Jacobi Gram matrices are identical, their potential operators differ byo(1), and the kernel projection perturbation iso(1). Equivalently repeat its rescaled contradiction proof verbatim.

The model residual isO(delta) inH*: the first quadratic boundary residual cancels; every remaining boundary source isO(delta²(1+r)^−1), whose dual-trace norm throughR=r0/delta isO(delta²R)=O(delta); the negative-strip extension volume source isO(delta²|A|²(1+r)^−2), whose L^{4/3} norm isO(delta²R)=O(delta); higherjets and nonlinear terms have the bounds already listed in the original rate proof. Cutoff errors areO(delta). Thus actual cut-off isolated-simple solutions andm_delta differ byO(delta) inH¹ after modulation, by the uniform projected inverse.

## Exact scale identity, no PDE assumption

For ANY smooth compactly supportedm in the Euclidean chart, let Tm=m+x·gradm. Direct differentiation of the critical bulk energy under m_s(x)=s m(sx), including its moving-domain Jacobian, gives

E'(m)[Tm]=∫boundary [(x·nu)(|gradm|²/2−2m4)+(H/3)m(m+x·gradm)].

There is no interior residual on the right and no approximation. The identity includes the boundary energy derivative2cHmv=(H/3)mv. Its sign can also be obtained from the divergence of the critical stress current.

For the explicitm_delta the first graph term (quadraticf2 against radialU) has zero angularmean. Its unique logarithmic term is the crossgradient withPhi2,

+(pi²/15)|A|²delta²log(r0/delta).

The Phi2² term, cubic/higher graph jets, actual-domain evaluation errors and all H terms contributeO(delta²): the same radial bounds as in agent4_n4_pohozaev_sign.md apply, except there is no unknownE. Cubicjet terms are odd and cancel; quartic and normalization errors have radialsize delta³R=delta²r0. The physical cutoff annulus has energy and scale pairingO(delta²). Therefore

E'(m_delta)[Tm_delta]=(pi²/15)|A|²delta²log(r0/delta)+O(delta²).

Let Z_delta be the cut-off scale Jacobi mode. The explicit model gives

||Tm_delta−Z_delta||H¹<=Cdelta[1+|A|sqrt(log(r0/delta))].

Indeed the difference isPhi2+x·gradPhi2 plus fixed-annulus cutoff terms. Pairing it against the O(delta) model residual costs at mostCdelta²(1+x), where x=|A|sqrt(log(r0/delta)). Consequently

E'(m_delta)[Z_delta]=(pi²/15)delta²x²+O(delta²(1+x)).

The actual cutoff solution residual paired againstZ_delta isO(delta²), since both the solution and the Jacobi mode areO(delta) on its fixed physical outer annulus. If eta is theO(delta) actual-minus-model correction, the linear difference pairedZ is bounded by ||eta|| times ||E''(W_delta)Z_delta||<=Cdelta²(1+x). The cubic nonlinear difference has the same bound, by ||m−W||<=Cdelta(1+x). Hence

(pi²/15)x²<=C(1+x).

This proves the rate without differentiating an unspecified asymptotic remainder. Constants are uniform under homothetic rescalings of the fixed manifold: its Q energy, projections and bubble operator are conjugated isometrically by the conformal scaling; shrinking cutoff radii were already treated in the inverse lemma.

The static addendum is not overwritten by running older checker files.
'''
Path('workspace/agent4_n4_rate_direct_scale_addendum.md').write_text(rateadd)
print('Saved exact direct-scale replacement for n4 rate proof.')
