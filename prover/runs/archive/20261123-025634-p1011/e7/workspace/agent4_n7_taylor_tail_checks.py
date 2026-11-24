import sympy as s
from pathlib import Path
# Explicit weighted C7 extension: normal jets through order7 match at t0.
c=s.symbols('c1:9')
sol=s.solve([sum(c[j-1]*(-j)**m for j in range(1,9))-1 for m in range(8)],c)
cs=[sol[x] for x in c]
assert all(sum(cs[j-1]*(-j)**m for j in range(1,9))==1 for m in range(8))
print('ExactC7 normal extension coefficients:',cs)

def parts(total,small=1):
 if total==0:yield ()
 for k in range(small,total+1):
  for p in parts(total-k,k):yield (k,)+p
for d in range(1,6):
 pp=list(parts(d)); assert len(pp)==[1,2,3,5,7][d-1]
 print('Weight',d,'graph degree partitions:',[tuple(x+1 for x in p) for p in pp])
e,R,eta,b,a,L=s.symbols('e R eta b a L',positive=True)
assert s.expand(eta*b*b/e**3+e/(4*eta)-b/e-(s.sqrt(eta)*b/e**s.Rational(3,2)-s.sqrt(e)/(2*s.sqrt(eta)))**2)==0
assert s.expand(eta*a*a/e+e*L*L/(4*eta)-a*L-(s.sqrt(eta)*a/s.sqrt(e)-s.sqrt(e)*L/(2*s.sqrt(eta)))**2)==0
assert s.simplify(e**(-5)*e**6*(R-1)-e*(R-1))==0
assert s.simplify(e**(-5)*e**7*(R**2-1)/2-e**2*(R**2-1)/2)==0
print('Youngabsorption and exact weight6/7 taildomination checked.')

proof=r'''# Independent diagnostic: exhaustive n7 weighted Taylor remainder

This is an audit lemma only, conditional on the graph/correction/unknown-error bounds stated below. It is NOT a claimed disproof of the problem's asserted theorem. It supplements agent2_n7_exhaustive_grading.md by removing an analyticity ambiguity, explicitly listing the additional E f2² class, and proving quantitative tail domination rather than asserting a formal series. Any counterexample to the claimed coefficient bounds or to this grading is invited; one must not infer the original classification from this diagnostic.

## Assumed bounds and fixed-radius order

Set n7, t=epsilon r, 1<=r<=delta/epsilon. First fix an outer physical radiusdelta0 so all analytic estimates hold with one constantC_delta0. Only afterwards letdelta<delta0/2 tendto0. The graph hasC7 Taylor expansion

F_epsilon(z)=sum_{k=2}^6 epsilon^{k−1}f_k(z)+Rem,
|D^j Rem|<=C epsilon6 r^{7−j}, j<=3.

The physical corrections satisfy, for all finite derivative orders used,

|D^j Phi2|<=C b(1+r)^−4−j,
|D^j Phi3|<=C a(1+r)^−3−j,

whereb=|II|=O(epsilon), a is the bounded cubic-jet norm. The unknown remainderE satisfies|E|<=C_delta0 epsilon³(1+r)^−2, |DE|<=C_delta0 epsilon³(1+r)^−3. The positive model U+epsilonPhi2+epsilon²Phi3 is comparable toU=(1+r²)^−5/2, and actualw<=CU. These are substantive analytic assumptions, not consequences of the present grading lemma.

## 1. No analyticity of the corrections is needed

To evaluate a correction at a slightly negative graph height, choose a weightedC7 extension, not merely the earlierC2 reflection. For t<0 define

Phi_ext(z,t)=sum_{j=1}^8 c_j Phi(z,−j t),
(c1,...,c8)=(36,−168,378,−504,420,−216,63,−8).

The exact identities sum_j c_j(−j)^m=1 for0<=m<=7 match all normal and mixed jets throughorder7. These coefficients are computed and checked in agent4_n7_taylor_tail_checks.py. On the thin cone|t|<=delta0|z|, all reflected radii are comparable, hence weighted derivative bounds are preserved. The extended linearized residual vanishes at t0 and is bounded byC|t|r^{tau−3} ifPhi=O(r^tau), by the mean value theorem and its weighted third derivatives. Thus the previous strip residual bounds remain valid (or improve). Tangential parity is preserved.

## 2. Uniform weighted Taylor expansion

For each fixed annularr>=1, normalize the graph coefficients asF/r, DF, rD²F, r²D³F. The degree-k contribution to every such coefficient isO(t^{k−1}); its angular/coefficient functions have uniformly bounded derivatives. The normalized graph Taylor remainder isO(t6). The model correction relative toU, and its gradient relative toDU, have termsO(b t) andO(a t²).

Normal vectors, area factors, tangential projections, H andxT·DH are smooth functions of these normalized variables as long as the slope stays uniformlysmall. Denominator factors have bounded derivatives throughorder6. Evaluation ofU orPhi_j at the graph is alsoC6 inF/r with uniform bounds, by the weighted derivatives and the precedingC7 extension. Therefore FINITE multivariable Taylor expansion, composed with these weighted variables, gives all terms of totalweightd<=5 plus a remainder bounded byC t6. No infiniteanalyticseries or analyticity of the originalsmooth graph is being assumed.

For the nonintegermodel nonlinearityq14/5, choose delta0 so the known model perturbation divided byU is in[−1/2,1/2]. The scalar function(1+s)^q has bounded derivatives throughorder6 there, so the same finite weighted expansion andC t6 remainder apply. At the smaller evaluationradiusdelta the unknown relativeerror is at mostC_delta0 delta³; it can also be made<1/2 if desired, but this is unnecessary: q>2 andw<=CU give a uniform second-order Taylor bound inE with coefficientC U^{q−2} even without a lowerboundonw.

## 3. Baseline radial degree and tails

The critical quadratic-gradient boundary stress has primitive radialdegree2−n=−5. Explicitly, before graph factors its radialdensity isr^−6dr. Every normalized graph/correction factor ofweightw supplies epsilon^w r^w. The H, xT·DH, H² andedge terms have the same dimension after compensating derivative/length factors. A monomial of totalweightd is therefore bounded by

C epsilon^d integral_1^R r^{d−6}dr.

For d<5 its core coefficient isfinite and normalizedorder epsilon^{d−5}; for d5 it islogR; for d>5 it isO(delta^{d−5}) after dividing byepsilon5. The potentialU^q sector has two EXTRA radial decaypowers and cannot worsen these bounds. The explicitTaylorremainderC t6 gives normalizedtail

epsilon^−5 integral_1^R r^−6(epsilon r)^6dr=epsilon(R−1)<=delta.

Onr<=1 its remainder isO(epsilon6), henceo(epsilon5). Thus ALL high-weight tails are quantitativelyO(delta), with no number-of-terms ambiguity. Sphere-cap corrections follow byC6 implicit differentiation of|z|²+F(z)²=R²; each extra factor has the same graph weight and no exceptional mass-order term.

## 4. Complete low-weight list

Every partition of weights1,...,5 is generated and checked by the script. Listing graphDEGREES ratherthanweights:

1: (2).
2: (3), (2,2).
3: (4), (2,3), (2,2,2).
4: (5), (2,4), (3,3), (2,2,3), (2,2,2,2).
5: (6), (2,5), (3,4), (2,2,4), (2,3,3), (2,2,2,3), (2,2,2,2,2).

Linear degree2 istracefree, degrees3and5 areodd, anddegrees4and6 require the explicitknownADMcounterterms. The exact second-order norms(2,2) and(3,3) arepositive. Mixed(2,3),(2,2,3),(2,5),(3,4),(2,2,2,3) areodd. Remaining unsignedterms, afterb=O(epsilon), arebounded by

b³/epsilon²=O(epsilon),
b A4/epsilon <=eta b²/epsilon³+C_eta epsilon A4²,
b4/epsilon=O(epsilon³),
b² A4logR=o(1),
b a²logR=o(1),
b5logR=o(1).

Parity on the nonsymmetricactual cap is handled by first pulling back to the symmetricreferencecap. Its Taylorchange contributesadditionalgraphweights alreadyincludedabove, ratherthan an unlisted parity exception.

## 5. Unknown E: include ALL low-weight classes

E has weight3. Every graphflux term containingE contains at leastonegraph factor, since theflatplane hasx·nu=H=0. The low-weight possibilities are:

* weight4: E f2, normalizedboundC b/epsilon;
* weight5: E f3, normalizedboundC a logR;
* weight5: E f2², including E f2Phi2 and evaluation/tangential-projection variants, normalizedboundC b²logR=o(1).

The last class is easy to overlook but harmless afterb=O(epsilon). The firsttwoareabsorbedbythe exactYoungidentities

b/epsilon <=eta b²/epsilon³+epsilon/(4eta),
a logR <=eta a²/epsilon+epsilon log²R/(4eta).

AnyE²term hasweightatleast7 andnormalizedboundO(delta²), sinceepsilon^−5 epsilon7∫_1^R r dr<=delta²/2. Model-timesE terms with morefactorsthanlisted arehigherweight. Thus unknownremainders introduce no further unlisted low-order class.

## Scope

This is a complete finite weighted-Taylor audit assuming the stated field/graph estimates, positivity/comparability and uniform coefficient bounds. It identifies no missinglow-weightterm capable of reversing the n7diagnostic's proposed sign. It is NOT a substitute for auditing the analytic weighted inverse, exact leadingbilinear coefficients, AFmass theorem hypotheses, or the full selectionbridge. No alternateclassification or contradiction of the user's assertedanswer is certified here.
'''
Path('workspace/agent4_n7_taylor_tail_diagnostic.md').write_text(proof)
Path('workspace/agent4_n7_taylor_tail_checks.py').write_text(Path(__file__).read_text())
print('Saved independentn7 finiteTaylor/taildiagnostic and executable exactchecks.')
