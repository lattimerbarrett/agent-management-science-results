# Dimension-four isolated-simple Pohozaev sign

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
